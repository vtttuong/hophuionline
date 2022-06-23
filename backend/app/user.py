

class UserInfo:
  def __init__(
      self,
      full_name,
      phone_number,
      email,
      credit_score,
      balance,
      password
  ):
    self.full_name = full_name
    self.phone_number = phone_number
    self.email = email
    self.credit_score = credit_score
    self.balance = balance
    self.password = password

  def create_user(self, get_db_conn):
    with get_db_conn() as conn:
      cursor = conn.cursor()
      query = f"""
            INSERT INTO user_info
                (
                    full_name, 
                    phone_number, 
                    email, 
                    credit_score, 
                    balance, 
                    "password")
            VALUES(
                '{self.full_name}', 
                '{self.phone_number}', 
                '{self.email}',
                {self.credit_score},
                {self.balance},
                '{self.password}'
            );
            """
      cursor.execute(query)

  @staticmethod
  def withdraw_money(user_id, hui_id, amount, get_db_conn):
    with get_db_conn() as conn:
      query = f"""
        UPDATE
          USERS_IN_GROUP
        SET 
          withdrawal_amount = {amount},
          withdrawal_date = CURRENT_DATE
        WHERE
          user_id = {user_id}
        AND
          hui_id = {hui_id};
      """
      cursor = conn.cursor()
      cursor.execute(query)

      query = f"""
        UPDATE 
          USER_INFO
        SET
          BALANCE = BALANCE + {amount}
        WHERE
          id = {user_id};
      """
      cursor.execute(query)

      query = f"""
        UPDATE
          HUI_GROUP
        SET
          BALANCE = BALANCE - {amount}
        WHERE
          ID = {hui_id}
      """
      cursor.execute(query)

  @staticmethod
  def find_user_by_phone_number(phone_number, get_db_conn):
    with get_db_conn() as conn:
      query = f"""
        SELECT
          *
        FROM
          USER_INFO
        WHERE
          PHONE_NUMBER LIKE '%{phone_number}%';
      """
      cursor = conn.cursor()
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
  def convert_from_json(request):
    return UserInfo(
        full_name=request['full_name'],
        phone_number=request['phone_number'],
        email=request['email'],
        credit_score=request['credit_score'],
        balance=request['balance'],
        password=request['password']
    )

  @staticmethod
  def get_user_info(user_id, get_db_conn):
    result = dict()
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
      col_name = [desc[0] for desc in cursor.description]

      row = cursor.fetchone()
    for name, value in zip(col_name, row):
      result[name] = value
    return result

  @staticmethod
  def check_dong_tien(user_id, hui_id, get_db_conn):
    with get_db_conn() as conn:
      cursor = conn.cursor()
      query = f"""
        SELECT 
          max(transaction_date),
          current_date
        FROM 
          transaction_log tl 
        where 
          user_id = {user_id} 
        and 
          hui_id = {hui_id}  
      """
      cursor.execute(query)
      last_date = cursor.fetchone()

    return last_date[0] == last_date[1]
