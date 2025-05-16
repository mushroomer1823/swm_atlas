import pandas as pd
from scipy.stats import zscore

# --- Optional pre-processing (commented out) ---
# # Load CSV file
# df0 = pd.read_csv("/path/to/selectSWM_updated.csv")
# df0["twinProb"] = df0["swmProb"] * df0["netProb"]
# df0.to_csv("/path/to/selectSWM_twinProb.csv", index=False)

# Load processed CSV with twinProb
csv_input_path = "/path/to/selectSWM_twinProb.csv"
df = pd.read_csv(csv_input_path)

print("Data shape:", df.shape)

print("Missing values in twinProb:", df["twinProb"].isna().sum())
print("Missing values in swmProb:", df["swmProb"].isna().sum())
print("Missing values in netProb:", df["netProb"].isna().sum())

# Compute Z-scores
df["z_twinProb"] = zscore(df["twinProb"].astype(float))
df["z_swmProb"] = zscore(df["swmProb"].astype(float))
df["z_netProb"] = zscore(df["netProb"].astype(float))

# Classify as SWM if all Z-scores exceed threshold
df["ifSWM"] = ((df["z_twinProb"] > 1.5) &
               (df["z_swmProb"] > 1.5) &
               (df["z_netProb"] > 1.5)).astype(int)

# Save results
csv_output_path = "/path/to/selectSWM_twinProb_ifSWM.csv"
df.to_csv(csv_output_path, index=False)
print("Saved result to:", csv_output_path)

