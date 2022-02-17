class RefreshToken():
    def __init__(
        self,
        id,
        token
    ):
        self.id = id
        self.token = token

    def to_dict(self):
        return {
            "id": self.id,
            "token": self.token,
        }

    def serialize(self):
        data = self.to_dict()
        return data

    @classmethod
    def from_dict(cls, dict):
        id = dict.get("id")
        token = dict.get("token")
        return RefreshToken(id, token)
