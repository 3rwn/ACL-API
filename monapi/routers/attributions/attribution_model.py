from pydantic import BaseModel, validator


class Attribution(BaseModel):
    """
    Modèle en charge de représenter la table Attribution de la base de données
    """
    email: str
    id_role: str

    @validator('email')
    def email_without_space(cls, value):
        if ' ' in value:
            raise ValueError("L'email ne doit pas contenir d'espace")
        return value

    @validator('id_role')
    def alphanumeric(cls, value):
        assert value.isalnum(), "l'identifiant doit être alphanumerique"
        return value
