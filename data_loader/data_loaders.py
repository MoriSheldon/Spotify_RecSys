import pandas as pd
import torch
from torch.utils.data import Dataset
from base import BaseDataLoader


class SpotifyDataset(Dataset):
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        self.features = self.data.drop(['id'], axis=1).values
        self.ids = self.data['id'].values

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        features = torch.tensor(self.features[idx], dtype=torch.float32)
        id = self.ids[idx]
        return features, id


class SpotifyDataLoader(BaseDataLoader):
    def __init__(self, data_dir, batch_size, shuffle=True, validation_split=0.0, num_workers=1, training=True):
        self.data_dir = data_dir
        self.dataset = SpotifyDataset("data/sample/sample.csv")
        super().__init__(self.dataset, batch_size, shuffle, validation_split, num_workers)
