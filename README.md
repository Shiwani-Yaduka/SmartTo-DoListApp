# SmartTo-DoListApp
A smart to-do list app built with Streamlit and powered by Gemini AI that helps users manage tasks and generate well-structured essays or content in PDF format based on task descriptions.

📘 Smart To-Do List with Gemini AI
This Streamlit-based application is an intelligent productivity tool that combines task management with the power of Google Gemini AI. Users can create and manage their tasks, and for any given task, the app can automatically generate structured content (like essays or answers) and export it as a downloadable PDF.

🚀 Features
Interactive Task Management
Easily add, view, and manage tasks with titles, descriptions, and deadlines.

AI-Powered Content Generation
Leverages the Gemini 2.0 Flash model to generate well-structured essays or explanations for each task using custom prompts derived from the task description.

Structured Output with Pydantic
Ensures consistent essay generation using pydantic models with fields like title, word count, sections, and full content.

Automatic PDF Export
Each generated response is converted into a clean, professional PDF using the FPDF library and saved locally.

Download Option
Instantly download generated answers as PDFs through the app UI.

Session Persistence
Maintains state using Streamlit's session_state, including tasks and their completion status.

🔧 Technologies Used
Python

Streamlit – UI & interactive web app

Google Gemini API – AI content generation

FPDF – PDF creation

Pydantic – Structured data validation

OS, datetime, pathlib – File management & utilities
