#!/usr/bin/env python3
"""
Knowledge Graph to D3.js Converter

This script converts a knowledge graph JSON file with entities and relations
into a D3.js-compatible graph object format.

Author: Generated for gpxmapper project
Date: 2025-01-14
"""

import re
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Set
from collections import defaultdict


# Sanitize the filename: remove path separators and allow only safe chars
def simple_secure_filename(filename):
    filename = re.sub(r"[\\/]", "", filename)  # Remove slashes
    filename = re.sub(r"[^A-Za-z0-9_.-]", "_", filename)  # Replace unsafe chars
    return filename or "output.json"


def load_knowledge_graph(json_file_path: str) -> Dict[str, Any]:
    """
    Load and validate the knowledge graph JSON file.

    Args:
        json_file_path: Path to the knowledge graph JSON file

    Returns:
        Parsed JSON data as dictionary

    Raises:
        FileNotFoundError: If the input file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    file_path = Path(json_file_path).resolve()
    allowed_dir = Path(__file__).parent.resolve()
    if not str(file_path).startswith(str(allowed_dir)):
        raise ValueError(
            f"Access to file outside allowed directory is not permitted: {json_file_path}"
        )

    if not file_path.exists():
        raise FileNotFoundError(f"Knowledge graph file not found: {json_file_path}")

    # Try different encodings to handle various file formats
    encodings = ["utf-8-sig", "utf-8", "utf-16", "cp1252"]

    for encoding in encodings:
        try:
            # Sanitize the filename to prevent path traversal
            safe_filename = simple_secure_filename(file_path.name)
            safe_path = allowed_dir / safe_filename
            if not str(safe_path.resolve()).startswith(str(allowed_dir)):
                raise ValueError(f"Path traversal detected: {safe_path}")
            with open(safe_path, "r", encoding=encoding) as file:
                return json.load(file)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            print(str(exc))
            continue

    # If all encodings fail, raise an error
    raise ValueError(
        f"Unable to decode file {json_file_path} with any supported encoding"
    )


def extract_nodes(
    entities: List[Dict[str, Any]], existing_groups: Set[str]
) -> List[Dict[str, Any]]:
    """
    Convert entities to D3.js nodes format.

    Args:
        entities: List of entity dictionaries from knowledge graph

    Returns:
        List of D3.js compatible node objects
    """
    nodes = []

    for entity in entities:
        if entity.get("type") != "entity":
            continue

        node = {
            "id": entity["name"],
            "type": entity.get("entityType", "Unknown"),
            "observations": entity.get("observations", []),
            "group": _get_group_index(
                entity.get("entityType", "Unknown"), existing_groups
            ),
        }
        nodes.append(node)

    return nodes


def extract_links(
    relations: List[Dict[str, Any]], relation_types: Dict[str, int]
) -> List[Dict[str, Any]]:
    """
    Convert relations to D3.js links format.

    Args:
        relations: List of relation dictionaries from knowledge graph

    Returns:
        List of D3.js compatible link objects
    """
    links = []

    for relation in relations:
        if relation.get("type") != "relation":
            continue

        link = {
            "source": relation["from"],
            "target": relation["to"],
            "type": relation["relationType"],
            "value": _get_relation_strength(relation["relationType"], relation_types),
        }
        links.append(link)

    return links


def validate_graph_integrity(nodes: List[Dict], links: List[Dict]) -> bool:
    """
    Validate that all links reference existing nodes.

    Args:
        nodes: List of node objects
        links: List of link objects

    Returns:
        True if graph is valid, False otherwise
    """
    node_ids = {node["id"] for node in nodes}
    missing_nodes = set()

    for link in links:
        if link["source"] not in node_ids:
            print(f"Warning: Link source '{link['source']}' not found in nodes")
            missing_nodes.add(link["source"])
        if link["target"] not in node_ids:
            print(f"Warning: Link target '{link['target']}' not found in nodes")
            missing_nodes.add(link["target"])

    if missing_nodes:
        print(f"Found {len(missing_nodes)} missing nodes: {missing_nodes}")
        print(
            "Consider adding these as entities or use --no-validate to skip validation"
        )
        return False

    return True


def extract_relation_types(relations: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Extract relation types from the knowledge graph.

    Args:
        relations: List of relation dictionaries from knowledge graph

    Returns:
        Dictionary mapping relation types to lists of relation objects
    """
    relation_types = defaultdict(list)

    for i, relation in enumerate(relations):
        rel_type = relation.get("relationType", "Unknown")
        relation_types.update({rel_type: relation_types.get(rel_type, 0) + 1})
    return relation_types


