import streamlit as st
from openai import OpenAI
import requests, feedparser, re
from urllib.parse import quote
from fpdf import FPDF
from deep_translator import GoogleTranslator
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OPENAI_API_KEY not found in environment. Check your .env file!")
    st.stop()

client = OpenAI(api_key=api_key)

st.set_page_config(page_title="AI Research Assistant", layout="wide")
st.title("AI Research Assistant (Crossref + arXiv)")

lang_map = {"English": "en", "Urdu": "ur", "Arabic": "ar"}


def safe(t):
    return re.sub(r'[^\x00-\x7F]+', ' ', str(t))

def search_crossref(query, limit):
    url = "https://api.crossref.org/works"
    params = {"query": query, "rows": limit}
    r = requests.get(url, params=params).json()
    papers = []
    for item in r["message"]["items"]:
        papers.append({
            "title": item.get("title", ["No title"])[0],
            "abstract": re.sub('<.*?>','',item.get("abstract","")),
            "year": item.get("issued", {"date-parts": [[0]]})["date-parts"][0][0],
            "authors": [a.get("family","") for a in item.get("author", [])],
            "url": item.get("URL","")
        })
    return papers

def search_arxiv(query, limit):
    encoded_query = quote(query)
    url = f"http://export.arxiv.org/api/query?search_query=all:{encoded_query}&start=0&max_results={limit}"
    feed = feedparser.parse(url)
    papers = []
    for e in feed.entries:
        papers.append({
            "title": e.title,
            "abstract": e.summary,
            "year": e.published[:4],
            "authors": [a.name for a in e.authors],
            "url": e.link
        })
    return papers

def summarize(text):
    if not text:
        return "No abstract available."
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Summarize:\n{text}"}],
        temperature=0.4
    )
    return res.choices[0].message.content

def ask(context, q):
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content": f"{context}\n\nQuestion: {q}"}],
        temperature=0.4
    )
    return res.choices[0].message.content

def make_pdf(papers, topic):
    pdf = FPDF()
    pdf.set_auto_page_break(True, 10)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.multi_cell(0, 10, safe(topic))
    pdf.ln(5)
    for p in papers:
        pdf.set_font("Arial", "B", 12)
        pdf.multi_cell(0, 8, safe(p["title"]))
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 8, safe(p["summary"]))
        pdf.ln(4)
    name = "research.pdf"
    pdf.output(name)
    return name

topic = st.text_input("Enter Research Topic")
limit = st.slider("Number of papers", 1, 10, 5)
lang = st.selectbox("Language", ["English", "Urdu", "Arabic"])

if st.button("Fetch Papers"):
    if not topic.strip():
        st.warning("Please enter a research topic.")
    else:
        st.info("Fetching papers...")
        papers = search_crossref(topic, limit) + search_arxiv(topic, limit)
        summaries = []
        for p in papers:
            s = summarize(p["abstract"])
            if lang != "English":
                s = GoogleTranslator(source='auto', target=lang_map[lang]).translate(s)
            p["summary"] = s
            summaries.append(p)
        st.session_state.data = summaries
        st.session_state.topic = topic

if "data" in st.session_state:
    for p in st.session_state.data:
        st.subheader(p["title"])
        st.write(p["summary"])
        st.markdown("---")

    q = st.text_input("Ask Question")
    if q:
        ctx = " ".join([p["summary"] for p in st.session_state.data])
        ans = ask(ctx, q)
        st.success(ans)

    if st.button("Download PDF"):
        f = make_pdf(st.session_state.data, st.session_state.topic)
        with open(f, "rb") as file:
            st.download_button("Download PDF", file, file_name=f)
