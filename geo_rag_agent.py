import os 
import pandas as pd
from dotenv import load_dotenv
from google import genai

from database_module.db_connector import AgTechDBConnector
from ai_engine_module.knowledge_builder import AgKnowledgeBase

class GeoRAGAgent:
    """
    Combines SQL Live Data, Vector DB Guidelines, 
    and LLM generation to produce expert agronomic advice.
    """
    def __init__ (self, use_mock=True):
        self.use_mock = use_mock

        load_dotenv()  # Load environment variables from .env file

        if not self.use_mock:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY not found in environment variables.")
            
            self.client = genai.Client(api_key=api_key)
        
        self.db = AgTechDBConnector()
        self.vector_db = AgKnowledgeBase(db_path = "/.ai_engine_module/vector_store")

    def _fetch_live_data(self, field_id: str) -> str:
        "Fetches the latest sensor data for a specific field using SQL."
        query = f"""
            SELECT 
                crop_type,
                ndvi_score,
                soil_moisture,
                temperature
            FROM field_metrics
            WHERE field_id = '{field_id}'
            ORDER BY record_date DESC LIMIT 1;
        """
        df = self.db.extract_to_dataframe(query)
        if df.empty:
            return "No recent data available for the specified field."
        
        return df.to_string(index=False)
    
    def generate_recommendation(self, field_id: str, farmer_question: str) -> str:
        "Runs the RAG pipeline."
        live_data = self._fetch_live_data(field_id)
        print(f"[AGENT] 1/3 - Live telemetry extracted from PostgreSQL.")

        guideline, metadata = self.vector_db.search_guideline(farmer_question)
        print(f"[AGENT] 2/3 - Knowledge retrieved from Vector DB.")

        prompt = f"""
        You are a Senior Agronomist AI. Answer the farmer's question using ONLY the provided live data and expert manual.
        Respond in English, be direct, and state if there is a critical alert.
        
        [LIVE FIELD DATA (PostgreSQL Telemetry)]
        Field ID: {field_id}
        {live_data}
        
        [MANUAL (Vector DB)]
        Target Crop: {metadata['crop']}
        Guideline: {guideline}
        
        [FARMER'S QUESTION]
        {farmer_question}
        """

        print(f"[AGENT] 3/3 - Generating response...\n")

        if self.use_mock:
            # Mocked response for testing without LLM
            return (
                "=== MOCK RESPONSE (NO API COST) ===\n"
                f"Based on the data for {field_id}, the crop is facing critical conditions. "
                "The telemetry shows temperatures exceeding safe limits, and according to the manual, "
                "immediate rescue irrigation is required. (Set USE_MOCK=False to see real LLM output)."
            )
        else:
            response = self.client.models.generate_content(
                model = "gemini-2.0-flash",
                contents= prompt,
            )
            return f"=== GEMINI AI RESPONSE ===\n{response.text}"

# Execution block for testing the GeoRAGAgent
if __name__ == "__main__":
    USE_MOCK = True  # Set to False to enable real LLM generation (requires valid API key)

    agent = GeoRAGAgent(use_mock=USE_MOCK)

    target_field_id = "FIELD_GAMMA_03"
    question = "My sensors are showing weird numbers today. What is the status of my crop and what action should I take?"

    final_answer = agent.generate_recommendation(field_id=target_field_id, farmer_question=question)
    print(final_answer)