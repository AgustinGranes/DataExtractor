import os
import json
import requests

def scrapear_horarios():
    print("Iniciando extracción automática desde la nueva API...")
    
    # URL directa de la nueva API en Vercel
    url_data = "https://theracingline.app/api/mobile/race-data/version"
    
    headers = {
        "Host": "theracingline.app",
        "Accept": "*/*",
        "User-Agent": "TheRacingLine/1 CFNetwork/3860.600.12 Darwin/25.5.0",
        "Accept-Language": "es-419,es;q=0.9",
        "Authorization": "Bearer eyJhbGciOiJFUzI1NiIsImtpZCI6IjYyNjYxMjE4LWJiZWQtNDRjOS1iMTgyLTFmNjNhYTQyMjQ2MiIsInR5cCI6IkpXVCJ9.eyJhYWwiOiJhYWwxIiwiYW1yIjpbeyJtZXRob2QiOiJvYXV0aCIsInRpbWVzdGFtcCI6MTc4NDQ4NjYzOH1dLCJhcHBfbWV0YWRhdGEiOnsicHJvdmlkZXIiOiJnb29nbGUiLCJwcm92aWRlcnMiOlsiZ29vZ2xlIl19LCJhdWQiOiJhdXRoZW50aWNhdGVkIiwic2Vzc2lvbl9pZCI6Ijg4OWUwZjliLWUyNmYtNDA0Mi05NjBlLTUzNjIxMjAyNTM0MSIsInN1YiI6ImFjYjUyYjQ2LTQ0MWYtNDljNC05ZTMwLTMxNzJjMjU3Nzk4NiIsInVzZXJfcm9sZSI6ImFmZmlsaWF0ZSJ9.1UArV6pn83NrvRh35M1LohmcbXHp8ECOtE-Z52Vd4JntHawVRhEMZmlRqPwOUJT6IZM231PjLKaLZtJvrLUhSg",
        "Accept-Encoding": "gzip, deflate, br"
    }
    
    try:
        # Petición directa al backend
        response_data = requests.get(url_data, headers=headers, timeout=30)
        
        if response_data.status_code != 200:
            print(f"❌ Error al consultar la API: {response_data.status_code}")
            return
            
        horarios_nuevos = response_data.json()
        print("✔ Datos descargados con éxito de la nueva API.")
        
        # Control de cambios y guardado inteligente
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
            print("✔ Al haber cambios, se modificó el archivo. Archivo guardado correctamente en 'data/horarios.json'.")
        else:
            print("✔ Como no había cambios, el archivo no se modificó.")
        
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado durante el flujo: {e}")

if __name__ == "__main__":
    scrapear_horarios()
