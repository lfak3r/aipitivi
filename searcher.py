import json
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import requests


# Función para verificar si una cadena es una URL válida
def es_url(cadena):
    regex = r'^(http|https)://[^\s/$.?#].[^\s]*$'
    return re.match(regex, cadena) is not None

# Función para buscar y extraer un valor específico de la respuesta
def buscar_valor(respuesta, clave):
    valor = None
    index = respuesta.find(f'"{clave}":"')
    if index != -1:
        valor = respuesta[index + len(f'"{clave}":"'):]
        valor = valor.split('"')[0]
    return valor

# Función para convertir un timestamp en una fecha y hora legible
def timestamp_a_fecha(timestamp):
    fecha = datetime.fromtimestamp(int(timestamp))
    return fecha.strftime('%Y-%m-%d %H:%M:%S')

# Leer las URLs desde el archivo de texto
with open('urls.txt', 'r') as file:
  lineas = file.read().splitlines()
# Filtrar las líneas que contienen URLs válidas
urls = [linea for linea in lineas if es_url(linea)]
# Filtro adicional: URLs que contienen '&type='
urls_filtradas = [url for url in urls if '&type=' not in url]

# Función para buscar y contar las apariciones de "category_name" y guardar los nombres de las categorías
def buscar_categorias(respuesta):
    categorias = set()  # Usar un conjunto para evitar duplicados
    contador = 0
    index = respuesta.find('"category_name":"')

    while index != -1:
        start_index = index + len('"category_name":"')
        end_index = respuesta.find('","', start_index)

        if end_index != -1:
            categoria = respuesta[start_index:end_index]
            try:
                decoded_categoria = json.loads(f'"{categoria}"')
                if isinstance(decoded_categoria, str):
                    categorias.add(decoded_categoria)
                    contador += 1
            except json.JSONDecodeError:
                pass

        # Actualizar el índice para buscar la siguiente categoría
        index = respuesta.find('"category_name":"', end_index)

    return contador, list(categorias)

# Función para analizar una URL
# Lista de URLs que deseas analizar
urls_a_analizar = urls
def analizar_url(original_url):
    url = original_url.replace("get.php", "panel_api.php")
    separahit = "\033[92m" + '=' * 30 + " ++ HIT ++ " + '=' * 30 + "\033[0m"
    separaerr = "\033[91m" + '=' * 30 + " -- ERROR -- " + '=' * 30 + "\033[0m"
    resultados = []

    try:
        # Realizar una solicitud HTTP GET a la URL
        response = requests.get(url)
        response.raise_for_status()

        # Buscar y extraer los valores
        exp_date = buscar_valor(response.text, "exp_date")
        max_connections = buscar_valor(response.text, "max_connections")
        active_connections = buscar_valor(response.text, "active_cons")
        user_ind = buscar_valor(response.text, "username")
        pass_ind = buscar_valor(response.text, "password")
        real_url = buscar_valor(response.text, "url")
        real_port = buscar_valor(response.text, "port")

        resultados.append(separahit)  # Imprime un separador personalizado con texto
        resultados.append(f"Website: {original_url}")
        with open('History/history.txt', 'r') as hits_file:
          urls_en_hits = [line.split('&type=')[0] for line in hits_file.read().splitlines()]
  
        # Comprueba si la URL (sin los parámetros) ya existe en el archivo
        # Obtén la URL base antes de '&type='
        url_base = original_url.split('&type=')[0]
        if url_base not in urls_en_hits:
            with open('History/history.txt', 'a') as hits_file:
                hits_file.write(f"{original_url}\n")


            
        if real_url is not None:
            resultados.append(f"RealURL: {real_url}:{real_port}")
        if exp_date is not None:
            fecha_exp_date = timestamp_a_fecha(exp_date)
            resultados.append(f"exp_date: {fecha_exp_date}")
        if max_connections is not None:
          max_connections = int(max_connections)
          if max_connections > 1:
              resultados.append(f"👀max_connections: {max_connections}")
          else:
              resultados.append(f"max_connections: {max_connections}")
  
        if active_connections is not None:
          active_connections = int(active_connections)
        if active_connections < 1:
          resultados.append(f"-active_connections: {active_connections}")
        else:
          resultados.append(f"active_connections: {active_connections}")
        if user_ind is not None:
            resultados.append(f"User: {user_ind}")
        if pass_ind is not None:
            resultados.append(f"Password: {pass_ind}")

        # Buscar y contar las apariciones de "category_name" y guardar los nombres de las categorías
        categories_data = response.text.split('"categories":{', 1)
        if len(categories_data) > 1:
            categories_data = categories_data[1]
            num_canals, categorias = buscar_categorias(categories_data)
            resultados.append("========== Channels ==========")
            resultados.append(f"Channels: {num_canals}")
            resultados.append(f"Categories: {', '.join(categorias)}")
            resultados.append("==============================")
    except requests.exceptions.RequestException as e:
        print(separaerr)  # Imprime un separador personalizado con texto
        print(f"{e}")

    except Exception as e:
        print(separaerr)  # Imprime un separador personalizado con texto
        print(f"{e}")

    return resultados


# Abre el archivo "results.txt" en modo escritura
with open('[results].txt', 'w') as results_file:
    # Utiliza ThreadPoolExecutor para analizar las URLs concurrentemente
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(analizar_url, url) for url in urls_a_analizar]

        # Espera a que todas las tareas se completen y escribe los resultados en el orden original
        for future in futures:
            resultados = future.result()
            for resultado in resultados:
                print(resultado)
                results_file.write(resultado + '\n')

print("""
  ███████╗██╗███╗   ██╗██╗███████╗██╗  ██╗
  ██╔════╝██║████╗  ██║██║██╔════╝██║  ██║
  █████╗  ██║██╔██╗ ██║██║███████╗███████║
  ██╔══╝  ██║██║╚██╗██║██║╚════██║██╔══██║
  ██║     ██║██║ ╚████║██║███████║██║  ██║
  ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝╚══════╝╚═╝  ╚═╝
""")
