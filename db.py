import logging
import re
import sqlite3
import warnings

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)

con = sqlite3.connect("./db.db")
con.row_factory = sqlite3.Row
con.set_trace_callback(logger.debug)


def framedata(query_str=''):
		with con:
				cur = con.cursor()
				if bool(query_str):
						query_str = ' ' + query_str
				execute_str = "select guard.ko as guard_ko, name.ko as name_ko, _framedata.* from (SELECT * FROM framedata {query_str} ) _framedata left join guard on (_framedata.guard = guard.en) ".format(query_str=query_str)
				execute_str += " left join name on (_framedata.charname = name.en) order by odr "
				cur.execute(execute_str)
				row = cur.fetchone()
				if row:
					logging.debug(row.keys())
				cur.execute(execute_str)
				rows = cur.fetchall()
				return rows


def fromCommand(charname, command):
	fromCommand_logger = logging.getLogger("fromCommand")
	fromCommand_logger.setLevel(logging.WARN)
	fromCommand_logger.info("커맨드에서 프레임데이터 검색")
	with con:
		cur = con.cursor()
		cur.execute((
			" select guard.ko as guard_ko, name.ko as name_ko, _framedata.* from ( "
			" SELECT * FROM framedata "
			" WHERE case when :charname in (trim(charname)) then 1 end is not null "
			" and trim(replace(command, ' ', '')) = replace(:command, ' ', '') "
			" ) _framedata left join guard on (_framedata.guard = guard.en) "
			" left join name on (_framedata.charname = name.en) "
			" order by odr "
			), {"charname": charname, "command": command})
		rows = cur.fetchall()
		if len(rows) == 1:
			fromCommand_logger.info("단일 결과 확인")
			return rows
		fromCommand_logger.info("유사 결과 검색")
		cur.execute((
			" select guard.ko as guard_ko, name.ko as name_ko, _framedata.* from ( "
			" SELECT * FROM framedata "
			" WHERE case when :charname in (trim(charname)) then 1 end is not null "
			" and instr(trim(replace(command, ' ', '')), replace(:command, ' ', '')) > 0 "
			" ) _framedata left join guard on (_framedata.guard = guard.en) "
			" left join name on (_framedata.charname = name.en) "
			" order by odr "
			), {"charname": charname, "command": command})
		rows = cur.fetchall()
		return rows


def fromSkill(charname, move_name_ko):
	with con:
		cur = con.cursor()
		cur.execute((
			" select guard.ko as guard_ko, name.ko as name_ko, _framedata.* from ( "
			" SELECT * FROM framedata "
			" WHERE case when :charname in (trim(charname)) then 1 end is not null "
			" and trim(replace(move_name_ko, ' ', '')) = replace(:move_name_ko, ' ', '') "
			" ) _framedata left join guard on (_framedata.guard = guard.en) "
			" left join name on (_framedata.charname = name.en) "
			" order by odr "
			), {"charname": charname, "move_name_ko": move_name_ko})
		rows = cur.fetchall()
		if len(rows) == 1:
			return rows
		cur.execute((
			" select guard.ko as guard_ko, name.ko as name_ko, _framedata.* from ( "
			" SELECT * FROM framedata "
			" WHERE case when :charname in (trim(charname)) then 1 end is not null "
			" and instr(trim(replace(move_name_ko, ' ', '')), replace(:move_name_ko, ' ', '')) > 0 "
			" ) _framedata left join guard on (_framedata.guard = guard.en) "
			" left join name on (_framedata.charname = name.en) "
			" order by odr "
			), {"charname": charname, "move_name_ko": move_name_ko})
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
	if not ko:
		return None
	with con:
		cur = con.cursor()
		query = "select en from name where ko = '{ko}'".format(ko=ko)
		cur.execute(query)
		row = cur.fetchone()
		if not row:
			return capitalize(ko)
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
	name_ko__logger = logging.getLogger("name_ko")
	name_ko__logger.setLevel(logging.WARN)
	name_ko__logger.debug(nickname)
	with con:
		cur = con.cursor()
		cur.execute("select * from nickname order by priority")
		for row in cur.fetchall():
			name_ko__logger.info("다음 패턴으로 확인")
			name_ko__logger.debug(row['regex'])
			if re.search(row['regex'], nickname):
				name_ko__logger.debug(row['ko'])
				return row['ko']
		return nickname


