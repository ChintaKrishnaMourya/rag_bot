from langchain.tools import DuckDuckGoSearchRun
import re
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent, create_pandas_dataframe_agent
import pandas as pd
import apis
import os
import streamlit as st

search = DuckDuckGoSearchRun()

def duck_search(query):
    try:
        duck_search_results = search.run(query)
        duck_search_results = duck_search_results.lower()
        link_pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+|www\.[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})|\b[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})\b"
        words_to_remove = ["hdfc", "square yards", "links", "link" ]
        combined_pattern = link_pattern + "|" + '|'.join(r'\b{}\b'.format(word) for word in words_to_remove)
    
        cleaned_results = re.sub(combined_pattern, '', duck_search_results)
    
        return cleaned_results
    except :
        return ""
    
csv_agent = create_csv_agent(
    ChatOpenAI(temperature=0, model="gpt-4", openai_api_key="sk"),
    "Final.csv",
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    handle_parsing_errors=True,
)


df = pd.read_csv(r"bank_transactions_sorted_2023.csv")

pd_agent = create_pandas_dataframe_agent(
    prefix="you are provided with  dataframe df, it has 'Date', 'Transaction Description', 'Amount', 'Balance' as columns. From the query, try to use these columns to retrive the infromation from the dataframe ",
    llm=ChatOpenAI(temperature=0, model="gpt-4", openai_api_key=""),
    df=df,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    handle_parsing_errors=True,
    include_df_in_prompt=True
)


def vector_search(query):
    import pinecone
    import openai
    openai.api_key = "sk-"
    pinecone.init(
      api_key=apis.pinekey,
      environment= apis.pineenv
    )
    index = pinecone.Index('sib')
    response = openai.Embedding.create(
            input=query,
            model="text-embedding-ada-002",
            openai_api_key=apis.openai_key
        )

    res = response["data"][0]["embedding"]

    result = index.query(
        vector=res,
        include_values=True,
        include_metadata=True,
        top_k=6,
    )

    data = ""

    for l, i in enumerate(result['matches']):
          ind = f"Query Match {l + 1} is: "
          data += ind + str(i['metadata']['page_content']) + '\n\n'
    return data

def vectara_search(query):
    pass

#decorator
def enable_chat_history(func):
    # to clear chat history after switching chatbot
    current_page = func.__qualname__
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = current_page
    if st.session_state["current_page"] != current_page:
        try:
            st.cache_resource.clear()
            del st.session_state["current_page"]
            del st.session_state["messages"]
        except:
            pass

    # to show chat history on ui
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "PropGPT", "content": "How can I help you?"}]
    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])


    def execute(*args, **kwargs):
        func(*args, **kwargs)
    return execute

def display_msg(msg, author):
    """Method to display message on the UI

    Args:
        msg (str): message to display
        author (str): author of the message -user/assistant
    """
    st.session_state.messages.append({"role": author, "content": msg})
    st.chat_message(author).write(msg)