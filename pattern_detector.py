try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.cluster import DBSCAN
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

def detect_incidents(tickets):
    """
    Smart Pattern Detection (Core Hackathon Differentiator)
    Uses clustering to detect patterns like:
    - Same issue reported by multiple users
    - Bug outbreak detection
    """
    if not tickets:
        return {}, []

    if not ML_AVAILABLE:
        # Fallback to simple text matching if scikit-learn is not available
        incidents = {}
        standalone = []
        seen = {}
        for t in tickets:
            q = t['user_query'].lower()
            if q in seen:
                incidents.setdefault(f"Incident_{seen[q]}", [seen[q]]).append(t['ticket_id'])
            else:
                seen[q] = t['ticket_id']
                standalone.append(t['ticket_id'])
        return incidents, standalone

    queries = [t['user_query'] for t in tickets]
    ids = [t['ticket_id'] for t in tickets]

    # Convert text to embeddings using TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(queries)

    # Cluster using DBSCAN
    db = DBSCAN(eps=0.5, min_samples=2).fit(X)
    
    incidents = {}
    standalone = []
    
    for i, label in enumerate(db.labels_):
        if label != -1: # -1 implies noise (no cluster)
            incident_name = f"Incident_Group_{label}"
            if incident_name not in incidents:
                incidents[incident_name] = []
            incidents[incident_name].append(ids[i])
        else:
            standalone.append(ids[i])
            
    return incidents, standalone
