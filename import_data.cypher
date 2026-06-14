// ============================================================
// STEP 1: Create constraints (run this first)
// ============================================================
CREATE CONSTRAINT intersection_id IF NOT EXISTS
FOR (n:Intersection) REQUIRE n.id IS UNIQUE;

// ============================================================
// STEP 2: Load Nodes — paste the file:/// path after copying CSVs
// ============================================================
:auto LOAD CSV WITH HEADERS FROM 'file:///nodes.csv' AS row
CALL {
  WITH row
  MERGE (n:Intersection {id: toInteger(row.id)})
  SET n.x = toFloat(row.x), n.y = toFloat(row.y)
} IN TRANSACTIONS OF 5000 ROWS;

// ============================================================
// STEP 3: Load Edges
// ============================================================
:auto LOAD CSV WITH HEADERS FROM 'file:///edges.csv' AS row
CALL {
  WITH row
  MATCH (a:Intersection {id: toInteger(row.src)})
  MATCH (b:Intersection {id: toInteger(row.dst)})
  MERGE (a)-[:ROAD {distance: toFloat(row.distance)}]->(b)
  MERGE (b)-[:ROAD {distance: toFloat(row.distance)}]->(a)
} IN TRANSACTIONS OF 5000 ROWS;
