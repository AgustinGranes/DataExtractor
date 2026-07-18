import os
import json
import requests

def scrapear_horarios():
    print("Iniciando extracción automática de data.json...")
    
    # 1. Autenticación en Backblaze
    url_auth = "https://api.backblazeb2.com/b2api/v2/b2_authorize_account"
    headers_auth = {
        "User-Agent": "TheRacingLine/1 CFNetwork/3860.600.12 Darwin/25.5.0",
        "Authorization": "Basic MDA1NWM3YjAzZWNiYTkyMDAwMDAwMDAwMjpLMDA1bGcxakJyRHczZ0JZeHladmlDUTBQNU5HblBr"
    }
    
    try:
        response_auth = requests.get(url_auth, headers=headers_auth, timeout=15)
        if response_auth.status_code != 200:
            print(f"Error crítico en autenticación: {response_auth.status_code}")
            return
            
        auth_data = response_auth.json()
        token_temporal = auth_data.get('authorizationToken')
        print("✔ Token temporal obtenido de Backblaze.")
        
        # 2. Descarga del JSON completo de carreras
        url_data = "https://f005.backblazeb2.com/file/theracingline/data.json"
        headers_data = {
            "User-Agent": "TheRacingLine/1 CFNetwork/3860.600.12 Darwin/25.5.0",
            "Authorization": token_temporal
        }
        
        response_data = requests.get(url_data, headers=headers_data, timeout=30)
        if response_data.status_code != 200:
            print(f"Error al bajar el JSON: {response_data.status_code}")
            return
            
        horarios_nuevos = response_data.json()
        print("✔ Archivo original data.json descargado con éxito.")
        
        # 3. Control de cambios y guardado inteligente
        ruta_archivo = "data/horarios.json"
        hubo_cambios = True
        
        # Si el archivo ya existía de una ejecución anterior, lo leemos para comparar
        if os.path.exists(ruta_archivo):
            try:
                with open(ruta_archivo, "r", encoding="utf-8") as f:
                    horarios_viejos = json.load(f)
                
                # Comparamos la estructura de ambos objetos JSON
                if horarios_viejos == horarios_nuevos:
                    hubo_cambios = False
            except Exception:
                # Si falla al leer el viejo (por estar corrupto), asumimos que hay que pisarlo
                hubo_cambios = True

        # Creamos la carpeta si no existe
        os.makedirs("data", exist_ok=True)
        
        if hubo_cambios:
            # Si cambió, lo guardamos en el disco
            with open(ruta_archivo, "w", encoding="utf-8") as f:
                json.dump(horarios_nuevos, f, ensure_ascii=False, separators=(',', ':'))
            print("✔ Al haber cambios, se modificó el archivo. Archivo guardado correctamente en 'data/horarios.json'.")
        else:
            # Si es idéntico, imprimimos el aviso de que no se tocó nada
            print("✔ Como no había cambios, el archivo no se modificó.")
        
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado durante el flujo: {e}")

if __name__ == "__main__":
    scrapear_horarios()
