class TransactionLog:
  def __init__(self) -> None:
    pass

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
