import re
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from sentence_transformers import SentenceTransformer
from data.incidents import incidents
from collections import defaultdict
from datetime import datetime

# ------------------ NORMALIZATION ------------------
def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    corrections = {
        "sattion": "station",
        "stn": "station",
        "metrostation": "metro station",
        "busstop": "bus stop",
        "railwaystation": "railway station"
    }
    for wrong, correct in corrections.items():
        text = text.replace(wrong, correct)
    return re.sub(r"\s+", " ", text).strip()

# ------------------ SETUP ------------------
model = SentenceTransformer("all-MiniLM-L6-v2")
client = QdrantClient(url="http://localhost:6333")
collection_name = "women_safety_incidents"

client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

print("Collection created successfully!")

# ------------------ INSERT DATA ------------------
points = []
for incident in incidents:
    embedding = model.encode(incident["text"]).tolist()
    normalized_location = normalize_text(incident["location"])
    points.append({
        "id": incident["id"],
        "vector": embedding,
        "payload": {
            "text": incident["text"],
            "location": normalized_location,
            "original_location": incident["location"],
            "time": incident["time"],
            "incident_type": incident["incident_type"],
            "severity": incident["severity"]
        }
    })

client.upsert(collection_name=collection_name, points=points)
print("Incident data stored in Qdrant successfully!")

# ------------------ BUILD TIME-LOCATION COUNT ------------------
time_location_count = defaultdict(lambda: defaultdict(int))

all_points = client.query_points(collection_name=collection_name, limit=500).points
for p in all_points:
    dt = datetime.strptime(p.payload["time"], "%Y-%m-%d %H:%M")
    hour = dt.hour
    loc = normalize_text(p.payload["location"])
    time_location_count[loc][hour] += 1

print("Time-location risk table built successfully!")
