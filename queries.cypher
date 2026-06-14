// ============================================================
// TASK 1: Total intersections and roads
// ============================================================
MATCH (n:Intersection)
WITH count(n) AS totalIntersections
MATCH ()-[r:ROAD]->()
WITH totalIntersections, count(r)/2 AS totalRoads
RETURN totalIntersections, totalRoads;


// ============================================================
// TASK 2: Shortest Path between two intersections (Dijkstra)
// First project the graph, then run shortest path
// ============================================================

// 2a. Create GDS graph projection
CALL gds.graph.project(
  'roadGraph',
  'Intersection',
  {
    ROAD: {
      orientation: 'UNDIRECTED',
      properties: 'distance'
    }
  }
);

// 2b. Run Dijkstra shortest path (change sourceNode/targetNode as needed)
MATCH (source:Intersection {id: 0}), (target:Intersection {id: 87574})
CALL gds.shortestPath.dijkstra.stream('roadGraph', {
  sourceNode: source,
  targetNode: target,
  relationshipWeightProperty: 'distance'
})
YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs
RETURN
  index,
  gds.util.asNode(sourceNode).id AS from,
  gds.util.asNode(targetNode).id AS to,
  totalCost,
  [nodeId IN nodeIds | gds.util.asNode(nodeId).id] AS path
ORDER BY index;


// ============================================================
// TASK 3: Intersections with degree > 3
// ============================================================
MATCH (n:Intersection)-[:ROAD]-()
WITH n, count(*) AS degree
WHERE degree > 3
RETURN n.id AS intersection, degree
ORDER BY degree DESC
LIMIT 20;

// Count total with degree > 3
MATCH (n:Intersection)-[:ROAD]-()
WITH n, count(*) AS degree
WHERE degree > 3
RETURN count(n) AS intersectionsWithHighDegree;


// ============================================================
// TASK 4: Betweenness Centrality (top 10)
// ============================================================
CALL gds.betweenness.stream('roadGraph', { samplingSize: 1000, samplingSeed: 42 })
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).id AS intersection, score AS betweennessCentrality
ORDER BY score DESC
LIMIT 10;


// ============================================================
// CLEANUP (run when done to free memory)
// ============================================================
CALL gds.graph.drop('roadGraph');
