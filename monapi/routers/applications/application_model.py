from typing import Optional

from pydantic import BaseModel, validator, Field


class Application(BaseModel):
    """
    Modèle en charge de représenter la table Application de la base de données
    """
    id: str = Field(description="identifiant de l'application (alphanumérique)")
    label: str = Field(description="désigne le nom de l'application")
    descriptif: Optional[str] = Field(None, description="description des fonctionnalités de l'application")

    @validator('id')
    def alphanumeric(cls, value):
        assert value.isalnum(), "l'identifiant doit être alphanumerique"
        return value
