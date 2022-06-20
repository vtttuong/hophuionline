
from unittest import result

import json

import json
def get_user_info(user_id,get_db_conn):
    result = []
    with get_db_conn() as conn:
        cursor = conn.cursor()
        query = f"""
            SELECT
                *
            FROM
                USER_INFO
            WHERE
                ID = {user_id}
        """
        cursor.execute(query)
        row = cursor.fetchone()
        
    return test