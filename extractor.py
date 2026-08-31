import os
import json
import requests

# Configuración de Supabase
SUPABASE_URL = "https://bdyoetafdooijwpojdju.supabase.co"
# Clave anónima pública completa extraída del cliente web/móvil
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJkeW9ldGFmZG9vaWp3cG9qZGp1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODgwNjUwNTAsImV4cGlyZXNfYXQiOjIwMDM2NDEwNTB9.k8pG3jP6Z2xS8jF6b4L9X5Z0W3v1Y7N5P8Q2a1R9t3c"

def obtener_bearer_token_fresco(refresh_token):
    print("🔑 Autenticando en Supabase con el refresh_token...")
    url_auth = f"{SUPABASE_URL}/auth/v1/token?grant_type=refresh_token"
    
    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "refresh_token": refresh_token
    }
    
    try:
        response = requests.post(url_auth, headers=headers, json=payload, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            print("✔ Bearer token renovado con éxito.")
            return data.get("access_token")
        else:
            print(f"❌ Error al renovar token en Supabase ({response.status_code}): {response.text}")
            return None
    except Exception as e:
        print(f"❌ Excepción al conectar con Supabase: {e}")
        return None

def scrapear_horarios():
    print("Iniciando extracción automática...")
    
    refresh_token = os.environ.get("SUPABASE_REFRESH_TOKEN")
    
    if not refresh_token:
        print("❌ Error: No se encontró la variable de entorno SUPABASE_REFRESH_TOKEN.")
        return
        
    access_token = obtener_bearer_token_fresco(refresh_token)
    
    if not access_token:
        print("❌ No se pudo obtener el token de acceso. Cancelando la descarga.")
        return

    url_data = "https://theracingline.app/api/mobile/race-data"
    
    headers = {
        "Host": "theracingline.app",
        "Accept": "*/*",
        "User-Agent": "TheRacingLine/1 CFNetwork/3860.600.12 Darwin/25.5.0",
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response_data = requests.get(url_data, headers=headers, timeout=30)
        
        if response_data.status_code != 200:
            print(f"❌ Error al consultar la API de carreras: {response_data.status_code}")
            return
            
        horarios_nuevos = response_data.json()
        print("✔ Datos descargados con éxito de la API.")
        
        ruta_archivo = "data/horarios.json"
        hubo_cambios = True
        
        if os.path.exists(ruta_archivo):
            try:
                with open(ruta_archivo, "r", encoding="utf-8") as f:
                    horarios_viejos = json.load(f)
                if horarios_viejos == horarios_nuevos:
                    hubo_cambios = False
            except Exception:
                hubo_cambios = True

        os.makedirs("data", exist_ok=True)
        
        if hubo_cambios:
            with open(ruta_archivo, "w", encoding="utf-8") as f:
                json.dump(horarios_nuevos, f, ensure_ascii=False, separators=(',', ':'))
            print("✔ Al haber cambios, se actualizó 'data/horarios.json'.")
        else:
            print("✔ Sin cambios detectados. El archivo no se modificó.")
        
    except Exception as e:
        print(f"❌ Error durante la ejecución del script: {e}")

if __name__ == "__main__":
    scrapear_horarios()
