import torch
import torch.nn as nn
import torch.nn.functional as F

class MiteScanCNN(nn.Module):
    def __init__(self):
        super().__init__()

        self.conv1 = nn.Conv2d(3, 16, 3)
        self.conv2 = nn.Conv2d(16, 32, 3)
        self.pool = nn.MaxPool2d(2, 2)

        self.fc1 = None 
        self.fc2 = nn.Linear(128, 3)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))

        x = x.view(x.size(0), -1)

        # cria fc1 dinamicamente
        if self.fc1 is None:
            self.fc1 = nn.Linear(x.shape[1], 128).to(x.device)

        x = F.relu(self.fc1(x))
        x = self.fc2(x)

        return x
