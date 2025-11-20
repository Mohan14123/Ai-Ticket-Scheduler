"""FastAPI REST API for AI Ticket Scheduler."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from db import DatabaseManager, Ticket
from utils.triage import TicketTriager

app = FastAPI(
    title="AI Ticket Scheduler API",
    description="REST API for AI-powered service desk ticket triage and automation",
    version="1.0.0"
)

# Initialize database and triager
db_manager = DatabaseManager()
triager = TicketTriager()


class TicketCreate(BaseModel):
    """Schema for creating a ticket."""
    title: str
    description: str
    category: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = 'open'


class TicketUpdate(BaseModel):
    """Schema for updating a ticket."""
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None


class TicketResponse(BaseModel):
    """Schema for ticket response."""
    id: int
    title: str
    description: str
    category: Optional[str]
    priority: Optional[str]
    status: str
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True


@app.get("/")
def read_root():
    """Root endpoint."""
    return {
        "message": "Welcome to AI Ticket Scheduler API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "tickets": "/tickets",
            "triage": "/tickets/triage"
        }
    }


@app.post("/tickets", response_model=TicketResponse)
def create_ticket(ticket: TicketCreate):
    """Create a new ticket.
    
    Args:
        ticket: Ticket data
        
    Returns:
        Created ticket
    """
    # Auto-triage if category or priority not provided
    if ticket.category is None or ticket.priority is None:
        triage_result = triager.triage_ticket(ticket.title, ticket.description)
        
        if ticket.category is None:
            ticket.category = triage_result['category']
        if ticket.priority is None:
            ticket.priority = triage_result['priority']
    
    # Create ticket in database
    db_ticket = db_manager.create_ticket(
        title=ticket.title,
        description=ticket.description,
        category=ticket.category,
        priority=ticket.priority,
        status=ticket.status
    )
    
    return TicketResponse(
        id=db_ticket.id,
        title=db_ticket.title,
        description=db_ticket.description,
        category=db_ticket.category,
        priority=db_ticket.priority,
        status=db_ticket.status,
        created_at=str(db_ticket.created_at),
        updated_at=str(db_ticket.updated_at)
    )


@app.get("/tickets", response_model=List[TicketResponse])
def get_tickets(limit: int = 100):
    """Get all tickets.
    
    Args:
        limit: Maximum number of tickets to return
        
    Returns:
        List of tickets
    """
    tickets = db_manager.get_all_tickets(limit=limit)
    return [
        TicketResponse(
            id=ticket.id,
            title=ticket.title,
            description=ticket.description,
            category=ticket.category,
            priority=ticket.priority,
            status=ticket.status,
            created_at=str(ticket.created_at),
            updated_at=str(ticket.updated_at)
        )
        for ticket in tickets
    ]


@app.get("/tickets/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: int):
    """Get a ticket by ID.
    
    Args:
        ticket_id: Ticket ID
        
    Returns:
        Ticket data
    """
    ticket = db_manager.get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    return TicketResponse(
        id=ticket.id,
        title=ticket.title,
        description=ticket.description,
        category=ticket.category,
        priority=ticket.priority,
        status=ticket.status,
        created_at=str(ticket.created_at),
        updated_at=str(ticket.updated_at)
    )


@app.put("/tickets/{ticket_id}", response_model=TicketResponse)
def update_ticket(ticket_id: int, ticket: TicketUpdate):
    """Update a ticket.
    
    Args:
        ticket_id: Ticket ID
        ticket: Updated ticket data
        
    Returns:
        Updated ticket
    """
    # Prepare update data
    update_data = {k: v for k, v in ticket.dict().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    # Update ticket
    updated_ticket = db_manager.update_ticket(ticket_id, **update_data)
    
    if not updated_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    return TicketResponse(
        id=updated_ticket.id,
        title=updated_ticket.title,
        description=updated_ticket.description,
        category=updated_ticket.category,
        priority=updated_ticket.priority,
        status=updated_ticket.status,
        created_at=str(updated_ticket.created_at),
        updated_at=str(updated_ticket.updated_at)
    )


@app.post("/tickets/triage")
def triage_ticket_endpoint(title: str, description: str):
    """Triage a ticket to predict category and priority.
    
    Args:
        title: Ticket title
        description: Ticket description
        
    Returns:
        Predicted category and priority
    """
    result = triager.triage_ticket(title, description)
    return {
        "title": title,
        "description": description,
        "predicted_category": result['category'],
        "predicted_priority": result['priority']
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
