import uuid
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class GameTable(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    max_players = Column(Integer)

    players = relationship("Player", back_populates="table")

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    balance = Column(Integer, default=1000)
    table_id = Column(Integer, ForeignKey("tables.id"))

    table = relationship("GameTable", back_populates="players")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("players.id"))
    receiver_id = Column(Integer, ForeignKey("players.id"))
    amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    sender = relationship("Player", foreign_keys=[sender_id], back_populates="sent_transactions")
    receiver = relationship("Player", foreign_keys=[receiver_id], back_populates="received_transactions")

