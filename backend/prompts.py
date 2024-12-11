from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def graph_prompt(): 
    examples = [
        {
            "question": "Can you graph the screen time of the first 50 users",
            "response": """
            START
            import pandas as pd
            import matplotlib.pyplot as plt

            def generate_plot():
                data = pd.read_csv('../public/data/filename.csv')

                plt.figure(figsize=(10,6))
                plt.plot(data['Screen On Time (hours/day)'].head(50), marker='o')
                plt.xlabel('User ID')
                plt.ylabel('Screen On Time (hours/day)')
                plt.title('Screen Time of the First 50 Users')

                return plt
                
            END

            <The graph shows the screen time in hours per day for the first 50 users, with each user represented by a single data point.>
            """
        }
    ]

    example_template = """
    User: {question}
    AI: {response}
    """

    example_prompt = PromptTemplate(
        input_variables=["question", "response"],
        template=example_template
    )

    prefix = """
    You will generate python code to create graphs.
    You Will be given a question: {question}
    This question will be asking for graphs on specfic data in the file: {dataFile}
    Here is the labels and a row of data: {data}
    You will generate the python code to create the requested graph.
    Wrap code in a function called generate_plot as seen in the example.
    Do Not talk about the code at all.
    The code should be executable and run without error.
    Wrap the exectuable code including imports in START and END blocks.
    Wrap you ending explenation of the graphs in < and >.
    Give a one sentence explenation of the graphs, do not talk about the code.
    The user only sees the generated graph and does not care about the code.
    Do not use the seaborn library.
    I have provided examples of the expected interaction.
    """

    suffix = """
    User: {question}
    AI: 
    """

    few_shot_prompt_template = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix=prefix,
        suffix=suffix,
        input_variables=["question", "data", "dataFile"]
    )

    return few_shot_prompt_template

def explain_prompt(llm, retreiver):
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, just "
        "reformulate it if needed and otherwise return it as is."
    )
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
    )
    history_aware_retriever = create_history_aware_retriever(
    llm, retreiver.as_retriever(), contextualize_q_prompt
    )

    qa_system_prompt = (
        "You are an assistant for question-answering tasks. Use "
        "the following pieces of retrieved context to answer the "
        "question. If you don't know the answer, just say that you "
        "don't know. Use three sentences maximum and keep the answer "
        "concise."
        "{context}"
    ) 

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt), MessagesPlaceholder("chat_history"), ("human", "{input}"),
        ]   
    )

    return qa_prompt, history_aware_retriever

def classification_prompt():
    classification_prompt = (
            "You are a classification assistant. Your task is to determine if the user's query is requesting "
            "an explanation of the data or asking for a graph to be generated. Respond with one of the following: "
            "'explanation' if the query seeks an explanation of the data, or 'graph' if the query requests a graph. "
            "Do not provide any other text. The query is: {query}"
    )
    return classification_prompt