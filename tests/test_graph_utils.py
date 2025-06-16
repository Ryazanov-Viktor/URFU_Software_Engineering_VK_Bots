import pytest
import networkx as nx
from app.graph_utils import make_graph_for_user, get_graph_features


@pytest.fixture
def sample_uid2friends():
    """
    Фикстура, имитирующая данные о друзьях, полученные из VK API.
    Структура:
    - Пользователь 'user1' дружит с 'friend1', 'friend2', 'friend3'.
    - 'friend1' дружит с 'user1' и 'friend2'.
    - 'friend2' дружит с 'user1' и 'friend1'.
    - 'friend3' дружит только с 'user1' (висячая вершина в эго-графе).
    """
    return {
        'user1': ['friend1', 'friend2', 'friend3'],
        'friend1': ['user1', 'friend2'],
        'friend2': ['user1', 'friend1'],
        'friend3': ['user1']
    }


def test_make_graph_for_user(sample_uid2friends):
    user_id = 'user1'
    graph = make_graph_for_user(user_id, sample_uid2friends)

    # Проверяем, что граф создан
    assert isinstance(graph, nx.Graph)
    # Проверяем наличие всех узлов
    assert set(graph.nodes()) == {'user1', 'friend1', 'friend2', 'friend3'}
    # Проверяем наличие ребер
    # Ребра от 'user1' к его друзьям
    assert graph.has_edge('user1', 'friend1')
    assert graph.has_edge('user1', 'friend2')
    assert graph.has_edge('user1', 'friend3')
    # Ребро между друзьями 'friend1' и 'friend2'
    assert graph.has_edge('friend1', 'friend2')
    # Проверяем отсутствие несуществующих ребер
    assert not graph.has_edge('friend1', 'friend3')


def test_get_graph_features():
    # Создаем простой граф-треугольник
    graph = nx.Graph()
    graph.add_edges_from([(1, 2), (2, 3), (1, 3)])

    features = get_graph_features(graph)

    # Проверяем, что все фичи посчитались и являются числами
    assert isinstance(features, dict)
    for feature_name, value in features.items():
        if feature_name == 'diameter':  # Диаметр может быть None
            assert value is not None
        assert isinstance(value, (int, float))

    # Проверяем конкретные значения для треугольника
    assert features['avg_cl'] == 1.0  # У всех вершин кластеризация 1.0
    assert features['trans'] == 1.0  # Транзитивность для треугольника = 1
    assert nx.is_connected(graph)
    assert features['diameter'] == 1.0
