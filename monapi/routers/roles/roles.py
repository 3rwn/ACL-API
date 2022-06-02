from typing import List

from fastapi import APIRouter, Path, Depends
from starlette import status
from starlette.responses import Response

from .role_model import Role, DroitApplication
from ..droits.droit_model import Droit
from ..roles import role_repository
from ...db import get_connection
from ...internal.logins.logins import get_current_active_user

router = APIRouter(prefix="/roles", tags=["Rôles"], dependencies=[Depends(get_current_active_user)])


@router.get("/", summary="Affiche la liste des rôles", response_model=List[Role])
def get_roles() -> list[Role]:
    with get_connection().cursor() as cur:
        roles = role_repository.get_roles(cur)
    return roles


@router.get("/{id_role}", summary="Affiche un rôle", response_model=Role)
def get_role(id_role: str = Path(..., title="l'identifiant du rôle")) -> Role:
    with get_connection().cursor() as cur:
        role = role_repository.get_role(cur, id_role)
    return role


@router.post("/", summary="Crée un rôle", status_code=status.HTTP_201_CREATED)
def add_role(role: Role):
    with get_connection().cursor() as cur:
        role_repository.add_role(cur, role)


@router.delete("/{id_role}", summary="Supprime un rôle", status_code=204, response_class=Response)
def remove_role(role: Role):
    with get_connection().cursor() as cur:
        role_repository.remove_role(cur, role)


@router.patch("/{id_role}", summary="Modifie un rôle")
def update_role(id_role: str, role: Role):
    with get_connection().cursor() as cur:
        role_repository.update_role(cur, id_role, role)


@router.get("/{id_role}/droits", summary="Affiche les droits d'un rôle et son application",
            response_model=List[DroitApplication])
def get_droit_role(id_role: str = Path(..., title="l'identifiant du rôle")):
    with get_connection().cursor() as cur:
        role_droit = role_repository.get_droits_role(cur, id_role)
        return role_droit


@router.post("/{id_role}/droits/{id_droit}", summary="Associe un droit à un rôle", status_code=status.HTTP_201_CREATED)
def add_droit_role(droit: Droit, role: Role):
    with get_connection().cursor() as cur:
        role_repository.add_droit_role(cur, droit, role)


@router.delete("/{id_role}/droits/{id_droit}", summary="Retire un droit d'un rôle",
               status_code=status.HTTP_204_NO_CONTENT)
def add_droit_role(droit: Droit, role: Role):
    with get_connection().cursor() as cur:
        role_repository.remove_droit_role(cur, droit, role)
