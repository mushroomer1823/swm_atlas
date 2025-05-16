import nibabel as nib
import numpy as np
import os

def load_nii_image(file_path):
    """Load NIfTI image and return its data."""
    img = nib.load(file_path)
    return img.get_fdata()

def categorize_brain_hemisphere(image_data):
    """Count voxel distribution of each label (0-70) in left, right, or both hemispheres."""
    X_size = image_data.shape[0]
    X_center = X_size // 2  # Calculate center along X-axis

    # Initialize statistics for each label
    category_statistics = {i: {'left': 0, 'right': 0} for i in range(71)}
    left_hemisphere_only = set()
    right_hemisphere_only = set()
    cross_hemisphere_categories = []

    # Iterate through voxels and count label occurrences per hemisphere
    for x in range(X_size):
        for y in range(image_data.shape[1]):
            for z in range(image_data.shape[2]):
                label = int(image_data[x, y, z])
                if label == 0:  # Skip background
                    continue
                
                if x < X_center:
                    category_statistics[label]['left'] += 1
                else:
                    category_statistics[label]['right'] += 1

    # Determine hemisphere category for each label
    cross_hemisphere_count = 0
    for label, stats in category_statistics.items():
        if stats['left'] > 0 and stats['right'] > 0:
            cross_hemisphere_count += 1
            cross_hemisphere_categories.append((label, stats['left'], stats['right']))
        elif stats['left'] > 0:
            left_hemisphere_only.add(label)
        elif stats['right'] > 0:
            right_hemisphere_only.add(label)

    # For cross-hemisphere labels, determine which hemisphere has more voxels
    more_left_hemisphere = []
    more_right_hemisphere = []
    
    for label, left_voxels, right_voxels in cross_hemisphere_categories:
        if left_voxels > right_voxels:
            more_left_hemisphere.append(label)
        elif right_voxels > left_voxels:
            more_right_hemisphere.append(label)

    return category_statistics, left_hemisphere_only, right_hemisphere_only, cross_hemisphere_count, more_left_hemisphere, more_right_hemisphere

def print_statistics(category_statistics, left_hemisphere_only, right_hemisphere_only, cross_count, more_left_hemisphere, more_right_hemisphere):
    """Print statistics about label distribution in hemispheres."""
    print("Voxel counts per label in hemispheres:")
    for label, stats in category_statistics.items():
        print(f"Label {label}: Left hemisphere: {stats['left']} voxels, Right hemisphere: {stats['right']} voxels")

    print("\n Number of labels exclusively in left hemisphere:", len(left_hemisphere_only))
    print("Left hemisphere labels:", sorted(left_hemisphere_only))

    print("\n Number of labels exclusively in right hemisphere:", len(right_hemisphere_only))
    print("Right hemisphere labels:", sorted(right_hemisphere_only))

    print("\nNumber of labels spanning both hemispheres:", cross_count)
    print("Labels with more voxels in left hemisphere:", len(more_left_hemisphere))
    print("Labels with more voxels in right hemisphere:", len(more_right_hemisphere))
    print("\nLabels spanning both hemispheres with more voxels on left:", sorted(more_left_hemisphere))
    print("Labels spanning both hemispheres with more voxels on right:", sorted(more_right_hemisphere))


# Usage example
# Hide full path by using basename or set a generic path variable
file_path = "/path/to/nifti/max_component_labels_IC_70.nii.gz"  # Replace with your actual file path or keep generic
print("Loading NIfTI file:", os.path.basename(file_path))

image_data = load_nii_image(file_path)
category_statistics, left_hemisphere_only, right_hemisphere_only, cross_count, more_left_hemisphere, more_right_hemisphere = categorize_brain_hemisphere(image_data)
print_statistics(category_statistics, left_hemisphere_only, right_hemisphere_only, cross_count, more_left_hemisphere, more_right_hemisphere)

