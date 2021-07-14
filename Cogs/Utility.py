from discord.ext import commands
import discord

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="join", help="tells bot to join voice channel you are in")   #join voice channel
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        await ctx.message.add_reaction('\U0001F596')
        await channel.connect()

    @commands.command(name="disconnect", aliases=['dc'], help="disconnects bot from voice channel")  #leave voice channel, uses aliases for command
    async def leave(self, ctx):
        await ctx.message.add_reaction('\U0001F44B')
        await ctx.voice_client.disconnect()

    @commands.command(name="invite", help="sends invite link to bot's support server")
    async def invite(self, ctx):
        embed = discord.Embed(title="Join bot's support server",
        description="https://discord.gg/Dx3JaJfkcD",
        color = discord.Color.green())
        embed.set_thumbnail(url="https://i.imgur.com/wcuNoz2.jpg?1")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Utility(bot))
