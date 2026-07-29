import pymysql

# 기본 접속 설정
DB_CONFIG = dict(
  host = "localhost",
  user = "root",
  port = 3307,
  password = "0516",
  database = "jerseydb",
  charset = "utf8mb4",
  cursorclass = pymysql.cursors.DictCursor
)

class DB :
  def __init__(self, **config) :
    self.config = config if config else DB_CONFIG

  def connect(self) :
    return pymysql.connect(**self.config)

  # 로그인 검증
  def verity_admin(self, username, password) :
    sql = """
        SELECT COUNT(*) AS cnt 
        FROM users
        WHERE username = %s AND password = %s AND role = 'ADMIN'
    """
    with self.connect() as conn :
      with conn.cursor() as cur :
        cur.execute(sql, (username, password))
        res = cur.fetchone()
        return res['cnt'] == 1

  # 조회
  def fetch_jerseys_by_team(self, team_keyword) :
    sql = """
        SELECT id, serial_number, back_number, product_number, jersey_type, stock, price
        FROM jerseys
        WHERE product_name LIKE %s
        ORDER BY back_number ASC
    """
    query_kw = f"%{team_keyword}%"
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