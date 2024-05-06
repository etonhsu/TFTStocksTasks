from time import sleep

from pymongo import DESCENDING

from utils.database import connect_user


def rank_update():
    user_collection = connect_user()

    pipeline = [
        {"$addFields": {
            "most_recent_value": {"$arrayElemAt": ["$portfolio_history.value", -1]}
        }},
        {"$sort": {"most_recent_value": DESCENDING}}
    ]

    results = list(user_collection.aggregate(pipeline))

    for rank, user in enumerate(results, start=1):
        user_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {"rank": rank}}
        )


if __name__ == "__main__":
    while True:
        rank_update()
        sleep(300)