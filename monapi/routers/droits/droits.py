from typing import List

from fastapi import APIRouter, Path, Depends
from starlette import status

from monapi.db import get_connection
from ..applications.application_model import Application
from ..droits import droit_repository
from .droit_model import Droit
from ...internal.logins.logins import get_current_active_user

router = APIRouter(prefix="/droits", tags=["Droits"], dependencies=[Depends(get_current_active_user)])


@router.get("/", summary="Affiche la liste des droits des applications", response_model=List[Droit])
def get_droits() -> list[Droit]:
    with get_connection().cursor() as cur:
        droits = droit_repository.get_droits(cur)
    return droits


@router.get("/{id_application}", summary="Affiche la liste des droits d'une application", response_model=List[Droit])
def get_application_droits(id_application: str = Path(..., title="l'identifiant de l'application")) -> list[Droit]:
    with get_connection().cursor() as cur:
        droits = droit_repository.get_droit(cur, id_application)
    return droits


@router.post("/{id_application}", summary="Crée un droit pour une application", status_code=status.HTTP_201_CREATED)
def add_droit(droit: Droit, application: Application):
    with get_connection().cursor() as cur:
        droit_repository.add_droit(cur, droit, application)


@router.delete("/{id_application}", summary="Supprime un droit d'application", status_code=status.HTTP_204_NO_CONTENT)
def remove_droit(droit: Droit):
    with get_connection().cursor() as cur:
        droit_repository.remove_droit(cur, droit)


@router.patch("/{id_application}/{id_droit}", summary="Modifie un droit d'une application", status_code=status.HTTP_204_NO_CONTENT)
def update_droit(id_droit, droit: Droit):
    with get_connection().cursor() as cur:
        droit_repository.update_droit(cur, id_droit, droit)
