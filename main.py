from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Member(BaseModel):
    nome: str
    cpf: int
    idade: int
    disponivel: bool = True

members = {
    1: {"nome": "Gustavo Suguyama Orlandini", "cpf": 38488266820, "idade": 32, "disponivel": True},
    2: {"nome": "Victor Belarlindo Gomes", "cpf": 33899844890, "idade": 61, "disponivel": True},
    3: {"nome": "Vitin Silva Sauro", "cpf": 32933444323, "idade": 43, "disponivel": True},
    4: {"nome": "João Pedro Cardoso", "cpf": 52299733830, "idade": 19, "disponivel": True},
}

@app.get("/")
def home():
    return {"Membros": len(members)}

@app.get("/members/{id_member}")
def pegar_membro(id_member: int):
    if id_member in members and members[id_member]["disponivel"]:
        return members[id_member]
    else:
        raise HTTPException(status_code=404, detail="Membro Indisponível ou não encontrado")
    

@app.post("/members/")
def criar_membro(membro: Member):
    novo_id = max(members.keys()) + 1
    members[novo_id] = membro.model_dump()
    return {"message": "Membro adicionada com sucesso", "novo_id": novo_id}


@app.put("/members/{id_member}")
def editar_membro(id_member: int, membro: Member):
    if id_member in members:
        members[id_member] = membro.model_dump()
        return {"message": f"Membro de ID {id_member} editado com sucesso"}
    else:
        raise HTTPException(status_code=404, detail="ID do membro inexistente")
    
    
@app.get("/members/")
def listar_membros():
    membros_disponiveis = {k: v for k, v in members.items() if v["disponivel"]}
    return {"Vendas disponíveis": membros_disponiveis}    


@app.put("/members/{id_member}/delete")
def delete_venda(id_member: int):
    if id_member in members:
        members[id_member]["disponivel"] = False
        return {"message": f"Membro de ID {id_member} marcada como não disponível"}
    else:
        raise HTTPException(status_code=404, detail="ID do membro inexistente")