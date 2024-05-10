from time import sleep

from utils.database import connect_lp, connect_user
from utils.pricing_model import price_model


def portfolio_update():
    user_collection = connect_user()
    lp_collection = connect_lp()
    users = user_collection.find()

    for user in users:
        portfolio = user['portfolio']['players']
        for player_name, player_info in portfolio.items():
            lp_data = lp_collection.find_one({'gameName': player_info['name']})
            if lp_data and 'leaguePoints' in lp_data and lp_data['leaguePoints']:
                # Assuming 'leaguePoints' is a list of prices
                current_price = price_model(lp_data['leaguePoints'][-1])
                portfolio[player_name]['current_price'] = current_price
        user_collection.update_one({'_id': user['_id']}, {'$set': {'portfolio.players': portfolio}})

if __name__ == "__main__":
    while True:
        portfolio_update()
        sleep(120)
