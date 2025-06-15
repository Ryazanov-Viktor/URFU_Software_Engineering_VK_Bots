from datetime import datetime
import pandas as pd
from app.vk_api import get_user_info, get_friends_ids, extract_id_from_link
from app.graph_utils import make_graph, make_graph_for_user, get_graph_features

PURE_FIELDS = ["has_photo", "sex", "has_mobile", "relation"]
COUNTER_FIELDS = [
    "albums", "audios", "followers", "friends", "pages",
    "photos", "subscriptions", "videos", "clips_followers"
]


def calculate_age(bdate: str):
    bdate_list = bdate.split(".")
    if len(bdate_list) != 3:
        return None
    bday, bmonth, byear = map(int, bdate_list)
    today = datetime.today()
    return today.year - byear - ((today.month, today.day) < (bmonth, bday))


def transform_user_info(user_info):
    transformed = {}
    for field in PURE_FIELDS:
        transformed[field] = user_info.get(field, None)
    for field in COUNTER_FIELDS:
        transformed[field] = user_info.get("counters", {}).get(field, None)
    if "bdate" in user_info:
        transformed["age"] = calculate_age(user_info.get("bdate", ""))
    else:
        transformed["age"] = None
    transformed["city"] = user_info.get("city", {}).get("id")
    transformed["country"] = user_info.get("country", {}).get("id")
    return transformed


def create_df_for_person(uid):
    user_id = extract_id_from_link(uid)
    info = transform_user_info(get_user_info(user_id))
    friends, count = get_friends_ids(user_id)
    info["friends"] = count
    graph = {user_id: friends}
    make_graph(user_id, graph)
    graph_obj = make_graph_for_user(user_id, graph)
    graph_feat = get_graph_features(graph_obj)
    data = {**info, **graph_feat}
    df = pd.DataFrame({k: [v] for k, v in data.items()})
    df.fillna(0, inplace=True)
    return df
