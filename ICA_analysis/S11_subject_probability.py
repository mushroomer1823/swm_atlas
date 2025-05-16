import pandas as pd
import glob
import os
from collections import defaultdict

def read_top_5_csv(file_path):
    # Read each sample's top_5_frequent_values.csv
    df = pd.read_csv(file_path)
    return df

def calculate_label_probabilities(subject_list, base_dir="/path/to/uncertainty_subjects"):
    # Store IC label counts for each prefix across all samples
    prefix_ic_labels = defaultdict(lambda: defaultdict(int))

    # Count occurrences of each IC label in different samples
    for subject in subject_list:
        top_5_file = os.path.join(base_dir, subject, "top_5_frequent_values.csv")
        if os.path.exists(top_5_file):
            print(f"Processing {os.path.basename(top_5_file)}")

            # Read CSV file
            df = read_top_5_csv(top_5_file)
            
            # Count IC labels per prefix
            for _, row in df.iterrows():
                prefix = row["Prefix"]
                for i in range(1, 6):
                    label = row[f"Value{i}"]
                    prefix_ic_labels[prefix][label] += 1

    return prefix_ic_labels

def calculate_global_label_probabilities(prefix_ic_labels, total_subjects):
    # Store global occurrence probabilities for each IC label
    global_label_probabilities = defaultdict(float)

    # Sum probabilities of IC labels across all prefixes
    for prefix, ic_labels in prefix_ic_labels.items():
        for label, count in ic_labels.items():
            probability = count / total_subjects
            global_label_probabilities[label] += probability
    
    # Sort and get top 5 IC labels by probability
    sorted_labels = sorted(global_label_probabilities.items(), key=lambda x: x[1], reverse=True)[:5]

    return sorted_labels

def save_final_results(prefix_ic_labels, global_label_probabilities, output_path="/path/to/uncertainty_subjects/top5.csv"):
    # Prepare final results in the same CSV format as the original
    final_results = []

    for prefix, ic_labels in prefix_ic_labels.items():
        row = [prefix]

        # Get top 5 IC labels and their counts
        for i in range(1, 6):
            if i <= len(ic_labels):
                value = list(ic_labels.keys())[i-1]
                prob = ic_labels[value]
            else:
                value = None
                prob = 0

            row.extend([value, prob])

        final_results.append(row)

    # Save the results to a CSV file
    final_df = pd.DataFrame(final_results, columns=["Prefix", "Value1", "Prob1", "Value2", "Prob2", "Value3", "Prob3", "Value4", "Prob4", "Value5", "Prob5"])
    final_df.to_csv(output_path, index=False)
    print(f"Final results saved to {output_path}")

def main():
    # Get list of all subjects
    subject_list = os.listdir("/path/to/uncertainty_subjects/")
    
    tck_files = glob.glob(os.path.join("/path/to/category/*.tck"))
    # Extract prefix from first 3 characters of each filename
    prefix_list = {os.path.basename(file)[:3] for file in tck_files}
    
    # Calculate IC label counts per prefix across all subjects
    prefix_ic_labels = calculate_label_probabilities(subject_list)
    
    # Calculate global probabilities of IC labels
    total_subjects = len(subject_list)
    global_label_probabilities = calculate_global_label_probabilities(prefix_ic_labels, total_subjects)

    # Save final aggregated results
    save_final_results(prefix_ic_labels, global_label_probabilities)

if __name__ == "__main__":
    main()

