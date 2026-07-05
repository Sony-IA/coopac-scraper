import cloudscraper

url = "https://www.coopacsdg.pe/ahorro-plazo-fijo"

def ver_codigo_en_pantalla():
    print("\n==================================================")
    print("INICIANDO CAPTURA DIRECTA DE LA COOPAC")
    print("==================================================")
    try:
        scraper = cloudscraper.create_scraper()
        respuesta = scraper.get(url, timeout=20)
        
        print(f"CÓDIGO DE RESPUESTA HTTP: {respuesta.status_code}\n")
        # Imprimimos los primeros 5000 caracteres del código real en los logs de GitHub
        print(respuesta.text[:5000])
        
    except Exception as e:
        print(f"FALLO CRÍTICO DE CONEXIÓN: {str(e)}")
    print("==================================================")

if __name__ == "__main__":
    ver_codigo_en_pantalla()
