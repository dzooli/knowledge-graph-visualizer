/*
  In-browser converter for memory.json -> D3 graph
  Exposes: window.convertMemoryJsonToD3Graph(memoryJson)
  - Accepts the raw JSON loaded from memory.json (same structure as used by convert_to_d3.py)
  - Returns a lightweight graph object: { nodes: [...], links: [...], metadata: {...} }
  - Leaves further normalization and placeholder insertion to the app's existing logic
*/
(function(){
  'use strict';

  function safeParseEmbeddedContent(memoryJson) {
    // memory.json structure: { result: { content: [ { type: 'text', text: '{\n  "entities": ... }' } ] } }
    try {
      const textBlocks = (((memoryJson||{}).result||{}).content||[]).filter(x => x && typeof x.text === 'string');
      if (!textBlocks.length) throw new Error('No content.text blocks');
      // Prefer first block that looks like an object with entities/relations
      for (const blk of textBlocks) {
        try {
          const obj = JSON.parse(blk.text);
          if (obj && (Array.isArray(obj.entities) || Array.isArray(obj.relations))) return obj;
        } catch (_) { /* keep scanning */ }
      }
      // Fallback: parse first block
      return JSON.parse(textBlocks[0].text);
    } catch (e) {
      throw new Error('Invalid memory.json structure: ' + (e && e.message || e));
    }
  }

  function extractGroups(entities) {
    const groups = new Set();
    for (const ent of entities) {
      if (ent && ent.type === 'entity') {
        groups.add(ent.entityType || 'Unknown');
      }
    }
    return Array.from(groups);
  }

  function getGroupIndex(entityType, groups) {
    const idx = groups.indexOf(entityType);
    return idx >= 0 ? idx : 0;
  }

  function extractNodes(entities, groups) {
    const out = [];
    for (const ent of entities) {
      if (!ent || ent.type !== 'entity') continue;
      out.push({
        id: ent.name,
        type: ent.entityType || 'Unknown',
        observations: Array.isArray(ent.observations) ? ent.observations : [],
        group: getGroupIndex(ent.entityType || 'Unknown', groups)
      });
    }
    return out;
  }

  function extractRelationTypes(relations) {
    const map = new Map();
    for (const rel of relations) {
      if (!rel || rel.type !== 'relation') continue;
      const k = rel.relationType || 'Unknown';
      map.set(k, (map.get(k) || 0) + 1);
    }
    return map;
  }

  function getRelationStrength(k, relTypes) {
    return relTypes.get(k) || 0;
  }

  function extractLinks(relations, relTypes) {
    const out = [];
    for (const rel of relations) {
      if (!rel || rel.type !== 'relation') continue;
      out.push({
        source: rel.from,
        target: rel.to,
        type: rel.relationType,
        value: getRelationStrength(rel.relationType, relTypes)
      });
    }
    return out;
  }

  function convertMemoryJsonToD3Graph(memoryJson) {
    const inner = safeParseEmbeddedContent(memoryJson);
    if (!inner || typeof inner !== 'object') throw new Error('Parsed content is not an object');
    if (!Array.isArray(inner.entities)) throw new Error("Knowledge graph must contain 'entities' array");
    if (!Array.isArray(inner.relations)) throw new Error("Knowledge graph must contain 'relations' array");

    const groups = extractGroups(inner.entities);
    const relTypes = extractRelationTypes(inner.relations);
    const nodes = extractNodes(inner.entities, groups);
    const links = extractLinks(inner.relations, relTypes);

    return {
      nodes,
      links,
      metadata: {
        nodeCount: nodes.length,
        linkCount: links.length,
        entityTypes: Array.from(new Set(nodes.map(n => n.type))),
        relationTypes: Array.from(new Set(links.map(l => l.type))),
        generatedAt: new Date().toISOString(),
        source: 'memory.json (client-side)'
      }
    };
  }

  // expose globally
  window.convertMemoryJsonToD3Graph = convertMemoryJsonToD3Graph;
})();
