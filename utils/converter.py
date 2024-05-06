import requests
from time import sleep

from utils.get_secret import get_secret

RIOT_API_KEY = get_secret('riot_api_key')

summoner_url = 'https://na1.api.riotgames.com/tft/summoner/v1/summoners/'
puuid_url = 'https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/'


# Converts summonerId -> puuid -> summonerName and stores all 3
def convert(data: list[str]) -> list[dict]:
    BATCH_SIZE = 10  # Process 10 summonerIds per batch, accounting for the two-step process
    REQUESTS_PER_2_MIN = 50  # After 50 summoner IDs, we reach the 100 requests limit
    res = []

    requests_made = 0

    for index, entry in enumerate(data):
        if index % BATCH_SIZE == 0 and index != 0:
            # Sleep for just over 1 second after each batch of 10 to not exceed 20 requests per second
            sleep(1.1)

        if requests_made >= REQUESTS_PER_2_MIN:
            # Sleep for 2 minutes after 100 requests
            sleep(120)
            requests_made = 0  # Reset the counter

        summ_api_url = f'{summoner_url}{entry}?api_key={RIOT_API_KEY}'
        summ_response = requests.get(summ_api_url)
        if summ_response.status_code == 200:
            summ_info = summ_response.json()
            puuid = summ_info.get('puuid')
            requests_made += 1  # Increment the request counter

            if puuid:
                puuid_api_url = f'{puuid_url}{puuid}?api_key={RIOT_API_KEY}'
                puuid_response = requests.get(puuid_api_url)
                if puuid_response.status_code == 200:
                    puuid_info = puuid_response.json()
                    gameName = puuid_info.get('gameName')
                    temp = {'gameName': gameName, 'puuid': puuid, 'summonerId': entry}
                    res.append(temp)
                    requests_made += 1  # Increment the request counter

        # Additional pause to ensure we don't hit the rate limit
        if (index + 1) % BATCH_SIZE == 0:
            sleep(1)

    return res

