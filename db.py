import logging
import re
import sqlite3

logger = logging.getLogger("db")
logger.setLevel(logging.WARN)

def regexp(expr, item):
	if not expr:
		return False
	if not item:
		return False
	reg = re.compile(expr)
	return reg.search(item) is not None 

con = sqlite3.connect("./db.db")
con.row_factory = sqlite3.Row
con.set_trace_callback(logger.debug)
con.create_function("REGEXP", 2, regexp)

def framedata(query_str=''):
	framedata_logger = logging.getLogger("framedata")
	framedata_logger.setLevel(logging.DEBUG)
	con.set_trace_callback(framedata_logger.debug)
	framedata_logger.debug(query_str)
	with con:
			cur = con.cursor()
			if bool(query_str):
					query_str = ' ' + query_str
			execute_str = "select guard.ko as guard_ko, name.ko as name_ko, _framedata.* from (SELECT * FROM framedata {query_str} ) _framedata left join guard on (_framedata.guard = guard.en) ".format(query_str=query_str)
			execute_str += " left join name on (_framedata.charname = name.en) order by odr "
			framedata_logger.debug(execute_str)
			cur.execute(execute_str)
			row = cur.fetchone()
			if row:
				logging.debug(row.keys())
			cur.execute(execute_str)
			rows = cur.fetchall()
			framedata_logger.info("프레임데이터 검색")
			return rows


def fromCommand(charname, command):
	fromCommand_logger = logging.getLogger("fromCommand")
	fromCommand_logger.setLevel(logging.WARNING)
	con.set_trace_callback(fromCommand_logger.debug)
	fromCommand_logger.info("커맨드에서 프레임데이터 검색")
	fromCommand_logger.debug(charname)
	fromCommand_logger.debug(command)
	with con:
		cur = con.cursor()
		cur.execute((
			" select guard.ko as guard_ko, name.ko as name_ko, _framedata.* from ( "
			" SELECT * FROM framedata "
			" WHERE case when :charname in (trim(charname)) then 1 end is not null "
			" and ( "
				" command = :command "
# 				" command REGEXP replace(:command, ' ', '.*') "
# 				" or :command REGEXP replace(command, ' ', '.*') "
			" ) "
			" ) _framedata left join guard on (_framedata.guard = guard.en) "
			" left join name on (_framedata.charname = name.en) "
			" order by odr "
			), {"charname": charname, "command": command})
		rows = cur.fetchall()
# 		if len(rows) == 1:
# 			fromCommand_logger.info("단일 결과 확인")
# 			return rows
# 		fromCommand_logger.info("유사 결과 검색")
# 		cur.execute((
# 			" select guard.ko as guard_ko, name.ko as name_ko, _framedata.* from ( "
# 			" SELECT * FROM framedata "
# 			" WHERE case when :charname in (trim(charname)) then 1 end is not null "
# 			" and instr(trim(replace(command, ' ', '')), replace(:command, ' ', '')) > 0 "
# 			" ) _framedata left join guard on (_framedata.guard = guard.en) "
# 			" left join name on (_framedata.charname = name.en) "
# 			" order by odr "
# 			), {"charname": charname, "command": command})
# 		rows = cur.fetchall()
		return rows


def fromSkill(charname, move_name_ko):
	fromSkill_logger = logging.getLogger("fromSkill")
	fromSkill_logger.setLevel(logging.DEBUG)
	fromSkill_logger.info("기술명에서 프레임데이터 검색")
	con.set_trace_callback(fromSkill_logger.debug)
	fromSkill_logger.debug(move_name_ko)

	with con:
		cur = con.cursor()
		cur.execute((
			" select guard.ko as guard_ko, name.ko as name_ko, _framedata.* from ( "
				" SELECT * "
					"" + getRateEquation("move_name_ko", ":move_name_ko") + ""
# 					" , min(length(:move_name_ko) * 1.0 / length(move_name_ko), length(move_name_ko) * 1.0 / length(:move_name_ko)) as rate "
				" FROM framedata "
				" WHERE case when :charname in (trim(charname)) then 1 end is not null "
				" and ( "
					" move_name_ko = :move_name_ko "
# 					" move_name_ko REGEXP replace(:move_name_ko, ' ', '.*') "
# 					" or :move_name_ko REGEXP replace(move_name_ko, ' ', '.*') "
				" ) "
			" ) _framedata left join guard on (_framedata.guard = guard.en) "
			" left join name on (_framedata.charname = name.en) "
			" order by rate desc, odr "
			), {"charname": charname, "move_name_ko": move_name_ko})
		rows = cur.fetchall()
