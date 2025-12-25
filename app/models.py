from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class GameTable(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    max_players = Column(Integer)

    players = relationship(
        "Player",
        back_populates="table",
        cascade="all, delete"
    )


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    balance = Column(Integer, default=1000)

    table_id = Column(Integer, ForeignKey("tables.id"))
    table = relationship("GameTable", back_populates="players")
