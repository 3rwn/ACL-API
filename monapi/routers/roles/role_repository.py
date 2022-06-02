from typing import List

from .role_model import Role, DroitApplication
from ..applications.application_model import Application
from ..droits.droit_model import Droit


def get_roles(cur) -> list[Role]:
    cur.execute("""
                SELECT 
                    id, 
                    label, 
                    descriptif 
                FROM role
                ORDER BY label ;
                """)
    data = cur.fetchall()
    roles: List[Role] = [Role(**item) for item in data]
    return roles


def get_role(cur, id_role) -> Role:
    cur.execute("""
                SELECT 
                    id, 
                    label, 
                    descriptif 
                FROM role 
                WHERE id = %s ;
                """, (id_role,))
    role: Role = Role(**cur.fetchone())
    return role


def add_role(cur, role: Role):
    cur.execute("""
                INSERT 
                INTO role (id, label, descriptif) 
                VALUES (%s, %s, %s) ;
                """, (role.id, role.label, role.descriptif))


def remove_role(cur, role: Role):
    cur.execute("""
                DELETE 
                FROM role 
                WHERE id = %s ;
                """, (role.id,))


def update_role(cur, id_role: str, role: Role):
    data = (role.id, role.label, role.descriptif, id_role)
    cur.execute("""
                UPDATE role 
                SET id = %s, label = %s, descriptif = %s 
                WHERE id = %s ;
                """, data)


def add_droit_role(cur, droit: Droit, role: Role):
    cur.execute("""
                INSERT 
                INTO role_droit (id_role, id_droit) 
                VALUES (%s, %s) ;
                """, (role.id, droit.id))


def get_droits_role(cur, id_role: str):
    cur.execute("""
            SELECT 
                d.id as droit_id, 
                d.label as droit_label, 
                d.descriptif as droit_descriptif, 
                d.id_application as droit_id_application,
                 
                a.id as application_id, 
                a.label as application_label, 
                a.descriptif as application_descriptif
                
            FROM role_droit rd 
            LEFT JOIN droit d ON d.id = rd.id_droit 
            INNER JOIN application a ON d.id_application = a.id 
            WHERE rd.id_role = %s ;
        """, (id_role,))
    data = cur.fetchall()
    droits: List[DroitApplication] = [
        DroitApplication(
            droit=Droit(
                id=item['droit_id'],
                label=item['droit_label'],
                descriptif=item['droit_descriptif'],
                id_application=item['droit_id_application'],
            ),
            application=Application(
                id=item['application_id'],
                label=item['application_label'],
                descriptif=item['application_descriptif'], )
        )
        for item in data
    ]
    return droits


def remove_droit_role(cur, droit, role):
    cur.execute("""
                DELETE 
                FROM role_droit 
                WHERE id_droit = %s 
                AND id_role = %s ;
                """, (droit.id, role.id))
