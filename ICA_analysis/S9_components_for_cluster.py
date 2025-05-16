import pandas as pd
import numpy as np
from collections import Counter
import glob

def extract_values_from_csv(file_path):
    # Load CSV file, skip the first line (filename)
    df = pd.read_csv(file_path, header=None, skiprows=1)

    # Extract the first column (index 0), which contains 30 space-separated values
    values_list = df.iloc[:, 0].astype(str).str.split(" ")

    # Convert to numpy array, ensure correct data type
    array = np.array(values_list.tolist(), dtype=np.float32)  # You can change to np.float64 for higher precision

    return array

def top_5_frequent_values(data_array):
    # Flatten the (n, 30) array into 1D
    flat_data = data_array.flatten()

    # Count occurrences of all values
    value_counts = Counter(flat_data)

    # Find the top 5 most common values
    top_5 = value_counts.most_common(5)

    # Calculate the occurrence probabilities for each value
    total_values = len(flat_data)
    probabilities = [item for val, count in top_5 for item in (val, count / total_values)]

    return probabilities

def compute_probabilities(data_array):
    """Compute the top 2 most frequent values in the entire array."""
    flat_data = data_array.flatten()
    value_counts = Counter(flat_data)
    top_2 = value_counts.most_common(2)  # Get top 2 values

    # If less than 2 values exist, pad with None
    if len(top_2) < 2:
        top_2.append((None, 0))

    total_values = len(flat_data)
    top_1_value, top_1_count = top_2[0]
    top_2_value, top_2_count = top_2[1]

    return top_1_value, top_1_count / total_values, top_2_value, top_2_count / total_values

def compute_column_probabilities(data_array, top_1_value, top_2_value):
    """Compute the proportion of top 1 and top 2 frequent values in each column."""
    n_rows, n_cols = data_array.shape
    col_1st_prob = []
    col_2nd_prob = []

    for col in range(n_cols):
        col_data = data_array[:, col]
        num_top_1 = np.sum(col_data == top_1_value)
        num_top_2 = np.sum((col_data == top_1_value) | (col_data == top_2_value))

        col_1st_prob.append(num_top_1 / n_rows)  # Proportion of top 1 value in current column
        col_2nd_prob.append(num_top_2 / n_rows)  # Proportion of top 1 and top 2 values in current column

    # Append mean for all 30 columns
    col_1st_prob.append(np.mean(col_1st_prob))
    col_2nd_prob.append(np.mean(col_2nd_prob))

    return col_1st_prob, col_2nd_prob

# Use a generic placeholder path for folder
file_list = glob.glob("/path/to/csv_folder/*.csv")  # Replace with your actual folder path

results_1st = []
results_2nd = []
results_top_values = []

for file in file_list:
    print("Now processing:", file.split("/")[-1])  # Print only the filename
    data_array = extract_values_from_csv(file)
    if np.any(data_array == 70):
        print("Value 70 exists in the array")

    print("Data shape:", data_array.shape)  # e.g. (n, 30)
    print("First 10 rows preview:", data_array[:10])

    top_5_probs = top_5_frequent_values(data_array)
    print(top_5_probs)

    '''
    top_1_value, top_1_prob, top_2_value, top_2_prob = compute_probabilities(data_array)
    results_top_values.append([file, top_1_value, top_1_prob, top_2_value, top_2_prob])

    # Compute per-column proportions for top 1 and top 2 values
    col_1st_prob, col_2nd_prob = compute_column_probabilities(data_array, top_1_value, top_2_value)

    # Store results
    results_1st.append([file] + col_1st_prob)
    results_2nd.append([file] + col_2nd_prob)
    '''
    
'''
columns = ["File"] + [f"Col_{i+1}" for i in range(30)] + ["Mean"]
columns_top_values = ["File", "Top_1_Value", "Top_1_Prob", "Top_2_Value", "Top_2_Prob"]

df_1st = pd.DataFrame(results_1st, columns=columns)
df_2nd = pd.DataFrame(results_2nd, columns=columns)
df_top_values = pd.DataFrame(results_top_values, columns=columns_top_values)

# Save CSVs with generic paths
df_1st.to_csv("/path/to/output/top1_probability.csv", index=False)
df_2nd.to_csv("/path/to/output/top2_probability.csv", index=False)
df_top_values.to_csv("/path/to/output/top_values.csv", index=False)

columns_top_values = ["File", "Top_1_Value", "Top_1_Prob", "Top_2_Value", "Top_2_Prob", "Top_3_Value", "Top_3_Prob", "Top_4_Value", "Top_4_Prob", "Top_5_Value", "Top_5_Prob"]
df_top_values = pd.DataFrame(results_top_values, columns=columns_top_values)
df_top_values.to_csv("/path/to/output/top_5_values_category.csv", index=False)

print("CSV files generated: top1_probability.csv, top2_probability.csv, top_values.csv")
'''

