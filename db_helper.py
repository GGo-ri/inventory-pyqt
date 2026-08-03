import pymysql

# 기본 접속 설정
DB_CONFIG = dict(
  host = "localhost",
  user = "root",
  port = 3307,
  password = "0516",
  database = "jerseydb",
  charset = "utf8mb4",
)

class DB :
  def __init__(self, **config) :
    self.config = config if config else DB_CONFIG

  def connect(self) :
    return pymysql.connect(**self.config)

  # 로그인 검증
  def verify_user(self, username, password) :
    sql = """
        SELECT COUNT(*) AS cnt
        FROM users
        WHERE username = %s AND password = %s
    """
    with self.connect() as conn :
      with conn.cursor() as cur :
        cur.execute(sql, (username, password))
        res = cur.fetchone()
        return res[0] == 1

  # 조회
  def get_jerseys(self, team = "") :
    sql = """
        SELECT id, serial_number, back_number, product_name, jersey_type, stock, price
        FROM jerseys
        WHERE product_name LIKE %s
        ORDER BY back_number ASC
    """
    query_kw = f"%{team}%"
    with self.connect() as conn :
      with conn.cursor() as cur :
        cur.execute(sql, (query_kw,))
        return cur.fetchall()
      
  # 검색
  def search_jerseys(self, team_keyword, search_keyword) :
    sql = """
        SELECT id, serial_number, back_number, product_name, jersey_type, stock, price 
        FROM jerseys 
        WHERE product_name LIKE %s 
          AND (product_name LIKE %s OR serial_number LIKE %s OR CAST(back_number AS CHAR) LIKE %s)
        ORDER BY back_number ASC
    """
    team_kw = f"%{team_keyword}%"
    search_kw = f"%{search_keyword}%"
    with self.connect() as conn :
      with conn.cursor() as cur :
        cur.execute(sql, (team_kw, search_kw, search_kw, search_kw))
        return cur.fetchall()

  # 추가
  def add_jersey(self, serial_number, back_number, product_name, jersey_type, stock, price, is_admin = False) :
    if not is_admin :
      return False

    sql = """
        INSERT INTO jerseys (serial_number, back_number, product_name, jersey_type, stock, price)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    with self.connect() as conn :
      try :
        with conn.cursor() as cur :
          cur.execute(sql, (serial_number, back_number, product_name, jersey_type, stock, price))
        conn.commit()
        return True
      except Exception as e :
        print(f"[Error] 유니폼 등록 실패 : {e}")
        conn.rollback()
        return False

  # 수정
  def update_stock(self, id, new_stock, new_price, is_admin = False) :
    if not is_admin :
      return False

    sql = "UPDATE jerseys SET stock = %s, price = %s WHERE id = %s"
    with self.connect() as conn :
      try :
        with conn.cursor() as cur :
          cur.execute(sql, (new_stock, new_price, id))
        conn.commit()
        return True
      except Exception as e :
        print(f"[Error] 수량 수정 실패 : {e}")
        conn.rollback()
        return False

  # 삭제
  def delete_jersey(self, id, is_admin = False):
    if not is_admin:
        return False

    sql = "DELETE FROM jerseys WHERE id = %s"
    with self.connect() as conn :
      try :
        with conn.cursor() as cur :
          cur.execute(sql, (id,))
        conn.commit()
        return True
      except Exception as e:
        print(f"[Error] 유니폼 삭제 실패 : {e}")
        conn.rollback()
        return False