from datetime import datetime
from time import sleep

from utils.database import connect_user
from utils.pricing_model import price_model


def update_portfolio_history():
    user_collection = connect_user()
    users = user_collection.find()
    for user in users:
        portfolio = 0
        for player in user['portfolio']['players']:
            price = price_model(user['portfolio']['players'][player]['current_price'])
            shares = user['portfolio']['players'][player]['shares']
            value = price * shares
            portfolio += value
        total = portfolio + user['balance']

        # Retrieve the last portfolio history entry
        last_entry = user.get('portfolio_history', [])[-1] if user.get('portfolio_history') else None

        # Check if there is a last entry and if the total value has changed
        if not last_entry or last_entry['value'] != total:
            # Only update if there's no last entry or if the total value has changed
            user_collection.update_one(
                {'_id': user['_id']},
                {'$push': {
                    'portfolio_history': {
                        'value': total,
                        'date': datetime.now()
                    }
                }}
            )
            print(f'Updated {user["_id"]} portfolio')


if __name__ == "__main__":
    while True:
        update_portfolio_history()
        sleep(300)