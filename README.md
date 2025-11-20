# AI Ticket Scheduler

An AI-powered service desk assistant that automates ticket triage, priority scoring, semantic KB search, and dashboard analytics.

## Features
- NLP-based ticket categorization (DistilBERT)
- Rule-based priority scoring
- Semantic knowledge-base search (FAISS)
- REST API (FastAPI)
- Dashboard (Streamlit)
- SQLite storage + assignment logs
## Files
  ai-ticket-scheduler/
  │
  ├── api.py
  ├── train.py
  ├── streamlit_app.py
  ├── db.py
  │
  ├── models/
  │   └── (trained model saved here)
  │
  ├── utils/ 
  │   ├── triage.py
  │   └── embeddings.py
  │
  ├── data/
  │   └── generate_synthetic.py
  │
  ├── sample_data/
  │
  ├── requirements.txt
  

  
## How to Run
pip install -r requirements.txt
python train.py
uvicorn api:app --reload
streamlit run streamlit_app.py
