import pandas as pd
import numpy as np

# --- Load adjacency matrices ---
yeo_adj_path = "/path/to/adj_matrix_Yeo.csv"  # Replace with actual path
dkt_adj_path = "/path/to/adj_matrix_DKT.csv"  # Replace with actual path

adj_matrix_Yeo = np.loadtxt(yeo_adj_path, delimiter=",", dtype=int)
adj_matrix_DKT = np.loadtxt(dkt_adj_path, delimiter=",", dtype=int)

# --- Load the main CSV data ---
csv_input_path = "/path/to/selectSWM_twinProb_ifSWM_regions.csv"  # Replace with actual path
df = pd.read_csv(csv_input_path)

# --- Define function to check adjacency in the Yeo matrix ---
def check_adjacency_yeo(node):
    try:
        x, y = map(int, node.split("_"))  # Example format: '3_5'
        return 1 if adj_matrix_Yeo[x-1, y-1] == 1 else 0  # Adjust for 0-based indexing
    except Exception:
        return 0  # Fallback for parsing errors

# --- Apply the Yeo adjacency check ---
df["ifAdj_Yeo"] = df["nodeList"].apply(check_adjacency_yeo)

# --- Define function to check adjacency in the DKT matrix ---
def check_adjacency_dkt(row):
    try:
        x, y = int(row["region1"]), int(row["region2"])
        return 1 if adj_matrix_DKT[x-1, y-1] == 1 else 0
    except Exception:
        return 0

# --- Apply the DKT adjacency check ---
df["ifAdj_DKT"] = df.apply(check_adjacency_dkt, axis=1)

# --- Save the updated DataFrame ---
csv_output_path = "/path/to/selectSWM_twinProb_ifSWM_regions_ifAdj.csv"  # Replace with desired output path
df.to_csv(csv_output_path, index=False)

print("Processing complete. Updated file saved.")

