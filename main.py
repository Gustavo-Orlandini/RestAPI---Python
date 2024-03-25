from fastapi import FastAPI, HTTPException, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from src.simulation_events_manager import SimulationEventsManager
from src.member_meneger import MemberManager
from datetime import datetime
from typing import Union
import pandas as pd
import io


# Connect to the PostgreSQL database
conn = psycopg2.connect(
    database="SIOGA TESTE",
    user="postgres",
    password="siogabancoteste",
    host="18.222.58.174",
    port="5432"
)

# Create a cursor object to interact with the database
cur = conn.cursor()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MemberWithAvatar(BaseModel):
    name: str
    lastName: str
    cpf: str
    email: str
    company: str
    role: str
    permission: str
    avatar: str
    active: bool = True

class Member(BaseModel):
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

class SimulationParams(BaseModel):
    indicador: str
    valor:  dict
    id_usuario: str
    data_simulacao: datetime


class SimulationParamsEventos(BaseModel):
    sigla_x: str
    id_tipo: int
    data: datetime
    id_ativo: int
    descricao: str
    sigla_y: str
    valor: float
    id_usuario: str
  
member_manager = MemberManager()


class AnalyticsParams(BaseModel):
    pass


@app.post("/analytics")
def gabriel_function(params: AnalyticsParams):
    return 'ok'



@app.post("/simulation")
def simulator_analitico(params: SimulationParams):
    print(params)

    if isinstance(params.valor, dict):
        for indicador, valor in params.valor.items():
            insert_query = "INSERT INTO fato_analitico (indicador, valor, id_usuario, data_simulacao) VALUES (%s, %s, %s, %s)"
            cur.execute(insert_query, (indicador, valor, params.id_usuario, params.data_simulacao))
            conn.commit()
    else:
        print('Um erro aconteceu')
        pass

    return 'ok'


@app.post("/simulation/events")
async def simulator_events(simulation_file: UploadFile):
        excel_content = simulation_file.file.read()
        excel_file_wrapper = io.BytesIO(excel_content)
        df = pd.read_excel(excel_file_wrapper)
        simulation_events_manager = SimulationEventsManager(df_default = df).process_simulation_file(cur=cur, conn=conn)
        return simulation_events_manager



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
def create_member(member: Member):
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







# SQL query for insertion

# Execute the query with the data   
# cur.execute(insert_query, (data_to_insert['name'], data_to_insert['age'], data_to_insert['city']))

# Commit the changes

# Close communication with the database
# cur.close()
# conn.close()