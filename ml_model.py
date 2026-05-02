"""
TriGuard AI — Real ML Classification Model
Uses TF-IDF + Support Vector Machine (SVM) for ticket classification.
Supports auto-retraining from human feedback (learning memory).
"""

import os
import json
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

MODEL_FILE = "triguard_model.pkl"
TRAINING_LOG = "training_log.json"

# ============================
# Seed Training Data
# ============================
# This is the initial knowledge the model starts with.
# It gets smarter over time as agents provide feedback corrections.

SEED_DATA = [
    # --- Payments ---
    ("My payment failed", "Payments", "Transaction Failed"),
    ("Payment declined three times", "Payments", "Transaction Failed"),
    ("Money was deducted but order not placed", "Payments", "Transaction Failed"),
    ("Transaction error on checkout", "Payments", "Transaction Failed"),
    ("Card payment keeps failing", "Payments", "Transaction Failed"),
    ("Payment gateway error", "Payments", "Transaction Failed"),
    ("When will I get my refund", "Payments", "Refund Delay"),
    ("Refund not processed after 10 days", "Payments", "Refund Delay"),
    ("Still waiting for my refund", "Payments", "Refund Delay"),
    ("Refund status pending for weeks", "Payments", "Refund Delay"),
    ("I was charged twice for the same subscription", "Payments", "Duplicate Charge"),
    ("Double charge on my credit card", "Payments", "Duplicate Charge"),
    ("Duplicate payment deducted", "Payments", "Duplicate Charge"),
    ("How do I update my billing info", "Payments", "Billing Query"),
    ("Where can I see my invoice", "Payments", "Billing Query"),
    ("Need a copy of my receipt", "Payments", "Billing Query"),
    
    # --- Security ---
    ("Someone accessed my account without permission", "Security", "Account Compromise"),
    ("I think my account has been hacked", "Security", "Account Compromise"),
    ("My account was compromised", "Security", "Account Compromise"),
    ("Unauthorized access to my profile", "Security", "Account Compromise"),
    ("Someone changed my password without my knowledge", "Security", "Account Compromise"),
    ("I see suspicious login attempts from another country", "Security", "Suspicious Activity"),
    ("Unusual activity on my account", "Security", "Suspicious Activity"),
    ("Unauthorized transaction on my card", "Security", "Suspicious Activity"),
    ("Strange login from unknown device", "Security", "Suspicious Activity"),
    ("I received a phishing email", "Security", "Phishing Report"),
    ("Got a suspicious link pretending to be your company", "Security", "Phishing Report"),
    ("Fake email asking for my password", "Security", "Phishing Report"),
    
    # --- HackerRank ---
    ("I can't login to my HackerRank account", "HackerRank", "Login Issue"),
    ("Unable to sign in to HackerRank", "HackerRank", "Login Issue"),
    ("Login page keeps showing error", "HackerRank", "Login Issue"),
    ("Can't access my account", "HackerRank", "Login Issue"),
    ("My account was locked after too many failed attempts", "HackerRank", "Account Locked"),
    ("Account locked out", "HackerRank", "Account Locked"),
    ("Too many failed login attempts", "HackerRank", "Account Locked"),
    ("Password reset email never arrived", "HackerRank", "Password Reset Issue"),
    ("Can't reset my password", "HackerRank", "Password Reset Issue"),
    ("Reset link expired before I could use it", "HackerRank", "Password Reset Issue"),
    
    # --- AI Tools ---
    ("The API is returning a 500 error", "AI Tools", "Server Error"),
    ("Server returned 503 service unavailable", "AI Tools", "Server Error"),
    ("Internal server error on API call", "AI Tools", "Server Error"),
    ("Getting 502 bad gateway", "AI Tools", "Server Error"),
    ("API timeout errors on every request", "AI Tools", "API Downtime"),
    ("API is completely unresponsive", "AI Tools", "API Downtime"),
    ("Service is down", "AI Tools", "API Downtime"),
    ("The application crashes when uploading files", "AI Tools", "Application Crash"),
    ("App crashes on startup", "AI Tools", "Application Crash"),
    ("Application keeps crashing", "AI Tools", "Application Crash"),
    
    # --- Performance ---
    ("The dashboard takes 30 seconds to load", "Performance", "Page Load Delay"),
    ("Website is extremely slow", "Performance", "Page Load Delay"),
    ("Pages take forever to load", "Performance", "Page Load Delay"),
    ("Database query performance is terrible", "Performance", "Database Slowdown"),
    ("Queries are running very slow", "Performance", "Database Slowdown"),
    ("DB response time is too high", "Performance", "Database Slowdown"),
    ("The server is extremely slow today", "Performance", "General Slowdown"),
    ("Everything is lagging", "Performance", "General Slowdown"),
    ("System performance has degraded", "Performance", "General Slowdown"),
    
    # --- General ---
    ("How do I submit my code", "General", "Unknown Issue"),
    ("Where is the documentation", "General", "Unknown Issue"),
    ("I have a question about your product", "General", "Unknown Issue"),
    ("Need help with something", "General", "Unknown Issue"),
]


