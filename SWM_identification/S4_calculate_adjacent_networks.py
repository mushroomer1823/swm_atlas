import nibabel as nib
import numpy as np
from scipy.ndimage import generate_binary_structure, binary_dilation

# --- Load the NIfTI file ---
nii_path = "/path/to/nodes.nii.gz"  # Replace with your actual file path
nii = nib.load(nii_path)
data = nii.get_fdata().astype(int)  # Convert to integers

# --- Extract region labels (excluding background) ---
labels = np.unique(data)
labels = labels[labels > 0]  # Keep only non-zero labels (e.g., 1 to 17)

# --- Initialize adjacency matrix ---
n_regions = len(labels)
adj_matrix = np.zeros((n_regions, n_regions), dtype=int)

# --- Define 3D 6-connected neighborhood structure ---
struct = generate_binary_structure(3, 1)

# --- Loop over all brain regions ---
for i, region1 in enumerate(labels):
    # Create binary mask for region1
    mask1 = (data == region1)

    # Dilate the mask to find adjacent voxels
    dilated_mask = binary_dilation(mask1, structure=struct)

    # Find labels of neighboring regions (excluding background and self)
    neighbor_labels = np.unique(data[dilated_mask])
    neighbor_labels = neighbor_labels[(neighbor_labels > 0) & (neighbor_labels != region1)]

    # Update adjacency matrix
    for region2 in neighbor_labels:
        j = np.where(labels == region2)[0][0]
        adj_matrix[i, j] = 1
        adj_matrix[j, i] = 1  # Ensure symmetry

# --- Print and optionally save the adjacency matrix ---
print("Adjacency matrix:")
print(adj_matrix)

# Save to CSV
adj_save_path = "/path/to/adjacency_matrix.csv"  # Replace with your desired output path
np.savetxt(adj_save_path, adj_matrix, delimiter=",", fmt="%d")
print(f"Adjacency matrix saved to: {adj_save_path}")

