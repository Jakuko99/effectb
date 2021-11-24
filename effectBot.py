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

@bot.event
async def on_guild_join(guild): #custom bot join message
     if guild.system_channel: #TODO: add alternative if can't send in system channel
        embed=discord.Embed(title="Thanks for adding me to your server!", description="My default prefix is **!**. Type !help to get started, I am still under development, so don't worry when I'm offline.", color=discord.Color.green())
        embed.set_thumbnail(url="https://i.imgur.com/wcuNoz2.jpg?1")
        embed.add_field(name="You can find support and updates here:", value="https://discord.gg/Dx3JaJfkcD", inline=False) #always check if there is correct invite link
        await guild.system_channel.send(embed=embed)

@bot.event
async def on_message(ctx): #mentioning the bot sends info embed
    if f"<@!{bot.user.id}>" in ctx.content:
        embed = discord.Embed(title="Bot mention",
                              description= "Bot's current prefix is **!**, customizable prefix maybe coming soon!",
                              color = discord.Color.green())
        embed.add_field(name="Support server", value="https://discord.gg/Dx3JaJfkcD \n Join if you found some bugs, that would be huge help for me.")
        embed.add_field(name="Last update:", value="24.11.2021") #don't forget to change after each update!!
        await ctx.channel.send(embed=embed)
    await bot.process_commands(ctx) #get rid of bot's soft lock

bot.load_extension("Cogs.Audio") #load audio commands (pl, play)
bot.load_extension("Cogs.Utility") #commands for joining and disconnecting from VCs
bot.load_extension("Cogs.Chat") #funny and meme comands
bot.load_extension("Cogs.Administrative") #protected set of commands
bot.load_extension("Cogs.IMDb") #load IMDb module
#bot.load_extension("Cogs.Components") #components cog

if OStype == "nt":
    bot.load_extension("Cogs.TTS") #only load on Windows for now

bot.run(TOKEN)