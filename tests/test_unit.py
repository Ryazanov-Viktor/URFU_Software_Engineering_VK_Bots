# tests/test_unit.py
import pytest
import networkx as nx
from app.graph_utils import get_graph_features, LIST_OF_FEATURES


def test_get_graph_features():
    # Создаём простой граф 1 - 2 - 3
    graph = nx.Graph()
    graph.add_edges_from([(1, 2), (2, 3), (1, 3)])  # треугольник

    features = get_graph_features(graph)

    # Проверяем, что результат — словарь
    assert isinstance(features, dict)

    # Проверяем наличие всех ключей
    for feature in LIST_OF_FEATURES:
        assert feature in features

    # Проверяем конкретные значения для треугольника
    assert features['avg_cl'] == 1.0  # clustering coefficient у треугольника = 1
    assert features['trans'] == 1.0   # transitivity тоже 1
    assert features['average_neighbor_degree'] is not None
    assert features['average_degree_connectivity'] is not None
    assert features['degree_centrality'] is not None
    assert features['closeness_centrality'] is not None
    assert features['betweenness_centrality'] is not None
    assert features['diameter'] == 1  # расстояние между любыми двумя узлами равно 1
