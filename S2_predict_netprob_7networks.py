#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import torch.nn.functional as F
import h5py
import numpy as np
import pandas as pd
from dipy.io.streamline import load_tck
from collections import OrderedDict
import os
import sys

# Add custom path for fiber feature extraction
sys.path.append('/path/to/line_check')
import beta_process

# Utility to create a fiber cluster dictionary
def create_dict(node="", cluster="", fibers=None, prob=0.0):
    if fibers is None:
        fibers = np.array([])
    return {
        "node": node,
        "cluster": cluster,
        "fibers": fibers,
        "prob": prob
    }

# Neural network model for fiber classification
class FiberClassifier(nn.Module):
    def __init__(self):
        super(FiberClassifier, self).__init__()
        self.fc1 = nn.Linear(5 * 3, 128)
        self.fc2 = nn.Linear(128, 256)
        self.fc3 = nn.Linear(256, 64)
        self.fc4 = nn.Linear(64, 2)  # Binary classification

    def forward(self, x):
        print(x.shape)
        x = x.view(-1, 5 * 3)  # Flatten
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        x = self.fc4(x)
        return x

# Load all fiber clusters from directory
dict_list = []
root_path = '/path/to/HCP_Parcels/Population_7Networks'
atlas_path = '/path/to/atlas/mni_template.nii'

dirs = os.listdir(root_path) 
print("Subject directories found:", dirs)

for dir in dirs:
    tckpath = os.path.join(root_path, dir, 'Cluster_clean_in_yeo_space')
    for root_tck, dirs_tck, files_tck in os.walk(tckpath):
        print("TCK files in", dir, ":", files_tck)
        for file_tck in files_tck:
            tck_path = os.path.join(root_tck, file_tck)
            print("Reading TCK:", tck_path) 

            tck = load_tck(tck_path, atlas_path)
            fibers = tck.streamlines
            fiber_betas = beta_process.get_betas(fibers)

            # Optional: Random mock data
            # n = np.random.randint(10,20)
            # fiber_betas = np.random.rand(n, 5, 3)

            cluster_dict = create_dict(dir, file_tck, fiber_betas)
            dict_list.append(cluster_dict)

print("Fiber cluster dictionaries created.")

# Load pretrained model
model = FiberClassifier()
model_path = '/path/to/model/normal724.pth'
state_dict = torch.load(model_path, map_location='cpu')

# Clean 'module.' prefixes from DataParallel saving
new_state_dict = OrderedDict()
for k, v in state_dict.items():
    new_key = k.replace('module.', '')
    new_state_dict[new_key] = v

model.load_state_dict(new_state_dict)

# Move model to device
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = nn.DataParallel(model, device_ids=[0, 1])
model = model.to(device)
model.eval()

# Predict SWM probability for each cluster
for cluster_dict in dict_list:
    fibers = cluster_dict["fibers"]
    predict_list = np.zeros(fibers.shape[0])

    input_fiber = torch.tensor(fibers).to(torch.float32).to(device)

    with torch.no_grad():
        output_fiber = model(input_fiber)
        _, predicted = torch.max(output_fiber, 1)

    predicted = predicted.cpu().numpy()

    swm_count = np.sum(predicted == 1)
    fiber_count = predicted.size
    swm_prob = swm_count / fiber_count
    cluster_dict["prob"] = swm_prob

print("Prediction completed.")
print(dict_list)

# Load SWM table and update with predicted probabilities
csv_path = "/path/to/selectSWM.csv"
df = pd.read_csv(csv_path)
df['netProb'] = pd.NA

for d in dict_list:
    mask = (df['nodeList'] == d["node"]) & (df['tckName'] == d['cluster'])
    df.loc[mask, 'netProb'] = d['prob']

# Save updated table
csv_savepath = "/path/to/selectSWM_updated.csv"
df.to_csv(csv_savepath, index=False)
print("Updated CSV saved to:", csv_savepath)

