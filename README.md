# Features

- **Priority Score (0-100)**: Calculated from severity and issue type, stored in `output.csv` and shown in logs.
- **Auto Escalation Rule**: Tickets with a priority score > 80 are automatically escalated to human support.
- **Professional Logs**: Structured audit logs with timestamp, domain, issue, score, status, and response, differentiating alerts for escalations.
- **System Dashboard Summary**: At the end of each run, a concise summary shows totals for processed tickets, escalations, automated replies, duplicates, and file locations.


A professional terminal-based support ecosystem built in Python. TriGuard AI automatically processes user support tickets, classifies the platform, assesses priority scores, and intelligently routes high-risk cases to human agents while automating standard responses.

Crucially, TriGuard AI features **Severity-Based Prioritization**. High-risk issues (like payment failures or potential fraud) are instantly escalated, while low and medium risk issues receive automated, helpful responses, drastically improving support efficiency.

## Features

- **Multi-Domain Support**: Seamlessly handles tickets for HackerRank, AI Tools, and Payments.
- **Smart Classification**: Detects the issue type (e.g., Login Issue, Submission Issue, Transaction Failure) based on keyword heuristics.
- **Severity-Based Prioritization**:
  - `🚨 High`: Critical issues (payment failure, money deducted, fraud). Requires immediate human escalation.
  - `⚠️ Medium`: Errors, failures, API downtime.
  - `✅ Low`: General or minor queries.
- **Automated Logging**: All tickets, along with their classification and generated response, are securely logged into a structured JSON file (`logs.json`) with accurate timestamps.
- **Modular Architecture**: Clean, readable, and highly extensible code structure.

## Folder Structure

```
TriGuard Ai/
│
├── main.py             # Entry point and terminal interface orchestration
├── classifier.py       # Logic for domain, issue, and severity classification
├── responder.py        # Logic for fetching responses and handling escalations
├── logger.py           # Logic for writing detailed ticket decisions to logs.json
├── responses.json      # Structured dictionary of domain-specific responses
├── .gitignore          # Keeps your repository clean from logs and environments
└── README.md           # Project documentation
```

## How to Run

1. Ensure you have Python 3 installed on your system.
2. Clone this repository to your local machine.
3. Navigate into the project directory.
4. Run the main script:
   ```bash
   python main.py
   ```
5. Enter your support tickets when prompted.
6. Type `exit` or `quit` to stop the application.

## Example Inputs & Outputs

**Input 1:**
```
Enter the support ticket: My payment failed but money was deducted from my account!
```
**Output 1:**
```
==================================================
📊 TRIAGE RESULT
==================================================
Domain:      Payments
Issue Type:  Transaction Failed
Severity:    🚨 [HIGH RISK] 🚨
--------------------------------------------------
💬 SUGGESTED RESPONSE:
[ESCALATION REQUIRED] This is a critical Transaction Failed in Payments. Forwarding to the human support team immediately.
==================================================
```

**Input 2:**
```
Enter the support ticket: I can't login to my HackerRank account
```
**Output 2:**
```
==================================================
📊 TRIAGE RESULT
==================================================
Domain:      HackerRank
Issue Type:  Login Issue
Severity:    ✅ [LOW RISK]
--------------------------------------------------
💬 SUGGESTED RESPONSE:
Please check your HackerRank username/password or reset your password.
==================================================
```