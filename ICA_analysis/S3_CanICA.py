import numpy as np
from nilearn.decomposition import CanICA
from pathlib import Path
from multiprocessing import Pool

FUNC_DATA_DIR = "/path/to/func_data"
OUTPUT_DIR = "/path/to/output_dir"
CACHE_DIR = "/path/to/cache_dir"

def canica_analysis(n_components, func_filenames, output_dir, cache_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    canica = CanICA(
        n_components=n_components,
        memory=cache_dir,
        memory_level=2,
        verbose=2,
        mask_strategy="whole-brain-template",
        random_state=0,
        standardize="zscore",
        n_jobs=2,
    )
    
    canica.fit(func_filenames)
    
    components = canica.components_
    canica_components_img = canica.components_img_

    npy_file = output_dir / f'canica_array_{n_components}.npy'
    nii_file = output_dir / f'canica_ncomponents_{n_components}.nii.gz'
    np.save(npy_file, components)
    canica_components_img.to_filename(str(nii_file))

    print(f"CanICA analysis completed for {n_components} components.")
    
    return n_components, npy_file, nii_file

def run_parallel_canica(func_filenames, output_dir, cache_dir):
    n_components_list = [110, 120, 130, 140, 150]
    
    with Pool(processes=len(n_components_list)) as pool:
        results = pool.starmap(
            canica_analysis,
            [(n, func_filenames, output_dir, cache_dir) for n in n_components_list]
        )
    
    for n_components, npy_file, nii_file in results:
        print(f"Result for {n_components} components saved to {npy_file} and {nii_file}")

if __name__ == "__main__":
    folder_path = Path(FUNC_DATA_DIR)
    func_filenames = [str(file) for file in folder_path.rglob('*') if file.is_file()]
    
    run_parallel_canica(func_filenames, OUTPUT_DIR, CACHE_DIR)

