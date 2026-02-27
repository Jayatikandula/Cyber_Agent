import os
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"

from dotenv import load_dotenv
load_dotenv()

from crewai import LLM
from tools.exa_tool import search_threats

llm = LLM(
    model="ollama/phi3",
    temperature=0.2,
    max_tokens=200
)

def run_pipeline(user_query):
    try:
        # 1️⃣ Get search results (limit to 1)
        results = search_threats(user_query)

        if not results:
            return "No threat data found."

        # 2️⃣ Use only first 1000 characters
        context = results[0][:1000]

        # 3️⃣ Generate report
        prompt = f"""
        Based on the following cybersecurity information:

        {context}

        Generate a structured threat report including:
        - Executive Summary
        - Risk Level
        - Affected Sector
        - Key Findings
        - Recommendations

        Keep it short and professional.
        """

        response = llm.call(prompt)
        return response

    except Exception as e:
        return f"Error: {str(e)}"