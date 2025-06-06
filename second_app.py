import streamlit as st
from fpdf import FPDF
import os
from datetime import datetime
from google import genai
from pydantic import BaseModel
from typing import List
import pathlib

# Create PDF directory if it doesn't exist
PDF_DIR = "pdfs"
pathlib.Path(PDF_DIR).mkdir(exist_ok=True)

# Define Pydantic models for structured output
class Task(BaseModel):
    title: str
    description: str
    deadline: str
    completed: bool = False
    pdf: str | None = None

class Essay(BaseModel):
    title: str
    content: str
    word_count: int
    sections: List[str]

# Initialize Gemini client
client = genai.Client(api_key="API_KEY")

# Initialize session state
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'clear_inputs' not in st.session_state:
    st.session_state.clear_inputs = False

# Handle input clearing flag
if st.session_state.get("clear_inputs", False):
    st.session_state.update({
        "📝 Task Title": "",
        "🗒 Description": "",
        "📅 Deadline": datetime.now().date(),
        "clear_inputs": False
    })

# --- UI: App Title and Input Form ---
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📝 Smart To-Do List with Gemini AI</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

with st.container():
    st.markdown("### ➕ Add a New Task")
    col1, col2 = st.columns([2, 1])
    with col1:
        title = st.text_input("📝 Task Title", key="📝 Task Title")
        description = st.text_area("🗒 Description", height=100, key="🗒 Description")
    with col2:
        deadline = st.date_input("📅 Deadline", key="📅 Deadline")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Add Task", use_container_width=True):
        task = Task(
            title=title,
            description=description,
            deadline=str(deadline)
        )
        st.session_state.tasks.append(task)
        st.success("✅ Task Added Successfully!")

# --- Display Tasks ---
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("📋 Your Tasks")

if not st.session_state.tasks:
    st.info("You don't have any tasks yet. Add one above to get started!")
else:
    for i, task in enumerate(st.session_state.tasks):
        st.markdown(f"#### 🗂 {task.title} &nbsp;&nbsp;&nbsp;🕒 Due: {task.deadline}")
        st.markdown(f"<div style='padding-left: 15px;'>{task.description}</div>", unsafe_allow_html=True)

        if not task.completed:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(f"🤖 Solve with Gemini", key=f"gemini_{i}"):
                with st.spinner("📡 Sending to Gemini..."):
                    prompt = f"Topic: {task.title}\n\nInstructions: {task.description}"

                    try:
                        response = client.models.generate_content(
                            model="gemini-2.0-flash",
                            contents=prompt,
                            config={
                                "response_mime_type": "application/json",
                                "response_schema": Essay,
                            }
                        )

                        essay: Essay = response.parsed

                        safe_title = "".join(c for c in task.title if c.isalnum() or c in (' ', '-', '_')).strip()
                        pdf_filename = f"{safe_title}{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
                        pdf_path = os.path.join(PDF_DIR, pdf_filename)

                        pdf = FPDF()
                        pdf.add_page()
                        pdf.set_font("Arial", size=12)
                        safe_content = essay.content.encode('latin-1', 'ignore').decode('latin-1')
                        pdf.multi_cell(0, 10, safe_content)
                        pdf.output(pdf_path)

                        task.completed = True
                        task.pdf = pdf_path
                        st.success("✅ Answer Generated & PDF Created!")

                        # ✅ Show download button immediately
                        with open(pdf_path, "rb") as f:
                            st.download_button(
                                "📥 Download Answer PDF",
                                f,
                                file_name=os.path.basename(pdf_path),
                                mime="application/pdf",
                                key=f"download_now_{i}"
                            )

                        # ✅ Set flag to clear inputs on rerun
                        st.session_state.clear_inputs = True

                        with st.expander("📚 View Essay Info"):
                            st.markdown(f"Word Count: {essay.word_count}")
                            st.markdown("Sections:")
                            for section in essay.sections:
                                st.markdown(f"- {section}")

                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        elif task.pdf and os.path.exists(task.pdf):
            try:
                with open(task.pdf, "rb") as f:
                    st.download_button(
                        "📥 Download Answer PDF",
                        f,
                        file_name=os.path.basename(task.pdf),
                        mime="application/pdf"
                    )
            except Exception as e:
                st.error(f"❌ Error accessing PDF: {str(e)}")
                st.info("PDF file might have been moved or deleted.")

        st.markdown("---")
