#라이브러리 임포트
import pymysql

#데이터베이스 클래스
class MariaDB:
    def read_config(p:str) -> dict: #config파일 읽어오는 함수
        with open(p, 'r') as f:
            lines = f.readlines()
        config_dict={}

        for l in lines:
            idx = l.index('=')
            k = l[:idx]
            v = l[idx+1:]
            config_dict[k] = v.rstrip()
        return config_dict
    
    def __init__(self, host, user, password, database, charset, port = 3306) -> None:
        self.host = host 
        self.port = int(port)
        self.conn = pymysql.connect(
                                    host = host,
                                    user = user,
                                    password = password,
                                    database = database,
                                    charset = charset,
                                    port = port)
        return 
    
    def insert_many(self, table_name, columns, values): #여러개의 값을 테이블에 삽입하는 함수
        with self.conn.cursor() as cursor:
            sql = 'INSERT INTO {}({}) VALUES ({})'.format(table_name,\
                ','.join(columns), ','.join(['%s'] * len(values[0])))
            cursor.executemany(sql, values)
        self.conn.commit()
        return
      
    def select_all(self): #TB_game 테이블에서 GameID에 해당하는 모든 값을 select해주는 함수
        with self.conn.cursor() as cursor:
            sql = "SELECT `GameID` FROM `TB_game`"
            cursor.execute(sql) 
            result=cursor.fetchall()
        return result
    
    def select_count(self, dttm): #TB_game 테이블에서 PlayedAt 칼럼의 날짜값이 dttm과 일치하는 갯수를 세서 그 값을 반환해주는 함수
        with self.conn.cursor() as cursor:
            sql = "SELECT COUNT(*) FROM `TB_game` WHERE DATE(`PlayedAt`)='{}'".format(dttm)
            cursor.execute(sql)
            result = cursor.fetchone()[0]
        return result
    
    def select_order(self): #TB_game 테이블에서 GameID칼럼을 기준으로 내림차순 정렬하여 상위 5개의 GameID를 select하는 함수
        with self.conn.cursor() as cursor:
            sql = "SELECT `GameID` FROM `TB_game` ORDER BY `GameID` DESC LIMIT 5"
            cursor.execute(sql) 
            result=cursor.fetchall()
        return result

baseballdb_config = MariaDB.read_config('./bb_modules/baseballdb_config')
db=MariaDB(**baseballdb_config)  #데이터베이스 지정
