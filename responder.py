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
        return f"[INCIDENT ALERT] We are currently experiencing a known system-wide issue regarding {domain} - {issue_type}. Our engineering team is actively investigating this SEV-1 incident. We apologize for the inconvenience."
        
    if severity == "SEV-1":
        return "[ESCALATION REQUIRED] This is a critical issue. Forwarding to the human support team immediately."
        
    responses = load_responses()
    domain_resps = responses.get(domain, {})
    return domain_resps.get(issue_type, "We have received your ticket and are looking into it.")


# ============================
# AI Response Generator Module
# ============================

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
        "Transaction Failed": [
            "Please verify your card details and ensure sufficient balance.",
            "Try using an alternative payment method (UPI, Net Banking, or another card).",
            "Clear your browser cache and retry the payment.",
            "If money was deducted, it will be auto-refunded within 3-5 business days."
        ],
        "Refund Delay": [
            "Refunds typically take 5-7 business days to process.",
            "Please share your transaction ID so we can trace the refund status.",
            "We have escalated this to our finance team for expedited processing."
        ],
        "Duplicate Charge": [
            "We have flagged the duplicate transaction for immediate reversal.",
            "Please do not dispute the charge with your bank yet — our system will auto-correct it.",
            "Expected resolution time: 24-48 hours."
        ],
        "Billing Query": [
            "You can view your billing history at: Dashboard > Billing > Invoices.",
            "For subscription changes, visit: Account Settings > Plan Management."
        ]
    },
    "Security": {
        "Account Compromise": [
            "Immediately change your password and enable Two-Factor Authentication (2FA).",
            "Review your recent login history for any unauthorized access.",
            "Revoke all active sessions from: Settings > Security > Active Sessions.",
            "Our security team has been notified and is investigating."
        ],
        "Suspicious Activity": [
            "We recommend changing your password as a precaution.",
            "Check if any unauthorized changes were made to your profile.",
            "Enable login notifications to monitor future access attempts."
        ],
        "Phishing Report": [
            "Do NOT click on any links in the suspicious message.",
            "Forward the email/message to our security team for analysis.",
            "We will block the reported source if confirmed malicious."
        ],
        "Security Concern": [
            "Enable 2FA for an additional layer of security.",
            "Review your account permissions and connected apps.",
            "Our cybersecurity team will investigate and respond within 24 hours."
        ]
    },
    "HackerRank": {
        "Login Issue": [
            "Try resetting your password using the 'Forgot Password' link.",
            "Clear your browser cookies and cache, then retry.",
            "Ensure you are using the correct email address associated with your account."
        ],
        "Account Locked": [
            "Your account was locked due to multiple failed login attempts.",
            "Wait 30 minutes for the auto-unlock, or contact support for immediate access.",
            "Verify your identity through the registered email to unlock."
        ],
        "Password Reset Issue": [
            "Check your spam/junk folder for the reset email.",
            "Request a new reset link — previous links expire after 15 minutes.",
            "Try using an incognito/private browser window."
        ]
    },
    "AI Tools": {
        "API Downtime": [
            "Check our status page for real-time service updates.",
            "Implement retry logic with exponential backoff in your integration.",
            "Switch to the backup API endpoint if available."
        ],
        "Application Crash": [
            "Clear your application cache and restart.",
            "Ensure you are running the latest version of the application.",
            "Submit the crash log for our engineering team to analyze."
        ],
        "Server Error": [
            "Our infrastructure team is actively working on the issue.",
            "Estimated restoration time: 30-60 minutes.",
            "Monitor our status page for live updates."
        ]
    },
    "Performance": {
        "Database Slowdown": [
            "Our DBA team is optimizing query performance.",
            "Consider using pagination for large data requests.",
            "We are scaling database resources to handle the load."
        ],
        "Page Load Delay": [
            "Clear your browser cache and disable unnecessary extensions.",
            "Try accessing from a different browser or device.",
            "We are optimizing CDN delivery for faster page loads."
        ],
        "General Slowdown": [
            "We are monitoring system performance metrics.",
            "Additional compute resources are being provisioned.",
            "Expected improvement within the next 1-2 hours."
        ]
    },
    "General": {
        "Unknown Issue": [
            "A support representative will review your request shortly.",
            "Please provide additional details to help us resolve this faster."
        ]
    }
}

# Escalation rules
ESCALATION_RULES = {
    "SEV-1": {"action": "IMMEDIATE ESCALATION", "team": "Senior Engineering + On-Call Manager", "sla": "15 minutes"},
    "SEV-2": {"action": "HIGH PRIORITY QUEUE", "team": "Engineering Team Lead", "sla": "1 hour"},
    "SEV-3": {"action": "STANDARD QUEUE", "team": "Support Agent", "sla": "4 hours"},
    "SEV-4": {"action": "LOW PRIORITY QUEUE", "team": "Auto-Reply Bot", "sla": "24 hours"},
}


def generate_ai_response(domain, issue_type, severity, ticket_text, is_incident=False):
    """
    AI Response Generator — Generates intelligent, context-aware responses
    with fix suggestions and escalation recommendations.
    """
    # Select appropriate tone based on severity
    if severity == "SEV-1":
        tone = TONE_TEMPLATES["urgent"]
    elif severity == "SEV-2":
        tone = TONE_TEMPLATES["empathetic"]
    elif domain == "Security":
        tone = TONE_TEMPLATES["urgent"]
    else:
        tone = TONE_TEMPLATES["professional"]
    
    # Get fix suggestions
    domain_fixes = FIX_SUGGESTIONS.get(domain, {})
    fixes = domain_fixes.get(issue_type, ["Our team is looking into this."])
    
    # Get escalation info
    escalation = ESCALATION_RULES.get(severity, ESCALATION_RULES["SEV-4"])
    
    # Build AI response
    response_parts = []
    
    # Opening
    if is_incident:
        response_parts.append(f"🚨 INCIDENT DETECTED — {domain}: {issue_type}")
        response_parts.append(f"Multiple users are affected by this issue. {tone}")
    else:
        response_parts.append(f"📋 Ticket Classification: {domain} → {issue_type} [{severity}]")
        response_parts.append(tone)
    
    # Suggested fixes
    response_parts.append("\n🔧 Suggested Actions:")
    for i, fix in enumerate(fixes, 1):
        response_parts.append(f"   {i}. {fix}")
    
    # Escalation
    response_parts.append(f"\n📌 Routing: {escalation['action']}")
    response_parts.append(f"   Assigned Team: {escalation['team']}")
    response_parts.append(f"   SLA Target: {escalation['sla']}")
    
    return "\n".join(response_parts)
