
uvicorn main:app --host 0.0.0.0 --port 8000 &

sleep 30


curl http://localhost:8000/ || echo "FastAPI NOT running!"


streamlit run app/ui/streamlit_app.py --server.port 7860 --server.address 0.0.0.0