# 		if len(rows) == 1:
# 			return rows
# 		cur.execute((
# 			" select guard.ko as guard_ko, name.ko as name_ko, _framedata.* from ( "
# 			" SELECT * FROM framedata "
# 			" WHERE case when :charname in (trim(charname)) then 1 end is not null "
# 			" and instr(trim(replace(move_name_ko, ' ', '')), replace(:move_name_ko, ' ', '')) > 0 "
# 			" ) _framedata left join guard on (_framedata.guard = guard.en) "
# 			" left join name on (_framedata.charname = name.en) "
# 			" order by odr "
# 			), {"charname": charname, "move_name_ko": move_name_ko})
# 		rows = cur.fetchall()
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
	con.set_trace_callback(command_logger.debug)
	with con:
		replace = pattern
		cur = con.cursor()
		cur.execute("select * from command where disabled is null order by priority, length(replace) DESC, length(pattern) desc, pattern desc, replace desc")
		for row in cur.fetchall():
			command_logger.debug(row['pattern'])
			replace = re.sub(re.compile(row['pattern']), row['replace'], replace)
		command_logger.debug(replace)
		replace = replace.strip()
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

def move(name, move_nick, charname):
	move_logger = logging.getLogger("move")
	move_logger.setLevel(logging.WARNING)
	con.set_trace_callback(move_logger.debug)
	move_logger.info("기술 별명에서 기술을 검색합니다.")
	move_logger.debug(name)
	move_logger.debug(move_nick)
	move_logger.debug(charname)
	if not move_nick:
		return None
	with con:
		cur = con.cursor()
		move = move_nick
		move_name_ko = _move_name_ko(charname, move)
		if move_name_ko:
			return move_name_ko
		cur.execute("select * from move_nick where name = :name and disabled is null order by priority, length(move) desc, length(move_nick) desc, move desc, move_nick desc", {"name": name})
		for row in cur.fetchall():
			move_logger.info("move pattern exists")
			move_name_ko = re.sub(re.compile("[^\w]+"), r".*".replace("\\", r"\\"), move)
			move_logger.debug(move_name_ko)
			cur.execute("select * from framedata where :charname in (charname) and ( "
# 						" move_name_ko REGEXP replace(:move_name_ko, ' ', '.*') "
# 						" or :move_name_ko REGEXP replace(move_name_ko, ' ', '.*') "
						" 0 = 1 "
						"" + getSearchCondition("move_name_ko", ":move_name_ko") + ""
					" ) ", {"charname": charname, "move_name_ko": move_name_ko})
			framedata = cur.fetchall()
			if not framedata:
				move_logger.info("no data")
				move_logger.debug(row['move_nick'])
				move = re.sub(re.compile(row['move_nick']), row['move'], move)
				move_logger.debug(move)
				move_name_ko = _move_name_ko(charname, move)
				if move_name_ko:
					return move_name_ko
				continue
			elif len(framedata) == 1:
				move_logger.info("single data")
				return framedata[0]["move_name_ko"]
			else:
				move_logger.info("multiple datas")
				return move
		move_logger.debug(move)	
		return move

