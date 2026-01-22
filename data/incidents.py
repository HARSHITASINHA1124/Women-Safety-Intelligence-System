import random
from datetime import datetime, timedelta

locations = [
    "Vasundhara Enclave", "Metro Station", "Bus Stop", "College Area",
    "Marketplace", "Residential Area", "Railway Station", "Park",
    "Shopping Mall", "Main Road"
]

incident_types = ["Harassment", "Stalking", "Theft", "Assault", "Verbal Abuse"]
severity_levels = ["Low", "Medium", "High"]

incidents = []

base_time = datetime(2025, 1, 1, 6, 0)  # starting date

for i in range(1, 101):
    loc = random.choice(locations)
    itype = random.choices(incident_types, weights=[0.4, 0.2, 0.25, 0.1, 0.05])[0]
    severity = random.choices(severity_levels, weights=[0.3, 0.4, 0.3])[0]
    
    # random datetime over 1 year
    random_days = random.randint(0, 364)
    random_hours = random.randint(0, 23)
    random_minutes = random.randint(0, 59)
    time = base_time + timedelta(days=random_days, hours=random_hours, minutes=random_minutes)
    
    text = f"{itype} reported near {loc.lower()} at {time.strftime('%H:%M')}."
    
    incidents.append({
        "id": i,
        "text": text,
        "location": loc,
        "time": time.strftime("%Y-%m-%d %H:%M"),
        "incident_type": itype,
        "severity": severity
    })
