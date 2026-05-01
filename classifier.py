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
    
    if any(kw in text_lower for kw in ["payment", "deducted", "money", "charged", "refund", "billing", "invoice", "subscription"]):
        domain = "Payments"
        if any(kw in text_lower for kw in ["failed", "error", "decline", "declined"]):
            issue_type = "Transaction Failed"
        elif any(kw in text_lower for kw in ["refund", "not processed"]):
            issue_type = "Refund Delay"
        elif any(kw in text_lower for kw in ["twice", "double", "duplicate"]):
            issue_type = "Duplicate Charge"
        else:
            issue_type = "Billing Query"
    elif any(kw in text_lower for kw in ["hack", "unauthorized", "suspicious", "fraud", "stolen", "breach", "phishing", "compromised"]):
        domain = "Security"
        if any(kw in text_lower for kw in ["hack", "compromised", "breach"]):
            issue_type = "Account Compromise"
        elif any(kw in text_lower for kw in ["unauthorized", "suspicious", "fraud"]):
            issue_type = "Suspicious Activity"
        elif any(kw in text_lower for kw in ["phishing", "spam"]):
            issue_type = "Phishing Report"
        else:
            issue_type = "Security Concern"
    elif any(kw in text_lower for kw in ["slow", "performance", "latency", "lag", "takes long", "loading", "speed"]):
        domain = "Performance"
        if any(kw in text_lower for kw in ["database", "query", "db"]):
            issue_type = "Database Slowdown"
        elif any(kw in text_lower for kw in ["dashboard", "page", "website", "loading"]):
            issue_type = "Page Load Delay"
        else:
            issue_type = "General Slowdown"
    elif any(kw in text_lower for kw in ["login", "account", "password", "sign in", "locked", "reset"]):
        domain = "HackerRank"
        if any(kw in text_lower for kw in ["locked", "lock"]):
            issue_type = "Account Locked"
        elif any(kw in text_lower for kw in ["password", "reset"]):
            issue_type = "Password Reset Issue"
        else:
            issue_type = "Login Issue"
    elif any(kw in text_lower for kw in ["api", "downtime", "server", "timeout", "500", "503", "crash", "down"]):
        domain = "AI Tools"
        if any(kw in text_lower for kw in ["crash", "crashes"]):
            issue_type = "Application Crash"
        elif any(kw in text_lower for kw in ["500", "503", "server"]):
            issue_type = "Server Error"
        else:
            issue_type = "API Downtime"
        
    # 2. Dynamic Severity Engine (replaces fixed rules)
    base_score = 0
    
    # Financial Impact (Heuristic)
    if domain == "Payments":
        base_score += 40
        if any(kw in text_lower for kw in ["fraud", "unauthorized", "stolen"]):
            base_score += 40
            
    # Security Impact (High urgency)
    if domain == "Security":
        base_score += 50
        if any(kw in text_lower for kw in ["hack", "compromised", "breach", "unauthorized"]):
            base_score += 30
            
    # Keyword Urgency
    if any(kw in text_lower for kw in ["down", "failed", "critical", "urgent", "not working", "crash", "crashes"]):
        base_score += 20
        
    # Smart Log Analytics (System Health)
    anomalies = analyze_system_health()
    if domain == "Payments" and "Payment gateway timeout spikes detected" in anomalies:
        base_score += 30
    if domain == "Security" and "Multiple security incidents detected" in anomalies:
        base_score += 20
        
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
