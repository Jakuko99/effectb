from discord.embeds import Embed
from discord.ext import commands, tasks
from pytube import YouTube, Search, Playlist
from tools import Tools
import re

import discord
import os

OStype = os.name

def playback(url, voice_channel, guild_id):
    Filename = f"downloaded-{guild_id}.mp3"
    if "http" in url: #check if string contains url address
        yt = YouTube(url)
        stream = yt.streams.get_audio_only()
        stream.download(filename=Filename)
    else:
        Yt = Search(url)
        stream= Yt.results[0].streams.get_audio_only()
        stream.download(filename=Filename)
        yt = Yt.results[0]
    if OStype == "nt":
        voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=Filename)) #windows play function
    elif OStype == "posix":
        voice_channel.play(discord.FFmpegPCMAudio(Filename)) #linux play function
    return yt

def getPlaylistItem(url):
    if "http" in url: #check if string contains url address
        yt = YouTube(url)
    else:
        Yt = Search(url)
        yt = Yt.results[0]
    return yt

class Audio(commands.Cog):
    def __init__(self, bot):
           self.bot = bot
           self.tools = Tools()
           self.pos = 0
           self. queue_list = []
           self.stop = True
           self.next = False
           self.pause = False

    @commands.command(name="play", help="plays audio form URL")
    async def play(self,ctx,*data):
        self.pause = False #just to be sure
        guild_id = ctx.message.guild.id
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
                    try:                                   
                        yt = playback(url, voice_channel, guild_id)
                        info = "Now playing"
                    except:
                        error = discord.Embed(title="Invalid video URL!", description="Check given link and try again.", color=discord.Color.green())
                        # error.set_thumbnail(url="https://imgur.com/a/IvIJnD8") #some problem with image
                        await ctx.send(embed=error)
                        return #end command after wrong link
            else:
                yt = getPlaylistItem(url)
                self. queue_list.append(yt)
                self.ctx = ctx
                self.voice_channel = voice_channel
                self.guild_id = guild_id
                self.bot.loop.create_task(self.Queue())
                try:
                     self.Queue.start() #really important to start the task afterwards !!!
                except:
                    pass #task should be running
                info = f"Added {yt.title} to playlist"

            print(yt.watch_url)
            embed = discord.Embed(title=info,  description=f"{yt.title}\n{yt.watch_url}", color = discord.Color.green()) #maybe add url later
            embed.set_thumbnail(url=yt.thumbnail_url)
            embed.set_footer(icon_url= ctx.author.avatar_url, text= f"Requestested by {ctx.author.name}")
            await ctx.message.add_reaction('\U0001F44C')
            await ctx.send(embed = embed)

    @tasks.loop(seconds = 1)             
    async def Queue(self):
        if not discord.utils.get(self.bot.voice_clients, guild=self.ctx.guild):
            self.Queue.stop() #stop task if disconnected from voice channel
        elif not self.voice_channel.is_playing() and self.pause == False and len(self. queue_list) >= 1: #if not playing then play next one                        
            async with self.ctx.typing():                
                yt = playback(self. queue_list[0].watch_url, self.voice_channel, self.guild_id)
                embed = discord.Embed(title="Currently playing", description=f"{yt.title}\n{yt.watch_url}", color=discord.Color.green())
                embed.set_thumbnail(url=yt.thumbnail_url)         
                self.queue_list.pop(0) #remove first link       
            await self.ctx.send(embed=embed, delete_after=60)                        
        elif self.next == True:
            self.voice_channel.stop()
            self.next = False   
        elif len(self. queue_list) == 0:
            self.Queue.stop()
    
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
            await ctx.message.delete(delay=5) #delete message after successful execution
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @commands.command(name='resume', aliases=['re'], help='resumes the playback')
    async def resume(self,ctx):
        self.pause = False
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            voice_client.resume()
            await ctx.message.add_reaction('\U000025B6')
            await ctx.message.delete(delay=5)
        else:
            await ctx.send("The bot was not playing anything before this. Use play command")            

    @commands.command(name='stop', help='stops the playback')
    async def stop(self,ctx):
        self. queue_list.clear() #clear the playlist
        voice_client = ctx.message.guild.voice_client
        try:
            self.track.stop()
            self.Queue.stop()
        except:
            pass
        if voice_client.is_playing():
            voice_client.stop()
            await ctx.message.add_reaction('\U000023F9')
            await ctx.message.delete(delay=5)
        else:
            await ctx.send("The bot is not playing anything at the moment.")            

    @commands.command(name="playlist", help = "plays videos from given playlist URL")
    async def playlist(self, ctx, url):
        self.pause = False
        self.stop = False
        self.guild_id = ctx.message.guild.id
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
                yt = playback(playlist.videos[self.pos].watch_url, voice_channel, self.guild_id)
                embed = discord.Embed(title="Playing content from playlist", description = f"{playlist.title} ({len(playlist)} tracks)", color=discord.Color.green())
                embed.add_field(name="Track:", value=f"{yt.title}\n{yt.watch_url}", inline=True)
                embed.set_thumbnail(url=playlist.videos[self.pos].thumbnail_url)
                embed.set_footer(icon_url= ctx.author.avatar_url, text= f"Requestested by {ctx.author.name}")
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
            self.track.stop() #stop background task
        elif not self.voice_channel.is_playing() and self.pos < len(self.playlist) and self.pause == False: #if not playing then play next one                        
            async with self.ctx.typing():
                yt = playback(self.playlist.videos[self.pos].watch_url, self.voice_channel, self.guild_id)
                embed = discord.Embed(title="Currently playing", description=f"{yt.title}\n{yt.watch_url}", color=discord.Color.green())
                embed.set_thumbnail(url=yt.thumbnail_url)
                self.pos += 1
            await self.ctx.send(embed=embed, delete_after=60)                        
        elif self.next == True:
            self.voice_channel.stop()
            self.next = False

    @commands.command(name="next", aliases= ['ne'], help="play next item in playlist")
    async def next(self, ctx):
        self.next = True
        await ctx.message.add_reaction('\U000023e9')
        await ctx.message.delete(delay=5) #perform deletion of message 5 seconds later

    @commands.command(name="now", help="returns currently playing track in playlist")
    async def now(self, ctx):
        yt = YouTube(self.playlist.videos[self.pos if self.pos==0 else self.pos-1].watch_url)
        embed = discord.Embed(title="Currently playing", description=f"{yt.title}\n{yt.watch_url}", color=discord.Color.green())
        embed.set_thumbnail(url=yt.thumbnail_url)
        await ctx.send(embed=embed, delete_after=60) #delete informational messages after 60 seconds to avoid cluttering
        await ctx.message.add_reaction('\U0001F3B5')
        await ctx.message.delete(delay=5)

def setup(bot):
    bot.add_cog(Audio(bot))