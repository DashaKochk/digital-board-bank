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

def get_all_transactions(db: Session):
    return (
        db.query(models.Transaction)
        .order_by(models.Transaction.timestamp.desc())
        .all()
    )

def transfer_money(
    db: Session,
    sender_id: int,
    receiver_id: int,
    amount: int
):
    sender = db.query(models.Player).get(sender_id)
    receiver = db.query(models.Player).get(receiver_id)

    if not sender or not receiver:
        return None

    if sender.balance < amount or amount <= 0:
        return None

    sender.balance -= amount
    receiver.balance += amount

    tx = models.Transaction(
        sender_id=sender.id,
        receiver_id=receiver.id,
        amount=amount
    )

    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx
