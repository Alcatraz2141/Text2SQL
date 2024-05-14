from typing import List
import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_community.utilities.sql_database import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain.memory import ChatMessageHistory
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from examples import get_example_selector
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,FewShotChatMessagePromptTemplate,PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from operator import itemgetter
from langchain.chains.openai_tools import create_extraction_chain_pydantic
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List
import pandas as pd
import os



st.set_page_config(
    page_title="Local RAG",
    page_icon=":brain:",
)
st.title("Text2SQL Using Personal Database ")
load_dotenv()

db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
db_host = os.getenv("db_host")
db_name = os.getenv("db_name")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Example Prompt
example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}\nSQLQuery:"),
        ("ai", "{query}"),
    ]
)
#Fe shot prompt
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    example_selector=get_example_selector(),
    input_variables=["input","top_k"],
)
# Final Prompt
final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a MySQL expert. Given an input question, create a syntactically correct MySQL query to run. Unless otherwise specificed.\n\nHere is the relevant table info: {table_info}\n\nBelow are a number of examples of questions and their corresponding SQL queries."),
        few_shot_prompt,
        MessagesPlaceholder(variable_name="messages"),
        ("human", "{input}"),
    ]
)
# Answer Prompt
answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)   


def main() -> None:
    # Set assistant_type in session state
    if "model" not in st.session_state:
        st.session_state["model"] = "gpt-3.5-turbo"
    # Initialize chat history
    if "messages" not in st.session_state:  
        # print("Creating session state")
        st.session_state.messages = []
    # Display chat messages from history on app rerun
        st.session_state["messages"] = [{"role": "assistant", "content": "Ask me a SQL query..."}]
    # for message in st.session_state.messages:
    #     with st.chat_message(message["role"]):
    #         st.markdown(message["content"])

    

    # Prompt for user input
    if prompt := st.chat_input():
        st.session_state["messages"].append({"role": "user", "content": prompt})

    # Display existing chat messages
    for message in st.session_state["messages"]:
        if message["role"] == "system":
            continue
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # If last message is from a user, generate a new response
    last_message = st.session_state["messages"][-1]
    if last_message.get("role") == "user":
        question = last_message["content"]
        with st.spinner("Generating response..."):
            with st.chat_message("assistant"):
                response=invoke_chain(prompt,st.session_state.messages)
                st.markdown(response)
                st.session_state["messages"].append({"role": "assistant", "content": response})

@st.cache_resource
# Create Chain
def get_chain():
    print("Creating chain")
    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")    
    generate_query = create_sql_query_chain(llm, db,final_prompt) 
    execute_query = QuerySQLDataBaseTool(db=db)
    rephrase_answer = answer_prompt | llm | StrOutputParser()
    # chain = generate_query | execute_query
    chain = (
    RunnablePassthrough.assign(table_names_to_use=select_table) |
    RunnablePassthrough.assign(query=generate_query).assign(
        result=itemgetter("query") | execute_query
    )
    | rephrase_answer
)

    return chain

# Add History to the Chatbot
def create_history(messages):
    history = ChatMessageHistory()
    for message in messages:
        if message["role"] == "user":
            history.add_user_message(message["content"])
        else:
            history.add_ai_message(message["content"])
    return history

# Invoke Response
def invoke_chain(question,messages):
    chain = get_chain()
    history = create_history(messages)
    response = chain.invoke({"question": question,"top_k":3,"messages":history.messages})
    history.add_user_message(question)
    history.add_ai_message(response)
    return response


# Select Relevant Tables
def get_table_details():
    # Read the CSV file into a DataFrame
    table_description = pd.read_csv("table_desc.csv")
    table_docs = []

    # Iterate over the DataFrame rows to create Document objects
    table_details = ""
    for index, row in table_description.iterrows():
        table_details = table_details + "Table Name:" + row['Tables'] + "\n" + "Table Description:" + row['Description'] + "\n\n"

    return table_details


class Table(BaseModel):
    """Table in SQL database."""

    name: str = Field(description="Name of table in SQL database.")

def get_tables(tables: List[Table]) -> List[str]:
    tables  = [table.name for table in tables]
    return tables

table_details = get_table_details()

# Table prompt
table_details_prompt = f"""Return the names of ALL the SQL tables that MIGHT be relevant to the user question.
The tables are:

{table_details}

Remember to include ALL 'POTENTIALLY RELEVANT' tables, even if you're not sure that they're needed."""

select_table = {"input": itemgetter("question")} | create_extraction_chain_pydantic(Table, llm, system_message=table_details_prompt) | get_tables





   
main()




