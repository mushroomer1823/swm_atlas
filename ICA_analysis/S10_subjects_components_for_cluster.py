import pandas as pd
import numpy as np
from collections import Counter, defaultdict
import glob
import os
from concurrent.futures import ProcessPoolExecutor, as_completed

def extract_values_from_csv(file_path):
    try:
        # Read CSV file, skip the first line (filename)
        df = pd.read_csv(file_path, header=None, skiprows=1)
        # Extract first column (index 0) which contains 30 space-separated values
        values_list = df.iloc[:, 0].astype(str).str.split(" ")

        # Convert to numpy array with correct data type
        array = np.array(values_list.tolist(), dtype=np.float32)
        return array

    except pd.errors.EmptyDataError:
        print(f"Warning: File {os.path.basename(file_path)} is empty, skipping...")
        return None  # Return None if file is empty

    except Exception as e:
        print(f"Error reading file {os.path.basename(file_path)}: {e}")
        return None  # Return None on other errors

def top_5_frequent_values(data_array):
    # Flatten (n, 30) array into 1D
    flat_data = data_array.flatten()

    # Count occurrences of all values
    value_counts = Counter(flat_data)

    # Get top 5 most common values
    top_5 = value_counts.most_common(5)

    # Calculate occurrence probabilities
    total_values = len(flat_data)
    probabilities = [item for val, count in top_5 for item in (val, count / total_values)]

    return probabilities


def process_subject(subject):
    basepath = os.path.join("/path/to/output_folder", subject)
    csv_path = os.path.join(basepath, "top_5_frequent_values.csv")
    print(f"Processing subject {subject}, saving results to {csv_path}")
    if not os.path.exists(basepath):
        os.makedirs(basepath)

    file_list = glob.glob(
        os.path.join("/path/to/input_folder", subject, "*_sampled.csv"))
    
    file_groups = defaultdict(list)
    for file in file_list:
        # Extract file prefix, e.g. "1_1"
        prefix = '_'.join(os.path.basename(file).split('_')[:2])
        file_groups[prefix].append(file)

    results_top_values = []

    for prefix, files in file_groups.items():
        print(f"Processing files with prefix: {prefix}")

        all_data = []
        for file in files:
            data_array = extract_values_from_csv(file)
            if data_array is None:
                print(f"Skipping file: {os.path.basename(file)} (empty or error)")
                continue
            all_data.append(data_array)

        # Concatenate all data arrays vertically
        concatenated_data = np.concatenate(all_data, axis=0)

        # Compute top 5 frequent values and probabilities
        top_5_probs = top_5_frequent_values(concatenated_data)

        # Append results
        results_top_values.append([prefix, *top_5_probs])

    # Save results to CSV
    output_df = pd.DataFrame(
        results_top_values,
        columns=[
            "Prefix",
            "Value1",
            "Prob1",
            "Value2",
            "Prob2",
            "Value3",
            "Prob3",
            "Value4",
            "Prob4",
            "Value5",
            "Prob5"])
    
    output_df.to_csv(csv_path, index=False)

    print(f"Finished processing subject {subject}, results saved to 'top_5_frequent_values.csv'.")


def main():
    subject_list = os.listdir("/path/to/input_folder")
    print("Subjects found:", subject_list)

    # Use ProcessPoolExecutor for parallel processing
    with ProcessPoolExecutor(max_workers=50) as executor:
        futures = []
        for subject in subject_list:
            # Submit each subject task to the process pool
            futures.append(executor.submit(process_subject, subject))

        # Wait for all tasks to complete
        for future in as_completed(futures):
            future.result()  # Ensure each task completes


if __name__ == "__main__":
    main()

