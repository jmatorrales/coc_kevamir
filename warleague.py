import json
import requests
import pandas as pd
from exclash import get_headers

# Función para sacar la lista de wartags de cada ronda
def wartags(clanID:str="%232Y8LQVG8U"):
    clanID = clanID.replace("#", "%23")
    return requests.get(
        f"https://api.clashofclans.com/v1/clans/{clanID}/currentwar/leaguegroup",
        headers=get_headers()).json()["rounds"]


# Detecta el número real de rondas que tienen asignado ya un tag
def rondas_conocidas(wtags: list) -> int:
    counter = 0
    for i in range(7):
        if "#0" in wtags[i]["warTags"]:
            return counter
        else:
            counter += 1
    return counter


# Devuelve todos los datos que nos conciernen de cualquier ronda
def datos_ronda(ronda, wtags) -> dict:
    for tag in wtags[ronda]["warTags"]:
        incumbe = nos_incumbe(tag)
        if incumbe:
            return incumbe 
        

# Verifica si en un wartag estaba kevamir como contendiente
def nos_incumbe(wartag:str, nombreClan:str = "Kevamir") -> [dict,bool]:
    wartag = wartag.replace("#","%23")
    war_data = requests.get(
        f"https://api.clashofclans.com/v1/clanwarleagues/wars/{wartag}",
        headers=get_headers()).json()
    if nombreClan in war_data["clan"]["name"]:
        return war_data["clan"]
    elif nombreClan in war_data["opponent"]["name"]:
        return war_data["opponent"]
    else:
        return False
    
        
# A partir de la lista de miembros con los detalles de ataque de una ronda, obtenemos resumen de datos relevantes
def resume_datos_miembros(members_data: dict) -> pd.DataFrame:

    df = pd.DataFrame(members_data["members"])

    def get_attack_data(attack: list, field = "stars"):
        if pd.isna(attack):
            return None
        else:
            return attack[0][field]
    try:
        # Añadimos los campos relativos al ataque, se incluye en bloque try por si hay alguna en preparación
        df["stars"] = df.apply(lambda f: get_attack_data(f["attacks"], "stars"), axis=1)
        df["destructionPercentage"] = df.apply(lambda f: get_attack_data(f["attacks"], "destructionPercentage"), axis=1)
        df["order"] = df.apply(lambda f: get_attack_data(f["attacks"], "order"), axis=1)
        df["duration"] = df.apply(lambda f: get_attack_data(f["attacks"], "duration"), axis=1)
        df["starsSofrides"] = df.apply(lambda f: get_attack_data([f["bestOpponentAttack"]], "stars"), axis=1)
        df["destructionSofrida"] = df.apply(lambda f: get_attack_data([f["bestOpponentAttack"]],
                                                                      "destructionPercentage"), axis=1)
        df["duracioDefensa"] = df.apply(lambda f: get_attack_data([f["bestOpponentAttack"]], "duration"), axis=1)
        df = df[["name", "townhallLevel", "mapPosition", "opponentAttacks", "stars", 
            "destructionPercentage", "order", "duration", "starsSofrides", "destructionSofrida", "duracioDefensa"]]
        df.columns = ["Nom", "THlevel", "Posicio", "Num oponent attacks", "Estrelles", "% Destrucció", "Ordre", 
                           "Duració atac", "Estrelles defensa", "% Destrucció defensa", "Duració defensa" ]
        df = df.sort_values("Estrelles", ascending=False)
    finally:
        return df
    
    
# Exporta a excel 
def exportaDatosMiembrosLiga(clanID: str) -> pd.DataFrame:
    wartags_list: list
    datos_ronda_lista: list
    datos_liga: list
    num_rondas: int
    writer: pd.ExcelWriter
        
    # Información de las rondas
    wartags_list = wartags(clanID)
    num_rondas = rondas_conocidas(wartags_list)
    
    # Generamos las listas con los resúmenes de ataques
    datos_liga = []
    for i in range(num_rondas):
        datos_ronda_lista = datos_ronda(i, wartags_list)
        datos_liga.append(resume_datos_miembros(datos_ronda_lista))
        
    # Finalmente exportamos el excel
    writer = pd.ExcelWriter("DatosLiga.xlsx", engine='xlsxwriter')
    for i in range(num_rondas):
        datos_liga[i].to_excel(writer, sheet_name=f"Ronda {i+1}", index=False)
    writer.close()
    return datos_liga


if __name__ == "__main__":	
	exportaDatosMiembrosLiga("#2Y8LQVG8U")
