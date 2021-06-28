from discord.ext import commands
import discord
from discord.ext.commands.core import command
import asyncio

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

def setup(bot):
    bot.add_cog(Utility(bot))
