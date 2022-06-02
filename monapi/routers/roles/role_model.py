from typing import Optional

from pydantic import BaseModel, validator

from monapi.routers.applications.application_model import Application
from monapi.routers.droits.droit_model import Droit


class Role(BaseModel):
    """
    Modèle en charge de représenter la table Role de la base de données
    """
    id: str
    label: str
    descriptif: Optional[str] = None

    @validator('id')
    def alphanumeric(cls, value):
        assert value.isalnum(), "l'identifiant doit être alphanumerique"
        return value


class DroitApplication(BaseModel):
    """
    Modèle en charge de représenter un droit  et l'application auquel il appartient
    """
    droit: Droit
    application: Application

