from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "Kamana01@")
)

with driver.session(database="usroadnetwork") as session:

    result = session.run("""
        MATCH (n:Intersection)
        RETURN count(n) AS total
    """)

    print(result.single()["total"])