# 🛡️ TriGuard AI — Intelligent Incident Auto-Grouping & Routing Engine

An enterprise-grade, AI-driven incident management platform built in Python. TriGuard AI transforms static ticket classification into an intelligent system that automatically detects patterns, groups related tickets into incidents, generates Root Cause Analyses (RCA), and dynamically calculates severity using real-time signals and a true Machine Learning pipeline.

---

## 🚀 The 6 Core AI Features

### 1. 🧠 AI Learning Behavior Layer (Feedback Loop)
- Implements a **reinforcement-style memory system** that learns from human agent corrections.
- When an agent corrects a ticket's classification, the system remembers it (`ticket_memory.json`).
- On future similar tickets, the AI instantly recalls the corrected classification and triggers the auto-retraining pipeline.
- **File:** `learning_memory.py`

### 2. 🤖 Real Machine Learning Model & Auto-Retraining
- Replaced basic keyword matching with a true **TF-IDF + Support Vector Machine (SVM)** pipeline.
- The system comes pre-seeded with training data but **gets smarter over time**.
- Automatically retrains itself on the fly whenever human feedback is provided.
- **File:** `ml_model.py`

### 3. 🔍 Smart Pattern Detection (Bug Outbreak Clustering)
- Uses **TF-IDF vectorization** + **DBSCAN clustering** to identify groups of similar tickets.
- Automatically detects when multiple users report the same issue, turning 50 tickets into 1 major incident.
- **File:** `pattern_detector.py`

### 4. ⚡ Dynamic Severity Engine (Real-Time Priority Scoring)
- Replaces static severity rules with a **dynamic scoring system (0–100)**.
- Factors include:
  - **Financial Impact** — Payment-related tickets get higher base scores.
  - **Keyword Urgency** — Words like "failed", "critical", "crash" boost scores.
  - **System Health Signals** — Real-time anomaly spikes boost priority dynamically.
  - **Incident Volume Scaling** — More tickets in a cluster = higher severity.
- Severity mapping: `SEV-1 (≥80)` → `SEV-2 (≥50)` → `SEV-3 (≥20)` → `SEV-4 (<20)`
- **File:** `classifier.py`

### 5. 🚨 Automated Incident Grouping & Routing
- Clusters related tickets into **named incidents** (e.g., `Incident_Group_0`).
- Processes incident groups as a **single batch** instead of individual tickets.
- Automatically escalates high-priority incidents (`score ≥ 80`) to the incident response team.
- **File:** `main.py`

### 6. 🔬 Automated Root Cause Analysis (RCA) Engine
- When an incident is detected, the RCA engine analyzes the text across the entire cluster.
- Extracts technical keywords to determine the **Probable Cause** (e.g., *Database Index Missing* or *Credential Stuffing Attack*).
- Automatically suggests step-by-step **Mitigation Strategies** for the engineering team.
- **File:** `rca_engine.py`

---

## 📊 Premium Command Center Dashboard

TriGuard AI comes with a stunning **Streamlit Web Dashboard** (`app.py`) for real-time visualization:
- **Live Ticket Flow & Severity Heatmap**
- **System Health Timeline** (Detecting anomaly spikes)
- **Top Affected Modules Treemap**
- **🚨 Incident Center** (Viewing active clusters and auto-generated RCA reports)
- **🤖 AI Response Generator** (Drafts intelligent replies, suggests fixes, and maps SLA routing rules)

---

## 📁 Project Structure

```text
TriGuard AI/
│
├── main.py                 # Entry point — orchestrates the full ML pipeline
├── app.py                  # Streamlit Web Dashboard (Command Center)
├── ml_model.py             # TF-IDF + SVM Machine Learning pipeline
├── classifier.py           # Dynamic Severity Engine scoring
├── pattern_detector.py     # DBSCAN clustering for incident grouping
├── rca_engine.py           # Root Cause Analysis generation
├── responder.py            # AI Response Generator & Escalation Rules
├── logger.py               # Audit logging + System Health Analytics
├── learning_memory.py      # AI Learning Behavior (Feedback Loop)
├── responses.json          # Domain-specific response templates
├── rca_reports.json        # Stored RCA reports from incidents
├── support_issue.csv       # Input: support tickets to process
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## ⚙️ How to Run

### 1. Installation
Ensure you have Python 3.10+ installed.
```bash
# Clone the repository
git clone https://github.com/kavyasriakkathi/TriGuard-AI.git
cd TriGuard-AI

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Core AI Engine
This will parse the tickets, run the ML clustering, detect incidents, and generate RCA reports.
```bash
python main.py
```

### 3. Launch the Web Dashboard (Command Center)
Open a new terminal and run:
```bash
python -m streamlit run app.py
```
*The dashboard will automatically open in your web browser at `http://localhost:8501`*

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Core Logic** | Python 3 |
| **Machine Learning** | `scikit-learn` (TF-IDF, SVM, DBSCAN) |
| **Web Dashboard UI** | `streamlit`, `plotly` |
| **Terminal UI** | `rich` (progress bars, styled output, tables) |
| **Data Storage** | CSV (input data), JSON (logs, memory, RCA models) |

---

## 📄 License
This project is open source and available for educational and demonstration purposes.