def ko_name(nickname):
	return name_ko(nickname)


def command(pattern):
	command_logger = logging.getLogger("command")
	command_logger.setLevel(logging.WARNING)
	with con:
		replace = pattern
		cur = con.cursor()
		cur.execute("select * from command where disabled is null order by priority, length(replace) DESC, length(pattern) desc, pattern desc, replace desc")
		for row in cur.fetchall():
			replace = re.sub(re.compile(row['pattern']), row['replace'], replace)
		command_logger.debug(replace)
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
	move_logger = logging.getLogger(__name__)
	move_logger.setLevel(logging.WARNING)
	move_logger.debug(name)
	move_logger.debug(move_nick)
	with con:
		cur = con.cursor()
		cur.execute("select * from move_nick where name = :name and disabled is null order by priority, length(move) desc, length(move_nick) desc, move desc, move_nick desc", {"name": name})
		move = move_nick
		for row in cur.fetchall():
			move_logger.info("move pattern exists")
			move_logger.debug(row['move_nick'])
#			move = move.replace(row['move_nick'], row['move'])
			move = re.sub(re.compile(row['move_nick']), row['move'], move)
			move_logger.debug(move)
			cur.execute("select * from framedata where :charname in (charname) and instr(move_name_ko, :move_name_ko) > 0 ", {"charname": name, "move_name_ko": move})
			row = cur.fetchone()
			if not row:
				continue
			if len(row) == 1:
				move_logger.info("move exists")
				return row["move_name_ko"]
			else:
				return move
		return move


def _command(name, command_nick):
	_command__logger = logging.getLogger("_command")
	_command__logger.setLevel(logging.WARNING)
	_command__logger.info("커맨드 별명에서 커맨드를 검색합니다.")
	_command__logger.debug(name)
	_command__logger.debug(command_nick)
	if not command_nick:
		return command_nick
	with con:
		cur = con.cursor()
		cur.execute("select * from {category}_nick where name = :name order by priority, length({category}) desc, length({category}_nick) desc, {category} desc, {category}_nick desc".format(category="command"), {"name": name})
		command = command_nick
		for row in cur.fetchall():
			command = re.sub(re.compile(row['command_nick']), row['command'], command)
			_command__logger.debug(command)
			cur.execute("select * from framedata where charname = :charname and instr(command, :command) > 0 order by odr desc ", {"charname": name, "command": command})
			row = cur.fetchone()
			if row:
				return row["command"]
		return command


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


def command_nick(name):
	with con:
		cur = con.cursor()
		cur.execute("select * from {category}_nick where name = :name order by length({category}) desc, length({category}_nick) desc, {category} desc, {category}_nick desc".format(category="command"), {"name": name})
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


def replace(pattern, table):
	if not pattern:
		return pattern
	with con:
		replace = pattern
		cur = con.cursor()
		cur.execute("select * from {table} order by priority, length(pattern) desc, length(replace) DESC, pattern desc, replace desc".format(table=table))
		for row in cur.fetchall():
			replace = re.sub(re.compile(row['pattern']), row['replace'], replace)
		return replace
	return pattern


def damage(pattern):
	return replace(pattern, "damage")


def active(pattern):
	return replace(pattern, "active")


def recovery(pattern):
	return replace(pattern, "recovery")


def capitalize(en):
	if not en:
		return en
	arr = re.split(re.compile("[^A-Za-z]"), en)
	if not arr:
		return en 
	elif len(arr) <= 1:
		return en.capitalize()
	else:
		merged = ""
		for each in arr:
			merged += "_" + each.capitalize()
		merged = merged.replace("_", "", 1)
		return merged 
