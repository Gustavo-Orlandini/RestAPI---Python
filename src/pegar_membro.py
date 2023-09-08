from fastapi import HTTPException

class MemberManager:
    def __init__(self, members):
        self.members = members

    def get_member(self, id):
        if id in self.members and self.members[id]["disponivel"]:
            return self.members[id]
        else:
            raise HTTPException(status_code=404, detail="Membro Indisponível ou não encontrado")
