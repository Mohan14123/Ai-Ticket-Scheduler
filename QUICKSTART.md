# Quick Start Guide

This guide will help you get the AI Ticket Scheduler up and running in minutes.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation Steps

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/Mohan14123/Ai-Ticket-Scheduler.git
cd Ai-Ticket-Scheduler

# Install dependencies
pip install -r requirements.txt
```

### 2. Use Existing Data and Model

The repository already includes:
- Pre-generated synthetic training data (1000 tickets)
- Pre-trained ML model

You can start using the system immediately!

### 3. Run the Web Interface

```bash
streamlit run streamlit_app.py
```

Open your browser to: http://localhost:8501

### 4. Or Run the API

```bash
python api.py
```

API will be available at: http://localhost:8000
API docs at: http://localhost:8000/docs

## Optional: Regenerate Training Data and Model

If you want to regenerate the data and retrain the model:

```bash
# Step 1: Generate new synthetic data
python data/generate_synthetic.py

# Step 2: Train the model
python train.py
```

## Quick Feature Tour

### Web Interface

1. **Create Ticket**: Submit new tickets with auto-triage
2. **View Tickets**: Browse and filter existing tickets
3. **Triage Demo**: Test the AI classification system
4. **Analytics**: View ticket statistics and trends

### API Usage

```python
import requests

# Create a ticket
ticket = {
    "title": "Cannot access email",
    "description": "My email account is not loading"
}
response = requests.post("http://localhost:8000/tickets", json=ticket)
print(response.json())
```

## Next Steps

- Check the [README.md](README.md) for detailed documentation
- Explore the API at http://localhost:8000/docs
- Customize ticket categories in `data/generate_synthetic.py`
- Adjust priority detection in `utils/triage.py`

## Troubleshooting

**Issue**: Module not found errors
**Solution**: Make sure you've installed all dependencies with `pip install -r requirements.txt`

**Issue**: Port already in use
**Solution**: 
- For Streamlit: Use `streamlit run streamlit_app.py --server.port 8502`
- For API: Change port in `api.py` or run with `uvicorn api:app --port 8001`

**Issue**: Database errors
**Solution**: Delete `tickets.db` file and restart the application

## Support

For issues, please open an issue on GitHub:
https://github.com/Mohan14123/Ai-Ticket-Scheduler/issues
