from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .internal.logins import logins
from .routers.applications import applications
from .routers.attributions import attributions
from .routers.roles import roles
from .routers.droits import droits

from .db import get_connection
from .db import init_connection, close_connection

tags_metadata = [
    {"name": "Applications", "description": "gestion des applications"},
    {"name": "Droits", "description": "gestion des droits des applications"},
    {"name": "Rôles", "description": "gestion des rôles"},
    {"name": "Attributions", "description": "gestion de l'attribution des rôles des utilisateurs"},
    {"name": "Login"}
]

description = "ACL API aide à la gestion des droits et accès des utilisateurs aux diverses applications."
app = FastAPI(title="AccessControlListApp",
              description=description,
              version="0.0.1")

@app.exception_handler(Exception)
async def value_error_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )


@app.on_event("startup")
def startup_event():
    init_connection()
    get_connection().set_session(autocommit=True)


@app.on_event("shutdown")
def shutdown_event():
    close_connection()


app.include_router(logins.router)
app.include_router(applications.router)
app.include_router(attributions.router)
app.include_router(droits.router)
app.include_router(roles.router)


app = CORSMiddleware(
    app=app,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
