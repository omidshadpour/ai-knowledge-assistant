import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
import requests
import uuid

API_URL = "https://om1d-ai-knowledge-assistant.hf.space"

st.set_page_config(page_title = "RAG Chatbot" , layout = "wide")

st.title("📄 RAG Chatbot (FastAPI + Groq)")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "document_id" not in st.session_state:
    st.session_state.document_id = None

if "message" not in st.session_state:
    st.session_state.message = []

# Upload PDF
st.sidebar.header("📄 Upload PDF")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file" , type = ["pdf"])

if uploaded_file:
    
    if st.sidebar.button("Upload"):

        response = requests.post(
            f"{API_URL}/upload",
            files = {"file": (uploaded_file.name , uploaded_file , "application/pdf")},
            timeout=180 
        )

        if response.status_code == 200:
            data = response.json()
            st.session_state.document_id = data["document_id"]

            st.sidebar.success("Uploaded successfully!")
            st.sidebar.write("Document ID:")
            st.sidebar.code(st.session_state.document_id)

        else:
            st.sidebar.error("Upload failed")


# Chat Section
st.subheader("💬 Chat with your document")

for msg in st.session_state.message:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask something about your document")

if user_input and st.session_state.document_id:
    st.session_state.message.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)


    with st.chat_message("assistant"):
        with requests.post(
            f"{API_URL}/ask-stream",
            json = {
                "question": user_input,
                "document_id": st.session_state.document_id,
                "session_id": st.session_state.session_id
            },
            stream = True
        ) as response:
            if response.status_code ==200:

                def stream_generator():
                    for chunk in response.iter_content(chunk_size = None):
                        if chunk:
                            yield chunk.decode("utf-8")


                full_answer = st.write_stream(stream_generator())

                st.session_state.message.append({
                    "role": "assistant",
                    "content": full_answer
                })

                sources_response = requests.post(
                    f"{API_URL}/ask-sources",
                    json = {
                        "question": user_input,
                        "document_id": st.session_state.document_id,
                        "session_id": st.session_state.session_id
                    }
                )

                if sources_response.status_code == 200:
                    sources = sources_response.json().get("sources" , [])
                    if sources:
                        st.caption("📚 Sources:")

                        for s in sources:
                            st.write(f"- Page {s['page']} | {s['source']}")

            else:
                st.error("Error calling API")

            
elif user_input and not st.session_state.document_id:
    st.warning("Please upload a PDF first")

