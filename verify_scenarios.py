import os
import sys
from classifier import process_ticket
from learning_memory import update_memory
from ml_model import train_model

def run_tests():
    print("🚀 Starting TriGuard AI Scenario Tests...\n")
    
    # Ensure model is trained first
    print("[1/3] 🤖 Initializing and training ML model...")
    train_model(force=True)
    print("✅ Model trained successfully.\n")

    scenarios = [
        "payment failed 3 times",
        "login not working",
        "website crashed"
    ]

    print("[2/3] 🔍 Testing Real Scenarios (Prediction & Severity)...\n")
    
    for text in scenarios:
        print(f"👉 Scenario: '{text}'")
        result = process_ticket(text)
        print(f"   Domain: {result['domain']} | Issue: {result['issue_type']}")
        print(f"   Severity: {result['severity']} (Score: {result['priority_score']}) | Source: {result['source']}\n")

    print("[3/3] 🧠 Testing Feedback Loop & Accuracy Update...\n")
    
    test_text = "login not working"
    print(f"👉 Correcting '{test_text}' via Human Feedback Loop...")
    print("   Setting to -> Domain: Security | Issue: Account Compromise | Severity: SEV-1")
    
    # Provide human correction
    update_memory(test_text, "Security", "Account Compromise", "SEV-1")
    
    # Process again to see if it remembers
    print("\n👉 Re-running classification for the same ticket...")
    updated_result = process_ticket(test_text)
    
    print(f"   Updated Domain: {updated_result['domain']} | Issue: {updated_result['issue_type']}")
    print(f"   Updated Severity: {updated_result['severity']} (Score: {updated_result['priority_score']}) | Source: {updated_result['source']}")
    
    if updated_result['domain'] == "Security" and updated_result['severity'] == "SEV-1":
        print("\n🏆 SUCCESS: Feedback Loop correctly updated accuracy!")
    else:
        print("\n❌ FAILED: Feedback Loop did not work as expected.")

    print("\n✨ All tests complete. If everything looks good, you're ready for the next level!")

if __name__ == "__main__":
    run_tests()
