from discord import guild, message
from discord.ext import commands
import logging
import random
import discord
import youtube_dl
import asyncio
import praw
import os
from dotenv import load_dotenv
import pyttsx3

OStype = os.name
engine = pyttsx3.init()
voices = engine.getProperty('voices') #get installed voices, pyttsx3 works only on Windows

load_dotenv()
reddit = praw.Reddit(client_id=os.getenv("REDDIT_ID"), client_secret=os.getenv("REDDIT_SECRET"), username=os.getenv("REDDIT_NAME"), password=os.getenv("REDDIT_PASS"), user_agent="effectbot", check_for_async=False)

TOKEN = os.getenv("BOT_TOKEN")   #bot token
servers = []
quotes = []

ffmpeg_options = {
    'options': '-vn'
}
ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

def loadFile(file):
    f = open(file)
    content = []
    for line in f.readlines():
        content.append(line.strip())
    return content

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

logger = logging.getLogger("discord")   #logger configuration
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix="!")  #creating object bot with ! prefix
@bot.event
async def on_ready():   #bot ready console message, prints servers where the bot is used
    print("Bot is running on",OStype)
    print(f'{bot.user} is ready!')
    for guild in bot.guilds:
        servers.append(guild.name)
    print("Bot is in these servers:",servers)

@bot.command(name="funny", help="returns funny quote, test command") #test command for messages
async def nine_nine(ctx):
    # quotes = [
    #     'Nespadol som, len som mužne napadol podlahu.',
    #     'Nie som lenivý, len mám silnú motiváciu nerobiť nič.',
    #     'Smejte sa svojím problémom, ostatní sa im smejú tiež.',
    #     'Však vy sa dosmejete, keď sa prestanete smiať.',
    #     'Pokiaľ budú kakaové bôby rásť na stromoch, je pre mňa čokoláda ovocie.',
    #     'Sú dva typy ľudí. Tí, ktorí umývajú riad, lebo práve dojedli a tí, ktorí umývajú riad, lebo práve sa chystajú jesť',
    #     'Multitasking - umenie pokaziť viac vecí naraz!',
    #     'Milujem cestovanie! Zvlášť keď cestujú ľudia, čo mi lezú na nervy.',
    #     'Ranné vtáča prezíva celý deň.',
    #     'Pozor! Chyba užívateľa. Vymeňte užívateľa a stlačte ľubovoľnú klávesu.'
    # ]
    response = random.choice(quotes)
    await ctx.send(response)

@bot.command(name="meme", help="displays funny meme from Reddit") #meme module with Praw
async def meme(ctx, subred = "memes"):
    sub = reddit.subreddit(subred)
    all_subs = []
    top = sub.top(limit= 50)
    for submission in top:
        all_subs.append(submission)
    random_sub = random.choice(all_subs)
    try:    #some posts don't have post_hint attribute
        if not random_sub.post_hint == "image":
            random_sub = random.choice(all_subs)    #generate new random post
    except:
        random_sub = random.choice(all_subs) #generate new random post, if there is no post_hint attribute
    em =  discord.Embed(title=random_sub.title, color=discord.Color.green())
    em.set_image(url = random_sub.url)
    await ctx.send(embed = em)

@bot.command(name="join", help="tells bot to join voice channel you are in")   #join voice channel
async def join(ctx):
    channel = ctx.author.voice.channel
    await ctx.message.add_reaction('\U0001F596')
    await channel.connect()
@bot.command(aliases=['disconnect', 'dc'], help="disconnects bot from voice channel")  #leave voice channel, uses aliases for command
async def leave(ctx):
    await ctx.message.add_reaction('\U0001F44B')
    await ctx.voice_client.disconnect()

