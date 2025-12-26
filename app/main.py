from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import models, schemas, crud
from app.database import engine, get_db

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    tables = db.query(models.GameTable).all()
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "tables": tables}
    )


@app.get("/create", response_class=HTMLResponse)
def create_table_form(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})


@app.post("/create")
def create_table(
    name: str = Form(...),
    max_players: int = Form(...),
    db: Session = Depends(get_db)
):
    table = schemas.TableCreate(name=name, max_players=max_players)
    crud.create_table(db, table)
    return RedirectResponse("/dashboard", status_code=303)


@app.get("/join", response_class=HTMLResponse)
def join_table_form(request: Request):
    return templates.TemplateResponse("join.html", {"request": request})


@app.post("/join")
def join_table(
    name: str = Form(...),
    user_id: str = Form(...),
    db: Session = Depends(get_db)
):
    table = crud.get_table_by_name(db, name)
    if not table:
        return RedirectResponse("/dashboard", status_code=303)

    player = crud.get_player_by_user_and_table(db, user_id, table.id)
    if not player:
        crud.create_player(
            db,
            schemas.PlayerCreate(
                user_id=user_id,
                name=f"Player-{user_id[:6]}",
                table_id=table.id
            )
        )

    return RedirectResponse(f"/tables/{table.id}", status_code=303)


@app.get("/tables/{table_id}", response_class=HTMLResponse)
def table_page(request: Request, table_id: int, db: Session = Depends(get_db)):
    table = crud.get_table(db, table_id)
    if not table:
        return RedirectResponse("/dashboard", status_code=302)

    return templates.TemplateResponse(
        "table.html",
        {"request": request, "table": table}
    )


@app.get("/transactions", response_class=HTMLResponse)
def transactions_page(request: Request, db: Session = Depends(get_db)):
    transactions = crud.get_all_transactions(db)
    return templates.TemplateResponse(
        "transactions.html",
        {"request": request, "transactions": transactions}
    )

@app.get("/api/tables")
def api_tables(db: Session = Depends(get_db)):
    tables = db.query(models.GameTable).all()
    return [
        {
            "id": t.id,
            "name": t.name,
            "max_players": t.max_players
        }
        for t in tables
    ]


@app.get("/api/tables/{table_id}")
def api_table(table_id: int, db: Session = Depends(get_db)):
    table = crud.get_table(db, table_id)
    if not table:
        return JSONResponse({"error": "Table not found"}, status_code=404)

    players = crud.get_players_by_table(db, table_id)
    return {
        "id": table.id,
        "name": table.name,
        "players": [
            {
                "id": p.id,
                "name": p.name,
                "balance": p.balance
            }
            for p in players
        ]
    }


@app.get("/api/players")
def api_players(db: Session = Depends(get_db)):
    players = db.query(models.Player).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "balance": p.balance,
            "table_id": p.table_id
        }
        for p in players
    ]


# @app.get("/api/transactions")
# def api_transactions(db: Session = Depends(get_db)):
#     txs = crud.get_all_transactions(db)
#     return [
#         {
#             "id": tx.id,
#             "sender": tx.sender.name,
#             "receiver": tx.receiver.name,
#             "amount": tx.amount,
#             "timestamp": tx.timestamp.isoformat()
#         }
#         for tx in txs
#     ]
