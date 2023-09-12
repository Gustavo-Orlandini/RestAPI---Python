from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.member_meneger import MemberManager

app = FastAPI()

class Member(BaseModel):
    id: int
    nome: str
    cpf: str
    idade: int
    disponivel: bool = True

members = [
{"id": 1, "nome": "Gustavo Suguyama Orlandini", "cpf": "38488266820", "idade": 32, "disponivel": True},
{"id": 2, "nome": "Victor Belarlindo Gomes", "cpf": "33899844890", "idade": 23, "disponivel": True},
{"id": 3, "nome": "Vitin Silva Sauro", "cpf": "32933444323", "idade": 34, "disponivel": True},
{"id": 4, "nome": "João Pedro Cardoso", "cpf": "52299733830", "idade": 31, "disponivel": True},
]

member_manager = MemberManager(members)

@app.get("/")
def home():
    return {"Membros": len(members)}

@app.get("/members/{id_member}")
def get_specific_member(id_member: int):
    specific_member = member_manager.get_member(id_member)
    return specific_member  

@app.post("/members/")
def create_member(membro: Member):
    new_member = member_manager.add_member(membro.model_dump())
    return new_member


@app.put("/members/{id_member}")
def edit_specific_member(id_member: int, membro: Member):
    try:
        edited_member = member_manager.edit_member(id_member, membro.model_dump())
        return edited_member
    except HTTPException as error:
        raise error
    
    
@app.get("/members/")
def list_all_members():
    members = member_manager.get_all_members()
    return members  


@app.put("/members/{id_member}/delete")
def delete_member(id_member: int):
    try:
        deleted_member = member_manager.excluir_membro(id_member)
        return deleted_member
    except HTTPException as error:
        raise error