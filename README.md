# AI Research Assistant

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Yes-green)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT-blueviolet)](https://platform.openai.com/)

A **Streamlit-based AI Research Assistant** that fetches academic papers from **Crossref** and **arXiv**, summarizes abstracts using OpenAI GPT, translates them into multiple languages, allows users to ask questions, and generates downloadable PDFs.

---

## 🔹 Features

- Fetch research papers by topic from **Crossref** & **arXiv**
- Summarize abstracts using **OpenAI GPT**
- Translate summaries to **English, Urdu, or Arabic**
- Ask questions about the collected research papers
- Export results as a **PDF file**
- Interactive and user-friendly **Streamlit interface**

---

## 💻 Installation

1. **Clone the repository:**

git clone https://github.com/ifrahgul/ai-research-assistant.git
cd ai-research-assistant

2. Create a virtual environment (recommended):
*python -m venv venv*

3. Activate the environment:
  
4. Windows:
 - venv\Scripts\activate
----
## Setup OpenAI API Key
Create a .env file in the project root:
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
----
## Run the App
streamlit run app.py

- Enter your research topic
- Select number of papers
- Choose language
- Click Fetch Papers
- Ask questions or download a PDF report
🔐 Security

.env contains your OpenAI API Key (do not share publicly)
venv/ and generated outputs are ignored in GitHub

🛠 Future Improvements

- Add more languages for translation
- Add AI-assisted keyword extraction
- Support larger batch downloads of papers
- Implement user authentication for private research projects

📄 License
MIT License © 2026 Ifrah Gul



