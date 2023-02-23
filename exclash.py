import json
import requests
import pandas as pd

# Para obtener headers necesarios para la request a la API
def get_headers():
    with open("token") as f:
        token = f.readlines()[0][:-1]
    return {
        'Accept': 'application/json',
        'authorization': f'Bearer ${token}'}
        
        
# Genera una tabla con la lista de jugadores e info relevante y guarda como excel        
def export_data():
    headers = get_headers()    
    url_clan = 'https://api.clashofclans.com/v1/clans/%23'
    response = requests.get(url_clan + '2Y8LQVG8U', headers=headers)
    data = response.json()
    df = pd.DataFrame(data["memberList"])[["name", "role", "expLevel", "trophies",
                                          "clanRank","donations","donationsReceived"]]
    df.columns = ["Nom", "Rol", "Experiencia", "Copes", "Clan Rank", "Donacions", "Donacions Rebudes"]
    df.to_excel("ranking.xlsx", index=False)


if __name__ == "__main__":
    export_data()
    
