import os
import json
import requests

def obtener_calendario_directo():
    print("Obteniendo calendario general desde la API...")
    
    # Endpoint directo público de la base de datos de The Racing Line
    url = "https://theracingline.app/api/events/upcoming"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ Error HTTP {response.status_code}: {response.text}")
            return
            
        data = response.json()
        
        # Validar si devolvió la lista real de eventos
        if not data or (isinstance(data, dict) and data.get("poisoned")):
            print("⚠️ La API sigue devolviendo un payload restringido.")
            return

        print("✔ Horarios obtenidos correctamente.")
        
        ruta = "data/horarios.json"
        os.makedirs("data", exist_ok=True)
        
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"✔ Datos actualizados en '{ruta}'.")

    except Exception as e:
        print(f"❌ Error en la petición: {e}")

if __name__ == "__main__":
    obtener_calendario_directo()
