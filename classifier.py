from learning_memory import check_memory
from logger import analyze_system_health

def process_ticket(ticket_text, volume_multiplier=1):
    """
    Dynamic Severity Engine and Classification logic.
    """
    # 1. AI Learning Behavior Layer (Feedback Loop)
    memory_recall = check_memory(ticket_text)
    if memory_recall:
        memory_recall['priority_score'] = 100 if memory_recall['severity'] == 'SEV-1' else 50
        return memory_recall

    text_lower = ticket_text.lower()
    
    # Base Classification
    domain = "General"
    issue_type = "Unknown Issue"
    
    if any(kw in text_lower for kw in ["payment", "deducted", "money", "charged"]):
        domain = "Payments"
        if any(kw in text_lower for kw in ["failed", "error", "decline"]):
            issue_type = "Transaction Failed"
        else:
            issue_type = "Billing Query"
    elif any(kw in text_lower for kw in ["login", "account", "password", "sign in"]):
        domain = "HackerRank"
        issue_type = "Login Issue"
    elif any(kw in text_lower for kw in ["api", "downtime", "server", "timeout"]):
        domain = "AI Tools"
        issue_type = "API Downtime"
        
    # 2. Dynamic Severity Engine (replaces fixed rules)
    base_score = 0
    
    # Financial Impact (Heuristic)
    if domain == "Payments":
        base_score += 40
        if any(kw in text_lower for kw in ["fraud", "unauthorized", "stolen"]):
            base_score += 40
            
    # Keyword Urgency
    if any(kw in text_lower for kw in ["down", "failed", "critical", "urgent", "not working", "crash"]):
        base_score += 20
        
    # Smart Log Analytics (System Health)
    anomalies = analyze_system_health()
    if domain == "Payments" and "Payment gateway timeout spikes detected" in anomalies:
        base_score += 30
        
    # Incident Volume (Dynamic Scaling)
    base_score += (volume_multiplier - 1) * 15
    
    priority_score = min(base_score, 100)
    
    # AI Score to Severity Mapping
    if priority_score >= 80:
        severity = "SEV-1"
    elif priority_score >= 50:
        severity = "SEV-2"
    elif priority_score >= 20:
        severity = "SEV-3"
    else:
        severity = "SEV-4"
        
    return {
        "domain": domain,
        "issue_type": issue_type,
        "severity": severity,
        "priority_score": priority_score
    }
