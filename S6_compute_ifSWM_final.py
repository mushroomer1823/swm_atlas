import pandas as pd
import numpy as np

# --- Load data file (already includes SWM probability and adjacency checks) ---
input_path = "/path/to/selectSWM_twinProb_ifSWM_regions_ifAdj.csv"  # Replace with actual path
df = pd.read_csv(input_path)

# --- Final filtering: mark fibers that are high-probability SWM and between adjacent regions ---
df["ifSWM_final"] = df["ifSWM"] * df["ifAdj_Yeo"] * df["ifAdj_DKT"]

# --- Save the final result ---
output_path = "/path/to/selectSWM_ifSWM_regions_final.csv"  # Replace with desired output path
df.to_csv(output_path, index=False)

print("Processing complete. Final file saved.")

