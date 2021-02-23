from __future__ import print_function, division
import os
import torch
import pandas as pd
from skimage import io, transform
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils

class ChildrensBookIllustrationsDataset(Dataset):
    """Children's Book Illustrations Dataset."""

    def __init__(self, csv_file, root_dir, transform=None):
        """
        Args:
            csv_file (string): Path to the csv file with annotations.
            root_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        self.labels = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        img_filename = (self.labels.iloc[idx, 2]).split('/')[-1]
        img_path = os.path.join(self.root_dir, img_filename)
        image = io.imread(img_path)
        text = str(self.labels.iloc[idx, 6])
        book = int(self.labels.iloc[idx, 3])
        sample = {'image': image, 'book': book, 'text': text}

        if self.transform:
            sample = self.transform(sample)

        return sample
