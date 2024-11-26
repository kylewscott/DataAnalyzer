from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders.csv_loader import CSVLoader
from DataAnalyzer.prompts import graph_prompt, explain_prompt, classification_prompt
import os
import time
import glob
import torch
import pandas as pd

DB_FAISS_PATH = 'vectorstore/db_faiss'

cuda_device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
llm = ChatOllama(model='llama3', temperature=0, device=cuda_device)

def classify_query(llm, query):
        prompt = classification_prompt().format(query=query)
        response = llm.invoke(prompt)
        return response.content.strip().lower()

def save_graph(plt, filename):
    output_dir = '../public/graphs'  
    os.makedirs(output_dir, exist_ok=True) 
    file_path = os.path.join(output_dir, filename)
    plt.savefig(file_path)
    plt.close()  
    return file_path

def clear_graph_directory():
    output_dir = 'C:\Projects\LLM\LLM_REPO\public\graphs'
    if os.path.exists(output_dir):
        files = glob.glob(os.path.join(output_dir, '*'))
        for file in files:
            os.remove(file);


def explain_data(prompt):
    loader = CSVLoader(file_path='../../Datasets/user_behavior_dataset.csv', encoding="utf-8", csv_args={'delimiter': ','})
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    text_chunks = text_splitter.split_documents(data)

    embeddings = HuggingFaceBgeEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    docsearch = FAISS.from_documents(text_chunks, embeddings)
    docsearch.save_local(DB_FAISS_PATH)

    qa_prompt, history_aware_retriever = explain_prompt(llm, docsearch)

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt) 
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    chat_history = []
    result = rag_chain.invoke({"input": prompt, "chat_history": chat_history})

    return result['answer'], ' '

def graph_data(prompt):
    df= pd.read_csv('../../Datasets/user_behavior_dataset.csv')[0:1]
    data_json = df.to_json(orient='records')

    few_shot_prompt_template = graph_prompt()
    rag_chain = few_shot_prompt_template | llm | StrOutputParser()
    generation = rag_chain.invoke({"data": data_json, "dataFile": '../../Datasets/user_behavior_dataset.csv', "question": prompt})

    code_only = generation.split("START")[-1].split("END")[0]
    explanation =  generation.split('<')[-1].split('>')[0]

    try:
        exec_locals = {"pd":pd}
        exec(code_only, exec_locals)

        if 'generate_plot' in exec_locals:
            timestamp = int(time.time())
            plt = exec_locals['generate_plot']() 
            graph_path = save_graph(plt, f'generated_graph_{timestamp}.png')
        else:
            print("No function named 'generate_plot' found in generated code.")

    except Exception as e: 
        print(e)
        return("AHHH")

    return explanation, graph_path


def analyzer(prompt):
    prompt_type = classify_query(llm, prompt)
    if(prompt_type == 'graph'):
        return graph_data(prompt)
    elif(prompt_type == 'explanation'):
        return explain_data(prompt)
    else:
        return 'Unable to do that', ''

    

#TODO Find a way for llama to be able to remember the last question and ouput in case the user references back to it
