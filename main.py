from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.member_meneger import MemberManager

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

member_manager = MemberManager(members)

@app.get("/")
def home():
    return {"Membros": len(members)}

@app.get("/members/{id_member}")
def pegar_membro(id_member: int):
    specific_member = member_manager.get_member(id = id_member)
    return specific_member   

@app.post("/members/")
def criar_membro(membro: Member):
    new_member = member_manager.add_member(membro)
    return new_member


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