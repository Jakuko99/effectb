from discord.ext import commands
from discord import guild,message
from pytube import YouTube, Search, Playlist
from tools import Tools

import discord
import asyncio
import os

OStype = os.name

class Audio(commands.Cog):
    def __init__(self, bot):
           self.bot = bot
           self.tools = Tools()

    @commands.command(name="play", help="plays audio form URL")
    async def play(self,ctx,*data):
        url = self.tools.tupleUnpack(data)
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
                Filename = "downloaded.mp3"
                if "http" in url:
                    yt = YouTube(url)
                    stream = yt.streams.get_by_itag(140)
                    stream.download(filename=Filename)
                else:
                    Yt = Search(url)
                    stream= Yt.results[0].streams.get_by_itag(140)
                    stream.download(filename=Filename)
                    yt = Yt.results[0]
                
                if OStype == "nt":
                    voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=Filename)) #windows play function
                elif OStype == "posix":
                    voice_channel.play(discord.FFmpegPCMAudio(Filename)) #linux play function
                embed = discord.Embed(title="Now playing",  description=f"{yt.title}\n{yt.watch_url}", color = discord.Color.green()) #maybe add url later
                embed.set_thumbnail(url=yt.thumbnail_url)
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
        
    @commands.command(name='pause', aliases = ['pa'], help='pauses current playback')
    async def pause(self,ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.pause()
            await ctx.message.add_reaction('\U000023F8')
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @commands.command(name='resume', aliases=['re'], help='resumes the playback')
    async def resume(self,ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            voice_client.resume()
            await ctx.message.add_reaction('\U000025B6')
        else:
            await ctx.send("The bot was not playing anything before this. Use play command")

    @commands.command(name='stop', help='stops the playback')
    async def stop(self,ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
            await ctx.message.add_reaction('\U000023F9')
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @commands.command(name="playlist", help = "plays videos from given playlist URL")
    async def playlist(self, ctx, url=None): #change later to normal
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
                # playlist = Playlist(url)
                # if OStype == "nt":
                #     voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename)) #windows play function
                # elif OStype == "posix":
                #     voice_channel.play(discord.FFmpegPCMAudio(filename)) #linux play function
                # embed = discord.Embed(title="Playing content from playlist", description = playlist.title, color=discord.Color.green())
                # embed.set_thumbnail(url=playlist.videos[0].thumbnail_url)
                # await ctx.message.add_reaction('\U0001F44C')
                # await ctx.send(embed=embed)
                await ctx.send("Playlist feature coming soon") #also add queue command

def setup(bot):
    bot.add_cog(Audio(bot))