@bot.command(name="play", help="playback test command")
async def play(ctx,url):
    try:
        user = ctx.message.author
        vc = user.voice.channel
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice == None:
            await vc.connect()
        server = ctx.message.guild
        voice_channel = server.voice_client
    except:
        await ctx.send("The bot is not connected to a voice channel.")
    else:
        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            if OStype == "nt":
                voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename)) #windows play function
            elif OStype == "posix":
                voice_channel.play(discord.FFmpegPCMAudio(filename)) #linux play function
            filename = filename.replace("_", " ")
            filename = filename[:-16]
            if (filename[-1] == "-"): 
                filename = filename[:-1]
            embed = discord.Embed(title="Now playing", description=filename, color = discord.Color.green())
            embed.set_footer(icon_url= ctx.author.avatar_url, text= f"Requestested by {ctx.author.name}")
        await ctx.message.add_reaction('\U0001F44C')
        await ctx.send(embed = embed)
        

@bot.command(name="pl", help="audio test command")
async def pl(ctx):
    try:
        user = ctx.message.author
        vc = user.voice.channel
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice == None:
            await vc.connect()
        server = ctx.message.guild
        voice_channel = server.voice_client
    except:
        await ctx.send("The bot is not connected to a voice channel.")
    else:
        filename = "test_file.mp3"
        if OStype == "nt":
                voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename)) #windows play function
        elif OStype == "posix":
            voice_channel.play(discord.FFmpegPCMAudio(filename)) #linux play function
        embed = discord.Embed(title="Now playing", description=filename, color = discord.Color.green())
        embed.set_footer(icon_url= ctx.author.avatar_url, text= f"Requestested by {ctx.author.name}")
    await ctx.send(embed = embed)

@bot.command(name='pause', help='pauses current song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.pause()
        await ctx.message.add_reaction('\U000023F8')
    else:
        await ctx.send("The bot is not playing anything at the moment.")

@bot.command(name='resume', help='resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        voice_client.resume()
        await ctx.message.add_reaction('\U000025B6')
    else:
        await ctx.send("The bot was not playing anything before this. Use play command")

@bot.command(name='stop', help='stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
        await ctx.message.add_reaction('\U000023F9')
    else:
        await ctx.send("The bot is not playing anything at the moment.")
@bot.command(name='say', help='Says text using tts, put your text in quotes')
async def say(ctx,message,voice="m"):
    if OStype == "nt": #check for operating system of computer, TTS only works on Windows for now
        engine.setProperty('rate',180) #say message a little bit slower, default setting is 200
        if voice.lower() == "f":
            engine.setProperty('voice', voices[1].id) #change voice to MS Zira
        elif voice.lower() == "m":
            engine.setProperty('voice', voices[0].id) #change voice to MS David, default setting
        engine.save_to_file(message, 'tts.mp3') #save message output to audio file, TODO: add queue for audio tracks
        engine.runAndWait()
        #engine.stop() #not neccessary to stop engine each time
        try:
            user = ctx.message.author
            vc = user.voice.channel
            voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
            if voice == None:
                await vc.connect()
            server = ctx.message.guild
            voice_channel = server.voice_client
        except:
            await ctx.send("The bot is not connected to a voice channel.")
        else:
            filename = "tts.mp3"
            if OStype == "nt":
                    voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename)) #windows play function
            elif OStype == "posix":
                voice_channel.play(discord.FFmpegPCMAudio(filename)) #linux play function
            embed = discord.Embed(title="Speaking message:", description=message, color = discord.Color.green())
            #embed.set_footer(icon_url= ctx.author.avatar_url, text= f"Requestested by {ctx.author.name}")
        await ctx.message.add_reaction('\U0001f4ac')
        await ctx.send(embed = embed)
    else:
        await ctx.message.add_reaction('\U0001F625')
        await ctx.send("TTS command is available only on Windows at this moment.")

# @bot.command(aliases=['members', 'memb'], help = 'Get members in current voice channel')  #Not working to get id of voice channel
# async def membs(ctx):
#     if ctx.author.voice and ctx.author.voice.channel:
#         channelName = ctx.author.voice.channel
#     else:
#         await ctx.send("You are not connected to a voice channel")
#     voice_channel = discord.utils.get(ctx.message.guild.channels, name=channelName, type=discord.ChannelType.voice)
#     voice_channel = discord.utils.get(message.Guild.members, name = channelName)
#     await ctx.send(voice_channel)

quotes= loadFile("quotes.txt")
bot.run(TOKEN)