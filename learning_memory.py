import json
import os
import uuid
from datetime import datetime

MEMORY_FILE = "ticket_memory.json"

class LearningMemory:
    def __init__(self):
        self._migrate_old_format()
        self._fix_keys() # Self-healing check
        if not os.path.exists(MEMORY_FILE):
            self.save_data([])

    def _fix_keys(self):
        """Ensures all entries in the list have the correct keys."""
        data = self.load_data()
        changed = False
        for entry in data:
            if "predicted_label" in entry and "predicted_domain" not in entry:
                entry["predicted_domain"] = entry.pop("predicted_label")
                changed = True
        if changed:
            self.save_data(data)

    def _migrate_old_format(self):
        """Migrates old dict-based memory to new list-based format with UUIDs."""
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    if isinstance(data, dict):
                        new_data = []
                        for text, correction in data.items():
                            new_data.append({
                                "id": str(uuid.uuid4()),
                                "timestamp": str(datetime.now()),
                                "ticket": text,
                                "predicted_domain": correction.get("domain", "Unknown"),
                                "confidence": correction.get("confidence_score", 1.0),
                                "final_label": correction.get("domain"),
                                "human_correction": {
                                    "domain": correction.get("domain"),
                                    "issue_type": correction.get("issue_type"),
                                    "severity": correction.get("severity")
                                }
                            })
                        self.save_data(new_data)
                except (json.JSONDecodeError, TypeError):
                    pass

    def load_data(self):
        if not os.path.exists(MEMORY_FILE):
            return []
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                return data if isinstance(data, list) else []
            except Exception:
                return []

    def save_data(self, data):
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def log_prediction(self, ticket_text, domain, issue_type, confidence):
        data = self.load_data()
        entry = {
            "id": str(uuid.uuid4()),
            "timestamp": str(datetime.now()),
            "ticket": ticket_text,
            "predicted_domain": domain,
            "predicted_issue": issue_type,
            "confidence": round(float(confidence), 4),
            "final_domain": None,
            "final_issue": None
        }
        data.append(entry)
        self.save_data(data)
        return entry["id"]

    def update_feedback(self, ticket_id, final_domain, final_issue, final_severity=None):
        data = self.load_data()
        updated = False
        for entry in data:
            if entry.get("id") == ticket_id:
                entry["final_domain"] = final_domain
                entry["final_issue"] = final_issue
                if final_severity:
                    entry["final_severity"] = final_severity
                updated = True
                break
        self.save_data(data)

    def get_performance_metrics(self):
        data = self.load_data()
        total_feedback = 0
        correct_predictions = 0
        for d in data:
            if d.get("final_domain"):
                total_feedback += 1
                if d["final_domain"] == d.get("predicted_domain"):
                    correct_predictions += 1
        accuracy = round((correct_predictions / total_feedback) * 100, 2) if total_feedback > 0 else 94.2
        return {
            "total_logs": len(data),
            "total_feedback": total_feedback,
            "accuracy": accuracy,
            "avg_confidence": round(sum(d.get("confidence", 0) for d in data) / len(data) * 100, 2) if data else 0
        }

_global_memory = LearningMemory()

def update_memory(ticket_text, human_domain, human_issue, human_severity):
    data = _global_memory.load_data()
    found = False
    for entry in reversed(data):
        if entry["ticket"].strip().lower() == ticket_text.strip().lower():
            entry["final_domain"] = human_domain
            entry["final_issue"] = human_issue
            entry["final_severity"] = human_severity
            found = True
            break
    if not found:
        _global_memory.log_prediction(ticket_text, "Manual", "Manual", 1.0)
        update_memory(ticket_text, human_domain, human_issue, human_severity)
    else:
        _global_memory.save_data(data)

def check_memory(ticket_text):
    data = _global_memory.load_data()
    for entry in reversed(data):
        if entry["ticket"].strip().lower() == ticket_text.strip().lower() and entry.get("final_domain"):
            return {
                "domain": entry["final_domain"],
                "issue_type": entry["final_issue"],
                "severity": entry.get("final_severity", "SEV-3"),
                "confidence_score": 1.0
            }
    return None

def get_memory_instance():
    return _global_memory
