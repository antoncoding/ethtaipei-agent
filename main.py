import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from tools.search import search
from configs.prompt import prompt
# Load environment variables
load_dotenv()

def main():
    # Initialize the model
    model = ChatOpenAI(
        model="gpt-4",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY")
    )

    # Define tools
    tools = [search]

    # Create the ReAct agent
    graph = create_react_agent(
        model,
        tools=tools,
        # Add a custom system prompt
        prompt=prompt
    )

    # Example interaction
    inputs = {
        "messages": [
            ("user", "What are the latest developments in AI?")
        ]
    }

    # Run the agent
    response = graph.invoke(inputs)
    
    # Print the response
    print("\nAgent's response:")
    print(response["messages"][-1][1])

if __name__ == "__main__":
    main() 