def _get_relation_strength(relation_type: str, relation_types: Dict[str, int]) -> int:
    """
    Get the strength of a link based on its relation type.

    Args:
        relation_type: The type of the relation

    Returns:
        Strength value for the link
    """
    return relation_types.get(relation_type, 0)


def extract_groups(entities: List[Dict[str, Any]]) -> List[str]:
    """
    Extract entity types from the knowledge graph.

    Args:
        entities: List of entity dictionaries from knowledge graph

    Returns:
        Dictionary mapping group numbers to lists of entity types
    """
    groups = set()
    for i, entity in enumerate(entities):
        group = entity.get("entityType", "Unknown")
        groups.add(group)
    return sorted(list(groups))


def _get_group_index(entity_type: str, groups: Set[str]) -> int:
    """
    Get the group index for a given entity type.

    Args:
        entity_type: The type of the entity

    Returns:
        Group index as an integer
    """
    if entity_type in groups:
        return list(groups).index(entity_type)
    return 0


def convert_to_d3(input_file: str, output_file: str, validate: bool = True) -> None:
    """
    Convert knowledge graph JSON to D3.js compatible format.

    Args:
        input_file: Path to the input knowledge graph JSON file
        output_file: Path to the output D3.js JSON file
        validate: Whether to validate graph integrity

    Raises:
        ValueError: If the knowledge graph structure is invalid
    """
    try:
        # Load the knowledge graph
        data = load_knowledge_graph(input_file)

        # Validate required structure
        content = json.loads(data["result"]["content"][0]["text"])
        if "entities" not in content:
            raise ValueError("Knowledge graph must contain 'entities' array")
        if "relations" not in content:
            raise ValueError("Knowledge graph must contain 'relations' array")

        # Extract nodes and links
        groups = extract_groups(content["entities"])
        relation_types = extract_relation_types(content["relations"])
        nodes = extract_nodes(content["entities"], groups)
        links = extract_links(content["relations"], relation_types)

        # Clean up
        del content
        del data

        # Validate graph integrity if requested
        if validate and not validate_graph_integrity(nodes, links):
            raise ValueError("Graph integrity validation failed")

        # Create D3.js compatible graph object
        d3_graph = {
            "nodes": nodes,
            "links": links,
            "metadata": {
                "nodeCount": len(nodes),
                "linkCount": len(links),
                "entityTypes": list(set(node["type"] for node in nodes)),
                "relationTypes": list(set(link["type"] for link in links)),
                "generatedAt": "2025-01-14",
                "source": input_file,
            },
        }

        # Write the D3.js graph to output file
        allowed_dir = Path(__file__).parent.resolve()

        safe_filename = simple_secure_filename(Path(output_file).name)
        output_path = allowed_dir / safe_filename
        # Ensure output_path is within allowed_dir (prevent path traversal)
        if not str(output_path.resolve()).startswith(str(allowed_dir)):
            raise ValueError("Output file path traversal detected.")
        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(d3_graph, file, indent=2, ensure_ascii=False)

        print("✓ Successfully converted knowledge graph to D3.js format")
        print(f"  Input:  {input_file}")
        print(f"  Output: {output_path}")
        print(f"  Nodes:  {len(nodes)}")
        print(f"  Links:  {len(links)}")

    except Exception as e:
        print(f"✗ Error converting knowledge graph: {e}")
        sys.exit(1)


def main():
    """Main entry point for the script."""
    if len(sys.argv) < 2:
        print(
            "Usage: python convert_to_d3.py <input_file> [output_file] [--no-validate]"
        )
        print("Example: python convert_to_d3.py knowledge_graph.json d3_graph.json")
        print(
            "         python convert_to_d3.py knowledge_graph.json d3_graph.json --no-validate"
        )
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = (
        sys.argv[2]
        if len(sys.argv) > 2 and not sys.argv[2].startswith("--")
        else "d3_graph.json"
    )

    # Check for --no-validate flag
    validate = "--no-validate" not in sys.argv

    convert_to_d3(input_file, output_file, validate)


if __name__ == "__main__":
    main()
