import sqlalchemy as sa

import json

from typing import Iterable, List

from models.model import Model
from models.attack import Attack
from models.defense import Defense
from models.benchmark import Benchmark

class Adapter:
    def __init__(self, url: str):
        self.engine = sa.create_engine(url)

    def _load_table(self, name: str) -> Iterable:
        with self.engine.connect() as conn:
            rows = conn.execute(sa.text(f'SELECT * FROM {name}'))
        
        return rows

    def load_models(self) -> List[Model]:
        rows = self._load_table('models')
        model_list = []
        for row in rows:
            args = json.loads(row.arguments)
            model_list.append(Model(row.name, row.repo, args))
        
        return model_list

    def load_attacks(self) -> List[Attack]:
        rows = self._load_table('attacks')
        attack_list = []
        for row in rows:
            args = json.loads(row.arguments)
            attack_list.append(Attack(row.name, row.repo, args))
        
        return attack_list

    def load_defenses(self) -> List[Defense]:
        rows = self._load_table('defenses')
        defense_list = []
        for row in rows:
            args = json.loads(row.arguments)
            defense_list.append(Defense(row.name, row.repo, args))
        
        return defense_list

    def load_benchmarks(self) -> List[Benchmark]:
        rows = self._load_table('benchmarks')
        benchmark_list = []
        for row in rows:
            model = None
            defense = None
            attack = None
            results = json.loads(row.results)
            benchmark_list.append(Benchmark(model, defense, attack, results))
        
        return benchmark_list
