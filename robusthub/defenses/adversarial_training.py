"""
Adversarial training
=====================

Catalog of adversarial training defenses.
"""

import torch

import numpy as np

from robusthub.models import Model
from robusthub.defenses import Defense
from robusthub.attacks import FastGradientSignMethod

from tqdm import tqdm

class AdversarialTraining(Defense):
    """
    Basic adversarial training defense. It uses the :py:class:`robusthub.attacks.pgd.ProjectedGradientDescent` attack.
    """

    def __init__(self,
                 training_data: torch.utils.data.DataLoader,
                 validation_data: torch.utils.data.DataLoader,
                 nb_epochs: int = 100,
                 epsilon: float = .06,
                 device: torch.device = torch.device('cuda')):
        """
        Initialize the defense.

        Parameters
        -----------
        training_data
            Clean training data.
        
        validation_data
            Clean validation data.
        
        nb_epochs
            Number of training epochs.
        
        epsilon
            Perturbation budget.

        device
            PyTorch device.
        """
        super().__init__()

        self.training_data = training_data
        self.validation_data = validation_data
        self.nb_epochs = nb_epochs
        self.epsilon = epsilon
        self.device = device

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
        optimizer = torch.optim.Adam(model.parameters())
        criterion = torch.nn.CrossEntropyLoss()
        attack = FastGradientSignMethod(model, self.epsilon)
        for epoch in range(self.nb_epochs):
            losses = []
            progbar = tqdm(self.training_data, desc=f'Epoch {epoch + 1} / {self.nb_epochs}')
            for batch in progbar:
                x_data, y_data = batch
                x_data, y_data = x_data.to(self.device), y_data.to(self.device)
                x_tilde = attack.apply(x_data, y_data)

                optimizer.zero_grad()
                y_pred = model(x_tilde)
                loss = criterion(y_pred, y_data)
                loss.backward()
                optimizer.step()

                losses.append(loss.item())
                progbar.set_postfix({'loss': np.mean(losses)})
            
            standard_losses = []
            robust_losses = []
            for batch in self.validation_data:
                x_data, y_data = batch
                x_data, y_data = x_data.to(self.device), y_data.to(self.device)
                x_tilde = attack.apply(x_data, y_data)

                y_pred = model(x_data)
                loss = criterion(y_pred, y_data)
                standard_losses.append(loss.item())

                y_pred = model(x_tilde)
                loss = criterion(y_pred, y_data)
                robust_losses.append(loss.item())
            print(f'Standard loss: {np.mean(standard_losses)}')
            print(f'Robust loss  : {np.mean(robust_losses)}')

        return model
