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
def get_specific_member(id_member: int):
    specific_member = member_manager.get_member(id = id_member)
    return specific_member   

@app.post("/members/")
def create_member(membro: Member):
    new_member = member_manager.add_member(membro)
    return new_member


@app.put("/members/{id_member}")
def edit_specific_member(id_member: int, new_datas_member: dict):
    try:
        edited_member = member_manager.edit_member(id_member, new_datas_member)
        return edited_member
    except HTTPException as error:
        raise error
    
    
@app.get("/members/")
def list_all_members():
    members = member_manager.get_all_members()
    return members  


@app.put("/members/{id_member}/delete")
def delete_member(id_member: int):
    if id_member in members:
        members[id_member]["disponivel"] = False
        return {"message": f"Membro de ID {id_member} marcada como não disponível"}
    else:
        raise HTTPException(status_code=404, detail="ID do membro inexistente")