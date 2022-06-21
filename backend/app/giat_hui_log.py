import json

class GiatHuiLog:
  def __init__(
    self,
    user_id,
    hui_id,
    ki_hui,
    amount,
    created_date=None,
  ):
    self.user_id = user_id
    self.hui_id = hui_id
    self.ki_hui = ki_hui
    self.amount = amount
    self.created_date= created_date


  def giat_hui(self, get_db_conn):
    with get_db_conn() as conn:
      cursor = conn.cursor()
      query = f"""
                INSERT INTO giat_hui_log (
                    user_id,
                    hui_id,
                    ki_hui,
                    amount,
                    created_date)
                VALUES(
                    {self.user_id},
                    '{self.hui_id}',
                    {self.ki_hui},
                    '{self.amount}',
                    {f"{self.created_date}" if self.created_date is not None else 'CURRENT_DATE'}
                     )
                RETURNING ID;
            """
      cursor.execute(query)
      conn.commit()
      giat_hui_log_id = cursor.fetchone()[0]

      return {'ID': giat_hui_log_id}

  @staticmethod
  def get_giat_hui_log(hui_id, get_db_conn):
    with get_db_conn() as conn:
      cursor = conn.cursor()
      query = f"""
        SELECT
          GHL.CREATED_DATE as DATE,
          GHL.KI_HUI, UI.FULL_NAME as NAME,
          GHL.AMOUNT
        FROM
          GIAT_HUI_LOG GHL
        JOIN
          USER_INFO UI
        ON
          UI.ID = GHL.USER_ID
        JOIN
          HUI_GROUP HG
        ON
          HG.ID = GHL.HUI_ID
        WHERE
          HG.ID = {hui_id}
      """
      cursor.execute(query)

      result = list()
      col_name = [desc[0] for desc in cursor.description]
      rows = cursor.fetchall()
      for row in rows:
        r = dict()
        for k, v in zip(col_name, row):
          r[k] = v
        result.append(r)
    return result
