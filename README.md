# 🛡️ TriGuard AI — Intelligent Incident Auto-Grouping & Routing Engine

An AI-driven, self-improving incident management platform built in Python. TriGuard AI transforms static ticket classification into an intelligent system that automatically detects patterns, groups related tickets into incidents, and dynamically calculates severity using real-time signals.

---

## 🚀 The 5 Core AI Features

### 1. 🧠 AI Learning Behavior Layer (Feedback Loop)
- Implements a **reinforcement-style memory system** that learns from human agent corrections.
- When an agent corrects a ticket's classification, the system remembers it (`ticket_memory.json`).
- On future similar tickets, the AI instantly recalls the corrected classification with **100% confidence**.
- **File:** `learning_memory.py`

### 2. 📊 Log Analytics Engine (Anomaly Detection)
- Parses historical ticket logs to detect **system-wide anomalies** and sudden ticket bursts.
- Monitors for spikes in specific domains (e.g., Payment gateway timeout spikes).
- Anomaly signals are fed back into the **Dynamic Severity Engine** to boost priority scores.
- **File:** `logger.py` → `analyze_system_health()`

### 3. 🔍 Smart Pattern Detection & Clustering (Bug Outbreak Detection)
- Uses **TF-IDF vectorization** + **DBSCAN clustering** to identify groups of similar tickets.
- Automatically detects when multiple users report the same issue (bug outbreaks).
- Falls back to simple text matching if `scikit-learn` is unavailable.
- **File:** `pattern_detector.py`

### 4. ⚡ Dynamic Severity Engine (Real-Time Priority Scoring)
- Replaces static severity rules with a **dynamic scoring system (0–100)**.
- Factors include:
  - **Financial Impact** — Payment-related tickets get higher base scores; fraud keywords escalate further.
  - **Keyword Urgency** — Words like "failed", "critical", "crash" boost scores.
  - **System Health Signals** — Log anomalies (from Feature #2) increase priority dynamically.
  - **Incident Volume Scaling** — More tickets in a cluster = higher severity (from Feature #3).
- Severity mapping: `SEV-1 (≥80)` → `SEV-2 (≥50)` → `SEV-3 (≥20)` → `SEV-4 (<20)`
- **File:** `classifier.py` → `process_ticket()`

### 5. 🚨 Automated Incident Grouping & Routing
- Clusters related tickets into **named incidents** (e.g., `Incident_Group_0`).
- Processes incident groups as a **single batch** instead of individual tickets.
- Automatically escalates high-priority incidents (`score ≥ 80`) to the incident response team.
- Standalone tickets are routed normally (auto-reply or human escalation).
- **File:** `main.py`

---

## 📁 Project Structure

```
TriGuard AI/
│
├── main.py                 # Entry point — orchestrates the full pipeline
├── classifier.py           # Dynamic Severity Engine + AI classification
├── pattern_detector.py     # TF-IDF + DBSCAN clustering for incident detection
├── responder.py            # Automated response generation
├── logger.py               # Audit logging + Log Analytics Engine
├── learning_memory.py      # AI Learning Behavior (Feedback Loop)
├── responses.json          # Domain-specific response templates
├── support_issue.csv       # Input: support tickets to process
├── requirements.txt        # Python dependencies
├── install_dependencies.bat # One-click Windows dependency installer
├── .gitignore              # Clean repo (excludes logs, cache, output)
└── README.md               # This file
```

---

## ⚙️ How to Run

### Prerequisites
- Python 3.10+ installed ([Download Python](https://www.python.org/downloads/))
- Git installed ([Download Git](https://git-scm.com/download/win))

### Installation
```bash
# Clone the repository
git clone https://github.com/kavyasriakkathi/TriGuard-AI.git
cd TriGuard-AI

# Install dependencies
pip install -r requirements.txt
```

### Run the Engine
```bash
python main.py
```

---

## 📊 Sample Output

```
TriGuard AI: Intelligent Incident Auto-Grouping & Routing Engine
─────────────────────────────────────────────────────────────────
Running Smart Pattern Detection & Clustering...

🚨 DETECTED INCIDENT: Incident_Group_0 (2 tickets affected) -> HackerRank - Login Issue [SEV-4]
Ticket #2: [Score: 60] [SEV-2] [Auto-Replied]
Ticket #3: [Score: 0]  [SEV-4] [Auto-Replied]

─────────────────────────────────────────────────────────────────
SYSTEM DASHBOARD SUMMARY
─────────────────────────────────────────────────────────────────
Total Tickets Processed : 6
Total Incidents Detected: 1
Human Escalations       : 0
Automated Replies       : 6
Data Saved To           : output.csv
Audit Logs Appended     : logs.json
─────────────────────────────────────────────────────────────────
Process Complete. System Standby.
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.14 |
| ML/Clustering | scikit-learn (TF-IDF, DBSCAN) |
| Terminal UI | Rich (progress bars, styled output) |
| Data | CSV (input), JSON (logs, memory, responses) |

---

## 📄 License

This project is open source and available for educational and demonstration purposes.