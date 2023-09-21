from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


from src.member_meneger import MemberManager

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Member(BaseModel):
    name: str
    lastName: str
    cpf: str
    email: str
    company: str
    role: str
    permission: str
    avatar: str
    active: bool = True

class Teste(BaseModel):
    name: str
    lastName: str
    cpf: str
    email: str
    company: str
    role: str
    permission: str
    active: bool = True


class MemberForEdit(BaseModel):
    name: str | None = None
    lastName: str | None = None
    cpf: str | None = None
    email: str | None = None
    company: str | None = None
    role: str | None = None
    permission: str | None = None
    avatar: str | None = None

member_manager = MemberManager()

@app.get("/")
def home():
    return member_manager.member_count()


@app.get("/members/{id_member}")
def get_specific_member(id_member: str):
    specific_member = member_manager.get_member(id_member)
    return specific_member  


@app.get("/members/firebase/{id_firebase}")
def get_specific_member_by_firebase_id(id_firebase: str):
    specific_member = member_manager.get_member_by_firebase_id(id_firebase)
    return specific_member  


@app.post("/members/")
def create_member(member: Teste):
    print(member)
    new_member = member_manager.add_member(member.model_dump())
    return new_member


@app.put("/members/{id_member}")
def edit_specific_member(id_member: str, member: MemberForEdit):
    try:
        edited_member = member_manager.edit_member(id_member, member.model_dump())
        return edited_member
    except HTTPException as error:
        raise error
    
    
@app.get("/members/")
def list_all_members(
    name: str | None = None, 
    role: str | None = None, 
    permission: str | None = None,
    company: str | None = None
    ):
    members = member_manager.get_all_members(
        name=name,
        role=role,
        permission=permission,
        company=company
    )
    return members


@app.put("/members/{id_member}/delete")
def delete_member(id_member: str):
    try:
        deleted_member = member_manager.exclude_member(id_member)
        return deleted_member
    except HTTPException as error:
        raise error
    

@app.get("/company/")
def list_all_companys():
    companys = {
        "company": [
            "Ibitu",
            "Eletronorte",
            "Furnas"
        ]
    }
    return companys


@app.get("/role/")
def list_all_roles():
    roles = {
        "role": [
            "Desenvolvedor",
            "Analista",
            "Coordenador",
            "Gerente"
        ]
    }
    return roles


@app.get("/permission/")
def list_all_permissions():
    permissions = {
        "permission": [
            "Cliente",
            "Administrador",
            "Master",
            "Gerente"
        ]
    }
    return permissions

