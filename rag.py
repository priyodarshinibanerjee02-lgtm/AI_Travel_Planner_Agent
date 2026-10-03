

from pathlib import Path
import os

from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma


# ---------------------------------------------------------
# Load API Key
# ---------------------------------------------------------

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env")


# ---------------------------------------------------------
# Directories
# ---------------------------------------------------------

BASE_DIR = Path(__file__).parent

TRAVEL_GUIDES_DIR = BASE_DIR / "travel_guides"

CHROMA_DIR = BASE_DIR / "chroma_db"


# ---------------------------------------------------------
# Google Embeddings
# ---------------------------------------------------------

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=GOOGLE_API_KEY
)


# ---------------------------------------------------------
# Load Travel Guide PDFs
# ---------------------------------------------------------

def load_travel_documents():

    documents = []

    for pdf_file in TRAVEL_GUIDES_DIR.glob("*.pdf"):

        loader = PyPDFLoader(str(pdf_file))

        documents.extend(loader.load())

    return documents


# ---------------------------------------------------------
# Split Documents into Chunks
# ---------------------------------------------------------

def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    return splitter.split_documents(documents)


# ---------------------------------------------------------
# Create Vector Store ONLY ONCE
# ---------------------------------------------------------

def create_vector_store():

    # If Chroma DB already exists,
    # DO NOT embed the PDFs again.

    if CHROMA_DIR.exists():

        print("Existing ChromaDB found. Using it.")

        vector_store = Chroma(
            persist_directory=str(CHROMA_DIR),
            embedding_function=embeddings
        )

        return vector_store


    # -----------------------------------------------------
    # First-time creation
    # -----------------------------------------------------

    print("Creating ChromaDB for the first time...")

    documents = load_travel_documents()

    if not documents:
        raise ValueError(
            "No PDF files found in the travel_guides folder."
        )

    chunks = split_documents(documents)

    print(f"Loaded {len(documents)} pages.")
    print(f"Created {len(chunks)} chunks.")

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR)
    )

    print("ChromaDB created successfully.")

    return vector_store


# ---------------------------------------------------------
# Create Retriever
# ---------------------------------------------------------

def get_retriever():

    vector_store = create_vector_store()

    return vector_store.as_retriever(
        search_kwargs={"k": 4}
    )
# from pathlib import Path

# from langchain_community.document_loaders import PyPDFLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter


# # ---------------------------------------------------------
# # Travel Guide PDF Folder
# # ---------------------------------------------------------

# BASE_DIR = Path(__file__).parent
# TRAVEL_GUIDES_DIR = BASE_DIR / "travel_guides"


# # ---------------------------------------------------------
# # Load all Travel Guide PDFs
# # ---------------------------------------------------------

# def load_travel_documents():
#     documents = []

#     for pdf_file in TRAVEL_GUIDES_DIR.glob("*.pdf"):
#         loader = PyPDFLoader(str(pdf_file))
#         documents.extend(loader.load())

#     return documents


# # ---------------------------------------------------------
# # Split Documents into Chunks
# # ---------------------------------------------------------

# def split_documents(documents):
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=1000,
#         chunk_overlap=200
#     )

#     return splitter.split_documents(documents)

# # ---------------------------------------------------------
# # Google Embeddings + ChromaDB
# # ---------------------------------------------------------

# import os
# from dotenv import load_dotenv
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_community.vectorstores import Chroma

# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# if not GOOGLE_API_KEY:
#     raise ValueError("GOOGLE_API_KEY not found in .env")


# # Create Google Embeddings
# embeddings = GoogleGenerativeAIEmbeddings(
#     model="models/gemini-embedding-001",
#     google_api_key=GOOGLE_API_KEY
# )


# # ---------------------------------------------------------
# # Create ChromaDB
# # ---------------------------------------------------------

# CHROMA_DIR = BASE_DIR / "chroma_db"


# def create_vector_store():
#     documents = load_travel_documents()
#     chunks = split_documents(documents)

#     vector_store = Chroma.from_documents(
#         documents=chunks,
#         embedding=embeddings,
#         persist_directory=str(CHROMA_DIR)
#     )

#     return vector_store

# # ---------------------------------------------------------
# # Create Retriever
# # ---------------------------------------------------------

# def get_retriever():
#     vector_store = create_vector_store()

#     return vector_store.as_retriever(
#         search_kwargs={"k": 4}
#     )
