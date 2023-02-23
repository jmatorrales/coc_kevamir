import json
import requests

key = 'token_here'


url_member = 'https://api.clashofclans.com/v1/players/%23' # el
url_clan = 'https://api.clashofclans.com/v1/clans/%23'


headers = {
    'Accept': 'application/json',
    'authorization': f'Bearer ${key}'}


def get_user(member):
    # return user profile information
    response = requests.get(url_member + member[1:], headers=headers)
    user = response.json()
    # print(json.dumps(user))
    print('- Lv. Ayuntamiento: %s' % user['townHallLevel'])
    print('- Donaciones hechas: %s' % user['donations'])
    print('- Donaciones recibidas: %s' % user['donationsReceived'])
    print('- Contribución capital clan: ' + str(user['clanCapitalContributions']))


def get_clash():
    # return clash search
    response = requests.get(url_clan + '2Y8LQVG8U', headers=headers)
    data = response.json()
    for member in data['memberList']:
        print('name: %s,' % member['name'], 'id: %s' % member['tag'])
        print('- Rol: %s' % member['role'])
        get_user(member['tag'])
        print('')


get_clash()
