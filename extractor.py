import os
import json
import requests
import base64

def extraer_access_token(cookie_str):
    try:
        parts = [p.strip() for p in cookie_str.split(';') if 'sb-auth-auth-token' in p]
        parts.sort(key=lambda x: x.split('=')[0])
        raw_b64 = "".join([p.split('=', 1)[1] for p in parts]).replace('base64-', '')
        padding = '=' * (-len(raw_b64) % 4)
        decoded = base64.b64decode(raw_b64 + padding).decode('utf-8')
        data = json.loads(decoded)
        return data.get("access_token")
    except Exception:
        return None

def scrapear_horarios():
    print("Iniciando extracción de datos para POLE...")
    
    cookie = os.environ.get("SUPABASE_COOKIE")
    if not cookie:
        print("❌ Error: No se encontró la variable SUPABASE_COOKIE.")
        return

    access_token = extraer_access_token(cookie)
    
    url_data = "https://theracingline.app/api/notifications/upcoming"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://theracingline.app/",
        "Cookie": cookie
    }

    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

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
