from pydantic import BaseModel

class TarefaCreate(BaseModel):
    titulo: str
    concluida: bool = False

class TarefaResponse(TarefaCreate):
    id: int
    
    class Config:
        from_attributes = True