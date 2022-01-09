import logging
import re
import sqlite3
import warnings

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

# def _db_table(db, query_str=''):
# 		with db:
# 			cur = db.cursor()
# 			if bool(query_str):
# 					query_str = ' ' + query_str
# 			execute_str = 'SELECT * FROM framedata' + query_str
# 			cur.execute(execute_str)
# 			rows = cur.fetchall()
# 			return rows

# db>데이터베이스 연결 , query>캐릭명
# def db_sktable(query_=''):
# 		with con:
# 				cur = con.cursor()
# 				if bool(query_):
# 						query_ = ' ' + query_
# 				execute_ = 'SELECT * FROM framedata' + query_
# 				cur.execute(execute_)
# 				row = cur.fetchone()
# 				if row:
# 					logging.debug(row.keys())
# 				cur.execute(execute_)
# 				rows = cur.fetchall()
# 				return rows


# db>데이터베이스 연결 , query>캐릭명
# def _db_sktable(db, query_=''):
# 		with db:
# 			cur = db.cursor()
# 			if bool(query_):
# 					query_ = ' ' + query_
# 			execute_ = 'SELECT * FROM framedata' + query_
# 			cur.execute(execute_)
# 			rows = cur.fetchall()
# 			return rows


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
		if not row:
			return ko
		return row['en']


def ko(en):
	with con:
		cur = con.cursor()
		query = "select ko from name where en = '{en}'".format(en=en)
		cur.execute(query)
		row = cur.fetchone()
		if not row:
			return en
		return row['ko']


def name_ko(nickname):
	with con:
		cur = con.cursor()
		cur.execute("select * from nickname order by priority")
		for row in cur.fetchall():
			if re.search(row['regex'], nickname):
				return row['ko']
		return nickname


def ko_name(nickname):
	return name_ko(nickname)


def command(pattern):
	with con:
		replace = pattern
		cur = con.cursor()
		cur.execute("select * from command order by length(pattern) desc, length(replace) DESC, pattern desc, replace desc")
		for row in cur.fetchall():
			# replace = replace.replace(row['pattern'], row['replace'])
			replace = re.sub(re.compile(row['pattern']), row['replace'], replace)
		return replace


def walkthrough(ko):
	with con:
		cur = con.cursor()
		cur.execute("select * from name where trim(ko) = :ko", {"ko": ko})
		return cur.fetchone()


def images(name, command):
	with con:
		cur = con.cursor()
		cur.execute("select * from move_image where name = :name and command = :command order by odr ", {"name": name, "command": command})
		return cur.fetchall()


def icon(name):
	with con:
		cur = con.cursor()
		cur.execute("select * from name where en = :en", {"en": name})
		row = cur.fetchone()
		return row['icon']


def move(name, move_nick):
	logging.info("기술 별명에서 기술을 검색합니다.")
	logging.debug(name)
	logging.debug(move_nick)
	with con:
		cur = con.cursor()
		cur.execute("select * from move_nick where name = :name order by length(move) desc, length(move_nick) desc, move desc, move_nick desc", {"name": name})
		move = move_nick
		for row in cur.fetchall():
			move = move.replace(row['move_nick'], row['move'])
			cur.execute("select * from framedata where skname = :skname", {"skname": move})
			rows = cur.fetchall()
			if rows:
				return move
		return move


def list():
	with con:
		cur = con.cursor()
		cur.execute("select * from list order by odr, name desc")
		return cur.fetchall()


def pattern():
	with con:
		replace = pattern
		cur = con.cursor()
		cur.execute("select * from command order by length(pattern) desc, length(replace) DESC, pattern desc, replace desc")
		return cur.fetchall()


def move_nick(name):
	with con:
		cur = con.cursor()
		cur.execute("select * from move_nick where name = :name order by length(move) desc, length(move_nick) desc, move desc, move_nick desc", {"name": name})
		return cur.fetchall()


def on(pattern):
	if not pattern:
		return pattern
	with con:
		replace = pattern
		cur = con.cursor()
		cur.execute("select * from on_ order by length(pattern) desc, length(replace) DESC, pattern desc, replace desc")
		for row in cur.fetchall():
			replace = replace.replace(row['pattern'], row['replace'])
		return replace
	return pattern
