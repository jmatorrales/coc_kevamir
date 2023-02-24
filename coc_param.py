import requests
import pandas as pd
import datetime

_url_member = 'https://api.clashofclans.com/v1/players/%23'
_url_clan = 'https://api.clashofclans.com/v1/clans/%23'

# Función para obtener los encabezados necesarios para realizar una solicitud HTTP que requiere autenticación.
# Lee el token de un archivo llamado "token", y lo utiliza en el encabezado de autorización en formato de portador.
# Devuelve un diccionario que contiene dos claves, 'Accept' y 'authorization'.
def get_headers():
    with open('token', "r") as f:
        token = f.read().strip()
    return {
        'Accept': 'application/json',
        'authorization': f'Bearer {token}'
    }


def get_clash():
    # Obtiene los encabezados necesarios para realizar la solicitud HTTP
    headers = get_headers()
    # Realiza la solicitud HTTP para obtener la información del clan
    response = requests.get(_url_clan + '2Y8LQVG8U', headers=headers)
    # Obtiene los datos de la respuesta en formato JSON
    data = response.json()

    # Convierte los datos del miembro del clan en un DataFrame de Pandas
    df = pd.DataFrame(data['memberList'],
                      columns=['name', 'role', 'expLevel', 'trophies', 'clanRank', 'donations', 'donationsReceived'])

    # Renombra las columnas del DataFrame para que sean más legibles
    df = df.rename(columns={'name': 'Nombre', 'role': 'Rol', 'expLevel': 'Nivel de experiencia', 'trophies': 'Copa',
                            'clanRank': 'Rango en el clan', 'donations': 'Donaciones',
                            'donationsReceived': 'Donaciones recibidas'})

    # Crea un nombre de archivo predeterminado basado en la fecha y hora actual
    nombre_archivo_predeterminado = datetime.datetime.now().strftime("ranking_%Y-%m-%d_%H-%M-%S.xlsx")

    # Solicita la ruta y el nombre del archivo al usuario, con el nombre de archivo predeterminado como valor por
    # defecto
    ruta_archivo = input(
        f"Ingrese la ruta y el nombre del archivo de Excel (o presione Enter para usar el nombre predeterminado '"
        f"{nombre_archivo_predeterminado}'): ") or nombre_archivo_predeterminado

    # Guarda el DataFrame en el archivo de Excel utilizando la ruta y el nombre ingresados por el usuario
    df.to_excel(ruta_archivo, index=False)


get_clash()
