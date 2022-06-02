from typing import List

from .droit_model import Droit
from ..applications.application_model import Application


def get_droits(cur) -> list[Droit]:
    cur.execute("""
                SELECT 
                    id , 
                    label , 
                    descriptif, 
                    id_application  
                FROM droit  
                ORDER BY id_application ; 
                """)
    data = cur.fetchall()
    droits: List[Droit] = [Droit(**item) for item in data]
    return droits


def get_droit(cur, id_application) -> list[Droit]:
    cur.execute("""
                SELECT 
                    id , 
                    label , 
                    descriptif, 
                    id_application 
                FROM droit  
                WHERE id_application = %s 
                ORDER BY label ASC ; 
                """, (id_application,))
    response = cur.fetchall()
    droits: List[Droit] = [Droit(**item) for item in response]
    return droits


def add_droit(cur, droit: Droit, application: Application):
    cur.execute("""
                INSERT INTO 
                    droit (id, label, descriptif, id_application) 
                VALUES (%s, %s, %s, %s) ;
                """, (droit.id, droit.label, droit.descriptif, application.id))


def remove_droit(cur, droit: Droit):
    cur.execute("""
                DELETE 
                FROM droit 
                WHERE id = %s ;
                """, (droit.id,))


def update_droit(cur, id_droit: str, droit: Droit):
    cur.execute("""
                UPDATE droit 
                SET id = %s, label = %s, descriptif = %s, id_application = %s 
                WHERE id = %s ;
                """, (droit.id, droit.label, droit.descriptif, droit.id_application, id_droit))
