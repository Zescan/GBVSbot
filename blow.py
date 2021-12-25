import asyncio
import logging
import re

from discord import embeds
import discord

import numpy as np


#logging.basicConfig(level=logging.DEBUG)
async def t_embed(channel, title, description, data, icon, image):
	embed = discord.Embed(title=title, description=description, color=0xfd4949)
	if icon and icon.lower().find("http") > -1:
		embed.set_thumbnail(url=icon)
	# if image and image.lower().find("http") > -1:
	#  embed.set_image(url = image)
	for info_key in data:
	#   if info_key == '가드판정' or info_key == '히트시 이득':
	#       embed.add_field(name=info_key, value="```" + str(data[info_key]) + "```", inline=False)
	#   else:
	#       embed.add_field(name=info_key, value="```" + str(data[info_key]) + "```", inline=True)
		embed.add_field(name=info_key, value="```{str}```".format(str=str(data[info_key]) or "-"), inline=False)
	messages = []
	message = await channel.send(embed=embed)
	messages.append(message)
	if image and image.lower().find("http") > -1:
		images = re.split("[\s,]+", image)
		logging.debug(images)
		for idx in range(0, len(images)):
				# embed.set_image(url = images[idx])
				# if idx == 0:
				#    embed.set_image(url = images[idx])
				# else:
				#    embed.add_field(name="추가 이미지", value=images[idx], inline=False)
				imgEmbed = discord.Embed(title="", color=0xfd4949)
				imgEmbed.add_field(name="기술 이미지", value=(idx + 1), inline=False)
				imgEmbed.set_image(url=images[idx])
				message = await channel.send(embed=imgEmbed)
				messages.append(message)
	# message = await channel.send(embed=embed)
	return messages


async def c_embed(channel, title, description, data):
	embed = discord.Embed(title=title, description=description, color=0xf3fd68)
	messages = []
	message = await channel.send(embed=embed)
	messages.append(message)
	command = None
	skname = None
	# for info_key in data:
		# value_str = ''
		# for obj in data[info_key]:
			# value_str += '\n' + obj
		# embed.add_field(name=info_key, value="```" + value_str + "```", inline=True)
		# embed.add_field(name=info_key, value="-", inline=True)
	# embed.add_field(name="커맨드", value="기술명", inline=True)
	# embed.add_field(name="기술명", value="-", inline=True)
	# messages = []
	# message = await channel.send(embed=embed)
	# messages.append(message)
	embed = discord.Embed(color=0xf3fd68)
	commands = data["커맨드"]
	sknames = data["기술명"]
	lst = ""
	for idx in range(0, len(commands)):
		command = commands[idx]
		skname = sknames[idx]
		if idx % 20 == 19:
				message = await channel.send(embed=embed)
				messages.append(message)
				embed = discord.Embed(color=0xf3fd68)
		# subEmbed = discord.Embed(color=0xf3fd68)
		embed.add_field(name=command, value=skname, inline=False)
		# message = await channel.send(embed=subEmbed)
		# messages.append(message)
	# messages = []
	# embed.add_field(name="-", value=lst, inline=True)
	message = await channel.send(embed=embed)
	messages.append(message)
	# for info_key in data:
	#
	return messages


