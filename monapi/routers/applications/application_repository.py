from typing import List

from .application_model import Application
from ..droits.droit_model import Droit


def get_applications(cur) -> list[Application]:
    cur.execute("""
                SELECT 
                    id, 
                    label, 
                    descriptif 
                FROM application
                ORDER by label;
                """)
    data = cur.fetchall()
    applications: List[Application] = [Application(**item) for item in data]
    return applications


def get_application(cur, id_application: str) -> Application:
    cur.execute("""
                SELECT 
                    id, 
                    label, 
                    descriptif 
                FROM application 
                WHERE id = %s ;
                """, (id_application,))
    application: Application = Application(**cur.fetchone())
    return application


def add_application(cur, application: Application):
    data = (application.id, application.label, application.descriptif)
    cur.execute("""
                INSERT 
                INTO application (id, label, descriptif) 
                VALUES (%s, %s, %s) ;
                """, data)


def update_application(cur, id_application: str, application: Application):
    data = (application.id, application.label, application.descriptif, id_application)
    cur.execute("""
                UPDATE application 
                SET id = %s, label = %s, descriptif = %s 
                WHERE id = %s ;
                """, data)


def remove_application(cur, application: Application):
    cur.execute("""
                DELETE 
                FROM application 
                WHERE id = %s ;
                """, (application.id,))


def get_droits(cur, email: str, id_application: str) -> List[Droit]:
    cur.execute("""
                SELECT 
                    d.id, 
                    d.label,
                    d.descriptif,
                    d.id_application 
                FROM attribution a
                inner JOIN "role" r ON a.id_role = r.id 
                inner JOIN role_droit rd ON r.id = rd.id_role
                inner join droit d on rd.id_droit = d.id 
                WHERE email = %s 
                AND d.id_application = %s 
                """, (email, id_application))
    data = cur.fetchall()
    droits: List[Droit] = [Droit(**item) for item in data]
    return droits
