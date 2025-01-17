import sqlalchemy as sa
import sqlalchemy.orm as orm

from typing import List, Optional

from models import Base, Model, Attack, Defense, Benchmark, Dataset, Usecase

class Adapter:
    def __init__(self, url: str):
        self.engine = sa.create_engine(url)

    def _load_table(self, table: sa.Table) -> List:
        stmt = sa.select(table)
        with orm.Session(self.engine) as session:
            rows = list(session.scalars(stmt))
        return rows
    
    def _get_table(self, table: sa.Table, id: int) -> Base:
        stmt = sa.select(table).where(sa.text(f'id = {id}'))
        with orm.Session(self.engine) as session:
            item = session.scalars(stmt).first()
        return item
    
    def _find_table(self, table: sa.Table, **kwargs) -> Optional[Base]:
        parts = [f'{kw} = "{kwargs[kw]}"' for kw in kwargs if kwargs[kw] is not None]
        stmt = sa.select(table).where(sa.text(' and '.join(parts)))
        with orm.Session(self.engine) as session:
            item = session.scalars(stmt).first()
        return item
    
    def load_usecases(self) -> List[Usecase]:
        return self._load_table(Usecase)

    def load_models(self) -> List[Model]:
        return self._load_table(Model)
    
    def get_model(self, id: int) -> Model:
        return self._get_table(Model, id)

    def load_attacks(self) -> List[Attack]:
        return self._load_table(Attack)
    
    def get_attack(self, id: int) -> Attack:
        return self._get_table(Attack, id)

    def load_defenses(self) -> List[Defense]:
        return self._load_table(Defense)
    
    def get_defense(self, id: int) -> Defense:
        return self._get_table(Defense, id)
    
    def load_datasets(self) -> List[Dataset]:
        return self._load_table(Dataset)
    
    def get_dataset(self, id: int) -> Dataset:
        return self._get_table(Dataset, id)

    def load_benchmarks(self) -> List[Benchmark]:
        return self._load_table(Benchmark)
    
    def get_benchmarks(self, **kwargs) -> List[Benchmark]:
        conds = ' and '.join([f'{arg} = {kwargs[arg]}' for arg in kwargs])
        stmt = sa.select(Benchmark).where(sa.text(conds))
        with orm.Session(self.engine) as session:
            items = list(session.scalars(stmt))
        return items

    def save_benchmark(self, model: Model, dataset: Dataset, threat: str, defense: Defense, attack: Attack, results: str):
        model = self._find_table(Model,
                                 name=model.name,
                                 repo=model.repo,
                                 arguments=model.arguments)
        attack = self._find_table(Attack,
                                 name=attack.name,
                                 repo=attack.repo,
                                 arguments=attack.arguments)
        defense = self._find_table(Defense,
                                 name=defense.name,
                                 repo=defense.repo,
                                 arguments=defense.arguments)
        dataset = self._find_table(Dataset,
                                   title=dataset.title,
                                   url=dataset.url)

        with orm.Session(self.engine) as sess:
            benchmark = Benchmark(
                model_id=model.id,
                defense_id=defense.id,
                attack_id=attack.id,
                dataset_id=dataset.id,
                threat_model=threat,
                results=results
            )
            sess.add(benchmark)
            sess.commit()
