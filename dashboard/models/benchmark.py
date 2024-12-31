from models.model import Model
from models.attack import Attack
from models.defense import Defense

class Benchmark:
    def __init__(self, model: Model, defense: Defense, attack: Attack, results: dict):
        self.model = model
        self.defense = defense
        self.attack = attack
        self.results = results
