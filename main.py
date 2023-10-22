import concurrent.futures
import html
import re
import requests


# Función para buscar y guardar URLs con credenciales
def buscar_urls_con_credenciales(url, archivo_salida, urls_unicas):
    try:
        response = requests.get(url)
        response.raise_for_status()
        # Obtener el contenido de la página web
        contenido = response.text
        # Buscar URLs que contengan "username" y "password"
        urls = re.findall(r'http[^\s"\']+', contenido)
        with open(archivo_salida, 'w') as archivo:
            for url_encontrada in urls:
                url_deco = html.unescape(url_encontrada)  # Decodificar la URL
                if 'username=' in url_deco and 'password=' in url_deco and url_deco not in urls_unicas:
                  urls_unicas.add(url_deco)
                  kurl = url_deco.replace("xmltv.php", "get.php")
                  archivo.write(f'{kurl}\n')
        print(f'URLs encontradas en {url} guardadas en {archivo_salida}')
    except requests.exceptions.RequestException as e:
        print(f'Error al acceder a {url}: {e}')
    except Exception as e:
        print(f'Error inesperado: {e}')

# Archivos que contiene/guarda las URLs a buscar
archivo_urls = '[leech].txt'
archivo_salida = 'urls.txt'
# Conjunto para almacenar URLs únicas
urls_unicas = set()
# Leer las URLs desde el archivo de texto
with open(archivo_urls, 'r') as file:
    urls = file.read().splitlines()

# Bucle para buscar URLs en todas las URLs de manera concurrente
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(buscar_urls_con_credenciales, url, archivo_salida, urls_unicas) for url in urls]
print('Leecher completed.')
exec(open("searcher.py").read())
