import os
import numpy as np
import nibabel as nb
from concurrent.futures import ProcessPoolExecutor

# TR and frequency range
TR = 0.72
HP_freq = 0.01
LP_freq = 0.1
sampling_rate = 1. / TR

# Base directory (replace with your actual path)
base_path = "/path/to/fMRI_data"

def process_subject(subject):
    print(f"Processing subject: {subject}")
    
    in_file = os.path.join(base_path, subject, 
                           'MNINonLinear/Results/rfMRI_REST2_LR/rfMRI_REST2_LR_hp2000_clean.nii.gz')
    if not os.path.exists(in_file):
        print("Input file not found.")
        return

    out_file = os.path.join(base_path, subject, 
                            'MNINonLinear/Results/rfMRI_REST2_LR/rfMRI_REST2_LR_hp2000_clean_filter.nii.gz')
    if os.path.exists(out_file):
        print("Output file already exists.")
        return

    img = nb.load(in_file)
    timepoints = img.shape[-1]
    
    # Frequency filter mask
    F = np.zeros(timepoints)
    lowidx = int(np.round(LP_freq / sampling_rate * timepoints)) if LP_freq > 0 else timepoints // 2 + 1
    highidx = int(np.round(HP_freq / sampling_rate * timepoints)) if HP_freq > 0 else 0
    F[highidx:lowidx] = 1
    F = ((F + F[::-1]) > 0).astype(int)

    data = img.get_fdata()
    if np.all(F == 1):
        filtered_data = data
    else:
        filtered_data = np.real(np.fft.ifftn(np.fft.fftn(data) * F))

    img_out = nb.Nifti1Image(filtered_data, img.affine, img.header)
    img_out.to_filename(out_file)
    print("Filtered data saved.")

# Gather subjects
subjects = [s for s in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, s))]

# Run in parallel
with ProcessPoolExecutor(max_workers=10) as executor:
    executor.map(process_subject, subjects)
