import torch
from torch.utils.data import DataLoader

import torchvision
import torchvision.transforms as transforms

from typing import Tuple

from dataset import Dataset

class CIFAR10(Dataset):
    """
    The CIFAR-10 data set :cite:`krizhevsky2009learning`.

    Parameters
    -----------
    path
        Path to local storage for the data.
    
    download
        True if the data should be downloaded if it doesn't already exist locally.
    """
    def __init__(self, path: str = './data', download: bool = True):
        super().__init__('CIFAR-10', path)
        self.download = download
    
    def load(self, batch_size: int = 32, seed: int = 42) -> Tuple[DataLoader, DataLoader, DataLoader]:
        generator = torch.Generator().manual_seed(seed)
        transform = transforms.Compose(
            [transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

        trainvalset = torchvision.datasets.CIFAR10(root=self.path, train=True, download=self.download, transform=transform)
        trainset, valset = torch.utils.data.random_split(trainvalset, [.8, .2], generator=generator)

        trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size, shuffle=True)
        valloader = torch.utils.data.DataLoader(valset, batch_size=batch_size, shuffle=False)

        testset = torchvision.datasets.CIFAR10(root=self.path, train=False, download=self.download, transform=transform)
        testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size, shuffle=False)

        return trainloader, valloader, testloader
