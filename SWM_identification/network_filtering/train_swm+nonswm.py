import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import torch.nn.functional as F
import h5py
import numpy as np

# Base paths (change these to your actual paths)
DATA_BASE = "/path/to/swm/data_swm+nonswm"
MODEL_SAVE_PATH = "/path/to/swm/models"

class FiberDataset(Dataset):
    def __init__(self, dwm_file, swm_file):
        # Load HDF5 data
        self.dwm_data = h5py.File(dwm_file, 'r')['x'][:]
        self.swm_data = h5py.File(swm_file, 'r')['x'][:]
        self.dwm_labels = h5py.File(dwm_file, 'r')['y'][:]
        self.swm_labels = h5py.File(swm_file, 'r')['y'][:]

        # Concatenate data arrays
        self.data = np.concatenate((self.dwm_data, self.swm_data), axis=0)

        # Uncomment below to sample a smaller subset for training
        '''
        total_size = self.data.shape[0]
        indices = np.arange(total_size)
        np.random.shuffle(indices)
        selected_indices = indices[:1000000]  # example subset size
        self.data = self.data[selected_indices]
        '''

        print("Data size:", self.data.shape)

        # Concatenate labels
        self.labels = np.concatenate((self.dwm_labels, self.swm_labels), axis=0)

        '''
        # If using subset, select corresponding labels
        self.labels = self.labels[selected_indices]
        '''

        # Convert to torch tensors
        self.data = torch.tensor(self.data, dtype=torch.float32)
        print("Tensor size:", self.data.shape)
        self.labels = torch.tensor(self.labels, dtype=torch.long)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]

class FiberClassifier(nn.Module):
    def __init__(self):
        super(FiberClassifier, self).__init__()
        self.fc1 = nn.Linear(5 * 3, 128)  # Input layer: flatten 5x3 matrix
        self.fc2 = nn.Linear(128, 256)    # Hidden layer 1
        self.fc3 = nn.Linear(256, 64)     # Hidden layer 2
        self.fc4 = nn.Linear(64, 2)       # Output layer (2 classes)

    def forward(self, x):
        x = x.view(-1, 5 * 3)  # Flatten input
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        x = self.fc4(x)
        return x

# File paths for train, val, and test datasets
train_dwm_file = f'{DATA_BASE}/train/nonswm_cos.h5'
train_swm_file = f'{DATA_BASE}/train/swm_cos.h5'
val_dwm_file = f'{DATA_BASE}/val/nonswm_cos.h5'
val_swm_file = f'{DATA_BASE}/val/swm_cos.h5'
test_dwm_file = f'{DATA_BASE}/test/nonswm_cos.h5'
test_swm_file = f'{DATA_BASE}/test/swm_cos.h5'

# Datasets and data loaders
train_dataset = FiberDataset(train_dwm_file, train_swm_file)
val_dataset = FiberDataset(val_dwm_file, val_swm_file)
test_dataset = FiberDataset(test_dwm_file, test_swm_file)

train_loader = DataLoader(train_dataset, batch_size=128, shuffle=True, num_workers=4)
val_loader = DataLoader(val_dataset, batch_size=128, shuffle=False, num_workers=4)
test_loader = DataLoader(test_dataset, batch_size=128, shuffle=False, num_workers=4)

# Model, loss function and optimizer
print("CUDA available:", torch.cuda.is_available())
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = FiberClassifier().to(device)
model = nn.DataParallel(model, device_ids=[0, 1])  # Use two GPUs for training

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

print("Training started")
num_epochs = 10
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item() * inputs.size(0)

    epoch_loss = running_loss / len(train_loader.dataset)
    print(f"Epoch {epoch + 1}/{num_epochs}, Loss: {epoch_loss:.4f}")

    # Validation phase
    model.eval()
    val_loss = 0.0
    corrects = 0
    total = 0
    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            val_loss += loss.item() * inputs.size(0)
            _, preds = torch.max(outputs, 1)
            corrects += torch.sum(preds == labels.data)
            total += labels.size(0)

    val_loss /= len(val_loader.dataset)
    val_acc = corrects.double() / total
    print(f"Validation Loss: {val_loss:.4f}, Accuracy: {val_acc:.4f}")

# Testing phase
model.eval()
test_loss = 0.0
corrects = 0
total = 0
with torch.no_grad():
    for inputs, labels in test_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        print(inputs.shape)
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        test_loss += loss.item() * inputs.size(0)
        _, preds = torch.max(outputs, 1)
        corrects += torch.sum(preds == labels.data)
        total += labels.size(0)

test_loss /= len(test_loader.dataset)
test_acc = corrects.double() / total
print(f"Test Loss: {test_loss:.4f}, Accuracy: {test_acc:.4f}")

'''
model_path = f'{MODEL_SAVE_PATH}/normal724.pth'
torch.save(model.state_dict(), model_path)
'''
