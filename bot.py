import logging
import os
import random
import re

import discord
from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv

import blow
import db

load_dotenv()

logging.basicConfig(level=logging.WARN, format="[%(funcName)s] %(message)s %(filename)s:%(lineno)d")

logger = logging.getLogger("bot")
logger.setLevel(logging.WARN)

cmdbot = commands.Bot(command_prefix="/")
bot = cmdbot
client = bot
if not client:
	logging.error("empty client")
	raise
slash = SlashCommand(bot, sync_commands=False)
logging.info("길드")
guild_ids = bot.guilds
logging.debug(guild_ids)
logging.info("채널")
channel = None

@bot.event
async def on_ready():
	global channel
	global guild_ids
	logging.info("클라이언트 확인")
	logging.debug(client)
	logging.info("채널 확인")
	logging.debug(os.environ['channel_id'])
	channel = client.get_channel(int(os.environ['channel_id']))
	if not channel:
		logging.error("empty channel")
		raise
	logging.info("채널 확인")
	logging.debug(channel)
	logging.info("길드 확인")
	guild_ids = [channel.guild.id]
	logging.debug(guild_ids)
	logging.info('다음으로 로그인합니다: ')
	logging.debug(bot.user.name)
	logging.info('connection was succesful')
	await bot.change_presence(status=discord.Status.online, activity=discord.Game("봇 채널에서 '/명령어', '명령어'로 기능확인"))


@bot.event
async def on_message(message):
	global channel
	on_message__logger = logging.getLogger("on_message")
	on_message__logger.setLevel(logging.ERROR)
	if not channel:
		logging.error("empty channel")
		raise
	logging.debug(message)
	logging.debug(message.content)
	arr = message.content.split()
	logging.debug(arr)
	first = ""
	if len(arr) > 0:
			first = arr[0].replace("/", "")
	charname = ""
	if len(arr) > 1:
			charname = arr[1]
	command = ""
	if len(arr) > 2:
			command = message.content.replace(first, "", 1).replace(charname, "", 1).strip()
	ctx = message.channel
	logging.info("채널 확인")
	logging.debug(channel)
	if not ctx == channel:
		on_message__logger.warning("wrong channel")
		return None
	if not first:
		logging.info("종료")
	elif first == "명령어":
			await __list(ctx)
	elif first == "설명서":
			await _tip(ctx)
	elif first == "핑":
			await _ping(ctx)
	elif first in ["랜덤", "루나루", "Lunalu", "lunalu"]:
			await _random(ctx)
	elif first == "캐릭터":
			await _char(ctx)
	elif first == "공략":
			await _walkthrough(ctx, charname)
	elif first == "깃허브":
			await _github(ctx)
	elif first == "패턴":
			await _pattern(ctx)
	elif first == "별명":
		await _move_nick(ctx, charname)
	elif first in ["기술", "검색"]:
			await _search(ctx, charname, command)
	else:
			logging.info("명령어 위치를 옮깁니다.")
			command = "{arg1} {arg2}".format(arg1=charname, arg2=command)
			charname = first
			charname = db.en(db.name_ko(charname))
			if (len(re.findall(re.compile("[a-zA-Z]+"), charname)) <= 0):
				logger.warning("normal message")
				return
			await _search(ctx, charname, command)


@cmdbot.command()
async def pass_normal(ctx):
	logging.error("이것은 무엇인가?")
	pass


@slash.slash(name="명령어", description='명령어 목록을 보여줍니다.', guild_ids=guild_ids)
async def _list(ctx):
	await validate(ctx)
	await __list(ctx)


async def __list(ctx):
		embed = discord.Embed(title='명령어 목록', description='-괄호 안의 인자도 같이 써주세요!', color=0xfd4949)
		for row in db._list():
			embed.add_field(name='/{name}'.format(name=row['name']), value=row['value'], inline=False)
		await ctx.send(embed=embed)
		await _tip(ctx)


@slash.slash(name="핑", description='현재 핑 상태를 측정합니다.', guild_ids=guild_ids)
async def ping(ctx):
	await validate(ctx)
	await _ping(ctx)


async def _ping(ctx):
		logger.warning("deprecated")
		latancy = bot.latency
		embed = discord.Embed(title='현재 ping상태는...', description=f'{round(latancy * 1000)}ms 입니다.', color=0xfd4949)
		await ctx.send(embed=embed)


@slash.slash(name="설명서", description='파스티바_봇 설명서를 보여줍니다.', guild_ids=guild_ids)
async def tip(ctx):
	await validate(ctx)
	await _tip(ctx)


async def _tip(ctx):
		embed = discord.Embed(title="설명서", description="담당 : DEEPDIVE, Zescan, 제작 : Rolling_Pumpkin", color=0x44e456)
		for row in db._tip():
			embed.add_field(name='{name}'.format(name=row['name']), value=row['value'], inline=False)
		await ctx.send(embed=embed)


