import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

class AgTechDBConnector:
    def __init__(self, host='localhost', port=5455, database='agtech_intelligence', user='admin', password='your_password'):
        self.db_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        self.engine = None

    def connect(self):
        try:
            self.engine = create_engine(self.db_url)
            print("Connection to the database was successful.")
        except SQLAlchemyError as e:
            print(f"An error occurred while connecting to the database: {e}")

    def extract_to_dataframe(self, query: str) -> pd.DataFrame:
        if not self.engine:
            self.connect()
        try:
            df = pd.read_sql_query(query, self.engine)
            print("Data extracted successfully.")
            return df
        except SQLAlchemyError as e:
            print(f"An error occurred while extracting data: {e}")
            return pd.DataFrame()  # Return an empty DataFrame on error

if __name__ == "__main__":
    db = AgTechDBConnector()

    advanced_query = """
        SELECT 
            crop_type,
            COUNT(DISTINCT field_id) AS fields_in_danger,
            ROUND(AVG(temperature), 2) AS avg_critical_temp,
            MIN(soil_moisture) AS lowest_moisture_recorded
        FROM field_metrics
        WHERE agronomic_alert = TRUE
        GROUP BY crop_type
        ORDER BY avg_critical_temp DESC;
    """

    print("Executing data extraction pipeline \n")

    df_alerts = db.extract_to_dataframe(advanced_query)
    print("=== CRITICAL AGRONOMIC ALERTS ===")
    print(df_alerts.to_string(index=False))
    