import cloudscraper

url = "https://www.coopacsdg.pe/ahorro-plazo-fijo"

def diagnostico_total():
    print("Capturando respuesta real del servidor...")
    try:
        scraper = cloudscraper.create_scraper()
        respuesta = scraper.get(url, timeout=20)
        
        # Guardamos exactamente lo que responde la web (sea el texto real o un mensaje de bloqueo)
        contenido = f"CÓDIGO HTTP: {respuesta.status_code}\n\n{respuesta.text}"
    except Exception as e:
        contenido = f"FALLO CRÍTICO DE CONEXIÓN EN LA NUBE: {str(e)}"
        
    with open("codigo_real.txt", "w", encoding="utf-8") as f:
        f.write(contenido)
    print("Archivo codigo_real.txt generado.")

if __name__ == "__main__":
    diagnostico_total()