def get_training_data():
    """
    Combines seed data with human feedback corrections from learning memory.
    """
    texts = [d[0] for d in SEED_DATA]
    domains = [d[1] for d in SEED_DATA]
    issues = [d[2] for d in SEED_DATA]
    
    # Load human corrections from feedback loop (new format)
    if os.path.exists("ticket_memory.json"):
        with open("ticket_memory.json", "r", encoding="utf-8") as f:
            try:
                memory = json.load(f)
                if isinstance(memory, list):
                    for entry in memory:
                        if entry.get("final_domain") and entry.get("ticket"):
                            texts.append(entry["ticket"])
                            domains.append(entry["final_domain"])
                            issues.append(entry.get("final_issue", "Unknown"))
                elif isinstance(memory, dict):
                    # Fallback for old format if migration wasn't triggered
                    for ticket_text, correction in memory.items():
                        texts.append(ticket_text)
                        domains.append(correction["domain"])
                        issues.append(correction["issue_type"])
            except json.JSONDecodeError:
                pass
    
    return texts, domains, issues


def train_model(force=False):
    """
    Trains the ML model using TF-IDF + SVM.
    Auto-retrains when new feedback data is available.
    """
    texts, domains, issues = get_training_data()
    
    # Check if retraining is needed
    if os.path.exists(MODEL_FILE) and not force:
        if os.path.exists(TRAINING_LOG):
            with open(TRAINING_LOG, "r") as f:
                log = json.load(f)
                if log.get("training_samples") == len(texts):
                    return log # No new data, skip retraining
    
    # --- Domain Classifier ---
    domain_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english', max_features=5000, ngram_range=(1, 2))),
        ('clf', LinearSVC(max_iter=10000, C=1.0, dual='auto'))
    ])
    domain_pipeline.fit(texts, domains)
    
    # --- Issue Type Classifier ---
    issue_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english', max_features=5000, ngram_range=(1, 2))),
        ('clf', LinearSVC(max_iter=10000, C=1.0, dual='auto'))
    ])
    issue_pipeline.fit(texts, issues)
    
    # Save model
    model = {
        'domain_pipeline': domain_pipeline,
        'issue_pipeline': issue_pipeline
    }
    with open(MODEL_FILE, 'wb') as f:
        pickle.dump(model, f)
    
    # Log training info
    training_log = {
        "training_samples": len(texts),
        "seed_samples": len(SEED_DATA),
        "feedback_samples": len(texts) - len(SEED_DATA),
        "domains": list(set(domains)),
        "issue_types": list(set(issues))
    }
    with open(TRAINING_LOG, 'w') as f:
        json.dump(training_log, f, indent=4)
    
    return training_log


def predict(ticket_text):
    """
    Predicts the domain and issue type with a confidence score.
    """
    if not os.path.exists(MODEL_FILE):
        train_model(force=True)
    
    with open(MODEL_FILE, 'rb') as f:
        model = pickle.load(f)
    
    # Predict Domain
    domain_scores = model['domain_pipeline'].decision_function([ticket_text])
    domain = model['domain_pipeline'].predict([ticket_text])[0]
    
    # Calculate confidence proxy (normalize decision function scores)
    def calculate_confidence(scores):
        if scores.ndim > 1:
            # Multi-class
            exp_scores = np.exp(scores - np.max(scores))
            probs = exp_scores / exp_scores.sum(axis=1)
            return np.max(probs)
        else:
            # Binary class
            prob = 1 / (1 + np.exp(-scores))
            return max(prob, 1-prob)

    try:
        confidence = calculate_confidence(domain_scores)
    except:
        confidence = 0.85 # Fallback
    
    issue_type = model['issue_pipeline'].predict([ticket_text])[0]
    
    return domain, issue_type, float(confidence)


def get_model_info():
    """
    Returns info about the current model for the dashboard.
    """
    if os.path.exists(TRAINING_LOG):
        with open(TRAINING_LOG, "r") as f:
            return json.load(f)
    return None
