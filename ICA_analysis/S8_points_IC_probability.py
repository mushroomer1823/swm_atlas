import pandas as pd
import numpy as np
import os

def extract_values_from_csv(file_path):
    """
    Load a CSV file and extract numeric values from the first column,
    converting them to a numpy array.
    """
    df = pd.read_csv(file_path, header=None, skiprows=1)  # Read CSV, skip first line
    values_list = df.iloc[:, 0].astype(str).str.split(" ")  # Split strings by space
    array = np.array(values_list.tolist(), dtype=np.float32)  # Convert to float array
    return array

def compute_probabilities(data_array):
    """
    Compute occurrence probabilities of integers 0-70 in the data array.
    """
    flat_data = data_array.flatten()  # Flatten the array
    total_values = len(flat_data)  # Total number of elements

    probabilities = np.zeros(71, dtype=np.float32)  # Array for probabilities of 0-70

    # Count occurrences and calculate probabilities
    for i in range(71):
        probabilities[i] = np.sum(flat_data == i) / total_values

    return probabilities

# Define folder path (hidden by using a generic variable)
csv_folder = "/path/to/csv_folder/"  # Replace with your folder path
csv_files = sorted([f for f in os.listdir(csv_folder) if f.endswith(".csv")])  # List CSV files

all_probabilities = []  # Store probabilities for all files

for csv_file in csv_files:
    file_path = os.path.join(csv_folder, csv_file)
    print(f"Processing file: {os.path.basename(file_path)}")

    data_array = extract_values_from_csv(file_path)  # Load and convert CSV to array
    probabilities = compute_probabilities(data_array)  # Compute probabilities
    all_probabilities.append(probabilities)  # Append result

# Convert list to NumPy array (shape: number_of_files × 71)
probability_matrix = np.array(all_probabilities)

# Save to CSV file (path hidden using generic variable)
output_file = "/path/to/output/category_probability.csv"  # Replace with your output path
df_output = pd.DataFrame(probability_matrix, columns=[f"Value_{i}" for i in range(71)])
df_output.to_csv(output_file, index=False)

print(f"Probability calculation completed. Results saved to {os.path.basename(output_file)}")

