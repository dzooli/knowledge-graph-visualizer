# Knowledge Graph Visualization Application

## Overview

![A knowledge graph visualization interface showing interconnected nodes and edges in a force-directed layout. The left sidebar contains controls for customizing the graph, and the top navbar displays badges for node count, link count, type count, and placeholder count. The environment is clean and modern, with a focus on usability. Visible text includes labels for nodes, sidebar headings, and navbar badge descriptions.](./screenshot.png)

### Goals

This application visualizes a knowledge graph using D3.js and Bootstrap 5 in a single HTML and a CSS file.

Usable for visualizing an MCP/server-memory knowledge graph used during Github Copilot or Claude Desktop assisted
development and research works.

Users can interact with nodes and edges through features like:
* Node dragging
* Node pinning
* Zooming and panning
* Tooltips for node details
* Entity type legend

A collapsible left sidebar provides controls for customizing the graph's appearance and behavior.

## Features

### Serving and Files

* Lightweight Python HTTP server (or any static server)
* The app now fetches `memory.json` and converts it to a D3.js graph client-side via `convert_to_d3.js`

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

1. Obtain the knowledge graph memory as `memory.json`.
  + Example: `read_graph.sh` works with the `@modelcontextprotocol/server-memory` reference server and calls the `read_graph` tool via stdio.
2. Serve the folder with a static server, e.g. on Windows:
  + Use `start.bat` or
  + Python: `python -m http.server -b 127.0.0.1 8080`
3. Open http://127.0.0.1:8080/knowledge_graph.html in your browser.
4. The page will fetch `memory.json`, convert it on-the-fly, validate, insert placeholders for missing referenced nodes, and render the graph.

Notes:
* The previous pre-conversion step (`convert_to_d3.py` → `d3_graph.json`) is no longer required for the page to work.
* The Python script still mirrors the logic and can be used offline or for exporting a static `d3_graph.json` if desired.

### Troubleshooting

* If data fails to load, the app falls back to a built-in sample dataset to remain usable.
* Ensure `memory.json` sits next to `knowledge_graph.html` when served.
* `memory.json` format: it should contain `result.content[].text` where `text` is a JSON string with `{ entities: [...], relations: [...] }`.
* Use a local server to avoid browser CORS/security limitations.

### Client-side converter API (for reference)

* File: `convert_to_d3.js`
* Function: `window.convertMemoryJsonToD3Graph(memoryJson)`
  + Input: the parsed `memory.json` object
  + Output: `{ nodes: [...], links: [...], metadata: {...} }`
  + The main HTML then runs its own validation/normalization and placeholder insertion before rendering.

## Contribution

Any contributions are welcome by modifying a fork and opening a PR, just contact me with your ideas and we discuss the further details. Development branches are mandatory, do not commit anyithing into the master branch.
