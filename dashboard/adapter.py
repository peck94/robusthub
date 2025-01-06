import sqlalchemy as sa
import sqlalchemy.orm as orm

from typing import List

from models import Model, Attack, Defense, Benchmark

class Adapter:
    def __init__(self, url: str):
        self.engine = sa.create_engine(url)

    def _load_table(self, table: sa.Table) -> List:
        stmt = sa.select(table)
        with orm.Session(self.engine) as session:
            rows = session.scalars(stmt)
            return list(rows)

    def load_models(self) -> List[Model]:
        return self._load_table(Model)

    def load_attacks(self) -> List[Attack]:
        return self._load_table(Attack)

    def load_defenses(self) -> List[Defense]:
        return self._load_table(Defense)

    def load_benchmarks(self) -> List[Benchmark]:
        return self._load_table(Benchmark)
