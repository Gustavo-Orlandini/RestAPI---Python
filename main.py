from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Venda(BaseModel):
    item: str
    preco_unitario: float
    quantidade: int

vendas = {
    1: {"item": "garrafa 2l", "preco_unitario": 9, "quantidade": 3},
    2: {"item": "garrafa 1.5l", "preco_unitario": 8, "quantidade": 6},
    3: {"item": "lata 350ml", "preco_unitario": 3.9, "quantidade": 4},
    4: {"item": "garrafa 600ml", "preco_unitario": 5, "quantidade": 11},
}

@app.get("/")
def home():
    return {"Vendas": len(vendas)}

@app.get("/vendas/{id_venda}")
def pegar_venda(id_venda: int):
    if id_venda in vendas:  
        return vendas[id_venda]
    else:
        raise HTTPException(status_code=404, detail="ID da venda inexistente")

@app.post("/vendas/")
def criar_venda(venda: Venda):
    nova_id = max(vendas.keys()) + 1
    vendas[nova_id] = venda.model_dump()
    return {"message": "Venda adicionada com sucesso", "nova_id": nova_id}

@app.put("/vendas/{id_venda}")
def editar_venda(id_venda: int, venda: Venda):
    if id_venda in vendas:
        vendas[id_venda] = venda.model_dump()
        return {"message": f"Venda ID {id_venda} editada com sucesso"}
    else:
        raise HTTPException(status_code=404, detail="ID da venda inexistente")