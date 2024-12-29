import torch

import numpy as np

from robusthub import threats

def test_l2(testloader):
    eps = .5
    threat = threats.L2(eps)
    for batch in testloader:
        x_batch, _ = batch
        x_tilde = x_batch + 100 * torch.randn(x_batch.shape)
        x_proj = threat.project(x_batch, x_tilde)
        
        assert x_proj.shape == x_batch.shape, 'Shapes of projected samples do not match originals'

        norms = torch.linalg.vector_norm(x_batch.view(x_batch.shape[0], -1) - x_proj.view(x_batch.shape[0], -1), ord=2, dim=1).cpu().numpy()
        assert all([norm <= eps or np.isclose(norm, eps) for norm in norms]), 'Projected samples are not within threat model'

def test_linf(testloader):
    eps = .03
    threat = threats.Linf(eps)
    for batch in testloader:
        x_batch, _ = batch
        x_tilde = x_batch + 100 * torch.randn(x_batch.shape)
        x_proj = threat.project(x_batch, x_tilde)
        
        assert x_proj.shape == x_batch.shape, 'Shapes of projected samples do not match originals'

        norms = torch.linalg.vector_norm(x_batch.view(x_batch.shape[0], -1) - x_proj.view(x_batch.shape[0], -1), ord=np.inf, dim=1).cpu().numpy()
        assert all([norm <= eps or np.isclose(norm, eps) for norm in norms]), 'Projected samples are not within threat model'
