import discord

import json
import logging
import sys
import os

from datetime import timedelta,datetime,timezone
from discord.ext import commands

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger('chall-bot')

config = json.load(open('conf.json', 'r'))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def kill(ctx):
	log.info("kill command executed")
	await bot.close()

@bot.command()
async def ticket(ctx):
	log.info("ticket command executed")

	await ctx.message.author.send(config['ticket_prompt'])

async def process_ticket(message):
	try:
		title,contents = message.content.split('\n')
		if '..' in title:
			raise ValueError('Invalid title')

		if not os.path.exists(config['ticket_dir']):
			os.mkdir(config['ticket_dir'])

		ticket_path = os.path.join(config['ticket_dir'], title)
		ticket_dir, _ = os.path.split(ticket_path)

		if not os.path.isdir(ticket_dir):
			raise ValueError('Invalid directory')

		with open(ticket_path, 'w') as f:
			f.write(contents)
		await message.reply(config['ticket_confirm'])
		
	except ValueError:
		await message.reply(config['ticket_fail'])

@bot.event
async def on_message(message):
	if message.guild == None and not message.author == bot.user:
		log.info(f"Received DM '{message.content}' from '{message.author}'")
		await process_ticket(message)

	await bot.process_commands(message)

bot.run(config['token'])
