import networkx as nx
from statistics import mean, StatisticsError
from time import sleep
from app.vk_api import get_friends_ids

LIST_OF_FEATURES = [
    'avg_cl', 'trans', 'average_neighbor_degree', 'average_degree_connectivity',
    'degree_centrality', 'closeness_centrality', 'betweenness_centrality', 'diameter'
]


def make_graph(user_id, uid2friends):
    get_friends_ids(user_id, uid2friends)
    sleep(0.3)
    for friend in uid2friends[user_id]:
        if friend not in uid2friends:
            get_friends_ids(friend, uid2friends)
            sleep(0.3)


def make_graph_for_user(user_id, uid2friends):
    graph = nx.Graph()
    graph.add_node(user_id)
    friends = set(uid2friends[user_id])
    for friend in friends:
        graph.add_edge(user_id, friend)
        second_gen = uid2friends.get(friend, [])
        for friend2 in second_gen:
            if friend2 in friends:
                graph.add_edge(friend, friend2)
    return graph


def get_graph_features(graph):
    avg_cl = nx.average_clustering(graph)
    trans = nx.transitivity(graph)
    try:
        avg_neighbor = mean(nx.average_neighbor_degree(graph).values())
    except StatisticsError:
        avg_neighbor = None
    try:
        avg_degree_conn = mean(nx.average_degree_connectivity(graph).values())
    except StatisticsError:
        avg_degree_conn = None
    deg_cent = mean(nx.degree_centrality(graph).values())
    close_cent = mean(nx.closeness_centrality(graph).values())
    btw_cent = mean(nx.betweenness_centrality(graph).values())
    diameter = nx.diameter(graph) if nx.is_connected(graph) else None

    values = [
        avg_cl, trans, avg_neighbor, avg_degree_conn,
        deg_cent, close_cent, btw_cent, diameter
    ]
    return dict(zip(LIST_OF_FEATURES, values))
