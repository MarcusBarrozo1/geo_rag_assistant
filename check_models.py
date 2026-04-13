import os
import requests
from dotenv import load_dotenv

# Carrega a chave do nosso .env
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

url = "https://api.groq.com/openai/v1/models"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

print("Consultando servidores do Groq...")
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print("\n✅ Modelos Disponíveis e Ativos agora:")
    for model in data.get("data", []):
        print(f" -> {model['id']}")
else:
    print(f"❌ Erro na API: {response.status_code} - {response.text}")