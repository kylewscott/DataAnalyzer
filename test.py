from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
import torch
import pandas as pd

#TODO  Create stronger template, do some research on it, put in own file eventually
examples = [
    {
        "question": "Add example questions and outputs here"
        "response": "This is the response"
    }
]

example_prompt = PromptTemplate(
    input_variables=["question","response"], template="Question: {question}\nResponse: {response}"
)

#STRENGTHEN THIS
prompt = PromptTemplate(
    template=""" 
    You will generate python code to create graphs.
    You Will be given a question: {question}
    This question will be asking for graphs on specfic data in the file: {dataFile}
    Here is the labels and a row of data: {data}
    You will generate the python code to create the requested graph.
    Do Not talk about the code at all.
    The code should be executable and run without error.
    Wrap the exectuable code including imports in START and END blocks.
    Wrap you ending explenation of the graphs in < and >.
    Give a one sentence explenation of the graphs, do not talk about the code.
    The user only sees the generated graph and does not care about the code.
    Do not use the seaborn library.
    """,
    input_variables=["data", "dataFile", "question"],
)

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

    explenation =  generation.split('<')[-1].split('>')[0]

    print("Explenation: ", explenation)

    with open('graphing.py', 'w') as file:
        file.write(code_only)

    with open('graphing.py', 'r') as file:
        graph = file.read()

    exec(graph)
    
    count += 1;

#TODO Find a way for llama to be able to remember the last question and ouput in case the user references back to it
#TODO Let user ask questions about the specfic graph generated or the explenation of it (Chatting)
