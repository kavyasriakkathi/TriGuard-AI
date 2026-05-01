import json
import os

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
        return f"[INCIDENT ALERT] We are currently experiencing a known system-wide issue regarding {domain} - {issue_type}. Our engineering team is actively investigating this SEV-1 incident. We apologize for the inconvenience."
        
    if severity == "SEV-1":
        return "[ESCALATION REQUIRED] This is a critical issue. Forwarding to the human support team immediately."
        
    responses = load_responses()
    domain_resps = responses.get(domain, {})
    return domain_resps.get(issue_type, "We have received your ticket and are looking into it.")
