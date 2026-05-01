import json
import os
from datetime import datetime

LOG_FILE = "logs.json"

def log_ticket(ticket_id, ticket_text, classification, response, is_incident=False):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "ticket_id": ticket_id,
        "ticket_text": ticket_text,
        "classification": classification,
        "response": response,
        "is_incident": is_incident
    }
    
    logs = get_all_logs()
    logs.append(log_entry)
    
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=4)

def get_all_logs():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def analyze_system_health():
    """
    Smart Log Analytics Engine
    Parses logs to detect system-wide anomalies or sudden ticket bursts.
    """
    logs = get_all_logs()
    recent_logs = logs[-100:] # Analyze recent 100 logs
    
    # Example heuristic: if we see multiple payment transaction failures
    payment_failures = sum(1 for log in recent_logs 
                           if log.get('classification', {}).get('domain') == 'Payments' 
                           and log.get('classification', {}).get('issue_type') == 'Transaction Failed')
    
    # Security incident detection
    security_incidents = sum(1 for log in recent_logs
                             if log.get('classification', {}).get('domain') == 'Security')
    
    anomalies = []
    # Spike detection
    if payment_failures >= 3:
        anomalies.append("Payment gateway timeout spikes detected")
    if security_incidents >= 3:
        anomalies.append("Multiple security incidents detected")
        
    return anomalies
