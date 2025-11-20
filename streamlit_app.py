"""Streamlit web interface for AI Ticket Scheduler."""
import streamlit as st
import pandas as pd
from db import DatabaseManager
from utils.triage import TicketTriager
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Ticket Scheduler",
    page_icon="🎫",
    layout="wide"
)

# Initialize database and triager
@st.cache_resource
def get_db_manager():
    """Get database manager instance."""
    return DatabaseManager()

@st.cache_resource
def get_triager():
    """Get triager instance."""
    return TicketTriager()

db_manager = get_db_manager()
triager = get_triager()


def main():
    """Main application."""
    st.title("🎫 AI Ticket Scheduler")
    st.markdown("AI-powered service desk ticket triage & automation system")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Create Ticket", "View Tickets", "Triage Demo", "Analytics"]
    )
    
    if page == "Create Ticket":
        show_create_ticket()
    elif page == "View Tickets":
        show_view_tickets()
    elif page == "Triage Demo":
        show_triage_demo()
    elif page == "Analytics":
        show_analytics()


def show_create_ticket():
    """Show create ticket page."""
    st.header("Create New Ticket")
    
    with st.form("create_ticket_form"):
        title = st.text_input("Title", placeholder="Brief description of the issue")
        description = st.text_area(
            "Description", 
            placeholder="Detailed description of the issue",
            height=150
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            auto_triage = st.checkbox("Auto-triage (AI prediction)", value=True)
            if not auto_triage:
                category = st.selectbox(
                    "Category",
                    ["network", "hardware", "software", "account", "security"]
                )
            else:
                category = None
        
        with col2:
            if not auto_triage:
                priority = st.selectbox("Priority", ["low", "medium", "high"])
            else:
                priority = None
        
        submitted = st.form_submit_button("Create Ticket")
        
        if submitted:
            if not title or not description:
                st.error("Please provide both title and description")
            else:
                # Auto-triage if enabled
                if auto_triage:
                    with st.spinner("AI is analyzing the ticket..."):
                        triage_result = triager.triage_ticket(title, description)
                        category = triage_result['category']
                        priority = triage_result['priority']
                    
                    st.info(f"🤖 AI Prediction: Category = **{category}**, Priority = **{priority}**")
                
                # Create ticket
                ticket = db_manager.create_ticket(
                    title=title,
                    description=description,
                    category=category,
                    priority=priority,
                    status='open'
                )
                
                st.success(f"✅ Ticket #{ticket.id} created successfully!")
                
                # Show ticket details
                with st.expander("View Ticket Details"):
                    st.write(f"**ID:** {ticket.id}")
                    st.write(f"**Title:** {ticket.title}")
                    st.write(f"**Description:** {ticket.description}")
                    st.write(f"**Category:** {ticket.category}")
                    st.write(f"**Priority:** {ticket.priority}")
                    st.write(f"**Status:** {ticket.status}")
                    st.write(f"**Created:** {ticket.created_at}")


def show_view_tickets():
    """Show view tickets page."""
    st.header("View Tickets")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_status = st.multiselect(
            "Filter by Status",
            ["open", "in_progress", "resolved"],
            default=["open", "in_progress"]
        )
    
    with col2:
        filter_priority = st.multiselect(
            "Filter by Priority",
            ["low", "medium", "high"],
            default=["low", "medium", "high"]
        )
    
    with col3:
        filter_category = st.multiselect(
            "Filter by Category",
            ["network", "hardware", "software", "account", "security"],
            default=["network", "hardware", "software", "account", "security"]
        )
    
    # Get tickets
    tickets = db_manager.get_all_tickets(limit=200)
    
    if tickets:
        # Convert to DataFrame
        data = []
        for ticket in tickets:
            data.append({
                'ID': ticket.id,
                'Title': ticket.title,
                'Category': ticket.category,
                'Priority': ticket.priority,
                'Status': ticket.status,
                'Created': ticket.created_at
            })
        
        df = pd.DataFrame(data)
        
        # Apply filters
        if filter_status:
            df = df[df['Status'].isin(filter_status)]
        if filter_priority:
            df = df[df['Priority'].isin(filter_priority)]
        if filter_category:
            df = df[df['Category'].isin(filter_category)]
        
        # Display tickets
        st.write(f"Found **{len(df)}** tickets")
        st.dataframe(df, use_container_width=True)
        
        # Ticket details
        if len(df) > 0:
            st.subheader("Ticket Details")
            selected_id = st.selectbox("Select Ticket ID", df['ID'].tolist())
            
            if selected_id:
                ticket = db_manager.get_ticket(selected_id)
                if ticket:
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**Title:** {ticket.title}")
                        st.write(f"**Description:** {ticket.description}")
                    
                    with col2:
                        st.write(f"**Category:** {ticket.category}")
                        st.write(f"**Priority:** {ticket.priority}")
                        st.write(f"**Status:** {ticket.status}")
                        st.write(f"**Created:** {ticket.created_at}")
    else:
        st.info("No tickets found. Create your first ticket!")


def show_triage_demo():
    """Show triage demo page."""
    st.header("🤖 AI Triage Demo")
    st.markdown("Test the AI-powered ticket classification system")
    
    st.write("Enter a ticket title and description to see how the AI categorizes and prioritizes it.")
    
    title = st.text_input("Ticket Title", placeholder="e.g., Cannot connect to VPN")
    description = st.text_area(
        "Ticket Description",
        placeholder="e.g., I am unable to connect to the company VPN from my laptop...",
        height=120
    )
    
    if st.button("Analyze Ticket", type="primary"):
        if title and description:
            with st.spinner("AI is analyzing..."):
                result = triager.triage_ticket(title, description)
            
            st.success("✅ Analysis Complete!")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Predicted Category", result['category'].upper())
            
            with col2:
                priority_emoji = {
                    'low': '🟢',
                    'medium': '🟡',
                    'high': '🔴'
                }
                st.metric(
                    "Predicted Priority", 
                    f"{priority_emoji.get(result['priority'], '')} {result['priority'].upper()}"
                )
            
            # Sample tickets
            st.subheader("Try These Examples")
            
            examples = [
                ("Network down", "The entire office network is down and nobody can work", "network", "high"),
                ("Forgot password", "I forgot my password and need to reset it", "account", "medium"),
                ("Printer not working", "The printer on the 3rd floor is not responding", "hardware", "low"),
            ]
            
            for ex_title, ex_desc, ex_cat, ex_pri in examples:
                with st.expander(f"Example: {ex_title}"):
                    st.write(f"**Description:** {ex_desc}")
                    st.write(f"**Expected Category:** {ex_cat}")
                    st.write(f"**Expected Priority:** {ex_pri}")
        else:
            st.warning("Please provide both title and description")


def show_analytics():
    """Show analytics page."""
    st.header("📊 Analytics Dashboard")
    
    tickets = db_manager.get_all_tickets(limit=500)
    
    if tickets:
        # Convert to DataFrame
        data = []
        for ticket in tickets:
            data.append({
                'Category': ticket.category,
                'Priority': ticket.priority,
                'Status': ticket.status
            })
        
        df = pd.DataFrame(data)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Total Tickets")
            st.metric("Count", len(df))
        
        with col2:
            st.subheader("Open Tickets")
            open_count = len(df[df['Status'] == 'open'])
            st.metric("Count", open_count)
        
        with col3:
            st.subheader("High Priority")
            high_priority = len(df[df['Priority'] == 'high'])
            st.metric("Count", high_priority)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Tickets by Category")
            category_counts = df['Category'].value_counts()
            st.bar_chart(category_counts)
        
        with col2:
            st.subheader("Tickets by Priority")
            priority_counts = df['Priority'].value_counts()
            st.bar_chart(priority_counts)
        
        # Status distribution
        st.subheader("Tickets by Status")
        status_counts = df['Status'].value_counts()
        st.bar_chart(status_counts)
    else:
        st.info("No tickets available for analytics. Create some tickets first!")


if __name__ == "__main__":
    main()
