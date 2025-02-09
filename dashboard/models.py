import sqlalchemy as sa
import sqlalchemy.orm as orm

from typing import Optional, List

class Base(orm.DeclarativeBase):
    pass

class Attack(Base):
    __tablename__ = 'attacks'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sa.String(50))
    title: orm.Mapped[str] = orm.mapped_column(sa.String(128))
    repo: orm.Mapped[str] = orm.mapped_column(sa.String(128))

    def __repr__(self) -> str:
        return f'Attack(id={self.id}, name={self.name}, title={self.title}, repo={self.repo})'

class Defense(Base):
    __tablename__ = 'defenses'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sa.String(50))
    title: orm.Mapped[str] = orm.mapped_column(sa.String(128))
    repo: orm.Mapped[str] = orm.mapped_column(sa.String(128))

    def __repr__(self) -> str:
        return f'Defense(id={self.id}, name={self.name}, title={self.title}, repo={self.repo})'

class Model(Base):
    __tablename__ = 'models'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sa.String(50))
    title: orm.Mapped[str] = orm.mapped_column(sa.String(128))
    repo: orm.Mapped[str] = orm.mapped_column(sa.String(128))

    def __repr__(self) -> str:
        return f'Model(id={self.id}, name={self.name}, title={self.title}, repo={self.repo})'

class Dataset(Base):
    __tablename__ = 'datasets'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    title: orm.Mapped[str] = orm.mapped_column(sa.String(50))
    url: orm.Mapped[str] = orm.mapped_column(sa.String(256))

    def __repr__(self) -> str:
        return f'Dataset(id={self.id}, title={self.title}, url={self.url})'

usecases_benchmarks_table = sa.Table(
    'usecases_benchmarks',
    Base.metadata,
    sa.Column('usecase_id', sa.ForeignKey('usecases.id')),
    sa.Column('benchmark_id', sa.ForeignKey('benchmarks.id')),
)

class Benchmark(Base):
    __tablename__ = 'benchmarks'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    model_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey('models.id'))
    model_args: orm.Mapped[str] = orm.mapped_column(sa.String())

    attack_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey('attacks.id'))
    attack_args: orm.Mapped[str] = orm.mapped_column(sa.String())

    defense_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey('defenses.id'))
    defense_args: orm.Mapped[str] = orm.mapped_column(sa.String())

    dataset_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey('datasets.id'))

    threat_model: orm.Mapped[str] = orm.mapped_column(sa.Text())
    metrics: orm.Mapped[str] = orm.mapped_column(sa.String())
    results: orm.Mapped[str] = orm.mapped_column(sa.Text())

    model: orm.Mapped[Model] = orm.relationship(Model, foreign_keys='Benchmark.model_id', lazy='joined')
    attack: orm.Mapped[Attack] = orm.relationship(Attack, foreign_keys='Benchmark.attack_id', lazy='joined')
    defense: orm.Mapped[Defense] = orm.relationship(Defense, foreign_keys='Benchmark.defense_id', lazy='joined')
    dataset: orm.Mapped[Dataset] = orm.relationship(Dataset, foreign_keys='Benchmark.dataset_id', lazy='joined')

    usecases: orm.Mapped[List['Usecase']] = orm.relationship(secondary=usecases_benchmarks_table, lazy='selectin')

    def __repr__(self) -> str:
        return f'Benchmark(id={self.id}, model={self.model_id}, attack={self.attack_id}, defense={self.defense_id}, results={self.results})'

class Usecase(Base):
    __tablename__ = 'usecases'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    title: orm.Mapped[str] = orm.mapped_column(sa.Text())
    short_description: orm.Mapped[str] = orm.mapped_column(sa.Text())
    full_description: orm.Mapped[str] = orm.mapped_column(sa.Text())
    thumbnail: orm.Mapped[str] = orm.mapped_column(sa.String())

    benchmarks: orm.Mapped[List[Benchmark]] = orm.relationship(secondary=usecases_benchmarks_table, lazy='selectin')

    def __repr__(self) -> str:
        return f'Usecase(id={self.id}, title={self.title}, short_description={self.short_description}, full_description={self.full_description}, thumbnail={self.thumbnail})'
