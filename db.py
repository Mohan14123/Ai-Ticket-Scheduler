"""Database operations for AI Ticket Scheduler."""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class Ticket(Base):
    """Ticket model for database."""
    __tablename__ = 'tickets'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50))
    priority = Column(String(20))
    status = Column(String(20), default='open')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DatabaseManager:
    """Manages database connections and operations."""
    
    def __init__(self, db_url: str = "sqlite:///./tickets.db"):
        """Initialize database manager.
        
        Args:
            db_url: Database connection URL
        """
        self.engine = create_engine(db_url, connect_args={"check_same_thread": False})
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def get_session(self):
        """Get a database session."""
        return self.SessionLocal()
    
    def create_ticket(self, title: str, description: str, category: str = None, 
                     priority: str = None, status: str = 'open'):
        """Create a new ticket.
        
        Args:
            title: Ticket title
            description: Ticket description
            category: Ticket category
            priority: Ticket priority
            status: Ticket status
            
        Returns:
            Created ticket object
        """
        session = self.get_session()
        try:
            ticket = Ticket(
                title=title,
                description=description,
                category=category,
                priority=priority,
                status=status
            )
            session.add(ticket)
            session.commit()
            session.refresh(ticket)
            return ticket
        finally:
            session.close()
    
    def get_ticket(self, ticket_id: int):
        """Get a ticket by ID.
        
        Args:
            ticket_id: Ticket ID
            
        Returns:
            Ticket object or None
        """
        session = self.get_session()
        try:
            return session.query(Ticket).filter(Ticket.id == ticket_id).first()
        finally:
            session.close()
    
    def get_all_tickets(self, limit: int = 100):
        """Get all tickets.
        
        Args:
            limit: Maximum number of tickets to return
            
        Returns:
            List of ticket objects
        """
        session = self.get_session()
        try:
            return session.query(Ticket).limit(limit).all()
        finally:
            session.close()
    
    def update_ticket(self, ticket_id: int, **kwargs):
        """Update a ticket.
        
        Args:
            ticket_id: Ticket ID
            **kwargs: Fields to update
            
        Returns:
            Updated ticket object or None
        """
        session = self.get_session()
        try:
            ticket = session.query(Ticket).filter(Ticket.id == ticket_id).first()
            if ticket:
                for key, value in kwargs.items():
                    if hasattr(ticket, key):
                        setattr(ticket, key, value)
                session.commit()
                session.refresh(ticket)
            return ticket
        finally:
            session.close()
