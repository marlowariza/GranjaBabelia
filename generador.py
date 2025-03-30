import requests
import json
import random
import time
from datetime import datetime
import argparse

# Conf
API_KEY = "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" 
API_URL = "https://openrouter.ai/api/v1"
MODEL = "google/gemma-3-1b-it:free" 

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://github.com/marlowariza/GranjaBabelia",
    "X-Title": "Generador de Palabras MCER"
}

# Niveles
niveles = ["A1", "A2", "B1", "B2", "C1", "C2"]

def generar_palabra():
    """Genera una palabra con nivel usando la API de OpenRouter"""
    nivel = random.choice(niveles)
    
    prompt = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": f"""Genera EXACTAMENTE una palabra en español para nivel {nivel} del MCER.
                
                FORMATO REQUERIDO (texto plano):
                palabra, "nivel"
                
                EJEMPLOS:
                casa, "A1"
                resiliencia, "C1"
                
                NO INCLUYAS:
                - Texto adicional
                - Explicaciones
                - Código
                - Saltos de línea"""
            }
        ]
    }
    
    try:
        response = requests.post(
            API_URL,
            headers=headers,
            data=json.dumps({
                "model": MODEL,
                "messages": [prompt],
                "temperature": 0.7,
                "max_tokens": 300
            }),
            timeout=15
        )
        
        # Debug
        print(f"Respuesta API (cruda): {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            contenido = data['choices'][0]['message']['content'].strip()
            
            # Procesamiento
            if "," in contenido:
                partes = [p.strip().replace('"', '').replace("'", "") for p in contenido.split(",")]
                if len(partes) == 2:
                    palabra, nivel_respuesta = partes
                    if nivel_respuesta.upper() in niveles:
                        return palabra, nivel_respuesta.upper()
        
        print("Error: Formato inesperado")
        return None, None
        
    except Exception as e:
        print(f"Error API: {str(e)}")
        return None, None

# ... (El resto de las funciones guardar_palabra() y main() permanecen IGUAL que en tu versión anterior)
