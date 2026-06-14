import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("degree_distribution.csv")

# Sort (important for correct order)
df = df.sort_values(by="degree")

# Plot
plt.figure(figsize=(10,6))
plt.bar(df["degree"].astype(str), df["frequency"])

plt.title("Degree Distribution of Road Network")
plt.xlabel("Degree (Number of Connected Roads)")
plt.ylabel("Number of Intersections")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()