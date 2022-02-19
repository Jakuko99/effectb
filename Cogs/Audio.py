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

def getItem(url):
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
           self.serverSide = {} #dictionary of dictionaries to store information about playback for isolation across guilds

    @commands.command(name="play", help="plays audio form URL")
    async def play(self,ctx,*data):
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
            return
        else:
            if not guild_id is self.serverSide:
                self.serverSide[guild_id] = {"next":False, "pause":False} #create entry for guild        
                self.serverSide[guild_id].update({"VC":voice_channel, "ctx":ctx})
                self.serverSide[guild_id]["pos"], self.serverSide[guild_id]["queue"] = 0, [] 
            if not voice_channel.is_playing():  
                async with ctx.typing():
                    try:                                   
                        yt = playback(url, voice_channel, guild_id)
                        self.bot.loop.create_task(self.Queue(guild_id))
                        self.serverSide[guild_id]["queue"].append(yt)
                        info = "Now playing"
                    except Exception as e:
                        print(e)
                        error = discord.Embed(title="Invalid video URL or error occured!", description="Check given link and try again.", color=discord.Color.green())                        
                        # error.add_field(name="**Exception:**", value=e)
                        await ctx.send(embed=error)
                        return #end command after wrong link
            else:
                yt = getItem(url)                
                self.serverSide[guild_id]["queue"].append(yt)
                self.serverSide[guild_id].update({"VC":voice_channel, "ctx":ctx}) #join dictionary to another one
                if not self.Queue.is_running(): #if the task is already running no need to start it again
                    print("task running")
                    try:                    
                        self.Queue.start(guild_id) #can you pass argument when starting task then ??
                    except Exception as e:
                        print(e)
                info = "Added to the queue"

            embed = discord.Embed(title=info,  description=f"{yt.title}\n{yt.watch_url}", color = discord.Color.green()) #maybe add url later
            embed.set_thumbnail(url=yt.thumbnail_url)
            embed.set_footer(icon_url= ctx.author.avatar_url, text= f"Requestested by {ctx.author.name}")
            await ctx.message.add_reaction('\U0001F44C')
            await ctx.send(embed = embed)

    @tasks.loop(seconds = 1)             
    async def Queue(self, guild_id):
        if guild_id in self.serverSide:
            playlist, pos, ctx, voiceChannel = self.serverSide[guild_id]["queue"], self.serverSide[guild_id]["pos"], self.serverSide[guild_id]["ctx"], self.serverSide[guild_id]["VC"]
            if not discord.utils.get(self.bot.voice_clients, guild=ctx.guild):                             
                self.Queue.stop() #stop task if disconnected from voice channel
                self.serverSide.pop(guild_id) #clear out the entry for guild       
            elif not voiceChannel.is_playing() and pos < len(playlist) and self.serverSide[guild_id]["pause"] == False: #if not playing then play next one                        
                async with ctx.typing():
                    try:
                        yt = playback(playlist[pos].watch_url, voiceChannel, guild_id)
                    except:
                        return
                    embed = discord.Embed(title="Currently playing", description=f"{yt.title}\n{yt.watch_url}", color=discord.Color.green())
                    embed.set_thumbnail(url=yt.thumbnail_url)
                    self.serverSide[guild_id]["pos"] += 1
                await ctx.send(embed=embed, delete_after=60)                        
            elif self.serverSide[guild_id]["next"] == True: #TODO: fix problem with next command
                voiceChannel.stop()
                self.serverSide[guild_id]["next"] = False
        else:
            try:
                self.Queue.stop() #stop task if there is no entry for guild
            except:
                pass


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
        guild_id = ctx.message.guild.id
        if guild_id in self.serverSide:
            self.serverSide[guild_id]["pause"] = True
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.pause()
            await ctx.message.add_reaction('\U000023F8')
            await ctx.message.delete(delay=5) #delete message after successful execution
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @commands.command(name='resume', aliases=['re'], help='resumes the playback')
    async def resume(self,ctx):
        guild_id = ctx.message.guild.id
        if guild_id in self.serverSide:
            self.serverSide[guild_id]["pause"] = False
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            voice_client.resume()
            await ctx.message.add_reaction('\U000025B6')
            await ctx.message.delete(delay=5)
        else:
            await ctx.send("The bot was not playing anything before this. Use play command")            

    @commands.command(name='stop', help='stops the playback')
    async def stop(self,ctx):
        guild_id = ctx.message.guild.id
        try:
            self.track.stop()
            self.Queue.stop()
            self.serverSide.pop(guild_id)
        except:
            pass
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
            await ctx.message.add_reaction('\U000023F9')
            await ctx.message.delete(delay=5)
        else:
            await ctx.send("The bot is not playing anything at the moment.")            

    @commands.command(name="playlist", help = "plays videos from given playlist URL")
    async def playlist(self, ctx, url):
        guild_id = ctx.message.guild.id
        self.serverSide[guild_id] = {"next":False, "pause":False} #create entry for guild
        try:
            user = ctx.message.author
            vc = user.voice.channel
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
            if voice == None:
                await vc.connect()
            server = ctx.message.guild
            voice_channel = server.voice_client
            voice_channel.stop()
        except:
            await ctx.send("The bot is not connected to a voice channel.")
        else:
            async with ctx.typing():
                playlist = Playlist(url)
                playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)") #fix empty videos playlist
                pos = self.serverSide[guild_id]["pos"] = 0                
                embed = discord.Embed(title="Playing content from playlist", description = f"{playlist.title} ({len(playlist)} tracks)", color=discord.Color.green())
                embed.set_thumbnail(url=playlist.videos[pos].thumbnail_url)
                embed.set_footer(icon_url= ctx.author.avatar_url, text= f"Requestested by {ctx.author.name}")
                self.bot.loop.create_task(self.track(guild_id)) #create task and pass guild id
                self.serverSide[guild_id].update({"VC":voice_channel, "playlist":playlist, "ctx":ctx}) #join dictionary to another one
                try:
                    self.track.start(guild_id) #can you pass argument when starting task then ??
                except Exception as e:
                    print(e)
                await ctx.message.add_reaction('\U0001F44C')
                await ctx.send(embed=embed) # adding delete_after=1 parameter would delete message after 1 second                    
    
    @tasks.loop(seconds = 1)             
    async def track(self, guild_id):
        if guild_id in self.serverSide:
            playlist, pos, ctx, voiceChannel = self.serverSide[guild_id]["playlist"], self.serverSide[guild_id]["pos"], self.serverSide[guild_id]["ctx"], self.serverSide[guild_id]["VC"]
            if not discord.utils.get(self.bot.voice_clients, guild=ctx.guild):                             
                self.track.stop() #stop task if disconnected from voice channel
                self.serverSide.pop(guild_id) #clear out the entry for guild       
            elif not voiceChannel.is_playing() and pos < len(playlist) and self.serverSide[guild_id]["pause"] == False: #if not playing then play next one                        
                async with ctx.typing():
                    try:
                        yt = playback(playlist.videos[pos].watch_url, voiceChannel, guild_id)
                    except:
                        return
                    embed = discord.Embed(title="Currently playing", description=f"{yt.title}\n{yt.watch_url}", color=discord.Color.green())
                    embed.set_thumbnail(url=yt.thumbnail_url)
                    self.serverSide[guild_id]["pos"] += 1
                await ctx.send(embed=embed, delete_after=60)                        
            elif self.serverSide[guild_id]["next"] == True: #TODO: fix problem with next command
                voiceChannel.stop()
                self.serverSide[guild_id]["next"] = False
        else:
            try:
                self.track.stop() #stop task if there is no entry for guild
            except:
                pass

    @commands.command(name="next", aliases= ['ne'], help="play next item in playlist")
    async def next(self, ctx):
        guild_id = ctx.message.guild.id
        self.serverSide[guild_id]["next"] = True
        await ctx.message.add_reaction('\U000023e9')
        await ctx.message.delete(delay=5) #perform deletion of message 5 seconds later

    @commands.command(name="now", help="returns currently playing track in playlist")
    async def now(self, ctx):
        guild_id = ctx.message.guild.id        
        if guild_id in self.serverSide:
            pos = self.serverSide[guild_id]["pos"]
            if "queue" in self.serverSide[guild_id]:
                current = self.serverSide[guild_id]["queue"][pos if pos==0 else pos-1]
            elif "playlist" in self.serverSide[guild_id]:
                current = self.serverSide[guild_id]["playlist"].videos[pos if pos==0 else pos-1]
        else:
            await ctx.send("Currently not playing any music")
            return #if no thing exists as playlist or queue
        yt = YouTube(current.watch_url)
        embed = discord.Embed(title="Currently playing", description=f"{yt.title}\n{yt.watch_url}", color=discord.Color.green())
        embed.set_thumbnail(url=yt.thumbnail_url)
        await ctx.send(embed=embed, delete_after=60) #delete informational messages after 60 seconds to avoid cluttering
        await ctx.message.add_reaction('\U0001F3B5')
        await ctx.message.delete(delay=5)
    
def setup(bot):
    bot.add_cog(Audio(bot))