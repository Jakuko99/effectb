import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import os
from dotenv import load_dotenv
import apraw
import random

def loadFile(file):
    f = open(file)
    content = []
    for line in f.readlines():
        content.append(line.strip())
    return content

load_dotenv()
reddit = apraw.Reddit(client_id=os.getenv("REDDIT_ID"), client_secret=os.getenv("REDDIT_SECRET"), username=os.getenv("REDDIT_NAME"), password=os.getenv("REDDIT_PASS"), user_agent="effectbot")
quotes = []
quotes= loadFile("quotes.txt")

class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command(name="meme", help="displays funny meme from Reddit") #meme module with Praw
    @cog_ext.cog_slash(name="meme", description="displays funny meme from Reddit")
    async def meme(self, ctx: SlashContext,sub=""):
        subred = sub if not len(sub) == 0 else random.choice(["memes", "funny", "comedycemetery", "teenagers", "dankmemes"]) #randomly choose subredit if none given
        # async with ctx.typing():
        sub = await reddit.subreddit(subred)
        all_subs = []
        top = sub.top(limit=50)
        async for submission in top:
            all_subs.append(submission)
        random_sub = random.choice(all_subs)
        try:    #some posts don't have post_hint attribute
            if not random_sub.post_hint == "image":
                random_sub = random.choice(all_subs)    #generate new random post
        except:
            random_sub = random.choice(all_subs) #generate new random post, if there is no post_hint attribute
        em = discord.Embed(title=random_sub.title, color=discord.Color.green())
        em.set_image(url = random_sub.url)
        await ctx.send(embed = em) 
    
    @cog_ext.cog_slash(name="funny", description="returns funny quote", options=None)
    # @commands.command(name="funny", help="returns funny quote, test command") #test command for messages
    async def nine_nine(self, ctx: SlashContext):
        response = random.choice(quotes)
        await ctx.send(response)

def setup(bot):
    bot.add_cog(Chat(bot))
