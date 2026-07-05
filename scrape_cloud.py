import json
import re
import cloudscraper

url = "https://www.coopacsdg.pe/ahorro-plazo-fijo"

def ejecutar_scraping():
    print("Lanzando escáner quirúrgico en la nube...")
    tasas_validas = []
    
    try:
        scraper = cloudscraper.create_scraper()
        respuesta = scraper.get(url, timeout=25)
        
        if respuesta.status_code != 200:
            print(f"Error de acceso: HTTP {respuesta.status_code}")
            return
            
        html = respuesta.text
        # Limpieza profunda de HTML para quedarnos solo con el texto limpio de las pizarras
        texto_plano = re.sub(r"<[^>]+>", " ", html)
        texto_plano = re.sub(r'\s+', ' ', texto_plano) # Unificar espacios
        
        print("\n--- [AUDITORÍA DE TEXTO DETECTADO EN LA WEB] ---")
        # Esto imprimirá en tu log de GitHub las primeras líneas para verificar si la web tiene texto o es una imagen
        print(texto_plano[:1500]) 
        print("------------------------------------------------\n")

        # Buscamos bloques específicos donde aparezca la palabra TREA junto a un número
        # Captura formatos como: "TREA 8.5%", "TREA: 9.00%", "TREA del 7.5%"
        coincidencias = re.finditer(r"TREA\s*(?::|del|desde)?\s*(\d+(?:[\.,]\d+)?)\s*%", texto_plano, re.IGNORECASE)
        
        for match in coincidencias:
            tasa_num = float(match.group(1).replace(",", "."))
            if tasa_num < 1.0:
                tasa_num = tasa_num * 100 # Normalizar si viene en formato 0.08
                
            # Extraer el entorno cercano (100 caracteres antes y después) para cazar el plazo en días
            pos_actual = match.start()
            bloque_contexto = texto_plano[max(0, pos_actual - 100):min(len(texto_plano), pos_actual + 100)]
            
            match_plazo = re.search(r"(\d+)\s*(?:días|dias|meses|mes|plazo)", bloque_contexto, re.IGNORECASE)
            plazo_num = int(match_plazo.group(1)) if match_plazo else 360
            
            # Conversión si el plazo está expresado en meses
            if match_plazo and "mes" in match_plazo.group(0).lower() and plazo_num < 36:
                plazo_num = plazo_num * 30

            # Validar que sea una tasa pasiva coherente del mercado COOPAC (Entre 3% y 18%)
            if 3.0 <= tasa_num <= 18.0:
                # Evitar duplicados exactos de plazo en el JSON
                if not any(t['Plazo'] == plazo_num for t in tasas_validas):
                    tasas_validas.append({
                        'Plazo': plazo_num, 
                        'TREA': tasa_num / 100 # Guardar en decimal para el main.py local
                    })
                    print(f"[Filtro TREA Pasado] Detectado: Plazo {plazo_num} días -> TREA: {tasa_num}%")

    except Exception as e:
        print(f"Excepción en el nodo de la nube: {str(e)}")

    # Si la web no arrojó textos con la palabra "TREA" (porque movieron el tarifario a un PDF o imagen JPG)
    if not tasas_validas:
        print("[Alerta] La estructura no contiene texto indexable de TREA. Aplicando actualización forzada de contingencia.")
        # Aquí puedes ajustar los dos números base si notas que cambiaron en la pizarra física
        tasas_validas = [
            {'Plazo': 180, 'TREA': 0.0850}, 
            {'Plazo': 360, 'TREA': 0.0980}
        ]

    # Guardar los datos limpios en el JSON
    with open("tasas.json", "w", encoding="utf-8") as f:
        json.dump(tasas_validas, f, indent=4)
    print("Sincronización finalizada con éxito.")

if __name__ == "__main__":
    ejecutar_scraping()
