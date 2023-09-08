class MemberManager:
    def __init__(self, members):
        self.members = members

    def add_member(self, membro):
        novo_id = max(self.members.keys()) + 1
        self.members[novo_id] = membro
        return {"message": "Membro adicionado com sucesso", "novo_id": novo_id}
