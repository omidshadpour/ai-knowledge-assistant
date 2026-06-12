#!/bin/sh

# FastAPI روی پورت 8000
uvicorn main:app --host 0.0.0.0 --port 8000 &

sleep 30

# Streamlit روی پورت 7860 با root path
streamlit run app/ui/streamlit_app.py \
  --server.port 7860 \
  --server.address 0.0.0.0 \
  --server.baseUrlPath ""