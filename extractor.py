import os
import json
import requests

def scrapear_horarios():
    print("Iniciando extracción automática de data.json...")
    
    url_auth = "https://api.backblazeb2.com/b2api/v2/b2_authorize_account"
    headers_auth = {
        "User-Agent": "TheRacingLine/1 CFNetwork/3860.600.12 Darwin/25.5.0",
        "Authorization": "Basic MDA1NWM3YjAzZWNiYTkyMDAwMDAwMDAwMjpLMDA1bGcxakJyRHczZ0JZeHladmlDUTBQNU5HblBr"
    }
    
    try:
        response_auth = requests.get(url_auth, headers=headers_auth, timeout=15)
        if response_auth.status_code != 200:
            print(f"Error en autenticación: {response_auth.status_code}")
            return
            
        auth_data = response_auth.json()
        token_temporal = auth_data.get('authorizationToken')
        print("✔ Token temporal obtenido.")
        
        url_data = "https://f005.backblazeb2.com/file/theracingline/data.json"
        headers_data = {
            "User-Agent": "TheRacingLine/1 CFNetwork/3860.600.12 Darwin/25.5.0",
            "Authorization": token_temporal
        }
        
        response_data = requests.get(url_data, headers=headers_data, timeout=30)
        if response_data.status_code != 200:
            print(f"Error al bajar el JSON: {response_data.status_code}")
            return
            
        horarios_json = response_data.json()
        print("✔ Archivo original data.json descargado.")
        
        os.makedirs("data", exist_ok=True)
        with open("data/horarios.json", "w", encoding="utf-8") as f:
            json.dump(horarios_json, f, ensure_ascii=False, separators=(',', ':'))
            
        print("✔ Archivo guardado correctamente en 'data/horarios.json'.")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    scrapear_horarios()
