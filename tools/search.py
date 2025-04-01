from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.tools import tool

@tool
def search(query: str) -> str:
    """Use this tool to search the internet using DuckDuckGo.
    
    Args:
        query: The search query to look up
        
    Returns:
        A string containing the search results with titles, links, and snippets
    """
    search_tool = DuckDuckGoSearchResults(output_format="list")
    results = search_tool.invoke(query)
    
    # Format the results in a readable way
    formatted_results = []
    for result in results:
        formatted_results.append(f"Title: {result['title']}\nLink: {result['link']}\nSnippet: {result['snippet']}\n")
    
    return "\n".join(formatted_results) 