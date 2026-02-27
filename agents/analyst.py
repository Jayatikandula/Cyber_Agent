from crewai import Agent
from crewai.tools import tool
from vector_store import retrieve


@tool("Retrieve stored threat documents")
def retrieval_tool(query: str) -> str:
    """Retrieve relevant threat documents from the vector store for analysis."""
    docs = retrieve(query)
    return "\n\n".join([d.page_content for d in docs]) if docs else "No documents found."


def get_analyst_agent(llm):
    return Agent(
        role="Cyber Threat Analyst",
        goal="Analyze threats and extract structured intelligence",
        backstory="Expert in cybersecurity risk assessment",
        llm=llm,
        tools=[retrieval_tool],
        verbose=True,
    )