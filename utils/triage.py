"""Ticket triage logic using ML models."""
import pickle
import os
from typing import Dict, Tuple
import numpy as np


class TicketTriager:
    """Triages tickets using trained ML models."""
    
    def __init__(self, model_path: str = 'models/triage_model.pkl'):
        """Initialize ticket triager.
        
        Args:
            model_path: Path to the trained model file
        """
        self.model_path = model_path
        self.model = None
        self.vectorizer = None
        self.load_model()
    
    def load_model(self):
        """Load the trained model from disk."""
        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as f:
                data = pickle.load(f)
                self.model = data.get('model')
                self.vectorizer = data.get('vectorizer')
        else:
            print(f"Warning: Model file not found at {self.model_path}")
    
    def predict_category(self, ticket_text: str) -> str:
        """Predict the category of a ticket.
        
        Args:
            ticket_text: Combined title and description of the ticket
            
        Returns:
            Predicted category
        """
        if self.model is None or self.vectorizer is None:
            return "uncategorized"
        
        # Vectorize the text
        text_vector = self.vectorizer.transform([ticket_text])
        
        # Predict category
        category = self.model.predict(text_vector)[0]
        return category
    
    def predict_priority(self, ticket_text: str) -> str:
        """Predict the priority of a ticket.
        
        Args:
            ticket_text: Combined title and description of the ticket
            
        Returns:
            Predicted priority (high, medium, low)
        """
        # Simple heuristic-based priority detection
        ticket_lower = ticket_text.lower()
        
        # High priority keywords
        high_priority_keywords = ['urgent', 'critical', 'emergency', 'down', 'outage', 
                                 'not working', 'broken', 'security', 'breach']
        
        # Medium priority keywords
        medium_priority_keywords = ['issue', 'problem', 'error', 'bug', 'slow', 
                                   'performance', 'help']
        
        # Check for high priority
        if any(keyword in ticket_lower for keyword in high_priority_keywords):
            return 'high'
        
        # Check for medium priority
        if any(keyword in ticket_lower for keyword in medium_priority_keywords):
            return 'medium'
        
        return 'low'
    
    def triage_ticket(self, title: str, description: str) -> Dict[str, str]:
        """Triage a ticket to determine category and priority.
        
        Args:
            title: Ticket title
            description: Ticket description
            
        Returns:
            Dictionary with category and priority
        """
        ticket_text = f"{title} {description}"
        
        category = self.predict_category(ticket_text)
        priority = self.predict_priority(ticket_text)
        
        return {
            'category': category,
            'priority': priority
        }
