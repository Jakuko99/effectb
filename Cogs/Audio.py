from discord.ext import commands, tasks
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
           self.pos = 0
           self.stop = True
           self.next = False
           self.pause = False

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
                try:
                    self.track.stop() #fully stop playback of playlist
                except:
                    pass
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
        self.pause = True
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.pause()
            await ctx.message.add_reaction('\U000023F8')
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @commands.command(name='resume', aliases=['re'], help='resumes the playback')
    async def resume(self,ctx):
        self.pause = False
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            voice_client.resume()
            await ctx.message.add_reaction('\U000025B6')
        else:
            await ctx.send("The bot was not playing anything before this. Use play command")

    @commands.command(name='stop', help='stops the playback')
    async def stop(self,ctx):
        voice_client = ctx.message.guild.voice_client
        self.stop = True
        self.track.stop()
        if voice_client.is_playing():
            voice_client.stop()
            await ctx.message.add_reaction('\U000023F9')
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @commands.command(name="playlist", help = "plays videos from given playlist URL")
    async def playlist(self, ctx, url):
        self.stop = False
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
                self.pos = 0
                yt = playback(playlist.videos[self.pos].watch_url, voice_channel)
                embed = discord.Embed(title="Playing content from playlist", description = f"{playlist.title} ({len(playlist)} tracks)", color=discord.Color.green())
                embed.add_field(name="Track:", value=f"{yt.title}\n{yt.watch_url}", inline=True)
                embed.set_thumbnail(url=playlist.videos[self.pos].thumbnail_url)
                self.pos += 1
                self.bot.loop.create_task(self.track())
                self.voice_channel = voice_channel
                self.playlist = playlist
                self.ctx = ctx
                try:
                    self.track.start()
                except:
                    pass #do nothing, because task is already running
                await ctx.message.add_reaction('\U0001F44C')
                await ctx.send(embed=embed) # adding delete_after=1 parameter would delete message after 1 second                    
    
    @tasks.loop(seconds = 1)             
    async def track(self):
        if not discord.utils.get(self.bot.voice_clients, guild=self.ctx.guild):
            self.track.stop() #stop task if disconnected from voice channel
        elif self.stop == True:
            self.stop = False
        elif not self.voice_channel.is_playing() and self.pos < len(self.playlist) and self.pause == False: #if not playing then play next one                        
            async with self.ctx.typing():
                yt = playback(self.playlist.videos[self.pos].watch_url, self.voice_channel)
                embed = discord.Embed(title="Currently playing", description=f"{yt.title}\n{yt.watch_url}", color=discord.Color.green())
                embed.set_thumbnail(url=yt.thumbnail_url)
            self.pos += 1
            await self.ctx.send(embed=embed, delete_after=60)   
            self.track.stop() #stop background task                     
        elif self.next == True:
            self.voice_channel.stop()
            self.next = False   

    @commands.command(name="next", aliases= ['ne'], help="play next item in playlis")
    async def next(self, ctx):
        self.next = True
        #await ctx.message.add_reaction('\U000023e9')
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(Audio(bot))