import streamlit as st
import json

def load_responses():
    with open("responses.json", "r") as file:
        return json.load(file)

def detect_domain(text):
    text = text.lower()
    if "hackerrank" in text:
        return "HackerRank"
    elif "api" in text or "ai" in text:
        return "AI Tool"
    elif "payment" in text or "transaction" in text or "refund" in text:
        return "Payments"
    else:
        return "Unknown"

def detect_issue(text):
    text = text.lower()
    if "login" in text:
        return "Login Issue"
    elif "submit" in text or "submission" in text:
        return "Submission Issue"
    elif "test case" in text:
        return "Test Case Issue"
    elif "api" in text:
        return "API Error"
    elif "transaction" in text or "failed" in text:
        return "Transaction Failed"
    elif "refund" in text:
        return "Refund Issue"
    else:
        return "General Issue"

# UI Configuration
st.set_page_config(page_title="TriGuard Ai Support", page_icon="🛡️")

st.title("🛡️ TriGuard Ai Support")
st.write("Welcome to the TriGuard Ai interactive support assistant! Type your issue below.")

# Load data
try:
    responses = load_responses()
except Exception as e:
    st.error(f"Error loading responses: {e}")
    st.stop()

# User Input
ticket = st.text_input("Enter your issue:", placeholder="E.g., I have a HackerRank login issue")

if ticket:
    with st.spinner("Analyzing..."):
        domain = detect_domain(ticket)
        issue = detect_issue(ticket)
        
        response = responses.get(domain, {}).get(issue, "No response available. Please try rephrasing or contact support.")
        
        st.markdown("### --- RESULT ---")
        col1, col2 = st.columns(2)
        col1.metric("Detected Domain", domain)
        col2.metric("Issue Type", issue)
        
        st.success(f"**Suggested Response:**\n\n{response}")