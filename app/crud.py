from sqlalchemy.orm import Session
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
    return db.query(models.GameTable).filter(models.GameTable.id == table_id).first()

def get_tables(db: Session):
    return db.query(models.GameTable).all()

def get_table_by_name(db: Session, name: str):
    return db.query(models.GameTable).filter(models.GameTable.name == name).first()

def create_player(db: Session, player: schemas.PlayerCreate):
    db_player = models.Player(
        user_id=player.user_id,
        name=player.name,
        table_id=player.table_id
    )
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

def get_player_by_user_and_table(db: Session, user_id: str, table_id: int):
    return (
        db.query(models.Player)
        .filter(
            models.Player.user_id == user_id,
            models.Player.table_id == table_id
        )
        .first()
    )

def get_players_by_table(db: Session, table_id: int):
    return db.query(models.Player).filter(models.Player.table_id == table_id).all()

def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    sender = db.query(models.Player).get(transaction.sender_id)
    receiver = db.query(models.Player).get(transaction.receiver_id)

    if sender and receiver and sender.balance >= transaction.amount:
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

    return None


def get_all_transactions(db: Session):
    return db.query(models.Transaction).all()
