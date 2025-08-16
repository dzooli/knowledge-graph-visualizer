# Knowledge Graph Visualization Application

## Overview

This application visualizes a knowledge graph using D3.js and Bootstrap 5 in a single HTML and a CSS file.

Usable for visualizing an MCP-memory knowledge graph used during Github Copilot or Claude Desktop assisted
development work.

Users can interact with nodes and edges through features like:
- Node dragging
- Zooming and panning
- Tooltips for node details
- Entity type legend

A collapsible left sidebar provides controls for customizing the graph's appearance and behavior.

## Features

### Serving and Files
- Lightweight Python HTTP server
- Graph data in a D3.js-compatible JSON file (hardcoded as `d3_graph.json`)

### Error Handling
- Validates JSON graph data
- User-friendly error messages
- Retry functionality for data loading
- Handles missing or malformed data gracefully
- Substitutes missing nodes with a differently shaped placeholder node with a clean description to mention that it is a placeholder
- Badges on the navbar displaying the node count, links count, types count and the number of placeholders created with affordable color coding

### Performance
- Optimized for large graphs (>500 nodes)
- Auto-hide labels for graphs with >1000 nodes
- Option to force label visibility

### Interactive Features
- Advanced graph force controls with global and per-entity-type settings
- Accordion widgets for managing settings by entity types including visibility control
- Labels on the graph edges with smaller font with option to hide them by the user when not needed
- Formatted tooltip popup upon hover over a node with clear sections and content displayed
- Highlighting connecting edges when hovering over a node

### Robust Lifecycle
- Proper initialization and error recovery mechanisms

