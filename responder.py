import json
import os

def load_responses(filepath="responses.json"):
    """
    Loads the structured responses from the JSON file.
    """
    try:
        with open(filepath, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def get_response(domain, issue_type, severity):
    """
    Retrieves the response based on domain and issue type.
    Escalates if severity is High.
    """
    if severity == "High":
        return f"[ESCALATION REQUIRED] This is a critical {issue_type} in {domain}. Forwarding to the human support team immediately."
        
    responses = load_responses()
    
    domain_responses = responses.get(domain, {})
    response = domain_responses.get(issue_type, "No specific response available. Please contact support for more details.")
    
    return response