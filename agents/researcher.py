from crewai import Agent
from crewai.tools import tool
from tools.exa_tool import search_threats
from vector_store import store_documents


# Cap total text returned to agent to reduce token usage (Groq rate limits)
MAX_RESEARCH_TOOL_CHARS = 3500


@tool("Search and store threats")
def research_tool(query: str) -> str:
    """Search for latest cybersecurity threats and store results in the vector database."""
    results = search_threats(query)
    store_documents(results)
    combined = "\n\n".join(results)
    return combined[:MAX_RESEARCH_TOOL_CHARS] if len(combined) > MAX_RESEARCH_TOOL_CHARS else combined


def get_research_agent(llm):
    return Agent(
        role="Cyber Threat Researcher",
        goal="Search and gather latest cybersecurity threat data",
        backstory="Expert in cybersecurity intelligence gathering",
        llm=llm,
        tools=[research_tool],
        verbose=True,
    )