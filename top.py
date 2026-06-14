import plotly.express as px
import pandas as pd

# Example data (replace with your Neo4j output)
degree_data = {
    "degree": [2, 4, 6, 8, 10, 12],
    "frequency": [2234, 35486, 29941, 119652, 227, 35]
}

df = pd.DataFrame(degree_data)

fig = px.bar(
    df,
    x="degree",
    y="frequency",
    title="Degree Distribution of Road Network"
)

fig.show()