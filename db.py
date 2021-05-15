import sqlite3

# print(sqlite3.version)
# print(sqlite3.sqlite_version)


def db_table(db, query_str=''):
    with db:
        cur = db.cursor()
        if bool(query_str):
            query_str = ' ' + query_str
        execute_str = 'SELECT * FROM skills' + query_str
        cur.execute(execute_str)
        rows = cur.fetchall()
        return rows

# db>데이터베이스 연결 , query>캐릭명
def db_sktable(db, query_=''):
    with db:
        cur = db.cursor()
        if bool(query_):
            query_ = ' ' + query_
        execute_ = 'SELECT * FROM skills' + query_
        cur.execute(execute_)
        rows = cur.fetchall()
        return rows
