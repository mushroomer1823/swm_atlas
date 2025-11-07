import pandas as pd
import numpy as np
from collections import Counter
import glob
import os

def extract_values_from_csv(file_path):
    # Read CSV file skipping the first line (filename)
    df = pd.read_csv(file_path, header=None, skiprows=1)

    # Extract second column (index 0), which contains 30 space-separated values
    values_list = df.iloc[:, 0].astype(str).str.split(" ")

    # Convert to numpy array ensuring correct format
    array = np.array(values_list.tolist(), dtype=np.float32)  # Use np.float64 for higher precision if needed

    return array


def top_5_frequent_values(data_array):
    # Flatten (n,30) array to 1D
    flat_data = data_array.flatten()

    # Count occurrences of all values
    value_counts = Counter(flat_data)

    # Get top 5 most common values
    top_5 = value_counts.most_common(5)

    # Calculate occurrence probabilities
    total_values = len(flat_data)
    probabilities = [item for val, count in top_5 for item in (val, count / total_values)]

    return probabilities

def compute_probabilities(data_array):
    """Compute the top 2 most frequent values for the entire array."""
    flat_data = data_array.flatten()
    value_counts = Counter(flat_data)
    top_2 = value_counts.most_common(2)  # Get top 2 frequent values

    # Pad if fewer than 2 values present
    if len(top_2) < 2:
        top_2.append((None, 0))

    total_values = len(flat_data)
    top_1_value, top_1_count = top_2[0]
    top_2_value, top_2_count = top_2[1]

    return top_1_value, top_1_count / total_values, top_2_value, top_2_count / total_values

def compute_column_probabilities(data_array, top_1_value, top_2_value):
    """Compute per-column proportions belonging to the top 1 and top 2 frequent values."""
    n_rows, n_cols = data_array.shape
    col_1st_prob = []
    col_2nd_prob = []

    for col in range(n_cols):
        col_data = data_array[:, col]
        num_top_1 = np.sum(col_data == top_1_value)
        num_top_2 = np.sum((col_data == top_1_value) | (col_data == top_2_value))

        col_1st_prob.append(num_top_1 / n_rows)  # Proportion of top 1 value in this column
        col_2nd_prob.append(num_top_2 / n_rows)  # Proportion of top 1 or top 2 values in this column

    # Append mean for the 30 columns
    col_1st_prob.append(np.mean(col_1st_prob))
    col_2nd_prob.append(np.mean(col_2nd_prob))

    return col_1st_prob, col_2nd_prob


# Use relative or generic path instead of full local path
data_dir = "/path/to/your/csv_files"
file_list = glob.glob(os.path.join(data_dir, "*.csv"))

results_1st = []
results_2nd = []
results_top_values = []

for file in file_list:
    print("Now processing:", os.path.basename(file))  # Only print the filename, hiding full path
    data_array = extract_values_from_csv(file)
    if np.any(data_array == 70):
        print("Value 70 detected in the array")
     
    print("Data shape:", data_array.shape)  # (n, 30)
    print("First 5 rows preview:", data_array[:5])  # Preview first 5 rows
    
    top_1_value, top_1_prob, top_2_value, top_2_prob = compute_probabilities(data_array)
    results_top_values.append([os.path.basename(file), top_1_value, top_1_prob, top_2_value, top_2_prob])

    # Calculate per-column proportions for top 1 and top 2 values
    col_1st_prob, col_2nd_prob = compute_column_probabilities(data_array, top_1_value, top_2_value)

    # Record results
    results_1st.append([os.path.basename(file)] + col_1st_prob)
    results_2nd.append([os.path.basename(file)] + col_2nd_prob)
    
    

columns = ["File"] + [f"Col_{i+1}" for i in range(30)] + ["Mean"]
columns_top_values = ["File", "Top_1_Value", "Top_1_Prob", "Top_2_Value", "Top_2_Prob"]

df_1st = pd.DataFrame(results_1st, columns=columns)
df_2nd = pd.DataFrame(results_2nd, columns=columns)
df_top_values = pd.DataFrame(results_top_values, columns=columns_top_values)

# Save to files using generic or relative paths (replace with your own target paths)
output_dir = "/path/to/output_dir"  # <--- Replace with your own output directory path or keep generic

df_1st.to_csv(os.path.join(output_dir, "top1_probability.csv"), index=False)
df_2nd.to_csv(os.path.join(output_dir, "top2_probability.csv"), index=False)
df_top_values.to_csv(os.path.join(output_dir, "top_values.csv"), index=False)

print("CSV files generated: top1_probability.csv, top2_probability.csv, top_values.csv")

