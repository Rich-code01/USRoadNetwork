import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("degrees.csv")

df['degree'].value_counts().sort_index().plot(kind='bar')

plt.title("Degree Distribution")
plt.xlabel("Degree")
plt.ylabel("Number of Intersections")
plt.show()