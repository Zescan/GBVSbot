import sqlite3
import warnings

# print(sqlite3.version)
# print(sqlite3.sqlite_version)

framedata = 'framedata'

db = sqlite3.connect("./framedata.db")

def db_table(query_str=''):
		with db:
				cur = db.cursor()
				if bool(query_str):
						query_str = ' ' + query_str
				execute_str = 'SELECT * FROM framedata' + query_str
				cur.execute(execute_str)
				rows = cur.fetchall()
				return rows


def _db_table(db, query_str=''):
		with db:
			warnings.warn("deprecated")
			cur = db.cursor()
			if bool(query_str):
					query_str = ' ' + query_str
			execute_str = 'SELECT * FROM framedata' + query_str
			cur.execute(execute_str)
			rows = cur.fetchall()
			return rows

# db>데이터베이스 연결 , query>캐릭명
def db_sktable(query_=''):
		with db:
				cur = db.cursor()
				if bool(query_):
						query_ = ' ' + query_
				execute_ = 'SELECT * FROM framedata' + query_
				cur.execute(execute_)
				rows = cur.fetchall()
				return rows


# db>데이터베이스 연결 , query>캐릭명
def _db_sktable(db, query_=''):
		with db:
			warnings.warn("deprecated")
			cur = db.cursor()
			if bool(query_):
					query_ = ' ' + query_
			execute_ = 'SELECT * FROM framedata' + query_
			cur.execute(execute_)
			rows = cur.fetchall()
			return rows
