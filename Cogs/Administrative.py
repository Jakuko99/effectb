from discord.ext import commands
import discord
import os
from dotenv import load_dotenv
import pyotp

load_dotenv()
key = pyotp.TOTP(os.getenv("SECRET_KEY"))

class Administrative(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="status", help="administrative command and yes, it is protected") #protected by OTP, so everybody can't use it
    async def status(self,ctx,status,otp):
        if str(key.now()) == str(otp):
            embed = discord.Embed(title="Status change", description="Status set to "+status, color = discord.Color.red())
            embed.set_footer(icon_url= ctx.author.avatar_url, text= f"Performed by {ctx.author.name}")
            await self.bot.change_presence(activity=discord.Game(name=status))
            await ctx.message.add_reaction('\U0001F512')
            await ctx.send(embed = embed)
        else:
            await ctx.message.add_reaction('\U000026A0')
            await ctx.send("Incorrect OTP, try again.")

def setup(bot):
    bot.add_cog(Administrative(bot))
