import os
import json
import requests

def scrapear_horarios():
    print("Iniciando extracción de datos para POLE...")
    
    # URL directa del JSON de eventos (Backblaze B2 CDN)
    url = "https://f005.backblazeb2.com/file/trl-public/events.json"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ Error HTTP {response.status_code}: {response.text}")
            return
            
        data = response.json()
        print("✔ Horarios obtenidos correctamente desde la fuente de datos.")
        
        ruta = "data/horarios.json"
        hubo_cambios = True
        
        if os.path.exists(ruta):
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    if json.load(f) == data:
                        hubo_cambios = False
            except Exception:
                hubo_cambios = True

        os.makedirs("data", exist_ok=True)
        
        if hubo_cambios:
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("✔ Cambios guardados en 'data/horarios.json'.")
        else:
            print("✔ Sin cambios en los horarios.")

    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")

if __name__ == "__main__":
    scrapear_horarios()
