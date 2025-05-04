from langchain_ollama.llms import OllamaLLM
from langchain_ollama import ChatOllama
from langchain.agents import initialize_agent, Tool, AgentType, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from stock_tools import get_stock_symbol
import streamlit as st

from db_tools import add_stock_tool, list_stock_tool, update_stock_tool, delete_stock_tool
from dotenv import load_dotenv
import os

def build_tools():
    stock_tools = [
        Tool(name="Add stock", func=add_stock_tool, description="Adds a stock to watchlist: with input in format 'SYMBOL:PRICE:QTY'. Extract only the symbol, price and quantity there should not be any other text to input. Also ensure these fields are separated by : and no other characters"),
        Tool(name="List stock", func=list_stock_tool, description="List all stocks from watchlist"),
        Tool(name="Update stock", func=update_stock_tool, description="Update a stock in watchlist"),
        Tool(name="Delete stock", func=delete_stock_tool, description="Delete a stock from watchlist"),
        Tool(name="Stock Symbol", func=get_stock_symbol, description="Get 4 letter NASDAQ stock symbol with input string as the full name of a US company")
    ]
    return stock_tools

def create_agent_executor(model, tools, prompt):
    # Create the ReAct agent
    agent = create_react_agent(llm=model, tools=tools, prompt=prompt)
    # Create an agent executor
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    return agent_executor

def main():
    ollama_model = OllamaLLM(model="gemma3:12b")
    tools = build_tools()
    prompt = PromptTemplate.from_template(os.getenv("PROMPT_TEMPLATE"))

    agent_executor = create_agent_executor(model=ollama_model, tools=tools, prompt=prompt)
    # response = agent_executor.invoke(({"input":"Can you add ORCL at threshold price of $30 for a quantity of 8 in watchlist?"}))
    response = agent_executor.invoke({"input": "Can you list shares we track?"})
    # response = agent_executor.invoke({"input": "Get you get stock symbol for Oracle?"})
    print(response)


def main_streamlit():
    ollama_model = ChatOllama(model="gemma3:12b")
    tools = build_tools()
    prompt = PromptTemplate.from_template(os.getenv("PROMPT_TEMPLATE"))

    agent_executor = create_agent_executor(model=ollama_model, tools=tools, prompt=prompt)
    st.title("🔍 US Stock Ticker Finder")
    st.markdown("Enter a company name to get its **4-letter US stock symbol** (if available).")

    company_name = st.text_input("Company Name", placeholder="e.g. Microsoft")

    if st.button("Find Symbol") and company_name:
        with st.spinner("Searching..."):
            result = agent_executor.invoke({"input": "Can you list shares we track?"})
            st.success(result["output"])

if __name__ == "__main__":
    load_dotenv()
    main_streamlit()