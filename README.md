# 🛡️ TriGuard AI
### **The Future of Autonomous Incident Management**

TriGuard AI is an elite, machine-learning-driven platform designed to transform chaotic support tickets into intelligent, grouped incidents with real-time business risk analysis.

---

## 🚀 **Quick Start (Judges Guide)**

To see the platform in action, follow these simple steps:

### **1. Install Dependencies**
Open your terminal in this folder and run:
```bash
pip install -r requirements.txt
```

### **2. Process Data (The AI Engine)**
Run the processing engine to analyze the sample tickets:
```bash
python main.py
```

### **3. Launch the Command Center**
Start the real-time web dashboard:
```bash
streamlit run app.py
```
*The dashboard will automatically open in your browser at http://localhost:8501*

---

## 💎 **Key Features**

- **🤖 ML-Driven Classification**: Uses TF-IDF and Support Vector Machines (SVM) to categorize tickets with high precision.
- **🚨 Incident Auto-Grouping**: Automatically detects outbreaks and groups related tickets into high-level incidents.
- **🧠 Active Learning Loop**: Allows agents to correct the AI, triggering automated model retraining to improve accuracy over time.
- **🌡️ Risk-Based Priority**: Dynamically calculates priority scores and financial impact ($) based on ticket volume and severity.
- **🔬 Auto-RCA**: Generates Root Cause Analysis reports for grouped incidents to speed up resolution.

---

## 🛠️ **Tech Stack**

- **Backend**: Python 3.10+
- **Machine Learning**: Scikit-Learn (TF-IDF, SVM)
- **Analytics**: Pandas, NumPy
- **Visuals**: Plotly, Rich
- **Frontend**: Streamlit (Premium Dark Theme)

---

**Built for the Hackathon Demo — 2026**