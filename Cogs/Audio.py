from discord.ext import commands
from discord import guild,message
from pytube import YouTube, Search, Playlist
from tools import Tools
import re

import discord
import asyncio
import os

OStype = os.name

def playback(url, voice_channel):
    Filename = "downloaded.mp3"
    if "http" in url: #check if string contains url address
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
    return yt

class Audio(commands.Cog):
    def __init__(self, bot):
           self.bot = bot
           self.tools = Tools()

    @commands.command(name="play", help="plays audio form URL")
    async def play(self,ctx,*data):
        url = self.tools.tupleUnpack(data) #combine tuple into single string
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
            if not voice_channel.is_playing():  
                async with ctx.typing():                                   
                    yt = playback(url, voice_channel)
                    info = "Now playing"
            else:
                voice_channel.stop() #stop previous playback and play given file
                yt = playback(url, voice_channel)
                info = "Stopping previous playback and playing"

            embed = discord.Embed(title=info,  description=f"{yt.title}\n{yt.watch_url}", color = discord.Color.green()) #maybe add url later
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
    async def playlist(self, ctx, url):
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
                playlist = Playlist(url)
                playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)") #fix empty videos playlist
                pos = 0
                yt = playback(playlist.videos[pos].watch_url, voice_channel)
                embed = discord.Embed(title="Playing content from playlist", description = playlist.title, color=discord.Color.green())
                embed.add_field(name="Track:", value=f"{yt.title}\n{yt.watch_url}", inline=True)
                embed.set_thumbnail(url=playlist.videos[pos].thumbnail_url)
                await ctx.message.add_reaction('\U0001F44C')
                await ctx.send(embed=embed) # adding delete_after=1 parameter would delete message after 1 second

def setup(bot):
    bot.add_cog(Audio(bot))