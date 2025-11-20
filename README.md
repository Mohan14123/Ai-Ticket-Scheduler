# AI Ticket Scheduler

AI-powered service desk ticket triage & automation system.

## Overview

AI Ticket Scheduler is an intelligent ticket management system that uses machine learning to automatically categorize and prioritize support tickets. The system includes:

- **Automated Ticket Triage**: ML-powered classification and priority assignment
- **REST API**: Full-featured API for ticket management
- **Web Interface**: Interactive Streamlit dashboard
- **Synthetic Data Generation**: Tools for training data creation

## Project Structure

```
ai-ticket-scheduler/
│
├── api.py                      # FastAPI REST API
├── train.py                    # ML model training script
├── streamlit_app.py            # Streamlit web interface
├── db.py                       # Database operations
│
├── models/                     # Trained models (generated)
│   └── triage_model.pkl
│
├── utils/                      # Utility modules
│   ├── triage.py              # Ticket triage logic
│   └── embeddings.py          # Text embeddings
│
├── data/                       # Data generation
│   └── generate_synthetic.py  # Synthetic data generator
│
├── sample_data/                # Generated data (created on first run)
│
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Features

- **Automatic Categorization**: Classifies tickets into categories (network, hardware, software, account, security)
- **Priority Detection**: Assigns priority levels (high, medium, low) based on content analysis
- **REST API**: Complete CRUD operations for ticket management
- **Web Dashboard**: User-friendly interface for ticket creation and management
- **Analytics**: Visual insights into ticket distribution and trends
- **ML Training Pipeline**: Train custom models on your data

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Mohan14123/Ai-Ticket-Scheduler.git
cd Ai-Ticket-Scheduler
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Generate Training Data

Generate synthetic ticket data for training:

```bash
python data/generate_synthetic.py
```

This creates `sample_data/synthetic_tickets.csv` with 1000 sample tickets.

### 2. Train the Model

Train the ML classification model:

```bash
python train.py
```

This creates `models/triage_model.pkl` with the trained model.

### 3. Run the API

Start the FastAPI server:

```bash
python api.py
```

Or use uvicorn directly:

```bash
uvicorn api:app --reload
```

Access the API documentation at: http://localhost:8000/docs

### 4. Run the Web Interface

Launch the Streamlit dashboard:

```bash
streamlit run streamlit_app.py
```

Access the web interface at: http://localhost:8501

## Usage

### Creating a Ticket (API)

```python
import requests

ticket = {
    "title": "Cannot connect to VPN",
    "description": "I am unable to connect to the company VPN from my laptop"
}

response = requests.post("http://localhost:8000/tickets", json=ticket)
print(response.json())
```

### Creating a Ticket (Python)

```python
from db import DatabaseManager
from utils.triage import TicketTriager

# Initialize
db = DatabaseManager()
triager = TicketTriager()

# Triage ticket
result = triager.triage_ticket(
    title="Network is down",
    description="The office network is completely down"
)

# Create ticket
ticket = db.create_ticket(
    title="Network is down",
    description="The office network is completely down",
    category=result['category'],
    priority=result['priority']
)
```

### Using the Web Interface

1. Navigate to "Create Ticket" to submit new tickets
2. Use "View Tickets" to browse and filter existing tickets
3. Try "Triage Demo" to test the AI classification
4. Check "Analytics" for ticket statistics and trends

## API Endpoints

- `GET /` - API information
- `POST /tickets` - Create a new ticket
- `GET /tickets` - Get all tickets
- `GET /tickets/{ticket_id}` - Get a specific ticket
- `PUT /tickets/{ticket_id}` - Update a ticket
- `POST /tickets/triage` - Triage a ticket (prediction only)

## Model Information

The system uses:
- **TF-IDF Vectorization** for text feature extraction
- **Naive Bayes Classifier** for category prediction
- **Keyword-based heuristics** for priority detection

Categories:
- network
- hardware
- software
- account
- security

Priority Levels:
- high (urgent, critical issues)
- medium (important issues)
- low (routine requests)

## Development

### Adding New Categories

1. Update `data/generate_synthetic.py` with new ticket templates
2. Regenerate training data
3. Retrain the model

### Customizing Priority Rules

Edit the `predict_priority` method in `utils/triage.py` to adjust priority detection logic.

## Dependencies

- FastAPI - REST API framework
- Streamlit - Web interface
- SQLAlchemy - Database ORM
- scikit-learn - Machine learning
- sentence-transformers - Text embeddings
- pandas - Data manipulation

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.
