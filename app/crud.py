from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas

def create_table(db: Session, table: schemas.TableCreate):
    db_table = models.GameTable(
        name=table.name,
        max_players=table.max_players,
        access_key=table.access_key
    )
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table

def get_table(db: Session, table_id: int):
    table = db.query(models.GameTable).filter(models.GameTable.id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    return table

def get_table_by_name(db: Session, name: str):
    return db.query(models.GameTable).filter(models.GameTable.name == name).first()

def get_tables(db: Session):
    return db.query(models.GameTable).all()

def create_player(db: Session, player: schemas.PlayerCreate):
    table = db.query(models.GameTable).filter(models.GameTable.id == player.table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found for player")
    
    db_player = models.Player(name=player.name, table_id=player.table_id)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

def get_players_by_table(db: Session, table_id: int):
    return db.query(models.Player).filter(models.Player.table_id == table_id).all()

def get_player(db: Session, player_id: int):
    player = db.query(models.Player).filter(models.Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    sender = db.get(models.Player, transaction.sender_id)
    receiver = db.get(models.Player, transaction.receiver_id)

    if not sender or not receiver:
        raise HTTPException(status_code=404, detail="Sender or receiver not found")
    if sender.balance < transaction.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    sender.balance -= transaction.amount
    receiver.balance += transaction.amount

    db_tx = models.Transaction(
        sender_id=sender.id,
        receiver_id=receiver.id,
        amount=transaction.amount
    )
    db.add(db_tx)
    db.commit()
    db.refresh(db_tx)
    return db_tx

def get_all_transactions(db: Session):
    return db.query(models.Transaction).all()
