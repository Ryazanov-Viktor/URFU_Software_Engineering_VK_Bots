import re
import requests
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()

BASIC_LINK = 'https://api.vk.com/method/'
ACCESS_TOKEN = os.getenv("VK_API_TOKEN")

USER_FIELDS = [
    "has_photo", "sex", "bdate", "city", "country", "has_mobile", "counters"
]


def extract_id_from_link(link: str) -> str:
    match = re.search(r"vk\.com/(id(\d+)|[a-zA-Z0-9_.]+)", link)
    if match:
        if match.group(2):
            return match.group(2)
        return match.group(1)
    return link


def get_user_info(user_id):
    method = 'users.get'
    payload = {
        'user_ids': [user_id],
        'fields': ','.join(USER_FIELDS),
        'v': '5.130',
        'access_token': ACCESS_TOKEN
    }
    response = requests.get(BASIC_LINK + method, params=payload).json()
    if 'response' in response and len(response['response']) > 0:
        return response['response'][0]
    else:
        raise HTTPException(status_code=404, detail="User not found")


def get_friends_ids(user_id, uid2friends=None):
    method = 'friends.get'
    payload = {
        'user_id': user_id,
        'count': 500,
        'offset': 1,
        'order': 'random',
        'v': '5.130',
        'access_token': ACCESS_TOKEN
    }
    response = requests.get(BASIC_LINK + method, params=payload).json()

    if 'response' in response:
        friends = response['response']['items']
        if uid2friends is not None:
            uid2friends[user_id] = friends
        return friends, len(friends)
    else:
        if uid2friends is not None:
            uid2friends[user_id] = []
        return [], 0
