

class TransactionLog:
  def __init__(self) -> None:
    pass

  @staticmethod
  def get_all_transaction_by_group(hui_id, get_db_conn):
    with get_db_conn() as conn:
      cursor = conn.cursor()
      query = f"""
        SELECT
          TL.*,
          UI.FULL_NAME,
          UI.EMAIL,
          UI.CREDIT_SCORE,
          UI.PHONE_NUMBER
        FROM 
          TRANSACTION_LOG TL
        JOIN
          USER_INFO UI
        ON
          UI.ID = TL.USER_ID
        WHERE
          HUI_ID = {hui_id}
      """
      cursor.execute(query)

      result = list()
      col_name = [desc[0] for desc in cursor.description]
      rows = cursor.fetchall()
      for row in rows:
        trans = dict()
        for name in col_name:
          trans[name] = row[0]
          row = row[1:]
        result.append(trans)
      return result

  @staticmethod
  def payment(user_id, hui_id, amount, get_db_conn, debtor_id=None):
    with get_db_conn() as conn:
      cursor = conn.cursor()

      if not debtor_id:
        query = f"""
          INSERT INTO
            TRANSACTION_LOG(
              HUI_ID,
              USER_ID,
              TRANSACTION_DATE,
              AMOUNT
            )
          VALUES
          (
            {hui_id},
            {user_id},
            CURRENT_DATE,
            {amount}
          )
          RETURNING ID;
        """
      else:
        query = f"""
          INSERT INTO
            TRANSACTION_LOG(
              HUI_ID,
              USER_ID,
              TRANSACTION_DATE,
              AMOUNT,
              DEBTOR_ID
            )
          VALUES
          (
            {hui_id},
            {user_id},
            CURRENT_DATE,
            {amount},
            {debtor_id}
          )
          RETURNING ID;
        """
      cursor.execute(query)

      query = f"""
        UPDATE 
          HUI_GROUP
        SET 
          BALANCE = BALANCE + {amount}
        WHERE
          ID = {hui_id};
      """
      cursor.execute(query)

      if debtor_id is None:
        query = f"""
          UPDATE
            USER_INFO
          SET
            BALANCE = BALANCE - {amount}
          WHERE
            ID = {user_id}
        """
      else:
        query = f"""
          UPDATE
            USER_INFO
          SET
            BALANCE = BALANCE - {amount}
          WHERE
            ID = {debtor_id}
        """
      cursor.execute(query)
