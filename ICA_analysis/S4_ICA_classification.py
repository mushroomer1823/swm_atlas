import nibabel as nib
import numpy as np

# Define base directory paths (change these to your actual paths)
BASE_ICA_DIR = "/path/to/ICA"
OUTPUT_DIR = "/path/to/output"

# Template for input files
file_template = BASE_ICA_DIR + "/canica_ncomponents_{num}.nii.gz"

# Define list of independent component numbers to process
ic_list = range(110, 151, 10)  # 110, 120, 130, 140, 150

for ic in ic_list:
    # Load the NIfTI file
    nii_file = file_template.format(num=ic)
    print(f"Processing: {nii_file}")

    try:
        img = nib.load(nii_file)
        data = img.get_fdata()  # shape: (X, Y, Z, IC)

        # Compute the max value and its index across IC dimension for each voxel
        max_indices = np.argmax(data, axis=-1)  # index of max IC
        max_values = np.max(data, axis=-1)      # max value across ICs

        # Mask voxels with all zero or near-zero values
        threshold = 1e-6
        no_value_mask = max_values < threshold

        # Label voxels by their max IC index +1 (to start labels from 1)
        labeled_data = max_indices + 1
        labeled_data[no_value_mask] = 0  # Set zero-value voxels to label 0

        print(f"Max label value: {np.max(labeled_data)}")

        # Output filename
        output_filename = f"{OUTPUT_DIR}/max_component_labels_IC_{ic}.nii.gz"

        # Save the labeled data as new NIfTI file
        output_img = nib.Nifti1Image(labeled_data.astype(np.int16), img.affine, img.header)
        nib.save(output_img, output_filename)

        print(f"Saved output to: {output_filename}")

    except FileNotFoundError:
        print(f"File not found: {nii_file}, skipping...")
    except Exception as e:
        print(f"Error processing {nii_file}: {e}")

