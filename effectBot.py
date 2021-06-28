from discord.ext import commands
import logging
import discord
import os
from dotenv import load_dotenv

OStype = os.name
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")   #bot token
servers = []

logger = logging.getLogger("discord")   #logger configuration
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix="!",status=discord.Status.online)  #creating object bot with ! prefix

@bot.event
async def on_ready():   #bot ready console message, prints servers where the bot is used
    print("Bot is running on",OStype)
    print(f'{bot.user} is ready!')
    for guild in bot.guilds:
        servers.append(guild.name)
    print("Bot is in these servers:",servers)

bot.load_extension("Cogs.Audio") #load audio commands (pl, play)
bot.load_extension("Cogs.Utility") #commands for joining and disconnecting from VCs
bot.load_extension("Cogs.Chat") #funny and meme comands
bot.load_extension("Cogs.Administrative") #protected set of commands

if OStype == "nt":
    bot.load_extension("Cogs.TTS") #only load on Windows for now

bot.run(TOKEN)