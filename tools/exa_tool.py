import os
from exa_py import Exa
from dotenv import load_dotenv

load_dotenv()

exa = Exa(api_key=os.getenv("EXA_API_KEY"))

# Limit result size to stay under Groq rate limits (fewer tokens per run)
MAX_RESULTS = 3
MAX_CHARS_PER_RESULT = 600


def search_threats(query):
    try:
        response = exa.search(query, num_results=MAX_RESULTS, type="auto")
    except (TypeError, AttributeError):
        response = exa.search_and_contents(
            query, type="neural", use_autoprompt=True, num_results=MAX_RESULTS
        )
    results = getattr(response, "results", []) or []

    contents = []
    for r in results:
        text = getattr(r, "text", None) or getattr(r, "content", None)
        if text:
            contents.append(text[:MAX_CHARS_PER_RESULT])
        elif getattr(r, "title", None):
            contents.append(str(r.title))

    return contents if contents else ["No results found for the query."]