# Knowledge Graph Visualization Application

## Overview

This application visualizes a knowledge graph using D3.js and Bootstrap 5 in a single HTML and a CSS file.

Usable for visualizing an MCP-memory knowledge graph used during Github Copilot or Claude Desktop assisted
development and research work.

Users can interact with nodes and edges through features like:
* Node dragging
* Node pinning
* Zooming and panning
* Tooltips for node details
* Entity type legend

A collapsible left sidebar provides controls for customizing the graph's appearance and behavior.

![A knowledge graph visualization interface showing interconnected nodes and edges in a force-directed layout. The left sidebar contains controls for customizing the graph, and the top navbar displays badges for node count, link count, type count, and placeholder count. The environment is clean and modern, with a focus on usability. Visible text includes labels for nodes, sidebar headings, and navbar badge descriptions.](./screenshot.png)

## Features

### Serving and Files

* Lightweight Python HTTP server
* Graph data in a D3.js-compatible JSON file (hardcoded as `d3_graph.json`)

### Error Handling

* Validates JSON graph data
* User-friendly error messages
* Retry functionality for data loading
* Handles missing or malformed data gracefully
* Substitutes missing nodes with a differently shaped placeholder node with a clean description to mention that it is a placeholder
* Badges on the navbar displaying the node count, links count, types count and the number of placeholders created with affordable color coding

### Performance

* Optimized for large graphs (>500 nodes)
* Auto-hide labels for graphs with >1000 nodes
* Option to force label visibility

### Interactive Features

* Advanced graph force controls with global and per-entity-type settings
* Accordion widgets for managing settings by entity types including visibility control
* Labels on the graph edges with smaller font with option to hide them by the user when not needed
* Formatted tooltip popup upon hover over a node with clear sections and content displayed
* Highlighting connecting edges when hovering over a node

## Usage

1. You need to get the knowledge graph memory into a JSON file. Example script ```read_graph.sh``` is compatible with ```@modelcontextprotocol/server-memory``` reference implementation. It calls the MCP via stdio to use the __read_graph__ tool.
2. Then by ```convert_to_d3.py``` you could create the D3.js compatible graph into ```d3_graph.json```. Use ```--no-validate``` to skip node consistency validation.
3. Finally start the server via ```start.bat``` or ```python -m http.server -b 127.0.0.1 8080``` and 
4. Open __http://127.0.0.1:8080/knowledge_graph.html__ in your browser.

## Contribution

Any contributions are welcome by modifying a fork and opening a PR, just contact me with your ideas and we discuss the further details. Development branches are mandatory, do not commit anyithing into the master branch.
