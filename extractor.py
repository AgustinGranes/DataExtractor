import os
import json
import requests

def scrapear_horarios():
    print("Iniciando extracción de datos para POLE...")
    
    # Endpoint de Supabase y Key pública (Anon Key) de la app
    url = "https://xhnxypogvsmkznqfhhzp.supabase.co/rest/v1/events?select=*&order=start_date.asc"
    
    # La clave pública del proyecto no requiere login ni expira
    anon_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inhobnh5cG9ndnNta3pucWZoaHpwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDY3MTA0NDAsImV4cCI6MjAyMjI4NjQ0MH0.sT9MlhfPXZiP-_gZJvJ1OaB5WbA7qO3Gj4R8uA2R"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "apikey": anon_key,
        "Authorization": f"Bearer {anon_key}",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code != 200:
            # Si el endpoint rest falla, probamos con la Edge Function pública
            url_alt = "https://theracingline.app/api/events"
            response = requests.get(url_alt, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
            
            if response.status_code != 200:
                print(f"❌ Error HTTP {response.status_code}: {response.text}")
                return

        data = response.json()
        print(f"✔ Horarios obtenidos correctamente ({len(data)} eventos cargados).")
        
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
