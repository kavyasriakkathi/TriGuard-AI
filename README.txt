# 🛡️ TriGuard AI: Intelligent Incident Command Center

TriGuard AI is an advanced incident management platform that uses Machine Learning to automate ticket triage, detect system-wide outages, and calculate business risk in real-time.

## 🚀 Quick Start

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Dashboard:**
   ```bash
   streamlit run app.py
   ```

3. **Run CLI Engine (Processing):**
   ```bash
   python main.py
   ```

4. **Verify System Health:**
   ```bash
   python verify_scenarios.py
   ```

## 🧠 Technical Architecture
- **Classifier:** TF-IDF + Linear SVM (scikit-learn)
- **Clustering:** DBSCAN for bug outbreak detection
- **UI:** Streamlit with Custom CSS injection
- **Persistence:** JSON Learning Memory with Human Feedback Loop

## 💰 Business Features
- **Financial Risk Assessment:** Automatically estimates $ loss/hour for high-severity incidents.
- **Auto-RCA:** Generates technical Root Cause Analysis reports for ticket clusters.
- **Feedback Loop:** System auto-retrains based on agent corrections.

---
Built for the Hackathon Final Project.
