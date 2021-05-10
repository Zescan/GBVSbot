import discord
import numpy as np
import asyncio


async def t_embed(channel, title, description, data):
  embed = discord.Embed(title=title, description=description, color=0xfd4949)
  for info_key in data:
    if info_key == '가드판정':
        embed.add_field(name=info_key, value=str(data[info_key]), inline=False)
    else:
        embed.add_field(name=info_key, value=str(data[info_key]), inline=True)
  message = await channel.send(embed=embed)
  return message

async def c_embed(channel, title, description, data):
    embed = discord.Embed(title=title, description=description)
    message = await channel.send(embed=embed)
    return message