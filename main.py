import os
import sys
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from tools.coinbase import get_coinbase_tools
from tools.search import search
from configs.prompt import prompt

# Load environment variables
load_dotenv()

def initialize_agent():
    """Initialize the agent with all available tools."""
    # Initialize the model
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY")
    )

    # Get all tools
    tools = [search] + get_coinbase_tools()
    
    # Create memory for the agent
    memory = MemorySaver()
    
    # Create the ReAct agent
    agent = create_react_agent(
        model=llm,
        tools=tools,
        checkpointer=memory,
        prompt=prompt
    )
    
    config = {"configurable": {"thread_id": "AI Assistant Chatbot"}}
    return agent, config

def run_chat_mode(agent_executor, config):
    """Run the agent interactively based on user input."""
    print("Starting chat mode... Type 'exit' to end.")
    while True:
        try:
            user_input = input("\nPrompt: ")
            if user_input.lower() == "exit":
                break

            # Run agent with the user's input in chat mode
            for chunk in agent_executor.stream(
                {"messages": [HumanMessage(content=user_input)]}, config
            ):
                if "agent" in chunk:
                    print(chunk["agent"]["messages"][0].content)
                elif "tools" in chunk:
                    print(chunk["tools"]["messages"][0].content)
                print("-------------------")

        except KeyboardInterrupt:
            print("Goodbye Agent!")
            sys.exit(0)

def main():
    """Start the chatbot agent."""
    print("Initializing Agent...")
    agent_executor, config = initialize_agent()
    print("Agent initialized successfully!")
    run_chat_mode(agent_executor=agent_executor, config=config)

if __name__ == "__main__":
    print("Starting Agent...")
    main() 