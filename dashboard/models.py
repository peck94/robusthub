import sqlalchemy as sa
import sqlalchemy.orm as orm

from typing import Optional

class Base(orm.DeclarativeBase):
    pass

class Attack(Base):
    __tablename__ = 'attacks'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sa.String(50))
    title: orm.Mapped[str] = orm.mapped_column(sa.String(128))
    repo: orm.Mapped[str] = orm.mapped_column(sa.String(128))
    arguments: orm.Mapped[Optional[str]] = orm.mapped_column(sa.Text())

    def __repr__(self) -> str:
        return f'Attack(id={self.id}, name={self.name}, title={self.title}, repo={self.repo}, arguments={self.arguments})'

class Defense(Base):
    __tablename__ = 'defenses'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sa.String(50))
    title: orm.Mapped[str] = orm.mapped_column(sa.String(128))
    repo: orm.Mapped[str] = orm.mapped_column(sa.String(128))
    arguments: orm.Mapped[Optional[str]] = orm.mapped_column(sa.Text())

    def __repr__(self) -> str:
        return f'Defense(id={self.id}, name={self.name}, title={self.title}, repo={self.repo}, arguments={self.arguments})'

class Model(Base):
    __tablename__ = 'models'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sa.String(50))
    title: orm.Mapped[str] = orm.mapped_column(sa.String(128))
    repo: orm.Mapped[str] = orm.mapped_column(sa.String(128))
    arguments: orm.Mapped[Optional[str]] = orm.mapped_column(sa.Text())

    def __repr__(self) -> str:
        return f'Model(id={self.id}, name={self.name}, title={self.title}, repo={self.repo}, arguments={self.arguments})'

class Dataset(Base):
    __tablename__ = 'datasets'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sa.String(50))
    url: orm.Mapped[str] = orm.mapped_column(sa.String(256))

    def __repr__(self) -> str:
        return f'Dataset(id={self.id}, name={self.name}, url={self.url})'

class Benchmark(Base):
    __tablename__ = 'benchmarks'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    model_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey('models.id'))
    attack_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey('attacks.id'))
    defense_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey('defenses.id'))
    dataset_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey('datasets.id'))

    results: orm.Mapped[str] = orm.mapped_column(sa.Text())

    model: orm.Mapped[Model] = orm.relationship(Model, foreign_keys='Benchmark.model_id', lazy='joined')
    attack: orm.Mapped[Attack] = orm.relationship(Attack, foreign_keys='Benchmark.attack_id', lazy='joined')
    defense: orm.Mapped[Defense] = orm.relationship(Defense, foreign_keys='Benchmark.defense_id', lazy='joined')
    dataset: orm.Mapped[Dataset] = orm.relationship(Dataset, foreign_keys='Benchmark.dataset_id', lazy='joined')

    def __repr__(self) -> str:
        return f'Benchmark(id={self.id}, model={self.model_id}, attack={self.attack_id}, defense={self.defense_id}, results={self.results})'
