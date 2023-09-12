from fastapi import HTTPException
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
import os
from bson import ObjectId 


MONGO_CONNECTION_STRING=os.getenv("MONGO_CONNECTION_STRING")
mongo = MongoClient(MONGO_CONNECTION_STRING)["dev"]["members"]

class MemberManager:
    def __init__(self):
        pass


    def member_count(self):
        return mongo.count_documents({})
        

    def get_member(self, id):
        specific_member = mongo.find_one({"_id": ObjectId(id)})
        if not specific_member:
            raise HTTPException(status_code=404, detail="ID incorreto ou inexistente")
        else:
            return {**specific_member, "_id": str(specific_member["_id"])}


    def add_member(self, member):
        mongo.insert_one(member)
        return {"message": "Membro adicionado com sucesso"}
    
    
    def edit_member(self, id_member, new_datas_member):
        for member in self.members:
            if member["id"] == id_member:
                for campo, valor in new_datas_member.items():
                    if campo in member:
                        member[campo] = valor
                    else:
                        raise HTTPException(status_code=400, detail="Campo incorreto ou inexistente")
                return {"message": f"Membro de ID {id_member} editado com sucesso"}
        raise HTTPException(status_code=404, detail="ID do membro inexistente")
        

    def get_all_members(self):
        active_members = [member for member in self.members if member["disponivel"] == True]
        return {"Membros disponíveis": active_members}
    
    
    def excluir_membro(self, id_member):
        for member in self.members:
            if member["id"] == id_member:
                if member["disponivel"] == True:
                    member["disponivel"] = False
                    return {"message": f"Membro de ID {id_member} marcado como não disponível"}
                else:
                    raise HTTPException(status_code=400, detail=f"Membro de ID {id_member} já está marcado como não disponível")
        raise HTTPException(status_code=404, detail="ID do membro inexistente")