from unittest.mock import MagicMock

from .graph import Edge, Graph, Vertex, VertexType, fetch


def test_empty_graph(mocker):
    mocked_graph_class = mocker.patch("rosgraph.impl.graph.Graph")
    mocked_graph = mocked_graph_class.return_value
    mocked_graph.nt_nodes = []
    mocked_graph.nn_nodes = []
    mocked_graph.nt_all_edges = []

    expected = Graph(vertices=set(), edges=set())
    actual = fetch()
    assert actual == expected


def test_single_edge_graph(mocker):
    mocked_graph_class = mocker.patch("rosgraph.impl.graph.Graph")
    mocked_graph = mocked_graph_class.return_value
    mocked_graph.nt_nodes = [" /topic1"]
    mocked_graph.nn_nodes = ["/node1", "/node2"]
    mocked_graph.nt_all_edges = [MagicMock(start="/node1", end=" /topic1"), MagicMock(start=" /topic1", end="/node2")]

    v_t_1 = Vertex.of(label="/topic1", type=VertexType.TOPIC)
    v_n_1 = Vertex.of(label="/node1", type=VertexType.NODE)
    v_n_2 = Vertex.of(label="/node2", type=VertexType.NODE)

    expected = Graph(
        vertices={v_t_1, v_n_1, v_n_2}, edges={Edge(source=v_n_1, target=v_t_1), Edge(source=v_t_1, target=v_n_2)}
    )
    actual = fetch()
    assert actual == expected


def test_mutual_rel_graph(mocker):
    mocked_graph_class = mocker.patch("rosgraph.impl.graph.Graph")
    mocked_graph = mocked_graph_class.return_value
    mocked_graph.nt_nodes = [" /topic1"]
    mocked_graph.nn_nodes = ["/node1", "/node2"]
    mocked_graph.nt_all_edges = [
        MagicMock(start="/node1", end=" /topic1"),
        MagicMock(start="/node2", end=" /topic1"),
        MagicMock(start=" /topic1", end="/node1"),
        MagicMock(start=" /topic1", end="/node2"),
    ]

    v_t_1 = Vertex.of(label="/topic1", type=VertexType.TOPIC)
    v_n_1 = Vertex.of(label="/node1", type=VertexType.NODE)
    v_n_2 = Vertex.of(label="/node2", type=VertexType.NODE)

    expected = Graph(
        vertices={v_t_1, v_n_1, v_n_2},
        edges={
            Edge(source=v_n_1, target=v_t_1),
            Edge(source=v_t_1, target=v_n_2),
            Edge(source=v_n_2, target=v_t_1),
            Edge(source=v_t_1, target=v_n_1),
        },
    )
    actual = fetch()
    assert actual == expected


def test_bad_edge_graph(mocker):
    mocked_graph_class = mocker.patch("rosgraph.impl.graph.Graph")
    mocked_graph = mocked_graph_class.return_value
    mocked_graph.nt_nodes = [" /topic1"]
    mocked_graph.nn_nodes = ["/node1"]
    mocked_graph.nt_all_edges = [
        MagicMock(start="/node1", end=" /topic1"),
    ]

    v_t_1 = Vertex.of(label="/topic1", type=VertexType.TOPIC)
    v_n_1 = Vertex.of(label="/node1", type=VertexType.NODE)

    expected = Graph(
        vertices={v_t_1, v_n_1},
        edges={
            Edge(source=v_n_1, target=v_t_1),
        },
    )
    actual = fetch()
    assert actual == expected
