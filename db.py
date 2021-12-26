import logging
import sqlite3
import warnings

# print(sqlite3.version)
# print(sqlite3.sqlite_version)

con = sqlite3.connect("./db.db")
con.row_factory = sqlite3.Row


def framedata(query_str=''):
		with con:
				cur = con.cursor()
				if bool(query_str):
						query_str = ' ' + query_str
				execute_str = 'select guard.ko as guard_ko, name.ko as name_ko, _framedata.* from (SELECT * FROM framedata ' + query_str + " ) _framedata left join guard on (_framedata.guard = guard.en) "
				execute_str += " left join name on (_framedata.charname = name.en) order by odr "
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
				warnings.warn("deprecated")
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
		query = 'select name.ko as name_ko, _framedata.charname from (select distinct charname from framedata) _framedata left join name on (_framedata.charname = name.en) order by name_ko, charname'
		cur.execute(query)
		rows = cur.fetchall()
		return rows


def en(ko):
	with con:
		cur = con.cursor()
		query = "select en from name where ko = '{ko}'".format(ko=ko)
		cur.execute(query)
		row = cur.fetchone()
		return row['en'] or None


def ko(en):
	with con:
		cur = con.cursor()
		query = "select ko from name where en = '{en}'".format(en=en)
		cur.execute(query)
		row = cur.fetchone()
		return row['ko'] or None
