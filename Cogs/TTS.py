from discord.ext import commands
import discord
import pyttsx3
import os

OStype = os.name

class TTS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.engine = pyttsx3.init() #works on linux as well, but only if it has tts voices installed
        self.voices = self.engine.getProperty('voices') #get installed voices, pyttsx3 works only on Windows

    @commands.command(name='say', help='Says text using tts, put your text in quotes')
    async def say(self,ctx,message,voice="m"):
        self.engine.setProperty('rate',180) #say message a little bit slower, default setting is 200
        if voice.lower() == "f":
            self.engine.setProperty('voice', self.voices[1].id) #change voice to MS Zira
        elif voice.lower() == "m":
            self.engine.setProperty('voice', self.voices[0].id) #change voice to MS David, default setting
        self.engine.save_to_file(message, 'tts.mp3') #save message output to audio file, TODO: add queue for audio tracks
        self.engine.runAndWait()
        #self.engine.stop() #not neccessary to stop engine each time
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
            filename = "tts.mp3"
            if OStype == "nt":
                voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename)) #windows play function
            elif OStype == "posix":
                voice_channel.play(discord.FFmpegPCMAudio(filename)) #linux play function
        embed = discord.Embed(title="Speaking message:", description=message, color = discord.Color.green())
        #embed.set_footer(icon_url= ctx.author.avatar_url, text= f"Requestested by {ctx.author.name}")
        await ctx.message.add_reaction('\U0001f4ac')
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(TTS(bot))
