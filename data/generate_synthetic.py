"""Generate synthetic ticket data for training."""
import random
import csv
from datetime import datetime, timedelta


# Categories and their associated templates
TICKET_TEMPLATES = {
    'network': [
        ('Network connectivity issues', 'Unable to connect to the office network from my laptop.'),
        ('VPN not working', 'VPN connection keeps dropping every few minutes.'),
        ('Slow internet speed', 'Internet is extremely slow, pages take forever to load.'),
        ('WiFi connection problems', 'Cannot connect to WiFi in conference room B.'),
        ('Network printer offline', 'Network printer is showing offline status.'),
    ],
    'hardware': [
        ('Laptop screen flickering', 'My laptop screen keeps flickering and going black.'),
        ('Keyboard keys not working', 'Several keys on my keyboard have stopped responding.'),
        ('Mouse not responding', 'Wireless mouse is not connecting to my computer.'),
        ('Monitor display issues', 'Second monitor is not being detected by my computer.'),
        ('Printer paper jam', 'Office printer has a paper jam that I cannot clear.'),
    ],
    'software': [
        ('Application crashing', 'Microsoft Excel crashes every time I open large files.'),
        ('Software installation error', 'Cannot install the updated version of Adobe Reader.'),
        ('Email client not syncing', 'Outlook is not syncing my emails properly.'),
        ('Browser performance issues', 'Chrome browser is very slow and unresponsive.'),
        ('Software license expired', 'AutoCAD showing license expired message.'),
    ],
    'account': [
        ('Password reset request', 'I forgot my password and need to reset it.'),
        ('Account locked out', 'My account has been locked after multiple login attempts.'),
        ('Access permission needed', 'Need access to the shared drive for marketing team.'),
        ('New user account setup', 'New employee needs account setup for all systems.'),
        ('Email account issues', 'Cannot access my email account, shows invalid credentials.'),
    ],
    'security': [
        ('Suspicious email received', 'Received a phishing email claiming to be from IT.'),
        ('Malware detected', 'Antivirus detected malware on my computer.'),
        ('Security certificate error', 'Getting security certificate error on company website.'),
        ('Unauthorized access attempt', 'Multiple failed login attempts on my account from unknown location.'),
        ('Data breach concern', 'Concerned about potential data breach, unusual activity noticed.'),
    ],
}


# Priority keywords
URGENT_MODIFIERS = ['URGENT:', 'CRITICAL:', 'EMERGENCY:', 'System down:', 'Major issue:']
IMPORTANT_MODIFIERS = ['Important:', 'High priority:', 'Need help:']


def generate_synthetic_tickets(num_tickets: int = 1000, output_file: str = 'sample_data/synthetic_tickets.csv'):
    """Generate synthetic ticket data.
    
    Args:
        num_tickets: Number of tickets to generate
        output_file: Path to output CSV file
    """
    tickets = []
    
    for i in range(num_tickets):
        # Select random category
        category = random.choice(list(TICKET_TEMPLATES.keys()))
        
        # Select random template from category
        title_template, desc_template = random.choice(TICKET_TEMPLATES[category])
        
        # Add urgency modifiers randomly
        if random.random() < 0.15:  # 15% urgent
            title = f"{random.choice(URGENT_MODIFIERS)} {title_template}"
            priority = 'high'
        elif random.random() < 0.35:  # 35% important
            title = f"{random.choice(IMPORTANT_MODIFIERS)} {title_template}"
            priority = 'medium'
        else:
            title = title_template
            priority = 'low'
        
        # Add some variation to descriptions
        variations = [
            desc_template,
            f"{desc_template} This is affecting my work.",
            f"{desc_template} Please help urgently.",
            f"{desc_template} Has been happening since yesterday.",
            f"{desc_template} Multiple users are reporting this issue.",
        ]
        description = random.choice(variations)
        
        # Generate timestamp
        days_ago = random.randint(0, 90)
        created_at = datetime.now() - timedelta(days=days_ago)
        
        # Random status
        status = random.choice(['open', 'open', 'open', 'in_progress', 'resolved'])
        
        tickets.append({
            'id': i + 1,
            'title': title,
            'description': description,
            'category': category,
            'priority': priority,
            'status': status,
            'created_at': created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        if tickets:
            writer = csv.DictWriter(f, fieldnames=tickets[0].keys())
            writer.writeheader()
            writer.writerows(tickets)
    
    print(f"Generated {num_tickets} synthetic tickets and saved to {output_file}")
    
    # Print statistics
    categories = {}
    priorities = {}
    for ticket in tickets:
        categories[ticket['category']] = categories.get(ticket['category'], 0) + 1
        priorities[ticket['priority']] = priorities.get(ticket['priority'], 0) + 1
    
    print("\nCategory distribution:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count} ({count/num_tickets*100:.1f}%)")
    
    print("\nPriority distribution:")
    for pri, count in sorted(priorities.items()):
        print(f"  {pri}: {count} ({count/num_tickets*100:.1f}%)")


if __name__ == '__main__':
    import os
    
    # Create sample_data directory if it doesn't exist
    os.makedirs('sample_data', exist_ok=True)
    
    # Generate synthetic data
    generate_synthetic_tickets(num_tickets=1000)
