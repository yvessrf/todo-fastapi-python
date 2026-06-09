from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from models import TarefaDB
from database import SessionLocal, engine, get_db, Base
import schemas
from sqlalchemy.orm import Session

# Criação do aplicativo FastAPI
app = FastAPI()

# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Minha primeira API com FastAPI!"}

@app.get(

    "/tarefas",
    response_model=list[schemas.TarefaResponse]
)
def listar_tarefas(

    db: Session = Depends(get_db)
):
    return db.query(TarefaDB).all()

   

@app.get(
    "/tarefas/{id}",
    response_model=schemas.TarefaResponse
)
def buscar_tarefa(
    id: int, 
    db: Session = Depends(get_db)
    ):

    tarefa = (
        db.query(TarefaDB)
        .filter(TarefaDB.id == id)
        .first()
    )

  
    if not tarefa:
        raise HTTPException(
            status_code=404,
            detail="Tarefa não encontrada"
        )

    return tarefa

@app.post(
    "/tarefas",
    response_model=schemas.TarefaResponse
)
def criar_tarefa(tarefa: schemas.TarefaCreate,  db: Session = Depends(get_db)):
   
    # Criar uma nova tarefa no banco de dados
    nova_tarefa = TarefaDB(
        titulo=tarefa.titulo,
        concluida=tarefa.concluida
    )
    # Adicionar a nova tarefa à sessão
    db.add(nova_tarefa)
    # Salvar as alterações no banco de dados
    db.commit()
    # Atualizar a tarefa com o ID gerado pelo banco de dados
    db.refresh(nova_tarefa)
   
    return nova_tarefa

@app.put(
    "/tarefas/{id}",
    response_model=schemas.TarefaResponse)

def atualizar_tarefa(
    id: int,
    tarefa_atualizada: schemas.TarefaCreate,
    db: Session = Depends(get_db)
    
):
  

    tarefa = (
        db.query(TarefaDB)
        .filter(TarefaDB.id == id)
        .first()
    )

    if not tarefa:
        db.close()

        raise HTTPException(
            status_code=404,
            detail="Tarefa não encontrada"
        )

    tarefa.titulo = tarefa_atualizada.titulo
    tarefa.concluida = tarefa_atualizada.concluida

    db.commit()

    db.refresh(tarefa)

    db.close()

    return tarefa

@app.delete("/tarefas/{id}",)
def deletar_tarefa(id: int,  db: Session = Depends(get_db)):

  
    tarefa = (
        db.query(TarefaDB)
        .filter(TarefaDB.id == id)
        .first()
    )

    if not tarefa:
        db.close()

        raise HTTPException(
            status_code=404,
            detail="Tarefa não encontrada"
        )

    db.delete(tarefa)

    db.commit()

    db.close()

    return {
        "mensagem": "Tarefa removida com sucesso"
    }