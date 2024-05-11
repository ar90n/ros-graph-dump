import json
from io import StringIO
from operator import itemgetter
from typing import Dict

import pytest

from ros_graph_dump.graph import GraphType
from ros_graph_dump.main import dump_impl


@pytest.mark.parametrize("roslaunch", [("rospy_tutorials", "talker_listener.launch")], indirect=True)
def test_nn_graph(roslaunch):
    def _calc_edge_key(edge: Dict[str, str]) -> str:
        return f"{edge['label']}_{edge['source']}_{edge['target']}"

    expected = {
        "directed": True,
        "multigraph": False,
        "graph": {},
        "nodes": [
            {"label": "/talker", "id": "/talker@node"},
            {"label": "/rosout", "id": "/rosout@node"},
            {"label": "/listener", "id": "/listener@node"},
        ],
        "links": [
            {"label": "/chatter", "source": "/talker@node", "target": "/listener@node"},
            {"label": "/rosout", "source": "/talker@node", "target": "/rosout@node"},
            {"label": "/rosout", "source": "/listener@node", "target": "/rosout@node"},
        ],
    }

    buffer = StringIO()
    dump_impl(None, buffer, GraphType.NODE_TO_NODE)
    actual = json.loads(buffer.getvalue())

    assert expected.keys() == actual.keys()
    assert expected["directed"] == actual["directed"]
    assert expected["multigraph"] == actual["multigraph"]
    assert expected["graph"] == actual["graph"]
    assert sorted(expected["nodes"], key=itemgetter("id")) == sorted(actual["nodes"], key=itemgetter("id"))
    assert sorted(expected["links"], key=_calc_edge_key) == sorted(actual["links"], key=_calc_edge_key)


@pytest.mark.parametrize("roslaunch", [("rospy_tutorials", "talker_listener.launch")], indirect=True)
def test_nt_graph(roslaunch):
    def _calc_edge_key(edge: Dict[str, str]) -> str:
        return f"{edge['source']}_{edge['target']}"

    expected = {
        "directed": True,
        "multigraph": False,
        "graph": {},
        "nodes": [
            {"label": "/chatter", "id": "/chatter@topic", "type": "topic"},
            {"label": "/rosout", "id": "/rosout@topic", "type": "topic"},
            {"label": "/rosout_agg", "id": "/rosout_agg@topic", "type": "topic"},
            {"label": "/talker", "id": "/talker@node", "type": "node"},
            {"label": "/rosout", "id": "/rosout@node", "type": "node"},
            {"label": "/listener", "id": "/listener@node", "type": "node"},
        ],
        "links": [
            {"source": "/chatter@topic", "target": "/listener@node"},
            {"source": "/rosout@node", "target": "/rosout_agg@topic"},
            {"source": "/rosout@topic", "target": "/rosout@node"},
            {"source": "/talker@node", "target": "/chatter@topic"},
            {"source": "/talker@node", "target": "/rosout@topic"},
            {"source": "/listener@node", "target": "/rosout@topic"},
        ],
    }

    buffer = StringIO()
    dump_impl(None, buffer, GraphType.NODE_TO_TOPIC)
    actual = json.loads(buffer.getvalue())

    assert expected.keys() == actual.keys()
    assert expected["directed"] == actual["directed"]
    assert expected["multigraph"] == actual["multigraph"]
    assert expected["graph"] == actual["graph"]
    assert sorted(expected["nodes"], key=itemgetter("id")) == sorted(actual["nodes"], key=itemgetter("id"))
    assert sorted(expected["links"], key=_calc_edge_key) == sorted(actual["links"], key=_calc_edge_key)
