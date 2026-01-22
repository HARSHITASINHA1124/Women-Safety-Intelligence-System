import streamlit as st
import re
import joblib
from datetime import datetime
from collections import defaultdict

from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Women Safety Intelligence System", layout="wide")
st.title("🚨 Women Safety Incident Intelligence System")

# ---------------- UTILS ----------------
def normalize_location(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def severity_to_num(sev):
    return {"Low": 1, "Medium": 2, "High": 3}.get(sev, 1)

def parse_time_safe(payload):
    try:
        return datetime.strptime(payload.get("time"), "%Y-%m-%d %H:%M")
    except:
        return datetime.now()

# ---------------- LOAD MODELS ----------------
@st.cache_resource
def load_embedder():
    return SentenceTransformer("all-MiniLM-L6-v2")

@st.cache_resource
def load_risk_model():
    return joblib.load("risk_model.pkl")

embedder = load_embedder()
risk_model = load_risk_model()

# ---------------- QDRANT ----------------
client = QdrantClient(url="http://localhost:6333")
COLLECTION = "women_safety_incidents"

# ---------------- MEMORY (TIME–LOCATION INDEX) ----------------
def build_time_location_memory():
    points = client.query_points(
        collection_name=COLLECTION,
        limit=1000
    ).points

    memory = defaultdict(lambda: defaultdict(list))

    for p in points:
        loc = normalize_location(p.payload.get("location", ""))
        dt = parse_time_safe(p.payload)
        hr = dt.hour

        memory[loc][hr].append({
            "severity": p.payload.get("severity", "Low"),
            "text": p.payload.get("text")
        })

    return memory

time_location_memory = build_time_location_memory()

def refresh_memory():
    global time_location_memory
    time_location_memory = build_time_location_memory()

# ---------------- ML FEATURE BUILDER ----------------
def build_features(location, hour, semantic_score):
    loc = normalize_location(location)
    incidents = time_location_memory.get(loc, {}).get(hour, [])

    count = len(incidents)
    avg_sev = (
        sum(severity_to_num(i["severity"]) for i in incidents) / count
        if count else 0
    )
    night_flag = 1 if hour >= 20 or hour <= 5 else 0

    return [count, avg_sev, night_flag, semantic_score]

def predict_risk_ml(features):
    pred = risk_model.predict([features])[0]
    return ["LOW", "MODERATE", "HIGH"][pred]

# ---------------- UI TABS ----------------
tab1, tab2, tab3 = st.tabs([
    "🔍 Search & Risk Check",
    "➕ Add Incident",
    "🚓 Police / SOS Dashboard"
])

# ================= SEARCH TAB =================
with tab1:
    query = st.text_input("Ask a safety question or search incidents")

    extracted_location = None
    extracted_hour = None

    match = re.search(
        r"(?:go to|going to|visit|travel to)\s(.+?)\s(?:at|around)\s(\d{1,2})",
        query,
        re.I
    )

    if match:
        extracted_location = match.group(1)
        extracted_hour = int(match.group(2))

    if st.button("Analyze") and query:
        query_vec = embedder.encode(normalize_text(query)).tolist()

        results = client.query_points(
            collection_name=COLLECTION,
            query=query_vec,
            limit=5
        ).points

        # semantic severity score
        severity_rank = {"Low": 1, "Medium": 2, "High": 3}
        semantic_score = 0

        for r in results:
            semantic_score = max(
                semantic_score,
                severity_rank.get(r.payload.get("severity", "Low"), 1)
            )

        if extracted_location and extracted_hour is not None:
            features = build_features(
                extracted_location,
                extracted_hour,
                semantic_score
            )

            risk = predict_risk_ml(features)

            st.subheader("🚦 Risk Assessment")
            if risk == "HIGH":
                st.error("🚨 HIGH RISK AREA")
            elif risk == "MODERATE":
                st.warning("⚠️ MODERATE RISK AREA")
            else:
                st.success("✅ LOW RISK AREA")

            # -------- Evidence --------
            st.subheader("📊 Evidence Used")
            st.write("Incidents at location & hour:", features[0])
            st.write("Average severity:", round(features[1], 2))
            st.write("Night time:", "Yes" if features[2] else "No")
            st.write("Semantic severity score:", features[3])

        st.subheader("🔎 Retrieved Past Incidents")
        for r in results:
            st.markdown(f"**{r.payload['text']}**")
            st.write("📍", r.payload.get("original_location", "Unknown"))
            st.write("⚠️", r.payload.get("severity"))
            st.divider()

# ================= ADD INCIDENT =================
with tab2:
    text = st.text_area("Incident Description")
    location = st.text_input("Location")
    severity = st.selectbox("Severity", ["Low", "Medium", "High"])

    if st.button("Add Incident"):
        if not text or not location:
            st.error("All fields are required.")
        else:
            vec = embedder.encode(normalize_text(text)).tolist()
            is_sos = severity == "High"

            client.upsert(
                collection_name=COLLECTION,
                points=[{
                    "id": abs(hash(text + location + str(datetime.now()))),
                    "vector": vec,
                    "payload": {
                        "text": text,
                        "location": normalize_location(location),
                        "original_location": location,
                        "severity": severity,
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "sos": is_sos
                    }
                }]
            )

            refresh_memory()
            st.success("Incident stored successfully.")

            if is_sos:
                st.error("🚨 SOS FLAGGED — Police Attention Required")

# ================= POLICE TAB =================
with tab3:
    st.subheader("🚓 SOS INCIDENTS")

    points = client.query_points(
        collection_name=COLLECTION,
        limit=1000
    ).points

    sos_cases = [
        p for p in points if p.payload.get("sos") is True
    ]

    if not sos_cases:
        st.info("No SOS incidents reported.")
    else:
        sos_cases.sort(
            key=lambda p: p.payload.get("time", ""),
            reverse=True
        )

        for p in sos_cases:
            st.error(p.payload["text"])
            st.write("📍", p.payload.get("original_location"))
            st.write("🕒", p.payload.get("time"))
            st.write("⚠️ Severity:", p.payload.get("severity"))
            st.divider()
