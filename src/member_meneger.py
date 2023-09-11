from fastapi import HTTPException

class MemberManager:
    def __init__(self, members):
        self.members = members

    def get_member(self, id):
        if id in self.members and self.members[id]["disponivel"]:
            return self.members[id]
        else:
            raise HTTPException(status_code=404, detail="Membro Indisponível ou não encontrado")


    def add_member(self, membro):
        novo_id = max(self.members.keys()) + 1
        self.members[novo_id] = membro
        return {"message": "Membro adicionado com sucesso", "novo_id": novo_id}
    
    
    def edit_member(self, id_member, novos_dados):
        if id_member in self.members:
            membro = self.members[id_member]
            for campo, valor in novos_dados.items():
                if campo in membro:
                    membro[campo] = valor
                else:
                    raise HTTPException(status_code=400, detail="Campo incorreto ou inexistente")
            return {"message": f"Membro de ID {id_member} editado com sucesso"}
        else:
            raise HTTPException(status_code=404, detail="ID do membro inexistente")
        

    def get_all_members(self):
        active_members = {k: v for k, v in self.members.items() if v["disponivel"] == True}
        return {"Membros disponíveis": active_members}