@slash.slash(name="캐릭터", description='캐릭터들 목록과 영문 이름을 보여줍니다.', guild_ids=guild_ids)
async def char(ctx):
	await validate(ctx)
	await _char(ctx)


async def _char(ctx):
		embed = discord.Embed(title="캐릭터 리스트", description="현재 검색 가능한 캐릭터(한글 가나다순) 목록입니다.", color=0x6b9fff)
		for row in db.char():
			embed.add_field(name=row['name_ko'], value=row['charname'], inline=False)
		await ctx.send(embed=embed)


@slash.slash(name="검색", description='해당 캐릭터의 기술의 프레임데이터를 보여줍니다.', guild_ids=guild_ids)
async def search(ctx, charname, command):
	await validate(ctx)
	await _search(ctx, charname, command)


async def _search(ctx, charname, string):
	_search__logger = logging.getLogger("_search")
	_search__logger.setLevel(logging.WARNING)
	charname = db.name_ko(charname)
# 	name_ko = charname
	charname = db.en(charname)
	name_ko = db.ko(charname)
	if not re.search(re.compile("[a-zA-z]+"), charname):
		return None
	logging.debug(charname)
	_search__logger.info("캐릭의 한글 이름을 영어 이름으로 변환")
	
	
	command = string.strip()
	_search__logger.debug(command)
	command = db.command(command)
	_search__logger.debug(command)
	command = db._command(charname, command)
	_search__logger.debug(command)
	_search__logger.info("커맨드 확인")
	rows = None
	commands = db.fromCommand(charname, command)
	_search__logger.info("커맨드에 의한 검색")
	_search__logger.debug(string)
	skname = string.strip()
	_search__logger.debug(skname)
	skname = db.move(name_ko, skname, charname)
	_search__logger.debug(skname)
	_search__logger.info("기술명 확인")
	skills = db.fromSkill(charname, skname)
	_search__logger.info("기술명에 의한 검색")
	if rows:
		_search__logger.error("invalid data")
		raise
	elif len(commands) == 1:
		rows = commands
	elif len(skills) == 1:
		rows = skills
	if not rows:
			await _tip(ctx)
# 			embed = discord.Embed(title="검색 안내", description="오른쪽과 같이 입력할 수록 검색률이 오릅니다.", color=0x44e456)
# 			for row in db._search_guide():
# 				embed.add_field(name=row["name"], value=row["value"], inline=False)
# 			await ctx.send(embed=embed)
			await _skill(ctx, charname, command, skname)
	else:
			for row in rows:
				info_dic = {'데미지': db.damage(row['damage']) or "-",
					'가드판정': row['guard_ko'] or db.guard(row['guard']),
					'시동 프레임': db.startup(row['startup']),
					'지속 프레임': db.active(row['active']),
					'회수 프레임': db.recovery(row['recovery']),
					'가드시 이득': db.on(row['onblock']),
					'히트시 이득': db.on(row['onhit']),
					'공격레벨': row['attack_level'],
					'상쇄레벨': row['clash_level'],
					'기타':row['etc']
					}
				await blow.t_embed(ctx, row['name_ko'] + " - " + row['command'], row['move_name_ko'] or row['skname'] or row['command'], info_dic, db.icon(row['charname']), db.images(row['charname'], row['command']))


@slash.slash(name='기술', description='해당 캐릭터의 기술의 프레임데이터를 보여줍니다.', guild_ids=guild_ids)
async def skill(ctx, character, command):
	await validate(ctx)
	await _search(ctx, character, command)


async def _skill(ctx, charname, command, skname):
	_skill_logger = logging.getLogger("_skill")
	_skill_logger.setLevel(logging.WARNING)
	_skill_logger.debug(charname)
	charname = db.name_ko(charname)
	_skill_logger.debug(charname)
	charname = db.en(charname)
	_skill_logger.debug(charname)
	move_name_ko = skname
	query_ = " where 1=1 "
	query_ += " and case when '{charname}' in (trim(charname)) then 1 end is not null ".format(charname=charname)
	if command or move_name_ko:
		query_ += " and case when ( 0 = 1 "
# 		query_ += " command REGEXP replace('{command}', ' ', '.*') ".format(command=command)
# 		query_ += " or '{command}' REGEXP replace(command, ' ', '.*') ".format(command=command)
# 		query_ += " or instr(command, '{command}') > 0 ".format(command=command)
# 		query_ += " or instr('{command}', command) > 0 ".format(command=command)
		query_ += db.getSearchCondition("command", "'{command}'".format(command=command))
