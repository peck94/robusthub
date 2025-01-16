"""
Adversarial training
=====================

Catalog of adversarial training defenses.
"""

import torch

from typing import Callable

from robusthub.threats import ThreatModel
from robusthub.models import Model
from robusthub.defenses import Defense
from robusthub.attacks import Attack, ProjectedGradientDescent

from tqdm import tqdm

class AdversarialTraining(Defense):
    """
    Basic adversarial training defense as proposed by :cite:`madry2017defense`.

    Parameters
    -----------
    training_data
        Clean training data.
    
    validation_data
        Clean validation data.
    
    threat_model
        Threat model of the attacks.
    
    nb_epochs
        Number of epochs of training.
    
    attack
        Adversarial attack to use for training. Defaults to :py:class:`robusthub.attacks.pgd.ProjectedGradientDescent`.
    
    optimizer
        Optimizer to use for training.
    
    criterion
        Loss function to use for training.

    device
        PyTorch device.
    """
    def __init__(self,
                 training_data: torch.utils.data.DataLoader,
                 validation_data: torch.utils.data.DataLoader,
                 threat_model: ThreatModel,
                 nb_epochs: int = 100,
                 attack: Attack | None = None,
                 optimizer: torch.optim.Optimizer = torch.optim.Adam,
                 criterion: Callable = torch.nn.CrossEntropyLoss(),
                 device: torch.device = torch.device('cuda')):
        super().__init__()

        self.training_data = training_data
        self.validation_data = validation_data
        self.attack = attack
        self.threat = threat_model
        self.nb_epochs = nb_epochs
        self.optimizer = optimizer
        self.criterion = criterion
        self.device = device

        if attack is None:
            self.attack = ProjectedGradientDescent(threat_model, device=device)

    def apply(self, model: Model) -> Model:
        """
        Adversarially train the given model.

        Parameters
        -----------
        model
            The model to train.
        
        Returns
        --------
        Model
            Adversarially trained model.
        """
        optimizer = self.optimizer(model.parameters())
        for epoch in range(self.nb_epochs):
            progbar = tqdm(self.training_data, desc=f'Epoch {epoch + 1} / {self.nb_epochs}')
            for batch in progbar:
                x_data, y_data = batch
                x_data, y_data = x_data.to(self.device), y_data.to(self.device)
                x_tilde = self.attack.apply(model, x_data, y_data)

                optimizer.zero_grad()
                y_pred = model(x_tilde)
                loss = self.criterion(y_pred, y_data)
                loss.backward()
                optimizer.step()

        return model
