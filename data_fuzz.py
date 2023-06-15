# Librerias
import requests, json, signal, urllib.parse 
from api_key import api_key
from tabulate import tabulate

#Colores
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'
RESET = '\033[39m'

# Funcion de salida cuando se hace ctrl + c
def ctrl_c(sig, frame):
    print(f"\n\n[{RED}!{RESET}] {RED}SALIENDO...{RESET}\n")
    exit(1)
signal.signal(signal.SIGINT, ctrl_c)

# Variables globales
banner = f"""{CYAN}
██████╗  █████╗ ████████╗ █████╗       ███████╗██╗   ██╗███████╗███████╗
██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗      ██╔════╝██║   ██║╚══███╔╝╚══███╔╝
██║  ██║███████║   ██║   ███████║█████╗█████╗  ██║   ██║  ███╔╝   ███╔╝ 
██║  ██║██╔══██║   ██║   ██╔══██║╚════╝██╔══╝  ██║   ██║ ███╔╝   ███╔╝  
██████╔╝██║  ██║   ██║   ██║  ██║      ██║     ╚██████╔╝███████╗███████╗
╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝      ╚═╝      ╚═════╝ ╚══════╝╚══════╝
                        {MAGENTA}BY: Alcatraz2033{RESET}
"""
url = "https://api.elsevier.com"
table_data = list()

# Variable que asigna el titulo a la tabla
col_names = [f"{GREEN}TITULO{RESET}",f"{GREEN}AUTOR{RESET}",f"{GREEN}ID{RESET}"]

#Funcion que comprueba si haz introducido una api key en epi_key.py
def api_key_cheker():
    if api_key == "":
        print(f"[{RED}!{RESET}] {RED}No se encontro ninguna api_key, introduzca una API KEY en api_key.py{RESET}\n\n")
        exit(1)
        
# Funcion encargada de hacer la peticion, almacenar los datos y mostrarlos por tablas
def process(query):
    # Cabeceras para que el output sea en json
    headers = {
        'Accept' : 'application/json'
    }

    # Peticion Get para obtener los datos
    r = requests.get(url + f"/content/nonserial/title?title={query}&apiKey={api_key}", headers=headers)

    #Lee los datos en json
    data = json.loads(r.text)
    
    # Para controlar errores
    try:
        # Itera por el contenido en json y parsea la informacion de titulo, autor e id, almacenandolas en variables
        for i in data['nonserial-metadata-response']['entry']:
            title =  i['dc:title']
            authors = i['authors']

            # En caso de que no contenga contenido el parametro autor, se le asigna el mensaje No Registrado
            if authors is None:
                authors = "No Registrado"
                
            ids =  i['prism:isbn']

            # Crea una sublista dentro de la lista table_data, esta sublista contendra los datos a precentar en la tabla
            table_data.append([ CYAN + title + RESET, MAGENTA + authors + RESET, RED + ids + RESET])

        # Crea la tabla y la imprime por pantalla
        print(f"\n{tabulate(table_data, headers=col_names, tablefmt='fancy_grid', showindex=True)}")
        
    # En caso de que se presente algun error durante la ejecucion del programa, se precentara el siguiente mensaje
    except:
        print(f"\n[{RED}!{RESET}] {RED}No se encontro ningun resultado o la api proporcionada es incorrecta{RESET}\n")

# Controla el flujo del programa        
if __name__ == '__main__':

    # Instancia de las fucniones
    print(banner)
    api_key_cheker()
    query = input(f"[{CYAN}+{RESET}] {CYAN}Ingrese la query a buscar:{RESET} ")
    urlencode_query = urllib.parse.quote(query)
    process(urlencode_query)
    
