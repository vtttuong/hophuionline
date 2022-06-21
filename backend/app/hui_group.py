from sqlite3 import Cursor
from typing_extensions import Self
from types import SimpleNamespace as Namespace
import json


class HuiGroup:
  def __init__(
      self,
      owner_id,
      group_name,
      maximum_number,
      hui_type,
      deposit_limit,
      start_date,
      end_date,
      cycle_hui,
      status,
      insurance,
      balance,
      created_date='',
  ):
    self.owner_id = owner_id
    self.group_name = group_name
    self.maximum_number = maximum_number
    self.insurance = insurance
    self.hui_type = hui_type
    self.deposit_limit = deposit_limit
    self.status = status
    self.start_date = start_date
    self.end_date = end_date
    self.cycle_hui = cycle_hui
    self.balance = balance

  def create_hui_group(self, get_db_conn):
    with get_db_conn() as conn:
      cursor = conn.cursor()
      query = f"""
                INSERT INTO hui_group (
                    owner_id, 
                    group_name, 
                    maximum_number, 
                    insurance, 
                    hui_type, 
                    deposit_limit, 
                    status,
                    created_date, 
                    start_date,
                    end_date,
                    cycle_hui, 
                    balance)
                VALUES(
                    {self.owner_id}, 
                    '{self.group_name}',
                    {self.maximum_number}, 
                    '{self.insurance}', 
                    '{self.hui_type}', 
                    {self.deposit_limit}, 
                    '{self.status}', 
                     CURRENT_DATE, 
                     '{self.start_date}',
                     '{self.end_date}',
                     '{self.cycle_hui}', 
                     {self.balance})
                RETURNING ID;
            """
      cursor.execute(query)
      conn.commit()
      group_id = cursor.fetchone()[0]
      self.invite_user(self.owner_id, group_id, get_db_conn, 'JOINED')

  @staticmethod
  def update_user_status_in_group(user_id,hui_id,status,get_db_conn):
    with get_db_conn() as conn:
      cursor = conn.cursor()

      query = f"""
                UPDATE 
                  USERS_IN_GROUP
                SET
                  STATUS = '{status}'
                WHERE
                  USER_ID = {user_id}
                AND
                  HUI_id = {hui_id};
      """      
      cursor.execute(query)


  @staticmethod
  def invite_user(user_id, hui_id, get_db_conn, status='PENDING'):
    with get_db_conn() as conn:
      cursor = conn.cursor()
      query = f"""
                SELECT
                    ID
                FROM 
                    USERS_IN_GROUP
                WHERE
                    USER_ID = {user_id}
                AND
                    HUI_ID = {hui_id}
            """
      cursor.execute(query)
      if cursor.rowcount > 0:
        return False, 'This user already in group'
      else:
        query = f"""
                INSERT INTO USERS_IN_GROUP(
                    USER_ID,
                    HUI_ID,
                    DATE_JOIN,
                    STATUS
                )
                VALUES(
                    {user_id},
                    {hui_id},
                    CURRENT_DATE,
                    '{status}'
                )
                RETURNING id;
                """
        cursor.execute(query)
        return True, cursor.fetchone()[0]

  @staticmethod
  def get_all_users_in_group(hui_id, get_db_conn):
    with get_db_conn() as conn:
      cursor = conn.cursor()
      query = f"""
        SELECT
          *
        FROM 
          USERS_IN_GROUP UIG
        JOIN
          USER_INFO UI
        ON
          UI.ID = UIG.USER_ID
        JOIN
          HUI_GROUP HG
        ON
          HG.ID = UIG.HUI_ID
        WHERE
          HG.ID = {hui_id}
      """
      cursor.execute(query)

      result = list()
      col_name = [desc[0] for desc in cursor.description]
      rows = cursor.fetchall()
      for row in rows:
        user = dict()
        for name in col_name:
          user[name] = row[0]
          row = row[1:]
        result.append(user)
    return result

  @staticmethod
  def get_hui_groups(user_id, get_db_conn):
    result = list()
    with get_db_conn() as conn:
      cursor = conn.cursor()
      query = f"""
                SELECT
                    HG.*,
                    UIG.*,
                    UI.FULL_NAME AS OWNER_NAME
                FROM
                    HUI_GROUP HG
                JOIN
                    USERS_IN_GROUP UIG
                ON
                    HG.ID = UIG.HUI_ID
                JOIN
                    USER_INFO UI
                ON
                    UI.ID = HG.OWNER_ID
                WHERE
                    UIG.USER_ID = {user_id}
            """
      cursor.execute(query)
      col_name = [desc[0] for desc in cursor.description]
      rows = cursor.fetchall()
      for row in rows:
        hui_group = dict()
        for name in col_name:
          hui_group[name] = row[0]
          row = row[1:]
        result.append(hui_group)
    return result

  @staticmethod
  def convert_from_json(request):
    return HuiGroup(
        owner_id=request['owner_id'],
        group_name=request['group_name'],
        maximum_number=request['maximum_number'],
        insurance=request['insurance'],
        hui_type=request['hui_type'],
        deposit_limit=request['deposit_limit'],
        status=request['status'],
        start_date=request['start_date'],
        end_date=request['end_date'],
        cycle_hui=request['cycle_hui'],
        balance=request['balance']
    )
