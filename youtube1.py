#####################################################
#                                                   #
#                  Samuel Herrera                   #
#                                                   #
#           Web scraping - pagina youtube           #
#                                                   #
#                                                   #
#                                                   #
#                                                   #
#####################################################

# Este script usa dos patrones diferentes para extraer la información que necesitas. El primero, video_pattern, busca el
# ID de cada video. El segundo, title_pattern, busca el título de cada video. Se usan dos llamadas separadas a re.findall
# para obtener las listas de IDs y títulos, y luego se itera sobre ambas al mismo tiempo usando enumerate para unir los IDs y títulos

# El título se procesa con la función split para eliminar la parte de fecha y visitas que no se necesita, y se escribe en el archivo CSV
# junto con el ID del video. El archivo CSV resultante tiene dos columnas: "videoId" y "title".


import subprocess
# expresión regular en un objeto de expresión regular, que puede ser usado para las coincidencias usando match(), search() ....
import re
import csv
# Como algo opcional también voy a usar la libreria time por simple capricho, para que el mensaje se imprima automáticamente después de esperar 1 segundo
import time
# No me apetece tener el html generado despues tener el csv, lo voy a borrar
import os


# Pedir al usuario el nombre del canal de YouTube
canal = input("Ingresa el nombre del canal de YouTube (sin '@'): ")

# Descargar el código fuente del canal de YouTube con curl
url = f"https://www.youtube.com/@{canal}"
filename = f"{canal}.html"
subprocess.run(["curl", "-L", url, "-o", filename])


# Leer el archivo HTML y encontrar el nombre del canal
with open(filename, "r", encoding='utf-8') as f_html:
    html_source = f_html.read()
    match = re.search(r'<title>(.*) - YouTube</title>', html_source)
    if match:
        channel_name = match.group(1).strip()
        print(f"El nombre del canal es: {channel_name}")


# Buscar los títulos y URLs de los videos en el código fuente
video_pattern = r'{"gridVideoRenderer":{"videoId":"([^"]+)","thumbnail'
# Antes tenía un problema porque cortaba los titulos de los videos cuando se encontraba un "de", ya que después del titulo sale "de {canal} a fecha xxxx, nº visitas xxxx"
# y todo eso no lo quiero, por lo que he buscado otra manera de que me dé el titulo completo sin que acabe en "de" // AÚN NO FUNCIONA

title_pattern = r'title":{"accessibility":{"accessibilityData":{"label":"([^"]+)"'



# Escribir los datos en un archivo CSV
with open("videos.csv", "w", newline='', encoding='utf-8') as f_html:
    # "quoting=csv.QUOTE_MINIMAL" Sirve para que si aparece más ";" no cuente como separadores
    writer = csv.writer(f_html, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["URLs", "Titulo"])

    with open(filename, "r", encoding='utf-8') as f_html:
        html_source = f_html.read()
        video_matches = re.findall(video_pattern, html_source)
        title_matches = re.findall(title_pattern, html_source)

        for i, match in enumerate(video_matches):
            video_id = match
# Esto es lo que dije antes, todo lo que haya despues de "de" se corta y no entra como titulo
            video_title = title_matches[i].split(' de ')[0]
            video_url = f"https://www.youtube.com/watch?v={video_id}&ab_channel={canal}"
            writer.writerow([video_url, video_title])



# Reemplazo los ";" por " ; "
with open('videos.csv', 'r') as f:
    data = f.read()

data = data.replace(';', ' ; ')

with open('videos_yt.csv', 'w') as f:
    f.write(data)


# Espero 1 seg para mostrar el mensaje
time.sleep(1)


# Lee el archivo CSV y mostrar los resultados en la terminal
# Como algo opcional claro, voy a preguntar si quiero que se muestre o no
show_results = input("¿Quieres ver los resultados en la terminal? (s/n): ")
if show_results.lower() == "s":
    with open("videos_yt.csv", "r", newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            print(row[0], row[1])


time.sleep(1)


# Preguntar si se desea eliminar el archivo HTML
delete_html = input("¿Desea eliminar el archivo HTML? (s/n): ")
if delete_html.lower() == "s":
    os.remove(filename)
    
    


# Elimino el viejo .csv, si lo quitas, pues ver por qué necesito poner " ; " y no ";"
os.remove('videos.csv')

# Espero 1 seg para mostrar el mensaje
time.sleep(1)


print("---------Se han guardado los Titulos y las URL en el archivo videos.csv----------")

