from learning_memory import check_memory
from logger import analyze_system_health
import ml_model

def process_ticket(query, volume_multiplier=1):
    """
    Main Classification Engine — Combines Memory + ML + Dynamic Scoring
    """
    # 1. Check AI Learning Memory (Feedback Loop)
    memory_match = check_memory(query)
    if memory_match:
        memory_match['source'] = "learning_memory"
        memory_match['confidence_score'] = 1.0
        return memory_match

    # 2. ML Prediction (TF-IDF + SVM)
    #    Auto-retrains if new feedback data is available
    ml_model.train_model() 
    domain, issue_type, confidence = ml_model.predict(query)
    
    # 3. Dynamic Priority Scoring
    base_score = 10
    
    # Keyword Weighting
    keywords = {
        'failed': 25, 'error': 15, 'critical': 30, 'crash': 35, 
        'payment': 20, 'money': 20, 'hacked': 40, 'unauthorized': 35,
        'slow': 10, 'down': 20, 'emergency': 30
    }
    
    for word, weight in keywords.items():
        if word in query.lower():
            base_score += weight
            
    # Domain weighting
    domain_weights = {'Security': 20, 'Payments': 15, 'Performance': 10, 'HackerRank': 5}
    base_score += domain_weights.get(domain, 0)
    
    # Confidence Factor: High confidence in serious issues boosts score
    if confidence > 0.8:
        base_score += 5
    elif confidence < 0.5:
        base_score -= 5

    # Volume scaling (if 10 people report the same thing, it's more urgent)
    volume_bonus = min(volume_multiplier * 5, 30)
    
    final_score = min(base_score + volume_bonus, 100)
    
    # Severity Mapping
    if final_score >= 80:
        severity = "SEV-1"
    elif final_score >= 50:
        severity = "SEV-2"
    elif final_score >= 20:
        severity = "SEV-3"
    else:
        severity = "SEV-4"
        
    return {
        "domain": domain,
        "issue_type": issue_type,
        "severity": severity,
        "priority_score": final_score,
        "confidence_score": round(confidence, 2),
        "source": "ml_model"
    }
