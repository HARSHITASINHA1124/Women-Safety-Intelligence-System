import re

def normalize_location(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def severity_to_num(sev):
    return {"Low": 1, "Medium": 2, "High": 3}.get(sev, 1)
