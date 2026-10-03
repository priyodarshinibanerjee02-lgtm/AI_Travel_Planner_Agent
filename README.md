 # AI_Travel_Planner_Agent
AI Travel Planner Agent using LangChain, Gemini, RAG and Streamlit


✈️ AI Travel Planner Agent

An AI-powered travel planning application that combines Agentic AI, RAG (Retrieval-Augmented Generation), LangChain, Gemini, ChromaDB, and Streamlit to generate practical and personalized travel plans.

The user provides a destination, number of days, budget, and email address. The AI agent searches the travel-guide knowledge base and generates a detailed itinerary based on the available information and the user's requirements.

## 🚀 Features

🤖 AI-powered travel planning

📚 RAG-based travel guide search

🧠 Agentic AI using LangChain

🔎 ChromaDB vector database for document retrieval

📄 PDF travel-guide ingestion

💰 Budget-aware travel planning

📅 Day-by-day itinerary generation

📧 Email travel plan delivery

📥 Download travel plan as PDF

💬 Follow-up questions with conversational interaction

🛡️ Error handling for API/quota errors

🎨 Streamlit web interface

✈️ Personalized travel recommendations

## 🧩 Technologies Used

Python

Streamlit

LangChain

LangGraph

Google Gemini

Google Generative AI Embeddings

ChromaDB

PyPDF

ReportLab

SMTP / Gmail

python-dotenv

## 🔄 How the System Works

User
  ↓
Streamlit Web App
  ↓
AI Travel Planner Agent
  ↓
Travel Guide Search Tool
  ↓
RAG Pipeline
  ↓
PDF Travel Guides
  ↓
Text Splitting
  ↓
Google Embeddings
  ↓
ChromaDB
  ↓
Relevant Travel Information
  ↓
Gemini LLM
  ↓
Generated Travel Plan
  ↓
PDF Download / Email



## 🧠 Agentic AI Workflow

The application uses an AI agent to understand the user's travel requirements and interact with the travel-guide knowledge base.

```text
User Travel Request
        ↓
Agent
        ↓
Understand Requirements
        ↓
Search Travel Knowledge Base
        ↓
Retrieve Relevant Information
        ↓
Gemini LLM
        ↓
Generate Travel Plan
        ↓
Display Result
      ↙   ↘
PDF Download   Email
```

The generated travel plan includes information such as:

Destination overview

Major tourist attractions

Best time to visit

Local food

Transportation

Accommodation areas

Approximate budget guidance

Safety and travel tips

Local culture

Suggested activities

Important practical information

Day-by-day itinerary


## 📚 RAG Pipeline

The application uses Retrieval-Augmented Generation (RAG) to provide travel information from the available travel-guide documents.

### RAG Process

```text
Travel Guide PDFs
        ↓
PDF Loading
        ↓
Text Extraction
        ↓
Text Splitting
        ↓
Google Embeddings
        ↓
ChromaDB
        ↓
Vector Similarity Search
        ↓
Relevant Documents
        ↓
Gemini
        ↓
Personalized Travel Plan
```

This allows the AI agent to use relevant information from the travel-guide knowledge base while generating the travel plan.

## 💻 User Input

The Streamlit interface allows the user to enter:

📍 Destination

📅 Number of Days

💰 Budget

📧 Email Address

After entering the details, the user can click:

✨ Generate Travel Plan

The application then generates a personalized travel plan based on the provided requirements.

## 📄 PDF Generation

The generated travel plan can be converted into a formatted PDF using ReportLab.

The PDF contains:

AI Travel Planner title

Personalized Travel Plan subtitle

Formatted headings

Paragraphs

Bullet points

Tables

Page numbers

The user can download the generated travel plan using the:

⬇️ Download Travel Plan as PDF

button.

## 📧 Email Delivery

Users can also receive their generated travel plan through email.

The application uses SMTP / Gmail to send the generated travel plan to the email address provided by the user.

The application also handles email errors and displays an appropriate message if the email cannot be sent.

## 💬 Follow-up Questions

After generating a travel plan, users can ask follow-up questions about their trip.

Examples:

What are the cheapest places to stay?

Which places are best for families?

Can you reduce the budget?

What local food should I try?

## 🛡️ Error Handling

The application includes error handling for problems such as:

Gemini API quota limits

API errors

Email delivery errors

Invalid or missing destination input

## 🎨 User Interface

The application is built using Streamlit and provides a simple web-based interface.

The interface includes:

AI Travel Planner branding

Travel details input section

Destination input

Number of days

Budget

Email address

Generate Travel Plan button

Generated travel plan

PDF download

Email confirmation

Follow-up interaction

## 📁 Project Structure

```text
AI_Travel_Planner_Agent/
│
├── app.py
├── agent.py
├── email_sender.py
├── prompts.py
├── rag.py
├── tools.py
├── requirements.txt
├── README.md
│
├── assets/
│   └── logo.png
│
└── travel_guides/
    ├── Darjeeling_Travel_Guide.pdf
    ├── Goa_Travel_Guide.pdf
    ├── Jaipur_Travel_Guide.pdf
    ├── Kerala_Travel_Guide.pdf
    └── Manali_Travel_Guide.pdf
```

The exact project structure may vary depending on the files used in the project.

## ⚙️ Installation

1. Clone the repository

git clone https://github.com/IshikaKarmakar/AI_Travel_Planner_Agent.git


2. Navigate to the project directory

cd AI_Travel_Planner_Agent

3. Install the required dependencies

pip install -r requirements.txt

## 🔐 Environment Variables

Create a .env file in the project directory and add the required API credentials.

Example:

GOOGLE_API_KEY=your_google_api_key

If email functionality requires Gmail credentials or an app password, configure them according to the email configuration used in email_sender.py.

Do not upload API keys, passwords, or other secrets to GitHub.

## ▶️ Running the Application

Start the Streamlit application using:

streamlit run app.py

The application will open in the browser.


## 🧪 Example Workflow

```text
1. Open the AI Travel Planner
             ↓
2. Enter destination
             ↓
3. Enter number of days
             ↓
4. Enter budget
             ↓
5. Enter email address
             ↓
6. Click "Generate Travel Plan"
             ↓
7. AI agent searches travel knowledge base
             ↓
8. Gemini generates the travel plan
             ↓
9. Travel plan is displayed
             ↓
10. Download PDF
             ↓
11. Receive plan through email
             ↓
12. Ask follow-up questions
```

## 🎯 Project Objective

The main objective of this project is to build an AI-powered travel planning system that combines:

Agentic AI

Retrieval-Augmented Generation

Large Language Models

Vector databases

Document retrieval

Personalized recommendations

Automated PDF generation

Email delivery

The system demonstrates how modern AI technologies can be integrated into a practical real-world application.

## 👥 Project Type

Group Project

Developed as part of an Agentic AI / AI project.

## 📌 Future Improvements

Possible future improvements include:

🌦️ Real-time weather information

🏨 Live hotel recommendations

✈️ Flight search integration

🗺️ Interactive maps

💱 Currency conversion

🌐 Multi-language travel plans

📍 Real-time location-based recommendations

💳 Live travel cost estimation

## ⭐ Conclusion

The AI Travel Planner Agent demonstrates the integration of Agentic AI, RAG, LangChain, Gemini, ChromaDB and Streamlit into a practical travel-planning application.

It provides users with personalized travel plans based on their destination, duration and budget, while also supporting PDF generation, email delivery and follow-up interaction.





