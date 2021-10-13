# Test script for interaction based messages using DiscordAPI compoments

from discord.ext import commands
import discord
import discord_slash.utils.manage_components as utils
from discord_slash.model import ButtonStyle
from discord_slash.cog_ext import cog_component

class Components(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="test", help="test command for discord components")
    async def test(self, ctx):
        buttons = [
            utils.create_button(style=ButtonStyle.green, label="A green button"),
            utils.create_button(style=ButtonStyle.blue, label="A blue button")
        ]
        action_row = utils.create_actionrow(*buttons)
        await ctx.send("Button test message", components=[action_row])

    @cog_component() #figure how to make component callback in cogs
    async def hello(self, ctx):
        await ctx.edit_origin(content="Button pressed")


def setup(bot):
    bot.add_cog(Components(bot))
