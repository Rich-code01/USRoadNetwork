import csv

input_file = "usa.txt"

# Read all non-empty lines
with open(input_file, "r") as f:
    lines = [line.strip() for line in f if line.strip()]

# First line contains:
# number_of_nodes number_of_edges
first_line = lines[0].split()

num_nodes = int(first_line[0])
num_edges = int(first_line[1])

print("Nodes:", num_nodes)
print("Edges:", num_edges)

# ==========================================
# Extract Nodes
# ==========================================

nodes = []

for i in range(1, num_nodes + 1):
    parts = lines[i].split()

    node_id = int(parts[0])
    x = int(parts[1])
    y = int(parts[2])

    nodes.append([node_id, x, y])

# Save intersections.csv

with open("intersections.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "x", "y"])
    writer.writerows(nodes)

print("intersections.csv created")

# ==========================================
# Extract Roads
# ==========================================

roads = []

edge_start = num_nodes + 1

for i in range(edge_start, len(lines)):
    parts = lines[i].split()

    # Skip anything that is not an edge
    if len(parts) != 2:
        continue

    try:
        source = int(parts[0])
        target = int(parts[1])

        roads.append([source, target])

        # Stop when expected number of edges reached
        if len(roads) == num_edges:
            break

    except ValueError:
        continue

# Save roads.csv

with open("roads.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["source", "target"])
    writer.writerows(roads)

print("roads.csv created")
print("Roads found:", len(roads))

if len(roads) == num_edges:
    print("SUCCESS: Correct number of roads extracted.")
else:
    print(f"WARNING: Expected {num_edges} roads but found {len(roads)}")