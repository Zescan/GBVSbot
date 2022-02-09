import discord
import db

async def t_embed(channel, title, description, data, icon, images):
	embed = discord.Embed(title=title, description=description, color=0xfd4949)
	if icon and icon.lower().find("http") > -1:
		embed.set_thumbnail(url=icon)
	for info_key in data:
		embed.add_field(name=info_key, value="```{str}```".format(str=str(data[info_key]) or "-"), inline=False)
	messages = []
	message = await channel.send(embed=embed)
	messages.append(message)
	for image in images:
		if image['image'] and image['image'].lower().find("http") > -1:
				imgEmbed = discord.Embed(title="", color=0xfd4949)
				imgEmbed.add_field(name="기술 이미지", value=image['odr'], inline=False)
				imgEmbed.set_image(url=image['image'])
				message = await channel.send(embed=imgEmbed)
				messages.append(message)
	return messages


async def c_embed(channel, title, description, data):
	embed = discord.Embed(title=title, description=description, color=0xf3fd68)
	messages = []
	message = await channel.send(embed=embed)
	messages.append(message)
	command = None
	skname = None
	embed = discord.Embed(color=0xf3fd68)
	commands = data["커맨드"]
	sknames = data["기술명"]
	for idx in range(0, len(commands)):
		command = commands[idx]
		skname = sknames[idx]
		if idx % 20 == 19:
				message = await channel.send(embed=embed)
				messages.append(message)
				embed = discord.Embed(color=0xf3fd68)
		embed.add_field(name=command, value=skname, inline=False)
	message = await channel.send(embed=embed)
	messages.append(message)
	return messages


async def g_embed(channel, title):
	row = db.walkthrough(title)
	if not row:
		embed = discord.Embed(title="해당하는 정보를 찾을 수 없습니다", description="다시 한 번 확인해 주세요", color=0xedf11e)
	else:
		embed = discord.Embed(title=title, description='공략글', color=0x00bd26)
		embed.add_field(name='링크', value=row['walkthrough'])
	await channel.send(embed=embed)
