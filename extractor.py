import os
import json
import requests

def scrapear_horarios():
    print("Iniciando extracción de datos para POLE...")
    
    # Endpoint principal de Supabase de la app
    url = "https://bdyoetafdooijwpojoju.supabase.co/rest/v1/events?select=*&order=start_date.asc"
    
    # Token JWT de autenticación capturado desde Proxyman (válido hasta su expiración)
    auth_token = "eyJhbGciOiJFUzI1NiIsImtpZCI6IjYyNjYxMjE4LWJiZWQtNDRjOS1iMTgyLTFmNjNhYTQyMjQ2MiIsInR5cCI6IkpXVCJ9.eyJhYWwiOiJhYWwxIiwiYW1yIjpbeyJtZXRob2QiOiJvYXV0aCIsInRpbWVzdGFtcCI6MTc4NDQ4NjYzOH1dLCJhcHBfbWV0YWRhdGEiOnsicHJvdmlkZXIiOiJnb29nbGUiLCJwcm92aWRlcnMiOlsiZ29vZ2xlIl19LCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZW1haWwiOiJhZ3VzdGluZ3JhbmVzQGdtYWlsLmNvbSIsImV4cCI6MTc4ODE0ODcxOSwiaWF0IjoxNzg4MTQ1MTE5LCJpc19hbm9ueW1vdXMiOmZhbHNlLCJpc3MiOiJodHRwczovL2JkeW9ldGFmZG9vaWp3cG9qZGp1LnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJwaG9uZSI6IiIsInJvbGUiOiJhdXRoZW50aWNhdGVkIiwic2Vzc2lvbl9pZCI6Ijg4OWUwZjliLWUyNmYtNDA0Mi05NjBlLTUzNjIxMjAyNTM0MSIsInN1YiI6ImFjYjUyYjQ2LTQ0MWYtNDljNC05ZTMwLTMxNzJjMjU3Nzk4NiIsInVzZXJfbWV0YWRhdGEiOnsiYXZhdGFyX3VybCI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0l4QVNiSUhCdEpJbHlpQV92NnB2eVBJMlJvRVRLV3JNUzNKS0M3VE4wS01McDJCc3NHPXM5Ni1jIiwiZW1haWwiOiJhZ3VzdGluZ3JhbmVzQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJldmVudHNfb3B0X2luIjp0cnVlLCJmdWxsX25hbWUiOiJBZ3VzdGluIEdyYW5lcyIsImlzcyI6Imh0dHBzOi8vYWNjb3VudHMuZ29vZ2xlLmNvbSIsIm1hcmtldGluZ19vcHRfaW4iOnRydWUsIm5hbWUiOiJBZ3VzdGluIEdyYW5lcyIsInBob25lX3ZlcmlmaWVkIjpmYWxzZSwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0l4QVNiSUhCdEpJbHlpQV92NnB2eVBJMlJvRVRLV3JNUzNKS0M3VE4wS01McDJCc3NHPXM5Ni1jIiwicHJvdmlkZXJfaWQiOiIxMTY1ODUwMjAyNjYzNDY4NDYwODEiLCJzaWdudXBfcGxhdGZvcm0iOiJpb3MiLCJzdWIiOiIxMTY1ODUwMjAyNjYzNDY4NDYwODEiLCJ0ZXJtc19hY2NlcHRlZCI6dHJ1ZX0sInVzZXJfcm9sZSI6ImFmZmlsaWF0ZSJ9.1UArV6pn83NrvRh35M1LohmcbXHp8ECOtE-Z52Vd4JntHawVRhEMZmlRqPwOUJT6IZM231PjLKaLZtJvrLUhSg"
    
    headers = {
        "Host": "theracingline.app",
        "x-trl-platform": "ios",
        "User-Agent": "TheRacingLine-iOS/2.62.0 (1)",
        "Authorization": f"Bearer {auth_token}",
        "Accept": "application/json",
        "Accept-Language": "es-419,es;q=0.9"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code != 200:
            # Si falla la consulta directa, probamos con la Edge Function oficial
            url_alt = "https://theracingline.app/api/events"
            response = requests.get(url_alt, headers=headers, timeout=30)
            
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
