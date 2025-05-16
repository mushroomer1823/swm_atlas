import pandas as pd
import os

def read_top_5_csv(file_path):
    """Read each sample's top_5_frequent_values.csv"""
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error reading file {os.path.basename(file_path)}: {e}")
        return None

def extract_prefix_from_path(path):
    """Extract prefix part from the filename"""
    basename = os.path.basename(path)
    parts = basename.split('_')
    return parts[0] + '_' + parts[1]

def load_global_top_2_ic_labels(global_csv_path="/path/to/uncertainty/top_5_values_category.csv"):
    """Load top 2 IC labels from the group-level data"""
    global_df = pd.read_csv(global_csv_path)
    prefix_global_top_2_ic = {}

    for _, row in global_df.iterrows():
        prefix = extract_prefix_from_path(row["File"])
        top_2_ic = [row["Top_1_Value"], row["Top_2_Value"]]
        prefix_global_top_2_ic[prefix] = top_2_ic

    return prefix_global_top_2_ic

def check_individual_ic_not_in_global_top2(subject_list, base_dir="/path/to/uncertainty_subjects", global_top_2_ic=None):
    """Check if individual's IC labels are not among the group's top 2 IC labels"""
    unusual_individuals = []

    for subject in subject_list:
        top_5_file = os.path.join(base_dir, subject, "top_5_frequent_values.csv")
        if os.path.exists(top_5_file):
            print(f"Processing {os.path.basename(top_5_file)}")

            df = read_top_5_csv(top_5_file)
            if df is not None:
                for _, row in df.iterrows():
                    prefix = extract_prefix_from_path(row["Prefix"])
                    top_1_ic = row["Value1"]
                    top_2_ic = row["Value2"]

                    if prefix in global_top_2_ic:
                        global_top_2 = global_top_2_ic[prefix]

                        # Consider unusual if both individual top 2 IC labels are not in group top 2
                        if top_1_ic not in global_top_2 and top_2_ic not in global_top_2:
                            unusual_individuals.append(
                                (subject, prefix, global_top_2[0], global_top_2[1], top_1_ic, top_2_ic)
                            )

    return unusual_individuals

def save_unusual_individuals(unusual_individuals, output_path="/path/to/uncertainty_subjects/unusual_individuals_top2-2.csv"):
    """Save unusual individuals and their IC labels to a CSV file"""
    unusual_df = pd.DataFrame(
        unusual_individuals,
        columns=[
            "Subject", "Prefix",
            "Global_IC_Label_1", "Global_IC_Label_2",
            "Individual_IC_Label_1", "Individual_IC_Label_2"
        ]
    )
    unusual_df.to_csv(output_path, index=False)
    print(f"Unusual individuals saved to {os.path.basename(output_path)}")

def main():
    # Get the list of all subjects
    subject_list = os.listdir("/path/to/uncertainty_subjects/")
    
    # Load group's top 2 IC labels for each prefix
    global_top_2_ic = load_global_top_2_ic_labels()

    # Check which individuals have IC labels outside the group's top 2
    unusual_individuals = check_individual_ic_not_in_global_top2(subject_list, global_top_2_ic=global_top_2_ic)

    # Save the results
    save_unusual_individuals(unusual_individuals)

if __name__ == "__main__":
    main()

