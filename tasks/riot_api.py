from datetime import datetime
from time import sleep

import requests

from utils.database import connect_lp, connect_player_Id
from utils.converter import convert
from utils.get_secret import get_secret

RIOT_API_KEY = get_secret('riot_api_key')


def riot_api():
    # Two databases use
    point_collection = connect_lp()
    Id_collection = connect_player_Id()

    # All the Riot API calls
    chall_url = f'https://na1.api.riotgames.com/tft/league/v1/challenger?queue=RANKED_TFT&api_key={RIOT_API_KEY}'
    gm_url = f'https://na1.api.riotgames.com/tft/league/v1/grandmaster?queue=RANKED_TFT&api_key={RIOT_API_KEY}'
    master_url = f'https://na1.api.riotgames.com/tft/league/v1/master?queue=RANKED_TFT&api_key={RIOT_API_KEY}'

    chall_resp = requests.get(chall_url)
    gm_resp = requests.get(gm_url)
    master_resp = requests.get(master_url)

    chall_info = chall_resp.json()
    gm_info = gm_resp.json()
    master_info = master_resp.json()

    # Extract relevant data
    chall_data = [{'summonerId': d['summonerId'], 'leaguePoints': d['leaguePoints']} for d in chall_info['entries']]
    gm_data = [{'summonerId': d['summonerId'], 'leaguePoints': d['leaguePoints']} for d in gm_info['entries']]
    master_data = [{'summonerId': d['summonerId'], 'leaguePoints': d['leaguePoints']} for d in master_info['entries']]
    combined_data = chall_data + gm_data + master_data

    summonerIds = [data['summonerId'] for data in combined_data]
    entries = Id_collection.find({'summonerId': {'$in': summonerIds}})
    entries_dict = {entry['summonerId']: entry for entry in entries}

    need_conversion = []
    cur = str(datetime.now())
    for data in combined_data:
        leaguePoints = data['leaguePoints']
        entry = entries_dict.get(data['summonerId'])

        if entry:
            gameName = entry.get('gameName')
            if gameName:
                # Retrieve the last leaguePoints entry
                points_entry = point_collection.find_one({'summonerId': data['summonerId']})
                last_points = points_entry['leaguePoints'][-1] if points_entry and 'leaguePoints' in points_entry else None

                # Only update if last leaguePoints is different from new leaguePoints
                if not last_points or last_points != leaguePoints:
                    update_operation = {
                        '$push': {
                            'leaguePoints': leaguePoints,
                            'date': cur
                        },
                        '$set': {
                            'gameName': gameName,
                            'summonerId': data['summonerId'],
                        }
                    }
                    point_collection.update_one({'summonerId': data['summonerId']}, update_operation, upsert=True)

        else:
            print(f"No entry found for summonerId: {data['summonerId']}")
            need_conversion.append(data['summonerId'])

    # Convert and insert new entries as necessary
    if need_conversion:
        converted = convert(need_conversion)
        Id_collection.insert_many(converted)


if __name__ == "__main__":
    riot_api()
    sleep(300)