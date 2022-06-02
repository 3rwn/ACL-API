from typing import List

from fastapi import APIRouter, Path, Depends
from starlette import status

from monapi.db import get_connection
from ..attributions import attribution_repository
from .attribution_model import Attribution
from ..roles.role_model import Role
from ...internal.logins.logins import get_current_active_user

router = APIRouter(prefix="/attributions", tags=["Attributions"], dependencies=[Depends(get_current_active_user)])


@router.get("/", summary="Affiche la liste des utilisateurs et leurs rôles", response_model=List[Attribution])
def get_attributions() -> list[Attribution]:
    with get_connection().cursor() as cur:
        attributions = attribution_repository.get_attributions(cur)
    return attributions


@router.get("/{email}", summary="Affiche la liste des rôles d'un utilisateur",
            description="exemple = exemple@gmail.com", response_model=List[Role])
def get_attribution(email: str = Path(..., title="l'email de l'utilisateur")) -> list[Role]:
    with get_connection().cursor() as cur:
        roles = attribution_repository.get_attribution(cur, email)
    return roles


@router.post("/{email}", summary="Attribue un rôle à un utilisateur", status_code=status.HTTP_201_CREATED)
def add_attribution(attribution: Attribution):
    with get_connection().cursor() as cur:
        attribution_repository.add_attribution(cur, attribution)


@router.delete("/{email}", summary="Retire un rôle à un utilisateur", status_code=status.HTTP_204_NO_CONTENT)
def remove_attribution(attribution: Attribution):
    with get_connection().cursor() as cur:
        attribution_repository.remove_attribution(cur, attribution)
