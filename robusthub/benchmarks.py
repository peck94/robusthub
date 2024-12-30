"""
Benchmarks evaluate combinations of models and adversarial defenses according to *task-specific metrics*,
which are unique to the particular task the models need to solve, and *task-agnostic metrics*
which are always relevant. All benchmarks always measure the following task-agnostic metrics:

* Runtime of training.
* Runtime of inference.
* Memory consumption during training.
* Memory consumption during inference.

Task-specific metrics must be specified by the user and are detailed in our :doc:`Metrics <metrics>` page.
All task-specific metrics are computed on clean as well as adversarially corrupted data.
"""

from typing import List

from robusthub import models
from robusthub import defenses
from robusthub import attacks
from robusthub import metrics

class Benchmark:
    """
    Base class for all benchmarks.

    Parameters
    -----------
    attack
        Adversarial attack used for robustness assessment.
    
    metrics
        List of task-specific metrics
    """
    def __init__(self, attack: attacks.Attack, metrics: List[metrics.Metric]):
        pass

    def run(self, model: models.Model, defense: defenses.Defense):
        pass
