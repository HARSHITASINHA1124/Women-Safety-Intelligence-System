<<<<<<< HEAD
# Women Safety Intelligence System

An AI-powered safety intelligence platform that uses semantic memory and machine learning to identify unsafe locations, time-based risk patterns, and recurring safety threats—helping women make informed, proactive safety decisions.

---

## 🚨 Problem Overview

Women’s safety incidents are often reported in fragmented ways—through informal conversations, social media, or delayed official complaints. Most existing safety solutions are reactive and fail to use historical data to prevent future incidents.

This project addresses that gap by transforming incident reports into a **living memory system** that continuously learns from past data to provide **context-aware safety insights**.

---

## 🧠 Key Features

- 📌 **Incident Reporting System**  
  Users can submit safety incidents with location, time, severity, and description.

- 🔍 **Semantic Search (Not Keyword-Based)**  
  Find relevant past incidents based on meaning, not exact words.

- 🧠 **Persistent Memory Using Qdrant**  
  Every incident becomes part of long-term system intelligence.

- 📊 **ML-Based Risk Prediction**  
  Predicts danger levels for a place and time using historical patterns.

- 🚓 **SOS Monitoring Dashboard**  
  High-risk incidents are flagged and prioritized for attention.

- ⏱️ **Time-Aware Risk Analysis**  
  Same location can have different risk levels at different times.

---

## 🏗️ System Architecture (High-Level)

1. **Frontend:** Streamlit interface for users and admins  
2. **Embedding Layer:** Sentence Transformer for text embeddings  
3. **Vector Database:** Qdrant for semantic memory storage  
4. **ML Layer:** Logistic Regression for risk classification  
5. **Logic Layer:** Ranking, filtering, and prediction aggregation  

---

## 📦 Why Qdrant?

Qdrant enables:
- Semantic similarity search on incident descriptions  
- Storage of vectors along with contextual metadata  
- Scalable, real-time memory that evolves with new data  

Traditional databases cannot support this level of semantic reasoning.

---

## 📊 Machine Learning Model

- **Model Used:** Logistic Regression  
- **Purpose:** Predict LOW / MODERATE / HIGH risk  
- **Features Include:**
  - Incident frequency by location & time
  - Average severity score
  - Day/Night indicator
  - Historical patterns

All predictions are backed by retrieved historical evidence.

---

## 🛠️ Tech Stack

- **Programming Language:** Python  
- **Frontend:** Streamlit  
- **Vector DB:** Qdrant  
- **Embeddings:** Sentence Transformers  
- **ML:** Scikit-learn  
- **Deployment:** Local / Docker  

---

## ▶️ How to Run

### 1. Start Qdrant
```bash
docker run -p 6333:6333 qdrant/qdrant
```

### 2. Run Data Ingestion
```bash
python main.py
```

### 3. Train Risk Prediction Model
```bash
python train_model.py
```

### 4. Launch UI
```bash
streamlit run ui.py
````

### Open in browser:

http://localhost:8501
=======
# Women-Safety-Intelligence-System
>>>>>>> b36b7f9d13889e23a2ce3a55e8cab33c6f8c964b
