### Install and Run 

1) Install the project environment:
```bash
uv sync
```

2) Start the backend (FastAPI):
```bash
uv run uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

3) In a separate terminal, start the frontend (Streamlit):
```bash
uv run streamlit run frontend/app.py
```

3) Open the UI:
- Streamlit: http://localhost:8501
- FastAPI docs: http://localhost:8000/docs
