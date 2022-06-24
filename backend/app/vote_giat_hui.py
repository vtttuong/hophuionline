import json

class VoteGiatHui:
  def __init__(
    self,
    user_id,
    hui_id,
    amount,
    ki_hui=None,
    created_date=None,
  ):
    self.user_id = user_id
    self.hui_id = hui_id
    self.ki_hui = ki_hui
    self.amount = amount
    self.created_date= created_date

  def vote_giat_hui(self, get_db_conn):

    if self.ki_hui is None:
      r = self.get_ki_hui(self.hui_id, get_db_conn)
      self.ki_hui = r['ki_hui'] if 'ki_hui' in r else 0

    with get_db_conn() as conn:
      cursor = conn.cursor()

      query = f"""
              INSERT INTO vote_giat_hui (
                    user_id,
                    hui_id,
                    ki_hui,
                    amount,
                    created_date)
			        VALUES(
                    {self.user_id},
                    {self.hui_id},
                    {self.ki_hui},
                    {self.amount},
                    {f"{self.created_date}" if self.created_date is not None else 'CURRENT_DATE'}
                     )
                on conflict (user_id, hui_id, ki_hui)
                DO UPDATE SET amount = EXCLUDED.amount
                RETURNING ID;
            """
      cursor.execute(query)
      conn.commit()
      vote_giat_hui_id = cursor.fetchone()[0]

      return {'ID': vote_giat_hui_id}

  @staticmethod
  def get_ki_hui(hui_id, get_db_conn):
    with get_db_conn() as conn:
      cursor = conn.cursor()
      query = f"""
    with dt as (
    select start_date, end_date, cycle_hui,
      case cycle_hui
      when 'Monthly' then 30
      when 'Daily' then 1
      when 'Weekly' then 7
      else 1
      end as inter

      from hui_group hg
      where hg.id = {hui_id}),

    final as
      (select (extract(day from CURRENT_DATE::timestamp - start_date::timestamp) / inter)::int as ki_hui
      from dt
      )
    select case when ki_hui < 0 then 1
		else ki_hui + 1 end
		from final
    """
      cursor.execute(query)
      ki_hui = cursor.fetchone()[0]

    return {'ki_hui': ki_hui}

  @staticmethod
  def get_vote_giat_hui(hui_id, user_id, ki_hui, get_db_conn):
    if ki_hui is None:
      r = VoteGiatHui.get_ki_hui(hui_id, get_db_conn)
      ki_hui = r['ki_hui'] if 'ki_hui' in r else 0

    with get_db_conn() as conn:
      cursor = conn.cursor()
      query = f"""
        SELECT
          VGH.UPDATED_DATE as DATE,
          HG.GROUP_NAME,
          VGH.KI_HUI,
          UI.FULL_NAME as NAME,
          VGH.AMOUNT
        FROM
          VOTE_GIAT_HUI VGH
        JOIN
          USER_INFO UI
        ON
          UI.ID = VGH.USER_ID
        JOIN
          HUI_GROUP HG
        ON
          HG.ID = VGH.HUI_ID
        WHERE
          HG.ID = {hui_id}
          and VGH.KI_HUI = {ki_hui}
          {f"and VGH.ID = {user_id}" if user_id is not None else ''}
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
