from typing import List

from .attribution_model import Attribution
from ..roles.role_model import Role


def get_attributions(cur) -> list[Attribution]:
    cur.execute("""
                SELECT 
                    email, 
                    id_role 
                FROM attribution 
                ORDER BY email, id_role ASC ;
                """)
    data = cur.fetchall()
    attributions: List[Attribution] = [Attribution(**item) for item in data]
    return attributions


def get_attribution(cur, email) -> list[Role]:
    cur.execute("""
                SELECT  
                    r.id, 
                    r.label, 
                    r.descriptif 
                FROM attribution a 
                LEFT JOIN role r ON r.id = a.id_role 
                WHERE email = %s ; 
                """, (email,))
    resp = cur.fetchall()
    roles: List[Role] = [Role(**item) for item in resp]
    return roles


def add_attribution(cur, attribution: Attribution):
    cur.execute("""
                INSERT INTO 
                    attribution (email, id_role) 
                VALUES (%s, %s) ;
                """, (attribution.email, attribution.id_role))


def remove_attribution(cur, attribution: Attribution):
    cur.execute("""
                DELETE 
                FROM attribution 
                WHERE email = %s 
                AND id_role = %s ;
                """, (attribution.email, attribution.id_role))
