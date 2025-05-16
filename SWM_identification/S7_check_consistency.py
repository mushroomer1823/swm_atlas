#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
from dipy.io.streamline import load_tck
import os
import numpy as np

# Load selected SWM connections
csv_path = "/path/to/selectSWM_ifSWM_regions_final.csv"
csv_savepath = "/path/to/selectSWM_checked.csv"
df = pd.read_csv(csv_path)

nodeList = df['nodeList']
tckName = df['tckName']
ifSWM = df['ifSWM_final']
swm_index = [i for i, v in enumerate(ifSWM) if v == 1]

percentList = np.zeros(len(nodeList))

# List all subjects (excluding Population dir)
subject_root = "/path/to/HCP_Parcels"
atlas_ref = "/path/to/mni_brain_template.nii"
subList = os.listdir(subject_root)
subList = [s for s in subList if s != 'Population_7Networks']

print("Total subjects:", len(subList))
print("Total candidate SWM:", len(swm_index))

for idx in swm_index:
    tck = tckName[idx]
    nodePair = nodeList[idx]
    
    count = 0  # how many subjects have this tck
    for sub in subList:
        tckpath = os.path.join(
            subject_root, sub, nodePair, 'Cluster_clean_in_yeo_space', tck
        )
        if not os.path.exists(tckpath):
            continue
        
        tract = load_tck(tckpath, atlas_ref)
        fibers = tract.streamlines
        if len(fibers) > 0:
            count += 1

    percentage = count / len(subList)
    print(f"node pair: {nodePair}, tck: {tck}, found in {percentage*100:.2f}% subjects")
    percentList[idx] = percentage

# Append result
df['percentage'] = percentList
df.to_csv(csv_savepath, index=False)

print("✓ Done. File saved to:", csv_savepath)

