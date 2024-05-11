import itertools
from dataclasses import dataclass
from enum import Enum
from json import JSONEncoder
from typing import Dict, Optional, Set, Tuple

import rosgraph
import rosgraph.impl
import rosgraph.impl.graph

Id = str


class GraphType(Enum):
    NODE_TO_NODE = "nn"
    NODE_TO_TOPIC = "nt"


class VertexType(Enum):
    NODE = "node"
    TOPIC = "topic"

    def __str__(self) -> str:
        return str(self.value)


class EnumJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Enum):
            return o.value
        return super().default(o)


def _create_vertex_id(label: str, type: VertexType) -> Id:
    return f"{label}@{str(type)}"


@dataclass(frozen=True)
class Vertex:
    id: Id
    label: str
    type: VertexType

    @staticmethod
    def of(label: str, type: VertexType) -> "Vertex":
        id_ = _create_vertex_id(label, type)
        return Vertex(id=id_, label=label, type=type)


@dataclass(frozen=True)
class Edge:
    source: Vertex
    target: Vertex
    label: Optional[str] = None


@dataclass(frozen=True)
class Graph:
    vertices: Set[Vertex]
    edges: Set[Edge]


def _parse_ros_graph_node_name(node: str) -> Tuple[str, VertexType]:
    if node.startswith(" "):
        return node[1:], VertexType.TOPIC

    return node, VertexType.NODE


def fetch() -> Graph:
    def _extract_vertices(ros_graph: rosgraph.impl.graph.Graph) -> Tuple[Set[Vertex], Dict[str, Vertex]]:
        verticess = set()
        ros_elem_name_to_vertex = {}

        ros_graph_elem_name_iter = itertools.chain(ros_graph.nt_nodes, ros_graph.nn_nodes)
        for i, elem_name in enumerate(ros_graph_elem_name_iter):
            label, t = _parse_ros_graph_node_name(elem_name)
            v = Vertex.of(label=label, type=t)
            verticess.add(v)
            ros_elem_name_to_vertex[elem_name] = v

        return verticess, ros_elem_name_to_vertex

    def _extract_edges(ros_graph: rosgraph.impl.graph.Graph, node_name_to_vertex: Dict[str, Vertex]) -> Set[Edge]:
        edges = set()
        for e in ros_graph.nt_all_edges:
            source = node_name_to_vertex[e.start]
            target = node_name_to_vertex[e.end]
            edges.add(Edge(source=source, target=target))

        return edges

    ros_graph = rosgraph.impl.graph.Graph()
    ros_graph.update()

    verticess, ros_elem_name_to_vertex = _extract_vertices(ros_graph)
    edges = _extract_edges(ros_graph, ros_elem_name_to_vertex)
    return Graph(vertices=verticess, edges=edges)
