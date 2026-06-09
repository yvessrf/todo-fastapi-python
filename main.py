from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models import TarefaDB
from database import SessionLocal, engine
import schemas

# Criação do aplicativo FastAPI
app = FastAPI()

# Criar as tabelas no banco de dados
TarefaDB.metadata.create_all(bind=engine)

class Tarefa(BaseModel):
    id: int
    titulo: str
    concluida: bool = False

tarefas = []

@app.get("/")
def home():
    return {"message": "Minha primeira API com FastAPI!"}

@app.get(

    "/tarefas",
    response_model=list[schemas.TarefaResponse]
)
def listar_tarefas():

    db = SessionLocal()

    tarefas = db.query(TarefaDB).all()

    db.close()

    return tarefas

@app.get("/tarefas/{id}")
def buscar_tarefa(id: int):
    for tarefa in tarefas:
        if tarefa["id"] == id:
            return tarefa
    
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")

@app.post(
    "/tarefas",
    response_model=schemas.TarefaResponse
)
def criar_tarefa(tarefa: schemas.TarefaCreate):
    # Criar uma nova sessão de banco de dados
    db = SessionLocal()
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
    # Fechar a sessão de banco de dados
    db.close()

    return nova_tarefa

@app.put("/tarefas/{id}")
def atualizar_tarefa(id: int, tarefa_atualiza: Tarefa):
    for tarefa in tarefas:
        if tarefa["id"] == id:
            tarefa["titulo"] = tarefa_atualiza.titulo
            tarefa["concluida"] = tarefa_atualiza.concluida
            return tarefa
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")

@app.delete("/tarefas/{id}")
def deletar_tarefa(id:int):
    for indice, tarefa in enumerate(tarefas):
        if tarefa["id"] == id:
            tarefa_removida = tarefas.pop(indice)
            
            return {"mensagem": "Tarefa deletada com sucesso", "tarefa": tarefa_removida
                    }
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")