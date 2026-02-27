from crewai import Agent

def get_report_agent(llm):

    return Agent(
        role="Cybersecurity Report Generator",
        goal="Generate structured intelligence reports",
        backstory="Professional cybersecurity documentation expert",
        llm=llm,
        verbose=True
    )