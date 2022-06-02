from typing import Optional

from pydantic import BaseModel, validator


class Droit(BaseModel):
    """
    Modèle en charge de représenter la table Droit de la base de données
    """
    id: str
    label: str
    descriptif: Optional[str]
    id_application: Optional[str]

    @validator('id')
    def alphanumeric(cls, value):
        assert value.isalnum(), "l'identifiant doit être alphanumerique"
        return value
