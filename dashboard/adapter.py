import sqlalchemy as sa
import sqlalchemy.orm as orm

from typing import List

from models import Base, Model, Attack, Defense, Benchmark

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

    def load_benchmarks(self) -> List[Benchmark]:
        return self._load_table(Benchmark)
    
    def get_benchmarks(self, **kwargs) -> List[Benchmark]:
        conds = ' and '.join([f'{arg} = {kwargs[arg]}' for arg in kwargs])
        stmt = sa.select(Benchmark).where(sa.text(conds))
        with orm.Session(self.engine) as session:
            items = session.scalars(stmt)
        return items
