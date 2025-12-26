from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class GameTable(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    max_players = Column(Integer)
    access_key = Column(String, unique=True, nullable=True)  # <- добавили access_key

    players = relationship("Player", back_populates="table")

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True)
    name = Column(String)
    balance = Column(Integer, default=1000)

    table_id = Column(Integer, ForeignKey("tables.id"))
    table = relationship("GameTable", back_populates="players")

    sent_transactions = relationship(
        "Transaction",
        foreign_keys="Transaction.sender_id",
        back_populates="sender"
    )
    received_transactions = relationship(
        "Transaction",
        foreign_keys="Transaction.receiver_id",
        back_populates="receiver"
    )

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey("players.id"))
    receiver_id = Column(Integer, ForeignKey("players.id"))
    amount = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

    sender = relationship("Player", foreign_keys=[sender_id])
    receiver = relationship("Player", foreign_keys=[receiver_id])
