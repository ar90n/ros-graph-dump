# ROS Graph Dump

A tool to dump the relationship of ROS nodes and ROS topics as JSON Graph Format.

## Features

- Supports ROS1
- Dumps the graph of ROS nodes and topics
- Filters the graph based on node or topic names
- Outputs the graph in JSON format using NetworkX
- Supports two graph types: node-to-node and node-to-topic

## Output
```
$ rgd
{
  "directed": true,
  "multigraph": false,
  "graph": {},
  "nodes": [
    {
      "label": "/talker",
      "id": "/talker@node"
    },
    {
      "label": "/listener",
      "id": "/listener@node"
    },
    {
      "label": "/rosout",
      "id": "/rosout@node"
    }
  ],
  "links": [
    {
      "label": "/chatter",
      "source": "/talker@node",
      "target": "/listener@node"
    },
    {
      "label": "/rosout",
      "source": "/talker@node",
      "target": "/rosout@node"
    },
    {
      "label": "/rosout",
      "source": "/listener@node",
      "target": "/rosout@node"
    }
  ]
}
```

## Requirements

- Python 3.8+
- ROS1
- poetry (for dependency management)

## Installation

1. Clone the repository:
   ```
   $ git clone https://github.com/your-username/ros-graph-dump.git
   ```

2. Navigate to the project directory:
   ```
   $ cd ros-graph-dump
   ```

3. Install rgd and dependencies using pip:
   ```
   $ pip install .
   ```

## Usage

To dump the ROS graph, use the following command:
```
rgd [--filter FILTER] [--output OUTPUT] [--graph-type GRAPH_TYPE]
```

- `--filter FILTER`: Filter the graph based on node or topic names (optional)
- `--output OUTPUT` or `-o OUTPUT`: Output file path. Use "-" for stdout (default).
- `--graph-type GRAPH_TYPE` or `-t GRAPH_TYPE`: Graph type: "nn" (node-to-node) or "nt" (node-to-topic). Default is "nt".

Examples:
```
# Dump the entire graph to stdout
rgd

# Dump the graph to a file
rgd --output graph.json

# Dump the node-to-node graph
rgd -t nn

# Dump the graph with a filter
rgd --filter /my_node
```

## Running Tests
To run the tests, use the following command:
```
poetry run pytest tests
```

## License
This project is licensed under the Apache License 2.0.
