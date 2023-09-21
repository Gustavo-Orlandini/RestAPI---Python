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
        

    def get_member_by_firebase_id(self, id):
        specific_firebase_member = mongo.find_one({"_id_firebase": id})
        if not specific_firebase_member:
            raise HTTPException(status_code=404, detail="ID incorreto ou inexistente")
        else:
            return {**specific_firebase_member, "_id": str(specific_firebase_member["_id"])}    


    def add_member(self, member):
        mongo.insert_one(member)
        return {"message": "Membro adicionado com sucesso"}
    
    
    def edit_member(self, id_member, new_datas_member):
        specific_member = mongo.find_one({"_id": ObjectId(id_member)})
        if not specific_member:
            raise HTTPException(status_code=404, detail="ID incorreto ou inexistente")
        for campo, valor in new_datas_member.items():
            if valor == None:
                continue
            if campo in specific_member:
                specific_member[campo] = valor
            else:
                raise HTTPException(status_code=400, detail="Campo incorreto ou inexistente")
        mongo.update_one({"_id": ObjectId(id_member)}, {"$set": specific_member})    
        return {"message": f"Membro de ID {id_member} editado com sucesso"}
        

    def get_all_members(self, **kwargs):
        filters = {key: value for key, value in kwargs.items() if value is not None}
        role = kwargs['role']
        permission = kwargs['permission']
        company = kwargs['company']
        search_term = kwargs['name']
        query = {
            "$and": [
                {
                    "$or": [
                        {"name": {"$regex": search_term, "$options": "i"}},
                        {"lastName": {"$regex": search_term, "$options": "i"}}
                    ]
                } if search_term else {},
                {"role": role} if role else {},
                {"permission": permission} if permission else {},
                {"company": company} if company else {},
                {'active': True}
            ]
        }
        if filters:
            active_members = list(map(lambda member: {
                **member,
                "_id": str(member["_id"]),
            }, mongo.find(query)))
        else:
            active_members = list(map(lambda member: {
                **member,
                "_id": str(member["_id"]),
            }, mongo.find({"active": True})))

        return active_members
    
    
    def exclude_member(self, id_member):
        result = mongo.update_one({"_id": ObjectId(id_member)}, {"$set": {"active": False}})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="ID do membro inexistente")
        if result.modified_count == 0:
            raise HTTPException(status_code=500, detail="Erro ao excluir o membro")
        return {"message": f"Membro de ID {id_member} excluido com sucesso"}