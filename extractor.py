import os
import json
import requests

def scrapear_horarios():
    print("Iniciando extracción de datos para POLE...")
    
    token = os.environ.get("SUPABASE_TOKEN")
    if not token:
        print("❌ Error: Falta la variable SUPABASE_TOKEN.")
        return

    # Endpoint de notificaciones / eventos
    url_data = "https://theracingline.app/api/notifications/upcoming"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(url_data, headers=headers, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ Error HTTP {response.status_code}: {response.text}")
            return
            
        horarios_nuevos = response.json()
        print("✔ Datos obtenidos correctamente.")
        
        ruta_archivo = "data/horarios.json"
        hubo_cambios = True
        
        if os.path.exists(ruta_archivo):
            try:
                with open(ruta_archivo, "r", encoding="utf-8") as f:
                    if json.load(f) == horarios_nuevos:
                        hubo_cambios = False
            except Exception:
                hubo_cambios = True

        os.makedirs("data", exist_ok=True)
        
        if hubo_cambios:
            with open(ruta_archivo, "w", encoding="utf-8") as f:
                json.dump(horarios_nuevos, f, ensure_ascii=False, separators=(',', ':'))
            print("✔ Cambios guardados en 'data/horarios.json'.")
        else:
            print("✔ Sin cambios en los horarios.")
            
    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")

if __name__ == "__main__":
    scrapear_horarios()
