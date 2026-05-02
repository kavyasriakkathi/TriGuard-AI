
import os
from datetime import datetime

LOG_FILE = "log.txt"

def log_ticket(ticket_id, ticket_text, classification, response):
    """
    Logs the ticket details into a professional audit file.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    score = classification['priority_score']
    status = "[ACTION REQUIRED] Escalated to Human" if score > 80 else "[SUCCESS] Automated Reply Sent"
    log_type = "ALERT" if score > 80 else "AUDIT"
    
    log_entry = (
        f"[{timestamp}] [{log_type}] Ticket #{ticket_id}\n"
        f"{'='*50}\n"
        f"PLATFORM : {classification['domain']}\n"
        f"ISSUE    : {classification['issue_type']}\n"
        f"SCORE    : {score}\n"
        f"STATUS   : {status}\n"
        f"QUERY    : {ticket_text}\n"
        f"RESPONSE : {response}\n"
        f"{'='*50}\n\n"
    )

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(log_entry)
        
    return True