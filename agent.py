import os
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent

from rag import get_retriever
from tools import (
    calculate_budget,
    create_itinerary,
    travel_checklist,
    check_destination,
    transport_recommendation,
    packing_recommendation
)


# ---------------------------------------------------------
# Load API Key
# ---------------------------------------------------------

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env")


# ---------------------------------------------------------
# Gemini LLM
# ---------------------------------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0,
    max_output_tokens = 3000
)


# ---------------------------------------------------------
# RAG Retriever Tool
# ---------------------------------------------------------

# retriever = get_retriever()


# def search_travel_guides(query: str) -> str:
#     """Search the travel guide knowledge base for relevant information."""

#     documents = retriever.invoke(query)

#     if not documents:
#         return "No relevant information found in the travel guides."

#     return "\n\n".join(
#         document.page_content
#         for document in documents
#     )

# def search_travel_guides(query: str) -> str:
#     """Search the travel guide knowledge base for relevant information."""
#     retriever = get_retriever()
#     documents = retriever.invoke(query)

retriever = get_retriever()
def search_travel_guides(query: str) -> str:
    """Search the travel guide knowledge base for relevant information."""
    documents = retriever.invoke(query)
    if not documents:
        return "No relevant information found in the travel guides."

    return "\n\n".join(
        document.page_content
        for document in documents
    )


# ---------------------------------------------------------
# Create AI Agent
# ---------------------------------------------------------

agent = create_agent(
    llm,
    # tools=[search_travel_guides],
    tools=[
        search_travel_guides,
        calculate_budget,
        create_itinerary,
        travel_checklist,
        check_destination,
        transport_recommendation,
        packing_recommendation
    ],

    system_prompt=SYSTEM_PROMPT
    
)




