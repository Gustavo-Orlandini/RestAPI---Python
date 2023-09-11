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
    
    
    def edit_member(self, id_member, new_datas_member):
        if id_member in self.members:
            membro = self.members[id_member]
            for campo, valor in new_datas_member.items():
                membro[campo] = valor
            return {"message": f"Membro de ID {id_member} editado com sucesso"}
        else:
            raise HTTPException(status_code=404, detail="ID do membro inexistente")