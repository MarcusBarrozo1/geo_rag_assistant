# Geo-RAG Assistant 🚜🤖

A modular Retrieval-Augmented Generation (RAG) pipeline designed to bridge the gap between live IoT sensor data (structured) and agronomic guidelines (unstructured text). 

This system acts as a specialized AI orchestrator, combining real-time database telemetry with a semantic vector knowledge base to generate actionable, context-aware agricultural recommendations.

## 🏗️ Architecture & Microservices

The repository is structured to separate data engineering, semantic search, and AI orchestration into independent, scalable modules:

* **`database_module/` (The Physical Layer)**
  * Uses **Docker** to spin up an isolated **PostgreSQL** instance.
  * Injects simulated historical IoT telemetry (NDVI, soil moisture, temperature).
  * Executes optimized SQL queries to aggregate and filter critical alerts, minimizing RAM payload before data reaches the Python runtime.
* **`ai_engine_module/` (The Knowledge Layer)**
  * Manages a local Vector Database using **ChromaDB**.
  * Utilizes `sentence-transformers` (`all-MiniLM-L6-v2`) to embed unstructured agronomic manuals into geometric vectors.
  * Performs local semantic search (Cosine Similarity) to fetch relevant guidelines without relying on exact keyword matching.
* **`geo_rag_agent.py` (The Orchestrator)**
  * The core application that fuses PostgreSQL data and Vector DB guidelines.
  * Uses Prompt Engineering to feed context into an LLM (**Google Gemini 1.5 Flash**).
  * Includes a Dependency Injection toggle (`USE_MOCK`) to allow safe, cost-free local testing without requiring an active API key.

## 🚀 How to Run Locally

### 1. Prerequisites
* Python 3.10+
* Docker Desktop installed and running.

### 2. Infrastructure Setup (Database)
Navigate to the database module and start the PostgreSQL container:
```bash
cd database_module
docker-compose up -d
```
Note: Wait ~15 seconds on the first boot for the script populate the tablets.

### 3. Install Python Dependencies
It is highly recommended to use a virtual environment (e.g., `venv` or `conda`). 
Install all required dependencies using the provided requirements file:

```bash
pip install -r requirements.txt
```

### 4. Security & Environment Variables
Create a .env file in the root directory and add your Groq API key (if you intend to use the real LLM):
```bash
GROQ_API_KEY=your_api_key_here
```
Ensure .env is added to your .gitignore.

### 5. Execute RAG Agent
Run the main orchestrator script:
```bash
python geo_rag_agent.py
```
By default, the script runs in MOCK MODE (bypassing the LLM API to ensure the architecture works without costs). To test the real AI generation, change USE_MOCK = False inside geo_rag_agent.py.

## 💡 Business Impact
Standard predictive models often lack real-world context. By combining a relational database (which answers what is happening in the field) with a vector database (which answers how to solve it), this architecture ensures that LLM hallucinations are grounded strictly in the company's approved operational manuals.