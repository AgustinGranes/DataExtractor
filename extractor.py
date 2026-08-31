import os
import json
import requests

def scrapear_horarios():
    print("Iniciando extracción de datos para POLE...")
    
    token = os.environ.get("SUPABASE_TOKEN")
    cookie = os.environ.get("SUPABASE_COOKIE")
    
    if not token and not cookie:
        print("❌ Error: No se encontraron credenciales de autenticación.")
        return

    url = "https://theracingline.app/api/notifications/upcoming"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://theracingline.app/home",
        "Origin": "https://theracingline.app"
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"
    if cookie:
        headers["Cookie"] = cookie

    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ Error HTTP {response.status_code}: {response.text}")
            return
            
        data = response.json()
        
        # Validar si devuelve el payload envenenado por falta de autenticación
        if isinstance(data, dict) and data.get("poisoned") is True and not data.get("sessions"):
            print("❌ La API devolvió un estado de sesión no autenticado (poisoned: true). Verifica la validez del SUPABASE_TOKEN.")
            return

        print("✔ Horarios obtenidos correctamente.")
        
        ruta = "data/horarios.json"
        os.makedirs("data", exist_ok=True)
        
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"✔ Cambios guardados en '{ruta}'.")

    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")

if __name__ == "__main__":
    scrapear_horarios()
