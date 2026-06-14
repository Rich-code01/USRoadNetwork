from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from neo4j import GraphDatabase

# ==========================================
# CONFIGURATION
# ==========================================

URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "Kamana01@"
DATABASE = "usroadnetwork"

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

# ==========================================
# HELPER
# ==========================================

def run_query(query):

    with driver.session(database=DATABASE) as session:

        result = session.run(query)

        return pd.DataFrame(
            [record.data() for record in result]
        )

# ==========================================
# TOTAL INTERSECTIONS
# ==========================================

nodes_query = """
MATCH (n:Intersection)
RETURN count(n) AS total
"""

nodes_df = run_query(nodes_query)

total_intersections = int(
    nodes_df.iloc[0]["total"]
)

# ==========================================
# TOTAL ROADS
# ==========================================

roads_query = """
MATCH ()-[r:ROAD]-()
RETURN count(r) AS roads
"""

roads_df = run_query(roads_query)

total_roads = int(
    roads_df.iloc[0]["roads"]
)

# ==========================================
# DEGREE DISTRIBUTION
# ==========================================

degree_query = """
MATCH (n:Intersection)

WITH n, COUNT {(n)--()} AS degree

RETURN degree,
       count(*) AS frequency

ORDER BY degree
"""

degree_df = run_query(degree_query)

degree_fig = px.bar(
    degree_df,
    x="degree",
    y="frequency",
    title="Degree Distribution"
)

# ==========================================
# TOP 10 CONNECTED INTERSECTIONS
# ==========================================

top10_query = """
MATCH (n:Intersection)

RETURN
n.id AS intersection,
COUNT {(n)--()} AS degree

ORDER BY degree DESC

LIMIT 10
"""

top10_df = run_query(top10_query)

top10_fig = px.bar(
    top10_df,
    x="intersection",
    y="degree",
    title="Top 10 Most Connected Intersections"
)

# ==========================================
# DEGREE CATEGORIES
# ==========================================

category_query = """
MATCH (n:Intersection)

WITH COUNT {(n)--()} AS degree

RETURN

CASE
WHEN degree <= 2 THEN 'Low'
WHEN degree <= 4 THEN 'Medium'
ELSE 'High'
END AS category,

count(*) AS total
"""

category_df = run_query(category_query)

category_fig = px.pie(
    category_df,
    names="category",
    values="total",
    title="Intersection Categories"
)

# ==========================================
# BETWENNESS CENTRALITY
# ==========================================

try:

    centrality_query = """
    CALL gds.betweenness.stream('roadNetwork')
    YIELD nodeId, score

    RETURN
    gds.util.asNode(nodeId).id AS intersection,
    score

    ORDER BY score DESC

    LIMIT 10
    """

    centrality_df = run_query(
        centrality_query
    )

    centrality_fig = px.bar(
        centrality_df,
        x="intersection",
        y="score",
        title="Top 10 Betweenness Centrality Intersections"
    )

except Exception as e:

    print("Betweenness Centrality unavailable")
    print(e)

    centrality_fig = px.bar(
        title="Betweenness Centrality Not Available"
    )

# ==========================================
# DASH APP
# ==========================================

app = Dash(__name__)

app.layout = html.Div([

    html.H1(
        "US Road Network Dashboard",
        style={
            "textAlign": "center"
        }
    ),

    html.Hr(),

    html.Div([

        html.Div([
            html.H3("Total Intersections"),
            html.H1(
                f"{total_intersections:,}"
            )
        ]),

        html.Div([
            html.H3("Total Roads"),
            html.H1(
                f"{total_roads:,}"
            )
        ])

    ],
    style={
        "display": "flex",
        "justifyContent": "space-around",
        "marginBottom": "30px"
    }),

    dcc.Graph(
        figure=degree_fig
    ),

    dcc.Graph(
        figure=top10_fig
    ),

    dcc.Graph(
        figure=category_fig
    ),

    dcc.Graph(
        figure=centrality_fig
    )

])

# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True,
        port=8050
    )