# 		query_ += " or move_name_ko REGEXP replace('{move_name_ko}', ' ', '.*') ".format(move_name_ko=move_name_ko)
# 		query_ += " or '{move_name_ko}' REGEXP replace(move_name_ko, ' ', '.*') ".format(move_name_ko=move_name_ko)
		query_ += db.getSearchCondition("move_name_ko", "'{move_name_ko}'".format(move_name_ko=move_name_ko))
		query_ += " ) then 1 end is not null "
	rows = db.framedata(query_)
	if not rows:
			embed = discord.Embed(title="해당하는 정보를 찾을 수 없습니다", description="다시 한 번 확인해 주세요", color=0xedf11e)
			await ctx.send(embed=embed)
	else:
			info_ = {'커맨드': [], '기술명': []}
			for row in rows:
					info_['커맨드'].append(row['command'])
					info_['기술명'].append(row['move_name_ko'] or row['skname'] or row['command'])
			await blow.c_embed(ctx, row['name_ko'], " 기술 목록 ", info_)


@slash.slash(name="공략", description='해당 캐릭터의 공략글을 보여줍니다.', guild_ids=guild_ids)
async def walkthrough(ctx, charname):
	await validate(ctx)
	await _walkthrough(ctx, charname)


async def _walkthrough(ctx, charname):
		charname = db.name_ko(charname)
		logging.debug(charname)
		await blow.g_embed(ctx, charname)


@slash.slash(name="랜덤", description='랜덤으로 아무 캐릭터나 뽑아줍니다.', guild_ids=guild_ids)
async def rand(ctx):
	await validate(ctx)
	await _random(ctx)


@slash.slash(name="루나루", description='랜덤으로 아무 캐릭터나 뽑아줍니다.', guild_ids=guild_ids)
async def lunalu(ctx):
	await validate(ctx)
	await _random(ctx)


@slash.slash(name="Lunalu", description='Get randomized name.', guild_ids=guild_ids)
async def Lunalu(ctx):
	await validate(ctx)
	await _random(ctx)


async def _random(ctx):
		charlist = db.char()
		choicechar = random.choice(charlist)
		choicechar = choicechar['name_ko'] or choicechar['charname']
		embed = discord.Embed(title="캐릭터 랜덤 선택 결과...", description=f'[{choicechar}] (이)가 나왔습니다.', color=0xb377ee)
		await ctx.send(embed=embed)


@slash.slash(name="깃허브", description='파스티바_봇의 깃허브 링크를 보여줍니다.', guild_ids=guild_ids)
async def github(ctx):
	await validate(ctx)
	await _github(ctx)


async def _github(ctx):
		embed = discord.Embed(title="파스티바_봇 깃허브 링크", description="https://github.com/crew852/GBVSbot", color=0xb377ee)
		await ctx.send(embed=embed)


@slash.slash(name="패턴", description="검색 가능한 커맨드 패턴을 보여줍니다.", guild_ids=guild_ids)
async def pattern(ctx):
	await validate(ctx)
	await _pattern(ctx)

	
async def _pattern(ctx):
	embed = discord.Embed(title="패턴목록", description='긴 패턴부터 우선 변환적용됩니다.', color=0xb377ee)
	messages = []
	message = await ctx.send(embed=embed)
	messages.append(message)
	embed = discord.Embed(color=0xf3fd68)
	i = 0
	for row in db.pattern():
		if i%20 == 19:
			message = await ctx.send(embed=embed)
			messages.append(message)
			embed = discord.Embed(color=0xf3fd68)
		embed.add_field(name=row['pattern'], value=row['replace'], inline=False)
		i = i + 1
	message = await ctx.send(embed=embed)
	messages.append(message)
	return messages


@slash.slash(name="별명", description="해당 캐릭터의 기술에 대한 별명을 보여줍니다. ", guild_ids=guild_ids)
async def move_nick(ctx, name):
	await validate(ctx)
	await _move_nick(ctx, name)


async def _move_nick(ctx, name):
	embed = discord.Embed(title="별명목록", description='긴 패턴부터 우선 변환적용됩니다.', color=0xb377ee)
	messages = []
	message = await ctx.send(embed=embed)
	messages.append(message)
	embed = discord.Embed(color=0xf3fd68)
	ko = db.name_ko(name)
	i = 0
	for row in db.move_nick(ko):
		if i % 20 == 19:
			message = await ctx.send(embed=embed)
			messages.append(message)
			embed = discord.Embed(color=0xf3fd68)
		embed.add_field(name=row['move_nick'], value=row['move'], inline=False)
		i = i + 1
	message = await ctx.send(embed=embed)
	messages.append(message)
	return messages


async def validate(ctx):
	global channel
	validate_logger = logging.getLogger("validate")
	validate_logger.setLevel(logging.ERROR)
	logging.debug(ctx)
	if not channel:
		logging.error("empty channel")
		raise
	if not ctx.channel_id == channel.id:
		validate_logger.warning("wrong channel")
		embed = discord.Embed(title="안내", description="허용되지 않은 채널입니다.", color=0xb377ee)
		await ctx.send(embed=embed)
		raise
	else:
		return True
	return False
token= os.environ['Bot_token']

if len(token) <= 0:
	raise 
bot.run(token, bot=True)

