import streamlit as st
import pandas as pd
import requests
from io import BytesIO
import fitz  # PyMuPDF
from PIL import Image
import base64

st.set_page_config(layout="wide")
st.title("📊 Tableau Dashboard Downloader + Chatbot Assistant")

# --- Sidebar for inputs and downloads ---
with st.sidebar:
    st.header("1. Tableau Dashboard Download")
    tableau_url = st.text_input("Enter Tableau View URL")
    if st.button("Download"):
        if not tableau_url:
            st.warning("Please enter a Tableau view URL.")
        else:
            st.session_state['files'] = {}

            # Simulated endpoints for demonstration — replace as needed
            csv_url = tableau_url + ".csv"
            excel_url = tableau_url + ".xlsx"
            pdf_url = tableau_url + ".pdf"
            png_url = tableau_url + ".png"

            try:
                # CSV
                csv_resp = requests.get(csv_url)
                csv_df = pd.read_csv(BytesIO(csv_resp.content))
                st.session_state['files']['csv'] = csv_df

                # Excel
                xlsx_resp = requests.get(excel_url)
                xlsx_df = pd.read_excel(BytesIO(xlsx_resp.content))
                st.session_state['files']['excel'] = xlsx_df

                # PDF
                pdf_resp = requests.get(pdf_url)
                pdf_text = ""
                with fitz.open(stream=pdf_resp.content, filetype="pdf") as doc:
                    for page in doc:
                        pdf_text += page.get_text()
                st.session_state['files']['pdf_text'] = pdf_text

                # PNG
                png_resp = requests.get(png_url)
                png_img = Image.open(BytesIO(png_resp.content))
                st.session_state['files']['png'] = png_img

                st.success("Download completed successfully!")
            except Exception as e:
                st.error(f"Error downloading files: {e}")

# --- Layout ---
col1, col2 = st.columns([1, 2])

# --- Left Side: Display Downloads ---
with col1:
    st.header("📁 Downloaded Files")
    if 'files' in st.session_state:
        if 'csv' in st.session_state['files']:
            st.subheader("CSV")
            st.dataframe(st.session_state['files']['csv'])

        if 'excel' in st.session_state['files']:
            st.subheader("Excel")
            st.dataframe(st.session_state['files']['excel'])

        if 'pdf_text' in st.session_state['files']:
            st.subheader("PDF Text")
            st.text_area("Extracted Text", st.session_state['files']['pdf_text'], height=200)

        if 'png' in st.session_state['files']:
            st.subheader("Dashboard Image")
            st.image(st.session_state['files']['png'], use_column_width=True)
    else:
        st.info("Enter a Tableau view URL and click Download.")

# --- Right Side: Chatbot ---
with col2:
    st.header("🤖 Chatbot Assistant")

    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    # User input
    prompt = st.chat_input("Ask me about the dashboard data...")

    if prompt:
        st.session_state['chat_history'].append({"role": "user", "content": prompt})

        # --- Construct context ---
        context = ""
        if 'files' in st.session_state:
            if 'csv' in st.session_state['files']:
                context += "CSV Data:\n" + st.session_state['files']['csv'].to_csv(index=False)[:2000] + "\n"
            if 'excel' in st.session_state['files']:
                context += "Excel Data:\n" + st.session_state['files']['excel'].to_csv(index=False)[:2000] + "\n"
            if 'pdf_text' in st.session_state['files']:
                context += "PDF Text:\n" + st.session_state['files']['pdf_text'][:2000] + "\n"
        else:
            context += "No data files loaded."

        # --- Simple response logic (replace with LLM call) ---
        response = f"Thanks for your question! You asked: '{prompt}'.\n\n(Here is some context from the files...)\n\n{context[:1500]}..."

        st.session_state['chat_history'].append({"role": "assistant", "content": response})

    # --- Display Chat History ---
    for msg in st.session_state['chat_history']:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if msg["role"] == "assistant" and 'files' in st.session_state and 'png' in st.session_state['files']:
                st.image(st.session_state['files']['png'], caption="Dashboard Screenshot", use_column_width=True)
