import itertools
import json
import sys
from typing import Optional, TextIO

import networkx as nx
import typer

from .graph import Edge, EnumJSONEncoder, Graph, GraphType, VertexType, fetch as fetch_graph

app = typer.Typer()


def filter_graph(graph: Graph, filter_pattern: str) -> Graph:
    filtered_vertices = {v for v in graph.vertices if v.label.startswith(filter_pattern)}
    filtered_edges = {e for e in graph.edges if e.source in filtered_vertices and e.target in filtered_vertices}
    return Graph(vertices=filtered_vertices, edges=filtered_edges)


def create_node_to_node_graph(graph: Graph) -> nx.DiGraph:
    def _is_node_to_node_path(pub_edge: Edge, sub_edge: Edge) -> bool:
        return pub_edge.target == sub_edge.source and pub_edge.target.type == VertexType.TOPIC

    G = nx.DiGraph()

    for vertex in graph.vertices:
        if vertex.type == VertexType.NODE:
            G.add_node(vertex.id, label=vertex.label)

    for pub_edge, sub_edge in itertools.product(graph.edges, graph.edges):
        if not _is_node_to_node_path(pub_edge, sub_edge):
            continue

        G.add_edge(pub_edge.source.id, sub_edge.target.id, label=pub_edge.target.label)
    return G


def create_node_to_topic_graph(graph: Graph) -> nx.DiGraph:
    G = nx.DiGraph()
    for vertex in graph.vertices:
        G.add_node(vertex.id, type=vertex.type, label=vertex.label)
    for edge in graph.edges:
        G.add_edge(edge.source.id, edge.target.id)

    return G


def create_target_graph(graph: Graph, graph_type: GraphType) -> nx.DiGraph:
    if graph_type == GraphType.NODE_TO_NODE:
        return create_node_to_node_graph(graph)
    elif graph_type == GraphType.NODE_TO_TOPIC:
        return create_node_to_topic_graph(graph)

    typer.echo(f'Invalid graph type: {graph_type}. Supported types: "nn" (node-to-node) or "nt" (node-to-topic)')
    raise typer.Exit(1)


@app.command()
def dump(
    filter: Optional[str] = typer.Option(None, "--filter", "-f", help="Filter nodes by name."),
    output: str = typer.Option("-", "--output", "-o", help='Output file path. Use "-" for stdout (default).'),
    graph_type: GraphType = typer.Option(
        GraphType.NODE_TO_NODE.value,
        "--graph-type",
        "-t",
        help='Graph type: "nn" (node-to-node) or "nt" (node-to-topic)',
    ),
):
    if output == "-":
        dump_impl(filter, sys.stdout, graph_type)
    else:
        with open(output, "w") as file:
            dump_impl(filter, file, graph_type)
        typer.echo(f"Graph saved as {output}")


def dump_impl(filter: Optional[str], output: TextIO, graph_type: GraphType):
    graph = fetch_graph()
    if filter:
        graph = filter_graph(graph, filter)

    G = create_target_graph(graph, graph_type)

    data = nx.node_link_data(G)
    json.dump(data, output, indent=2, cls=EnumJSONEncoder)


if __name__ == "__main__":
    app()
