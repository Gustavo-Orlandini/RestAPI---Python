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
        if not self.members:
            novo_id = 1
        else:
            novo_id = max([x[“id”] for x in self.members]) + 1
        membro["id"] = novo_id
        self.members.append(membro)
        return {"message": "Membro adicionado com sucesso", "novo_id": novo_id}
    
    
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