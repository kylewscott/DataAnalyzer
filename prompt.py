from langchain.prompts import PromptTemplate

examples = [
    {
        "Question": "Add example questions and outputs here"
    }
]

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