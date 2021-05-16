import discord
from discord.ext import commands
import os

import asyncio
import numpy as np
import random
import sqlite3

import nchanger as ncg
import db
import embed as blow
import changer as cg
import kor_changer as kcg

bot = commands.Bot(command_prefix='>', help_command=None)

charlist_path = os.path.dirname(os.path.abspath(__file__)) + "/캐릭목록.txt"
o = open(charlist_path, "r", encoding="utf-8")
charlist = o.read().split()


dab = sqlite3.connect("./framedata.db")
dbb = sqlite3.connect("sklist.db")

@bot.event
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(bot.user.name)
    print('connection was succesful')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("'>명령어'로 기능확인"))


# commands


@bot.command(aliases=['help'])
async def 명령어(ctx):
    embed=discord.Embed(title='명령어 목록', description='-괄호 안에 인자도 같이 써주세요!', color=0xfd4949)
    embed.add_field(name='>tip\n>설명서', value='파스티바_봇 사용설명서를 보여줍니다.', inline=False)
    embed.add_field(name='>핑\n>ping', value='현재 핑 상태를 측정합니다.', inline=False)
    embed.add_field(name='>랜덤\n>r', value='랜덤으로 아무 캐릭터나 뽑아줍니다.', inline=False)
    embed.add_field(name='>캐릭터\n>char', value='캐릭터들 목록과 영문 이름을 보여줍니다.', inline=False)
    embed.add_field(name='>기술 (캐릭명)\n>m (캐릭명)', value='해당 캐릭터의 기술 목록을 보여줍니다.', inline=False)
    embed.add_field(name='>공략 (캐릭명)\n>g (캐릭명)', value='해당 캐릭터의 공략글을 보여줍니다.', inline=False)
    embed.add_field(name='>i (캐릭명) (기술 커맨드)\n>검색 (캐릭명) (기술 커맨드)', value='해당 캐릭터의 기술의 프레임데이터를 보여줍니다.', inline=False)
    embed.add_field(name='>깃허브\n>githib', value='파스티바_봇의 깃허브 링크를 보여줍니다.', inline=False)
    await ctx.send(embed=embed)

@bot.command(aliases=['핑'])
async def ping(ctx):
    latancy = bot.latency
    embed=discord.Embed(title='현재 ping상태는...', description=f'{round(latancy * 1000)}ms 입니다.', color=0xfd4949)
    await ctx.send(embed=embed)

@bot.command(aliases=['tip'])
async def 설명서(ctx):
    embed=discord.Embed(title="파스티바_봇 사용 설명서", description="제작 - Rolling_Pumpkin", color=0x44e456)
    embed.add_field(name="#프레임데이터", value="파스티바_봇은 Dustloop wiki 에서 프레임 데이터를 가져왔습니다", inline=False)
    embed.add_field(name="#대,소문자", value="검색기능을 영어로 이용하실 때는 가능한 모두 소문자로 입력해주세요", inline=False)
    embed.add_field(name="#한·영사용", value="기술 커맨드의 방향 표시의 숫자를 제외하면 모두 한·영 구분없이 사용하셔도 괜찮습니다", inline=False)
    embed.add_field(name="#버튼 입력", value="약공격은 l (light)\n중공격은 m (middle)\n강공격은 h (heavy)\n아무 버튼이든 상관없는 경우 x (예시 : 236x)\n모으기 커맨드는 따로 표시할 필요없이 방향만 입력해주세요 \n(예시 : 샤를로테 글리터 온슬로트 커맨드 -> 46h)", inline=False)
    embed.add_field(name="#특수 기술", value="잡기는 tr (throw), 오버헤드는 oh (overhead) 또는 mh (커맨드) 로 입력해주세요", inline=False)
    embed.add_field(name="#공중 사용 기술", value="공중에서 사용하는 기술은 커맨드 앞에 j 를 붙여주세요", inline=False)
    embed.add_field(name="#근,원거리 기본기", value="근거리는 공격키 앞에 c (close), 원거리는 f (far)를 붙여주세요", inline=False)
    embed.add_field(name="검색예시)", value=">검색 그랑 214H (그랑-드라이브 버스트 강버젼)\n >i metera fm (메테라 원거리 중)", inline=False)
    embed.add_field(name="#피드백", value="틀린 부분, 추가할 부분, 개선할 부분은 @Rolling_Pumpkin 으로 말씀해주세요", inline=False)
    await ctx.send(embed=embed)

