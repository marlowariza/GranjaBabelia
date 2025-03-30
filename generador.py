import requests
import json
import random
import time
from datetime import datetime
import argparse  # Nuevo import para manejar argumentos

# Configuración
API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "allenai/molmo-7b-d:free"

# Headers requeridos por OpenRouter
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://github.com/marlowariza/GranjaBabelia",
    "X-Title": "Generador de Palabras MCER"
}

# Niveles de competencia lingüística
niveles = ["A1", "A2", "B1", "B2", "C1", "C2"]

def generar_palabra():
    """Genera una palabra con nivel usando la API de OpenRouter"""
    nivel = random.choice(niveles)
    
    prompt = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": f"""Responde EXCLUSIVAMENTE con este formato:
<palabra>, "<nivel>"

REQUISITOS:
1. Una palabra en español adecuada para nivel {nivel} del MCER
2. Nivel entre comillas: "{nivel}"
3. SIN texto adicional
4. SIN explicaciones
5. SIN caracteres especiales

Ejemplo válido:
libro, "A1"

Respuesta:"""
            }
        ]
    }
    
    try:
        response = requests.post(
            url=API_URL,
            headers=headers,
            data=json.dumps({
                "model": MODEL,
                "messages": [prompt],
                "temperature": 0.7,
                "max_tokens": 200
            })
        )
        
        # Debug: Mostrar respuesta en crudo
        print(f"Respuesta API (cruda): {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            contenido = data['choices'][0]['message']['content'].strip()
            
            # Procesamiento robusto
            if "," in contenido:
                partes = [p.strip().replace('"', '').replace("'", "") for p in contenido.split(",")]
                if len(partes) == 2:
                    palabra, nivel_respuesta = partes
                    if nivel_respuesta.upper() in niveles:
                        return palabra, nivel_respuesta.upper()
        
        print(f"Error: Formato inesperado o API no respondió adecuadamente")
        return None, None
        
    except Exception as e:
        print(f"Excepción al llamar a la API: {str(e)}")
        return None, None

def guardar_palabra(palabra, nivel):
    """Guarda la palabra en el archivo si es válida"""
    if not palabra or not nivel:
        return False
    
    try:
        # Verificar duplicados
        with open("palabras_generadas.txt", "r+", encoding="utf-8") as f:
            contenido = f.read()
            
            if f'"{palabra}"' in contenido:
                print(f"⚠️ Palabra duplicada: {palabra}")
                return False
                
            # Escribir al final del archivo
            f.seek(0, 2)
            f.write(f'insertWord("{palabra}", "{nivel}");\n')
            return True
            
    except Exception as e:
        print(f"❌ Error al guardar: {e}")
        return False

def main():
    # Manejo de argumentos
    parser = argparse.ArgumentParser()
    parser.add_argument('--run-once', action='store_true', help='Ejecuta solo una generación')
    args = parser.parse_args()

    # Inicializar archivo
    try:
        with open("palabras_generadas.txt", "a+", encoding="utf-8") as f:
            if f.tell() == 0:  # Archivo vacío
                f.write("// Listado generado automáticamente - " + datetime.now().strftime("%Y-%m-%d %H:%M") + "\n\n")
    except Exception as e:
        print(f"Error inicializando archivo: {e}")
        return
    
    # Modo ejecución única (para GitHub Actions)
    if args.run_once:
        palabra, nivel = generar_palabra()
        if palabra and nivel:
            guardar_palabra(palabra, nivel)
        return
    
    # Bucle principal (para ejecución local)
    contador = 0
    while True:
        contador += 1
        print(f"\n--- Intento #{contador} [{datetime.now().strftime('%H:%M:%S')}] ---")
        
        palabra, nivel = generar_palabra()
        if palabra and nivel:
            if guardar_palabra(palabra, nivel):
                print(f"✅ Guardado: {palabra} ({nivel})")
            else:
                print("❌ No se pudo guardar la palabra")
        
        # Espera adaptable (5-8 minutos)
        espera = random.randint(300, 480)
        minutos = espera // 60
        print(f"⏳ Esperando {minutos} minutos...")
        time.sleep(espera)

if __name__ == "__main__":
    main()
