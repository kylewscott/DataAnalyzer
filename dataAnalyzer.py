from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
import torch
import pandas as pd
from prompt import getPrompt

prompt = getPrompt()

cuda_device=torch.device("cuda" if torch.cuda.is_available() else "cpu")

llm = ChatOllama(model='llama3', temperature=0, device=cuda_device)

rag_chain = prompt | llm | StrOutputParser()

df= pd.read_csv('../Datasets/user_behavior_dataset.csv')[0:1]
data_json = df.to_json(orient='records')


count = 0;
while(1):

    if count==0:
        print(
        """
        *********************************************************
                        GRAPH GENERATION
        *********************************************************
        """
        )
        print("\nHello, what kind of graphs can I help create for you?\n") 
    else:
        print("\nWhat else can I graph for you?\n")

    #TODO add quit option
    question = input("ENTER QUESTION: ")
    print("\n")

    generation = rag_chain.invoke({"data": data_json, "dataFile": '../Datasets/user_behavior_dataset.csv', "question": question})

    code_start = "START"
    code_end = "END"

    print(generation)

    code_only = generation.split(code_start)[-1].split(code_end)[0]
    #TODO check for errors in code, if errors, give llama the code back and ask for fix
    #TODO check if the graph provided actually answers the question asked

    explenation =  generation.split('<')[-1].split('>')[0]

    print("Explenation: ", explenation)

    with open('graphing.py', 'w') as file:
        file.write(code_only)

    with open('graphing.py', 'r') as file:
        graph = file.read()

    try:
        exec(graph)
    except Exception as e: 
        print("There was an error...\n")
        fix = f"There was an error with code you provided: {e} \n Can you provide improved code?"
        generation = rag_chain.invoke({"data": data_json, "dataFile": '../Datasets/user_behavior_dataset.csv', "question": fix})
        print(generation)
        code_only = generation.split(code_start)[-1].split(code_end)[0]
        explenation =  generation.split('<')[-1].split('>')[0]

        with open('graphing.py', 'w') as file:
            file.write(code_only)
        with open('graphing.py', 'r') as file:
             graph = file.read()

        exec(graph)

        count +=1

        continue
    
    count += 1;

#TODO Find a way for llama to be able to remember the last question and ouput in case the user references back to it
#TODO Let user ask questions about the specfic graph generated or the explenation of it (Chatting)
