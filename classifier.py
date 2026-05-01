from learning_memory import check_memory
from logger import analyze_system_health
from ml_model import predict, train_model

def process_ticket(ticket_text, volume_multiplier=1):
    """
    Dynamic Severity Engine and Classification logic.
    Now powered by a real ML model (TF-IDF + SVM) instead of keyword matching.
    """
    # 1. AI Learning Behavior Layer (Feedback Loop)
    #    Check if a human has corrected this ticket type before
    memory_recall = check_memory(ticket_text)
    if memory_recall:
        memory_recall['priority_score'] = 100 if memory_recall['severity'] == 'SEV-1' else 50
        memory_recall['source'] = 'feedback_memory'
        return memory_recall

    # 2. Real ML Model Prediction (replaces keyword matching)
    #    Auto-retrains if new feedback data is available
    train_model()  # Auto-retrain check (skips if no new data)
    domain, issue_type = predict(ticket_text)
    
    text_lower = ticket_text.lower()
        
    # 3. Dynamic Severity Engine (real-time scoring)
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
        "priority_score": priority_score,
        "source": "ml_model"
    }