async def g_embed(channel, title):
	embed = discord.Embed(title=title, description='공략글', color=0x00bd26)
	if title == '그랑':
		embed.add_field(name='링크', value='https://docs.google.com/spreadsheets/d/1KUXnX6EP0RmoNWdRoHzJ3P5F28s4OzrlwFrYJ6aNf24/edit#gid=214206506')
	elif title == '나루메아':
		embed.add_field(name='링크', value='https://docs.google.com/spreadsheets/d/1bHuWRYGxkfgK0dcRKKaca3tVivRf8-JENPfunGIML5A/edit#gid=1138560127')
	elif title == '랜슬롯':
		embed.add_field(name='링크', value='https://docs.google.com/spreadsheets/d/1RPdLqP347qjsBZ1zGIoXGBJYxaUXa7NhE-mz-SfBfJA/edit#gid=1138560127')
	elif title == '로아인':
		embed.add_field(name='링크', value='https://docs.google.com/spreadsheets/d/1IZwMa2a9u95MpDp0XTFOtJ0K2DYTj5EWsAi1-ZBh4e0/edit#gid=1458995862')
	elif title == '메테라':
		embed.add_field(name='링크', value='https://docs.google.com/spreadsheets/d/179OqwGaL6xR0DaUsx-wa68CBgNJCdG9vWjZoy32PVKk/edit#gid=706569324')
	elif title == '바자라가':
		embed.add_field(name='링크', value='https://docs.google.com/spreadsheets/d/1q7A4BePDKWxzGejQgi3GdOQtdeyRE-ZGVmHMKTe9Yhk/edit#gid=1138560127')
	elif title == '벨리알':
		embed.add_field(name='링크', value='https://docs.google.com/spreadsheets/d/13riXpv2ZeASmmCRFzF2hUAwDqHb2uBqbEVx5I-_Jhxg/edit#gid=214206506')
	elif title == '벨제붑':
		embed.add_field(name='링크', value='https://docs.google.com/spreadsheets/d/1fDkQ39cEHCjb2nCxgZp0mrijzAXU1sWetMTJw-XDRbg/edit#gid=1138560127')
	elif title == '샤를로테':
		embed.add_field(name='링크', value='https://docs.google.com/spreadsheets/d/1AM_bs5mD9dDzqTneN3xTlUXYCu5p8sQi5kYeUa3h-lI/edit#gid=550430936')
	elif title == '소리즈':
		embed.add_field(name='링크', value='https://docs.google.com/spreadsheets/d/1nz_K6CwhZ020U2MWd8oApsoDFBxEJM1pOmDA61oXqf4/edit#gid=1670795521')
	elif title == '우노':
		embed.add_field(name='링크', value='https://docs.google.com/spreadsheets/d/1S3Nbb_wyoc8u-zHBNvLVpdXE8cbOJKqjkJpjVeVcgmM/edit#gid=1468237284')
	elif title == '유스테스':
		embed.add_field(name='링크', value='https://docs.google.com/spreadsheets/d/1aBDKMP9aVKJq08yEGrFY5LYUU3ug8cU102AgRo-h-wE/edit#gid=703581033')
	elif title == '유엘':
		embed.add_field(name='링크', value='https://docs.google.com/spreadsheets/d/1Z11wYziu2fn3tl5eHvu3KVZUrVn-4muEIuZuDmKlzyc/edit')
	elif title == '제타':
		embed.add_field(name='링크', value='https://docs.google.com/spreadsheets/d/1oEgW3a-sfuYEsnynsNY4W1jaio0GeO0v3C7tESXRs0Q/edit#gid=854574556')
	elif title == '조이':
		embed.add_field(name='링크', value='https://docs.google.com/spreadsheets/d/1rS7PXESMCnKQLTfMxcNtmaSKQYSHU2mnf5mLhA2ed1o/edit#gid=1138560127')
	elif title == '지타':
		embed.add_field(name='링크', value='https://docs.google.com/spreadsheets/d/1TANkejJus0FGSqrmAUFvo1gLBNFsVMaDyNwU86U_uKw/edit#gid=1558871192')
	elif title == '카타리나':
		embed.add_field(name='링크', value='https://docs.google.com/spreadsheets/d/1n_NAR2sCh-MEg8hg5BVYcmw4Bl8jyxCrd9MUIPo-IUc/edit#gid=1085753018')
	elif title == '칼리오스트로':
		embed.add_field(name='링크', value='https://docs.google.com/spreadsheets/d/13dBgGrmkBJVR3ukLoDNhZeopNgtmDBwRgOh5v2xLV58/edit#gid=1559228280')
	elif title == '파스티바':
		embed.add_field(name='링크', value='https://docs.google.com/spreadsheets/d/1UfgUJeo0XCH72Ns9Um0mMk7tQZomwfOP7MxEiRWjEfc/edit#gid=1364340536')
	elif title == '퍼시벌':
		embed.add_field(name='링크', value='https://docs.google.com/spreadsheets/d/1ncZM9ioBxpWsolZKZ5fLxZotmAAmCc2nBxUQ2RT0dLU/edit#gid=69722501')
	elif title == '페리':
		embed.add_field(name='링크', value='https://docs.google.com/spreadsheets/d/1e8OrLo-n0hZYfztgr2b9IV6Mnz8k7qkgpBsqIvquLEw/edit#gid=2137001956')

	await channel.send(embed=embed)
