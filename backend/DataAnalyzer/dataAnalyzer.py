from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
import torch
import pandas as pd
from DataAnalyzer.prompt import getPrompt
import os

prompt = getPrompt()
cuda_device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
llm = ChatOllama(model='llama3', temperature=0, device=cuda_device)
rag_chain = prompt | llm | StrOutputParser()

df= pd.read_csv('../../Datasets/user_behavior_dataset.csv')[0:1]
data_json = df.to_json(orient='records')

def save_graph(plt, filename):
    output_dir = '../public/graphs'  
    os.makedirs(output_dir, exist_ok=True) 
    file_path = os.path.join(output_dir, filename)
    plt.savefig(file_path)
    plt.close()  
    return file_path

def analyzer(prompt):
    generation = rag_chain.invoke({"data": data_json, "dataFile": '../../Datasets/user_behavior_dataset.csv', "question": prompt})

    code_only = generation.split("START")[-1].split("END")[0]
    explanation =  generation.split('<')[-1].split('>')[0]

    try:
        exec_locals = {"pd":pd}
        exec(code_only, exec_locals)

        if 'generate_plot' in exec_locals:
            plt = exec_locals['generate_plot']() 
            graph_path = save_graph(plt, 'generated_graph.png')
        else:
            print("No function named 'generate_plot' found in generated code.")

    except Exception as e: 
        print(e)
        return("AHHH")

    return explanation, graph_path
        

#TODO Find a way for llama to be able to remember the last question and ouput in case the user references back to it
#TODO Let user ask questions about the specfic graph generated or the explenation of it (Chatting)
