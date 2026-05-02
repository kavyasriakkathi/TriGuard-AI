import json
import os
import random

RESPONSES_FILE = "responses.json"

def load_responses():
    if not os.path.exists(RESPONSES_FILE):
        return {}
    with open(RESPONSES_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def get_response(domain, issue_type, severity, is_incident=False):
    if is_incident:
        return f"[INCIDENT ALERT] We are currently experiencing a known system-wide issue regarding {domain} - {issue_type}. Our engineering team is actively investigating this SEV-1 incident."
        
    if severity == "SEV-1" or severity == "High":
        return "[ESCALATION REQUIRED] This is a critical issue. Forwarding to the human support team immediately."
        
    responses = load_responses()
    domain_resps = responses.get(domain, {})
    return domain_resps.get(issue_type, "We have received your ticket and are looking into it.")

# Tone templates for AI-generated responses
TONE_TEMPLATES = {
    "empathetic": "We completely understand how frustrating this must be.",
    "urgent": "Our team is treating this as a top priority.",
    "reassuring": "Rest assured, we are actively working to resolve this.",
    "professional": "Thank you for bringing this to our attention.",
}

# Fix suggestions by domain and issue type
FIX_SUGGESTIONS = {
    "Payments": {
        "Transaction Failed": ["Please verify your card details.", "Try using an alternative payment method."],
        "Refund Delay": ["Refunds typically take 5-7 business days."],
    },
    "Security": {
        "Account Compromise": ["Change your password immediately.", "Enable 2FA."],
    },
    "HackerRank": {
        "Login Issue": ["Try resetting your password.", "Clear cookies."],
    },
    "AI Tools": {
        "API Downtime": ["Check our status page.", "Switch to backup API."],
    },
    "Performance": {
        "General Slowdown": ["We are scaling resources.", "Expected improvement soon."],
    }
}

ESCALATION_RULES = {
    "SEV-1": {"action": "IMMEDIATE ESCALATION", "team": "Senior Engineering", "sla": "15 minutes"},
    "SEV-2": {"action": "HIGH PRIORITY QUEUE", "team": "Engineering Team Lead", "sla": "1 hour"},
    "SEV-3": {"action": "STANDARD QUEUE", "team": "Support Agent", "sla": "4 hours"},
    "SEV-4": {"action": "LOW PRIORITY QUEUE", "team": "Auto-Reply Bot", "sla": "24 hours"},
}

BUSINESS_IMPACT = {"Payments": 5000, "Security": 10000, "AI Tools": 2500, "HackerRank": 1500, "Performance": 2000, "General": 500}

def generate_ai_response(domain, issue_type, severity, ticket_text, is_incident=False):
    tone = TONE_TEMPLATES["urgent"] if severity == "SEV-1" else TONE_TEMPLATES["professional"]
    fixes = FIX_SUGGESTIONS.get(domain, {}).get(issue_type, ["Our team is looking into this."])
    escalation = ESCALATION_RULES.get(severity, ESCALATION_RULES["SEV-4"])
    
    response_parts = [f"📋 Ticket Classification: {domain} -> {issue_type} [{severity}]", tone, "\n🔧 Suggested Actions:"]
    for i, fix in enumerate(fixes, 1):
        response_parts.append(f"   {i}. {fix}")
    
    response_parts.append(f"\n📌 Routing: {escalation['action']}")
    
    base_cost = BUSINESS_IMPACT.get(domain, 500)
    estimated_risk = base_cost * 1.0 if severity == "SEV-1" else base_cost * 0.1
    
    return "\n".join(response_parts), estimated_risk