from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.member_meneger import MemberManager

app = FastAPI()

class Member(BaseModel):
    nome: str
    cpf: str
    idade: int
    disponivel: bool = True

member_manager = MemberManager()

@app.get("/")
def home():
    return member_manager.member_count()


@app.get("/members/{id_member}")
def get_specific_member(id_member: str):
    specific_member = member_manager.get_member(id_member)
    return specific_member  


@app.post("/members/")
def create_member(member: Member):
    new_member = member_manager.add_member(member.model_dump())
    return new_member


@app.put("/members/{id_member}")
def edit_specific_member(id_member: str, member: Member):
    try:
        edited_member = member_manager.edit_member(id_member, member.model_dump())
        return edited_member
    except HTTPException as error:
        raise error
    
    
@app.get("/members/")
def list_all_members():
    members = member_manager.get_all_members()
    return members  


@app.put("/members/{id_member}/delete")
def delete_member(id_member: str):
    try:
        deleted_member = member_manager.exclude_member(id_member)
        return deleted_member
    except HTTPException as error:
        raise error