@bot.command(aliases=['char'])
async def 캐릭터(ctx):
    embed=discord.Embed(title="캐릭터 리스트", description="현재 검색 가능한 캐릭터 목록입니다.", color=0x6b9fff)
    embed.add_field(name="그랑", value="Gran", inline=True)
    embed.add_field(name="나루메아", value="Narmaya", inline=True)
    embed.add_field(name="랜슬롯", value="Lancelot", inline=True)
    embed.add_field(name="로아인", value="Lowain", inline=True)
    embed.add_field(name="메테라", value="Metera", inline=True)
    embed.add_field(name="바자라가", value="Vaseraga", inline=True)
    embed.add_field(name="벨리알", value="Belial", inline=True)
    embed.add_field(name="벨제붑", value="Beelzebub", inline=True)
    embed.add_field(name="샤를로테", value="Charlotta", inline=True)
    embed.add_field(name="소리즈", value="Soriz", inline=True)
    embed.add_field(name="우노", value="Anre", inline=True)
    embed.add_field(name="유스테스", value="Eustace", inline=True)
    embed.add_field(name="유엘", value="Yuel", inline=True)
    embed.add_field(name="제타", value="Zeta", inline=True)
    embed.add_field(name="조이", value="Zooey", inline=True)
    embed.add_field(name="지타", value="Djeeta", inline=True)
    embed.add_field(name="카타리나", value="Katalina", inline=True)
    embed.add_field(name="칼리오스트로", value="Cagliostro", inline=True)
    embed.add_field(name="파스티바", value="Ladiva", inline=True)
    embed.add_field(name="퍼시벌", value="Percival", inline=True)
    embed.add_field(name="페리", value="Ferry", inline=True)
    await ctx.send(embed=embed)

@bot.command(aliases=['검색', 'I'])
async def i(ctx, charname, command):
    charname = ncg.ncgr(charname)
    charname = charname.capitalize()
    # command = command.lower()
    command = cg.cgr(command)
    command = kcg.nor_cgr(command)
    k = '12'
    for j in k:
        command = kcg.com_cgr(command)
    print(charname)
    print(command)
    if '.'in command:
        pass
    else:
        command = command.upper()
    query_str = "WHERE charname = '" + charname + "' AND command = '" + command + "'"

    rows = db.db_table(dab,query_str)
    if not rows:
        embed=discord.Embed(title="해당하는 정보를 찾을 수 없습니다", description="다시 한 번 확인해 주세요", color=0xedf11e)
        await ctx.send(embed=embed)
    else:
        row = rows[0]
        info_dic = {'데미지': row[3],
        '가드판정': row[4],
        '시동 프레임': row[5],
        '지속 프레임': row[6],
        '회수 프레임': row[7],
        '가드시 이득': row[8],
        '히트시 이득': row[9]}
        await blow.t_embed(ctx, charname + " - " + command, row[2], info_dic)

@bot.command(aliases=['기술'])
async def m(ctx, character):
    character = ncg.ncgr(character)
    charname = character.capitalize()
    print(charname)
    query_ = "WHERE charname = '" + charname + "'"
    # print(query_)
    rows = db.db_sktable(dbb,query_)
    if not rows:
        embed=discord.Embed(title="해당하는 정보를 찾을 수 없습니다", description="다시 한 번 확인해 주세요", color=0xedf11e)
        await ctx.send(embed=embed)
    else:
        info_ = {'기술명': [], '커맨드': []}
        for row in rows:
            info_['기술명'].append(row[1])
            info_['커맨드'].append(row[2])
        await blow.c_embed(ctx, charname, " 기술 목록 ", info_)

@bot.command(aliases=['공략', 'G'])
async def g(ctx, charname):
    charname = ncg.rncgr(charname)
    if charname in charlist:
        await blow.g_embed(ctx, charname)
    else:
        embed=discord.Embed(title="해당하는 정보를 찾을 수 없습니다", description="다시 한 번 확인해 주세요", color=0xedf11e)
        await ctx.send(embed=embed)

@bot.command(aliases=['랜덤'])
async def r(ctx):
    choicechar = random.choice(charlist)
    embed = discord.Embed(title="캐릭터 랜덤 선택 결과...", description=f'[{choicechar}] (이)가 나왔습니다.', color=0xb377ee)
    await ctx.send(embed=embed)

@bot.command(aliases=['깃허브'])
async def github(ctx):
    embed = discord.Embed(title="파스티바_봇 깃허브 링크", description="https://github.com/crew852/GBVSbot", color=0xb377ee)
    await ctx.send(embed=embed)

bot.run(os.environ['token'])