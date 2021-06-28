from re import A
from discord.ext import commands
from discord import guild,message
import discord
import youtube_dl
import asyncio
import os

OStype = os.name

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

class Audio(commands.Cog):
    def __init__(self, bot):
           self.bot = bot

    @commands.command(name="play", help="plays audio form URL")
    async def play(self,ctx,url):
        try:
            user = ctx.message.author
            vc = user.voice.channel
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
            if voice == None:
                await vc.connect()
            server = ctx.message.guild
            voice_channel = server.voice_client
        except:
            await ctx.send("The bot is not connected to a voice channel.")
        else:
            async with ctx.typing():
                filename = await YTDLSource.from_url(url, loop=self.bot.loop) #voice.play(discord.FFMPegPCMAudio(file), afted = playlist)
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
    
    @commands.command(name="pl", help="audio test command")
    async def pl(self, ctx):
        try:
            user = ctx.message.author
            vc = user.voice.channel
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild) #bot = self.bot
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
        
    @commands.command(name='pause', help='pauses current song')
    async def pause(self,ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.pause()
            await ctx.message.add_reaction('\U000023F8')
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @commands.command(name='resume', help='resumes the song')
    async def resume(self,ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            voice_client.resume()
            await ctx.message.add_reaction('\U000025B6')
        else:
            await ctx.send("The bot was not playing anything before this. Use play command")

    @commands.command(name='stop', help='stops the song')
    async def stop(self,ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
            await ctx.message.add_reaction('\U000023F9')
        else:
            await ctx.send("The bot is not playing anything at the moment.")


def setup(bot):
    bot.add_cog(Audio(bot))