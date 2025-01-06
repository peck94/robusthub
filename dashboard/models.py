import sqlalchemy as sa
import sqlalchemy.orm as orm

from typing import Optional

class Base(orm.DeclarativeBase):
    pass

class Attack(Base):
    __tablename__ = 'attacks'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sa.String(50))
    repo: orm.Mapped[str] = orm.mapped_column(sa.String(128))
    arguments: orm.Mapped[Optional[str]] = orm.mapped_column(sa.Text())

    def __repr__(self) -> str:
        return f'Attack(id={self.id}, name={self.name}, repo={self.repo}, arguments={self.arguments})'

class Defense(Base):
    __tablename__ = 'defenses'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sa.String(50))
    repo: orm.Mapped[str] = orm.mapped_column(sa.String(128))
    arguments: orm.Mapped[Optional[str]] = orm.mapped_column(sa.Text())

    def __repr__(self) -> str:
        return f'Defense(id={self.id}, name={self.name}, repo={self.repo}, arguments={self.arguments})'

class Model(Base):
    __tablename__ = 'models'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sa.String(50))
    repo: orm.Mapped[str] = orm.mapped_column(sa.String(128))
    arguments: orm.Mapped[Optional[str]] = orm.mapped_column(sa.Text())

    def __repr__(self) -> str:
        return f'Model(id={self.id}, name={self.name}, repo={self.repo}, arguments={self.arguments})'

class Benchmark(Base):
    __tablename__ = 'benchmarks'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    model: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey('models.id'))
    attack: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey('attacks.id'))
    defense: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey('defenses.id'))
    results: orm.Mapped[str] = orm.mapped_column(sa.Text())

    def __repr__(self) -> str:
        return f'Benchmark(id={self.id}, model={self.model}, attack={self.attack}, defense={self.defense}, results={self.results})'
