import logging
import sqlite3
import warnings

# print(sqlite3.version)
# print(sqlite3.sqlite_version)
framedata = 'framedata'

con = sqlite3.connect("./framedata.db")
con.row_factory = sqlite3.Row

def db_table(query_str=''):
		with con:
				cur = con.cursor()
				if bool(query_str):
						query_str = ' ' + query_str
				execute_str = 'SELECT * FROM framedata' + query_str
				cur.execute(execute_str)
				row = cur.fetchone()
				if row:
					logging.debug(row.keys())
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
		with con:
				cur = con.cursor()
				if bool(query_):
						query_ = ' ' + query_
				execute_ = 'SELECT * FROM framedata' + query_
				cur.execute(execute_)
				row = cur.fetchone()
				if row:
					logging.debug(row.keys())
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


def char():
	with con:
		cur = con.cursor()
		query = 'select distinct name_ko, charname from framedata order by name_ko, charname'
		cur.execute(query)
		rows = cur.fetchall()
		return rows
