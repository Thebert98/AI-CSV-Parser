import streamlit as st
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv

def main():
    load_dotenv()
    st.set_page_config(page_title = "CSV Parser")
    st.header = "Ask the CSV file"
    user_csv = st.file_uploader("Upload your CSV file", type = "csv")

    if user_csv is not None:
        option = st.selectbox(
            "Choose what llm to use",
            ("OpenAI","Groq"),
            index = None,
            placeholder = "Select an LLM provider..."
        )
        if option is not None and option != "":
            user_question = st.text_input("Ask a question to the CSV:")
            
            if option == "OpenAI":
                llm = OpenAI(temperature = 0)
                agent = create_csv_agent(llm,
                                        user_csv,
                                        verbose = True)
                if user_question is not None and user_question !="":
                    response = agent.run(user_question)

                    st.write(response)
                
            elif option == "Groq":
                llm = ChatGroq(temperature=0, model_name="mixtral-8x7b-32768")
                agent = create_csv_agent(llm,
                                        user_csv,
                                        verbose = True)
                if user_question is not None and user_question !="":
                    response = agent.run(user_question)

                    st.write(response)

if __name__ == "__main__":
    main()
