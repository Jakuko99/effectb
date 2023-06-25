from discord.ext import commands
import discord
from discord_slash import cog_ext, SlashContext

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="join", description="tells bot to join voice channel you are in", options=None)
    # @commands.command(name="join", help="tells bot to join voice channel you are in")   #join voice channel
    async def join(self, ctx: SlashContext):
        channel = ctx.author.voice.channel
        await ctx.send("Connecting to voice channel")
        await channel.connect()

    @cog_ext.cog_slash(name="disconnect", description="disconnects bot from voice channel", options=None)
    # @commands.command(name="disconnect", aliases=['dc'], help="disconnects bot from voice channel")  #leave voice channel, uses aliases for command
    async def leave(self, ctx: SlashContext):
        await ctx.send("Disconnecting from voice channel")
        await ctx.voice_client.disconnect()

    @cog_ext.cog_slash(name="invite", description="sends invite to bot's support server", options=None)
    # @commands.command(name="invite", help="sends invite link to bot's support server")
    async def invite(self, ctx):
        embed = discord.Embed(title="Join bot's support server",
                              description="https://discord.gg/Dx3JaJfkcD",
                              color = discord.Color.green())
        embed.add_field(name="About", value="Be part of community and become tester for the bot to help me improve it and most importantly find bugs!")
        embed.set_thumbnail(url="https://i.imgur.com/wcuNoz2.jpg?1")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Utility(bot))
