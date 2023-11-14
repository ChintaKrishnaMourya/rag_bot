import streamlit as st
import pandas as pd
from bank_agent import agent, Financial_BehaviourAnalysis
    

##############################################################################################################    
from langchain.callbacks import StreamlitCallbackHandler
from utils import enable_chat_history, display_msg

# Initialize the behaviour analysis object
# Make sure that Financial_BehaviourAnalysis has a __call__ method if you want to use it as behaviour(query, context)
behaviour = Financial_BehaviourAnalysis()



###############################################################################################
st.header('Banking Mate')
st.caption(':blue[_A Personalized Banking Assistant_]')

@enable_chat_history
def main():
        user_query = st.chat_input(placeholder="Ask your Query")
        uploaded_csv = st.file_uploader("Upload your balance sheet (csv):", type=["csv"])
        if user_query:
            if uploaded_csv is not None:
                df = pd.read_csv(uploaded_csv)
                last_50 = df.tail(50)  # Extract the last 50 rows
                display_msg(user_query, 'user')
            # Convert the last 50 rows to a string representation
                query = user_query + '\n'+ last_50.to_string(index=False, header=False)
            # Make sure behaviour can be called like this
                with st.chat_message("BankingMate"):
                    # st_cb = StreamlitCallbackHandler(st.container())
                    response = behaviour(query)
                    st.session_state.messages.append({"role": "BankingMate", "content": response})
                    st.write(response)

            else:
                display_msg(user_query, 'user')
                with st.chat_message("BankingMate"):
                    st_cb = StreamlitCallbackHandler(st.container())
                    response = agent.run(user_query, callbacks=[st_cb])
                    st.session_state.messages.append({"role": "BankingMate", "content": response})
                    st.write(response)


if __name__ == "__main__":
    main()
