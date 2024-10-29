from langchain.prompts import PromptTemplate, FewShotPromptTemplate

examples = [
    {
        "question": "Can you graph the screen time of the first 50 users",
        "response": """
        START
        import pandas as pd
        import matplotlib.pyplot as plt

        def generate_plot():
            data = pd.read_csv('../../Datasets/user_behavior_dataset.csv')

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

def getPrompt():
    return few_shot_prompt_template