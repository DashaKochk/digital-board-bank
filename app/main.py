from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine
from fastapi.responses import RedirectResponse

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/create", response_class=HTMLResponse)
def create_table_form(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})

@app.post("/create", response_class=HTMLResponse)
def create_table(request: Request, name: str = Form(...), max_players: int = Form(...), db: Session = Depends(get_db)):
    table = schemas.TableCreate(name=name, max_players=max_players)
    crud.create_table(db, table)
    return RedirectResponse(url="/dashboard", status_code=303)

@app.get("/join", response_class=HTMLResponse)
def join_table_form(request: Request):
    return templates.TemplateResponse("join.html", {"request": request})

@app.post("/join", response_class=HTMLResponse)
def join_table(
    request: Request,
    name: str = Form(...),
    user_id: str = Form(...),
    db: Session = Depends(get_db)
):
    table = crud.get_table_by_name(db, name)
    if not table:
        return RedirectResponse("/dashboard", status_code=302)

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

    return RedirectResponse(url=f"/tables/{table.id}", status_code=303)
    
    player = crud.create_player(db, schemas.PlayerCreate(name="Игрок", table_id=table.id))

    response = RedirectResponse(url=f"/tables/{table.id}", status_code=303)
    response.set_cookie(key="player_uuid", value=player.uuid)
    return response

    return RedirectResponse(url=f"/tables/{table.id}", status_code=303)

@app.post("/api/join_with_uuid")
def join_with_uuid(uuid: str, table_id: int, db: Session = Depends(get_db)):
    player = db.query(models.Player).filter(models.Player.uuid == uuid).first()
    if not player:
        return {"error": "Player not found"}
    player.table_id = table_id
    db.commit()
    return {"success": True, "player_id": player.id}

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    tables = db.query(models.GameTable).all()
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "tables": tables
    })

@app.get("/tables/{table_id}", response_class=HTMLResponse)
def table_page(request: Request, table_id: int, db: Session = Depends(get_db)):
    table = crud.get_table(db, table_id)
    if not table:
        return RedirectResponse("/dashboard", status_code=302)
    return templates.TemplateResponse("table.html", {"request": request, "table": table})

@app.get("/transactions", response_class=HTMLResponse)
def transactions(request: Request, db: Session = Depends(get_db)):
    txs = crud.get_all_transactions(db)
    return templates.TemplateResponse("transactions.html", {"request": request, "transactions": txs})

from fastapi.responses import JSONResponse

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


@app.get("/api/players")
def api_players(db: Session = Depends(get_db)):
    players = db.query(models.Player).all()
    return JSONResponse([{"id": p.id, "name": p.name, "balance": p.balance, "table_id": p.table_id} for p in players])

@app.get("/api/transactions")
def api_transactions(db: Session = Depends(get_db)):
    txs = crud.get_all_transactions(db)
    return JSONResponse([{
        "id": tx.id,
        "sender": tx.sender.name,
        "receiver": tx.receiver.name,
        "amount": tx.amount,
        "timestamp": tx.timestamp.isoformat()
    } for tx in txs])

from fastapi.responses import JSONResponse

@app.get("/api/tables/{table_id}")
def api_table(table_id: int, db: Session = Depends(get_db)):
    table = crud.get_table(db, table_id)

    if table is None:
        return {"error": "Table not found"}

    try:
        players = [
            {
                "id": p.id,
                "name": p.name,
                "balance": p.balance
            }
            for p in table.players
        ]
    except Exception as e:
        return {"error": str(e)}

    return {
        "id": table.id,
        "name": table.name,
        "players": players
    }