def _move_name_ko(charname, move):
	move_name_ko__logger = logging.getLogger("_move_name_ko")
	con.set_trace_callback(move_name_ko__logger.debug)
	move_name_ko__logger.setLevel(logging.WARNING)
	move_name_ko = re.sub(re.compile("[^\w]+"), r"\W*".replace("\\", r"\\"), move)
	move_name_ko__logger.debug(move_name_ko)
	with con:
		cur = con.cursor()
		cur.execute("select * "
# 				" , min(length(:move_name_ko) * 1.0 / length(move_name_ko), length(move_name_ko) * 1.0 / length(:move_name_ko)) as rate "
				"" + getRateEquation("move_name_ko", ":move_name_ko") + ""
				" from framedata where :charname in (charname) and ( "

# 					" move_name_ko = :move_name_ko "
# 					" or move_name_ko REGEXP replace(:move_name_ko, ' ', '.*') "
# 					" or :move_name_ko REGEXP replace(move_name_ko, ' ', '.*') "
					" 0 = 1 "
					"" + getSearchCondition("move_name_ko", ":move_name_ko") + ""
				" ) "
				" order by rate desc, odr "
				, {"charname": charname, "move_name_ko": move_name_ko})
		framedatas = cur.fetchall()
		if len(framedatas) == 1:
			framedata = framedatas[0]
			move_name_ko__logger.debug(framedata["move_name_ko"])
			return framedata["move_name_ko"]
# 		else:
# 			move_name_ko__logger.info("multiple results")
# 			return move
	return None

def _command(name, command_nick):
	_command__logger = logging.getLogger("_command")
	_command__logger.setLevel(logging.DEBUG)
	con.set_trace_callback(_command__logger.debug)
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
			cur.execute(
				"select * "
# 				" , min(length(:command) * 1.0 / length(command), length(command) * 1.0 / length(:command)) as rate "
				"" + getRateEquation("command", ":command") + ""
				" from framedata where charname = :charname "
				" and ( "
# 					" command = :command "
# 					" or command REGEXP replace(:command, ' ', '.*') "
# 					" or :command REGEXP replace(command, ' ', '.*') "
					" 0 = 1 "
					"" + getSearchCondition("command", ":command") + ""
				" ) "
				" order by rate desc, odr, rowid",
					{"charname": name, "command": command})
			rows = cur.fetchall()
			if len(rows) == 1:
				row = rows[0]
				_command__logger.debug(row["command"])
				return row["command"]
		return command


def _list():
	with con:
		cur = con.cursor()
		cur.execute("select * from list order by odr, name desc")
		return cur.fetchall()


def pattern():
	with con:
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

def guard(en):
	if not en:
		return en
	with con:
		replace = en
		cur = con.cursor()
		cur.execute("select * from guard order by length(en) desc, length(ko) DESC")
		for row in cur.fetchall():
			replace = replace.replace(row['en'], row['ko'])
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

def startup(pattern):
	return replace(pattern, "startup")

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
			merged += "-" + each.capitalize()
		merged = merged.replace("-", "", 1)
		return merged 

def getQuoted(param):
	return " '{param}' ".format(param=param)


def getColoned(param):
	return " :{param} ".format(param=param)


def getDivEquation(first, second):
	return " (length({first}) * 1.0 / length({second})) ".format(first=first, second=second)


def getAbsEquation(param):
	return " (abs({param} - 1.0)) ".format(param=param)


def getRateEquation(key, value):
	return " , min({abs1}, {abs2}) as rate ".format(abs1=getAbsEquation(getDivEquation(key, value)), abs2=getAbsEquation(getDivEquation(value, key)))


def getSearchCondition(key, value):
	query_ = ""
	query_ += " or {key} REGEXP replace({value}, ' ', '.*') ".format(key=key, value=value)
	query_ += " or {value} REGEXP replace({key}, ' ', '.*') ".format(key=key, value=value)
	query_ += " or instr({key}, {value}) > 0 ".format(key=key, value=value)
	query_ += " or instr({value}, {key}) > 0 ".format(key=key, value=value)
	return query_
