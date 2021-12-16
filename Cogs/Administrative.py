from discord.ext import commands
import discord
import os
from dotenv import load_dotenv
import pyotp

load_dotenv()
#key = pyotp.TOTP(os.getenv("SECRET_KEY"))

class Administrative(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.key = pyotp.TOTP(os.getenv("SECRET_KEY"))
        self.wrong = discord.Embed(title="Invalid OTP!", description="Seems like you entered wrong OTP, try again!", color=discord.Color.red())
        self.wrong.set_thumbnail(url="https://i.imgur.com/nfDZ49m.png") #admistrative error embed
    
    @commands.command(name="status") #protected by OTP, so everybody can't use it
    async def status(self,ctx,status,otp):
        if str(self.key.now()) == str(otp):
            embed = discord.Embed(title="Status change", description="Status set to "+status, color = discord.Color.red())
            embed.set_footer(icon_url= ctx.author.avatar_url, text= f"Performed by {ctx.author.name}")
            await self.bot.change_presence(activity=discord.Game(name=status))
            await ctx.message.add_reaction('\U0001F512')
            await ctx.send(embed = embed)
        else:
            await ctx.message.add_reaction('\U000026A0')
            await ctx.send(embed=self.wrong)

    @commands.command(name="info")
    async def info(self,ctx,type,otp):
        if str(self.key.now()) == str(otp):
            if type == "servers":
                servers,count = "",0
                for guild in self.bot.guilds:
                    servers += guild.name + ", "
                    count +=1
                servers = servers[:-2] #remove last two characters
                embed = discord.Embed(title="Bot is in these servers:", description=servers, color=discord.Color.gold())
                embed.add_field(name="Total count of servers: ", value=str(count), inline=True)
                await ctx.message.add_reaction('\U0001F512')
                await ctx.send(embed = embed)
        else:
            await ctx.message.add_reaction('\U000026A0')
            await ctx.send(embed=self.wrong)
        
    @commands.command(name="send")
    async def send(self,ctx,server,message,otp):
        if str(self.key.now()) == str(otp):
            if server == "":
                await ctx.send("Please specify a server!")
            else:
                sent = False
                for guild in self.bot.guilds:
                    if guild.name == server:
                        sent = True
                        await guild.system_channel.send(message)
                        await ctx.message.add_reaction('\U0001F4E3')
                        await ctx.send(f"Message successfully sent to {server}.")
                if sent == False:
                    await ctx.send(f"Guild {server} not found!")
        else:
            await ctx.message.add_reaction('\U000026A0')
            await ctx.send(embed=self.wrong) 

    @commands.command(name="cogs")
    async def cogs(self, ctx, action, module, otp):
        module = f"Cogs.{module}" #add Cogs. prefix to the command parameter
        if str(self.key.now()) == str(otp):
            if action == "load":
                try:
                    self.bot.load_extension(module)
                except Exception as ex:
                    await ctx.send(f"Loading {module} failed, {ex}")
                else:
                    await ctx.send(f"{module} loaded successfully!")
            elif action == "unload":
                try:
                    self.bot.unload_extension(module)
                except Exception as ex:
                    await ctx.send(f"Unloading {module} failed, {ex}")
                else:
                    await ctx.send(f"{module} unloaded successfully!")
            elif action == "reload":
                try:
                    self.bot.reload_extension(module)
                except Exception as ex:
                    await ctx.send(f"Reloading {module} failed, {ex}")
                else:
                    await ctx.send(f"{module} reloaded successfully!")
            elif action == "check": #check if given cog is loaded or not
                try:
                    self.bot.load_extension(module)
                except commands.ExtensionAlreadyLoaded:
                    await ctx.send("Cog is loaded")
                except commands.ExtensionNotFound:
                    await ctx.send("Cog not found")
                else:
                    await ctx.send("Cog is unloaded")
                    self.bot.unload_extension(module)
            else:
                await ctx.message.add_reaction('\U000026A0')
                await ctx.send(embed=self.wrong)
    @commands.command(name="verify") #command for verifying security key
    async def verify(self, ctx, otp):
        key = self.key.now()
        if str(key) == str(otp):
            await ctx.message.add_reaction('\U00002705')
            await ctx.send("Verification passed!")
        else:
            await ctx.message.add_reaction('\U000026A0')
            await ctx.send(f"Verification failed!")

def setup(bot):
    bot.add_cog(Administrative(bot))
