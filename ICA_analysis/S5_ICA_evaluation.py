import nibabel as nib
import numpy as np
from sklearn.metrics import davies_bouldin_score

# Define base directory for ICA files and output
BASE_ICA_DIR = "/path/to/ICA"

# Template for feature images and label images
feature_template = BASE_ICA_DIR + "/canica_ncomponents_{num}.nii.gz"     # original feature images
label_template = BASE_ICA_DIR + "/max_component_labels_IC_{num}.nii.gz"  # clustering results

# Range of independent component numbers
ic_list = range(110, 151, 10)  # 110, 120, ..., 150

# Store Davies-Bouldin Index (DBI) results
dbi_results = {}

for ic in ic_list:
    try:
        # Load label image
        label_file = label_template.format(num=ic)
        label_img = nib.load(label_file)
        labels = label_img.get_fdata().astype(int)  # shape (X, Y, Z)

        # Load original feature image
        feature_file = feature_template.format(num=ic)
        feature_img = nib.load(feature_file)
        features = feature_img.get_fdata()  # shape (X, Y, Z, IC)

        # Filter valid voxels
        mask = labels >= 0
        print(f"Mask shape: {mask.shape}")
        valid_labels = labels[mask]       # voxel labels, shape (N,)
        valid_features = features[mask]   # voxel feature vectors, shape (N, IC)
        print(f"Valid labels shape: {valid_labels.shape}")
        print(f"Valid features shape: {valid_features.shape}")

        # Calculate Davies-Bouldin Index
        dbi = davies_bouldin_score(valid_features, valid_labels)
        dbi_results[ic] = dbi
        print(f"IC={ic}: Davies-Bouldin Index = {dbi:.4f}")

    except FileNotFoundError:
        print(f"File {label_file} or {feature_file} not found, skipping...")
    except Exception as e:
        print(f"Error processing IC={ic}: {e}")

# Print final results
print("\nDavies-Bouldin Index calculation complete:")
for ic, dbi in dbi_results.items():
    print(f"IC={ic}: Davies-Bouldin Index = {dbi:.4f}")

