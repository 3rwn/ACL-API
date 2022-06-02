from typing import List

from fastapi import APIRouter, Path, status, Depends

from monapi.db import get_connection
from .application_model import Application
from ..applications import application_repository
from ..droits.droit_model import Droit
from ...internal.logins.logins import get_current_active_user

router = APIRouter(prefix="/applications", tags=["Applications"], dependencies=[Depends(get_current_active_user)])


@router.get("/", summary="Affiche la liste des applications", response_model=List[Application])
def get_applications():
    with get_connection().cursor() as cur:
        applications = application_repository.get_applications(cur)
    return applications


@router.post("/", summary="Crée une application", status_code=status.HTTP_201_CREATED)
def add_application(application: Application):
    with get_connection().cursor() as cur:
        application_repository.add_application(cur, application)


@router.get("/{id_application}", summary="Affiche une application", response_model=Application)
def get_application(id_application: str = Path(..., title="l'identifiant de l'application")):
    with get_connection().cursor() as cur:
        application = application_repository.get_application(cur, id_application)
        return application


@router.patch("/{id_application}", summary="Modifie une application", status_code=status.HTTP_204_NO_CONTENT)
def update_application(id_application: str, application: Application):
    with get_connection().cursor() as cur:
        application_repository.update_application(cur, id_application, application)


@router.delete("/{id_application}", summary="Supprime une application", status_code=status.HTTP_204_NO_CONTENT)
def remove_application(application: Application):
    with get_connection().cursor() as cur:
        application_repository.remove_application(cur, application)


@router.get("/{id_application}/user/{email}", summary="Affiche les droits d'un utilisateur pour une application",
            response_model=List[Droit])
def get_application(id_application: str = Path(..., title="l'identifiant de l'application"),
                    email: str = Path(..., title="l'email de l'utilisateur")):
    with get_connection().cursor() as cur:
        droits = application_repository.get_droits(cur, email, id_application)
        return droits
