import json
import os

MEMORY_FILE = "ticket_memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
        except (json.JSONDecodeError, TypeError):
            return {}

def save_memory(memory):
    if not isinstance(memory, dict):
        return
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(memory, f, indent=4)

def update_memory(ticket_text, human_domain, human_issue, human_severity):
    """
    Simulates Reinforcement-style scoring feedback loop
    """
    if not ticket_text:
        return
        
    memory = load_memory()
    # Ensure key is a clean lowercase string
    key = str(ticket_text).strip().lower()
    
    memory[key] = {
        "domain": human_domain,
        "issue_type": human_issue,
        "severity": human_severity,
        "confidence_score": 1.0 # 100% since it's human corrected
    }
    save_memory(memory)

def check_memory(ticket_text):
    """
    Returns the mapped classification if a human has corrected it before.
    """
    if not ticket_text:
        return None
        
    memory = load_memory()
    key = str(ticket_text).strip().lower()
    return memory.get(key, None)
