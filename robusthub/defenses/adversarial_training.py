"""
Adversarial training
=====================

Catalog of adversarial training defenses.
"""

import torch

import numpy as np

from robusthub.threats import ThreatModel
from robusthub.models import Model
from robusthub.defenses import Defense
from robusthub.attacks import ProjectedGradientDescent
from robusthub.metrics import Accuracy

from tqdm import tqdm

class AdversarialTraining(Defense):
    """
    Basic adversarial training defense as proposed by :cite:`madry2017defense`. It uses the :py:class:`robusthub.attacks.pgd.ProjectedGradientDescent` attack.

    Parameters
    -----------
    training_data
        Clean training data.
    
    validation_data
        Clean validation data.
    
    threat_model
        Threat model of the attacks.
    
    nb_epochs
        Number of training epochs.
    
    nb_iterations
        Number of PGD iterations.

    device
        PyTorch device.
    """

    def __init__(self,
                 training_data: torch.utils.data.DataLoader,
                 validation_data: torch.utils.data.DataLoader,
                 threat_model: ThreatModel,
                 nb_epochs: int = 100,
                 nb_iterations: int = 100,
                 device: torch.device = torch.device('cuda')):
        super().__init__()

        self.training_data = training_data
        self.validation_data = validation_data
        self.nb_epochs = nb_epochs
        self.nb_iterations = nb_iterations
        self.threat = threat_model
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
        attack = ProjectedGradientDescent(model, self.threat, self.nb_iterations, self.device)
        metric = Accuracy()
        for epoch in range(self.nb_epochs):
            losses = []
            accs = []
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
                accs.append(metric.compute(model, x_data, y_data))
                progbar.set_postfix({
                    'loss': np.mean(losses),
                    'acc': np.mean(accs)})
            
            standard_losses, standard_accs = [], []
            robust_losses, robust_accs = [], []
            for batch in self.validation_data:
                x_data, y_data = batch
                x_data, y_data = x_data.to(self.device), y_data.to(self.device)
                x_tilde = attack.apply(x_data, y_data)

                y_pred = model(x_data)
                loss = criterion(y_pred, y_data)
                standard_losses.append(loss.item())
                standard_accs.append(metric.compute(model, x_data, y_data))

                y_pred = model(x_tilde)
                loss = criterion(y_pred, y_data)
                robust_losses.append(loss.item())
                robust_accs.append(metric.compute(model, x_tilde, y_data))
            print(f'Standard loss: {np.mean(standard_losses)}')
            print(f'Robust loss  : {np.mean(robust_losses)}')
            print(f'Standard acc : {np.mean(standard_accs):.2%}')
            print(f'Robust acc   : {np.mean(robust_accs):.2%}')

        return model
