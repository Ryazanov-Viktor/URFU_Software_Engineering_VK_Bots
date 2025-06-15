# tests/test_features.py
from unittest.mock import Mock, patch
from app.features import create_df_for_person

@patch("app.features.get_user_info")
@patch("app.features.get_friends_ids")
@patch("app.features.get_graph_features")
def test_create_df_for_person(mock_graph, mock_friends, mock_user):
    mock_user.return_value = {"id": 1, "has_photo": 1, "sex": 2}
    mock_friends.return_value = ([2, 3], 2)
    mock_graph.return_value = {
        'avg_cl': 0.5,
        'trans': 0.6,
        'average_neighbor_degree': 1.5,
        'average_degree_connectivity': 2,
        'degree_centrality': 0.3,
        'closeness_centrality': 0.4,
        'betweenness_centrality': 0.2,
        'diameter': 2
    }

    df = create_df_for_person("1")
    assert df.shape == (1, 18)  # Проверь точное количество фич!
    assert "has_photo" in df.columns
    assert "avg_cl" in df.columns
