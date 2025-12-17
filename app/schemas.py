from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TableCreate(BaseModel):
    name: str
    max_players: int = 8
    access_key: Optional[str] = None

class PlayerCreate(BaseModel):
    user_id: str
    name: str
    table_id: int
    
class Player(BaseModel):
    id: int
    user_id: str
    name: str
    balance: int
    table_id: int

    class Config:
        from_attributes = True
        
class TransactionCreate(BaseModel):
    sender_id: int
    receiver_id: int
    amount: float

class TransactionOut(BaseModel):
    sender: str
    receiver: str
    amount: float
    timestamp: datetime

class PlayerBase(BaseModel):
    name: str

class PlayerCreate(PlayerBase):
    table_id: int

class Player(PlayerBase):
    id: int
    balance: int
    table_id: int
    uuid: str 

    class Config:
        orm_mode = True
