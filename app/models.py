import uuid
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class GameTable(Base):
    __tablename__ = "game_tables"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    max_players = Column(Integer, default=8)
    access_key = Column(String, nullable=True)

    players = relationship("Player", back_populates="table")

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    balance = Column(Float, default=1000.0)
    table_id = Column(Integer, ForeignKey("game_tables.id"))
    
    uuid = Column(String, default=lambda: str(uuid.uuid4()), unique=True, index=True)

    table = relationship("GameTable", back_populates="players")
    sent_transactions = relationship("Transaction", foreign_keys="Transaction.sender_id", back_populates="sender")
    received_transactions = relationship("Transaction", foreign_keys="Transaction.receiver_id", back_populates="receiver")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("players.id"))
    receiver_id = Column(Integer, ForeignKey("players.id"))
    amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    sender = relationship("Player", foreign_keys=[sender_id], back_populates="sent_transactions")
    receiver = relationship("Player", foreign_keys=[receiver_id], back_populates="received_transactions")

