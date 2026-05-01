import json
import os
from collections import Counter

RCA_FILE = "rca_reports.json"

# Knowledge base for Root Cause Analysis
# Maps keywords from tickets to probable technical root causes
RCA_KNOWLEDGE_BASE = {
    "Payments": {
        "keywords": ["timeout", "gateway", "declined", "failed", "deducted"],
        "probable_cause": "Upstream Payment Gateway (Stripe/PayPal) API latency or timeout.",
        "mitigation": "1. Verify gateway status page.\n2. Enable fallback payment processor.\n3. Run reconciliation script for deducted amounts."
    },
    "Security": {
        "keywords": ["hacked", "compromised", "unauthorized", "login", "password", "suspicious", "phishing"],
        "probable_cause": "Potential Credential Stuffing Attack or Session Hijacking.",
        "mitigation": "1. Force global password reset for affected user segment.\n2. Invalidate active JWT sessions.\n3. Increase WAF rate limiting on /login endpoint."
    },
    "HackerRank": {
        "keywords": ["locked", "reset", "login", "access"],
        "probable_cause": "Auth service rate-limiter over-triggering or Redis cache failure.",
        "mitigation": "1. Check Redis memory usage.\n2. Temporarily increase rate-limit thresholds.\n3. Manually unlock affected user batches."
    },
    "AI Tools": {
        "keywords": ["500", "503", "timeout", "crash", "unresponsive", "api"],
        "probable_cause": "Inference server out of memory (OOM) or GPU node failure.",
        "mitigation": "1. Restart inference pods.\n2. Scale up auto-scaling group.\n3. Rollback recent model deployment if applicable."
    },
    "Performance": {
        "keywords": ["slow", "lagging", "forever", "loading", "database", "load"],
        "probable_cause": "Database index missing or unoptimized query causing table locks.",
        "mitigation": "1. Analyze slow query logs in RDS.\n2. Kill long-running sleeping queries.\n3. Add read-replicas to handle load."
    }
}

def generate_rca(incident_id, domain, tickets):
    """
    Analyzes a cluster of tickets and generates a Root Cause Analysis report.
    """
    # Combine all text
    combined_text = " ".join([t['user_query'] for t in tickets]).lower()
    
    # Default fallback
    probable_cause = "Unknown anomaly detected. Requires manual engineering investigation."
    mitigation = "1. Check Datadog/NewRelic logs.\n2. Escalate to On-Call Engineer."
    
    # Find matching domain knowledge
    domain_kb = RCA_KNOWLEDGE_BASE.get(domain)
    if domain_kb:
        # Count keyword hits
        hits = sum(1 for kw in domain_kb["keywords"] if kw in combined_text)
        if hits > 0:
            probable_cause = domain_kb["probable_cause"]
            mitigation = domain_kb["mitigation"]
            
    report = {
        "incident_id": incident_id,
        "domain": domain,
        "affected_tickets": len(tickets),
        "probable_cause": probable_cause,
        "mitigation": mitigation,
        "status": "Investigating"
    }
    
    # Save to JSON
    reports = load_rca_reports()
    reports[incident_id] = report
    
    with open(RCA_FILE, 'w', encoding='utf-8') as f:
        json.dump(reports, f, indent=4)
        
    return report

def load_rca_reports():
    if os.path.exists(RCA_FILE):
        with open(RCA_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}
