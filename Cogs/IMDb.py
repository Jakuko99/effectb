from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import discord
from imdb import IMDb
from tools import Tools

class Imdb(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.imdb = IMDb()
        self.tools = Tools()

    @cog_ext.cog_slash(name="search", description="search phrase on IMDb")
    # @commands.command(name="search", help="search phrase on IMDb")
    async def search(self, ctx: SlashContext, search_phrase: str):
        # queryString = self.tools.tupleUnpack(data)
        # async with ctx.typing():
        query = self.imdb.search_movie(search_phrase)
        movies = ""
        for movie in query:
            movies += f"{movie}, "
        movies = movies[:-2]
        Search = discord.Embed(title=f'Found {len(query)} results containing "{search_phrase}":',description=movies, color=discord.Color.green())
        Search.set_footer(icon_url= ctx.author.avatar_url, text= f"Searched by {ctx.author.name}")
        Search.set_thumbnail(url="https://i.imgur.com/jQgjBgO.png")
        await ctx.send(embed=Search)
    
    @cog_ext.cog_slash(name="movie", description="sends info about movie or series")
    # @commands.command(name="movie", help="sends info about movie or series")
    async def movie(self,ctx: SlashContext, phrase: str):
        # movie = self.tools.tupleUnpack(data)
        search = self.imdb.search_movie(phrase)
        content = self.imdb.get_movie(search[0].movieID)
        if 'cover url' in content:
            ThumbUrl = content['full-size cover url']
        else:
            ThumbUrl = "https://i.imgur.com/jQgjBgO.png"
        if not content['kind'].find("series") == -1:
            year = content['series years']
            if 'plot outline' in content:
                plot = self.tools.shortenText(content['plot outline'], 4)
            else: 
                plot = self.tools.shortenText(content['plot'][0], 3)
            movieEmbed = discord.Embed(title = f"{content['title']} ({year})",
                                    description = plot,
                                    url= f"https://imdb.com/title/tt{content.movieID}", 
                                    color=discord.Color.green())
            movieEmbed.add_field(name= "Genres", value= self.tools.joinList(content['genres']), inline= True)
            movieEmbed.add_field(name= "Rating", value= content['rating'], inline= True)
            movieEmbed.add_field(name= "Seasons", value= content['seasons'], inline= True)
            movieEmbed.add_field(name= "Runtime", value= self.tools.convertTime(content['runtimes'][0]), inline= True)
            movieEmbed.add_field(name= "Writers", value= self.tools.joinList(content['writer']), inline = True)
            #maybe add something else to second line
            movieEmbed.add_field(name= "Cast", value= self.tools.partialJoin(content['cast'], 15), inline= False)
        else:
            year = content['year']
            if 'plot outline' in content:
                plot = self.tools.shortenText(content['plot outline'], 4)
            elif 'plot' in content: 
                plot = self.tools.shortenText(content['plot'][0], 4)
            else:
                plot = "None"
            movieEmbed = discord.Embed(title = f"{content['title']} ({year})",
                                    description = plot,
                                    url= f"https://imdb.com/title/tt{content.movieID}", 
                                    color=discord.Color.green())
            movieEmbed.add_field(name="Genres", value= self.tools.joinList(content['genres']), inline= True)
            try:
                movieEmbed.add_field(name="Rating", value=content['rating'], inline= True)
            except:
                movieEmbed.add_field(name="Rating", value="Not rated", inline= True)
            movieEmbed.add_field(name="Runtime", value=self.tools.convertTime(content['runtimes'][0]), inline= True)
            movieEmbed.add_field(name= "Writers", value= self.tools.joinList(content['writer']), inline = True)
            movieEmbed.add_field(name="Cast", value=self.tools.partialJoin(content['cast'], 15), inline= False)
        movieEmbed.set_thumbnail(url = ThumbUrl)
        movieEmbed.set_footer(icon_url= ctx.author.avatar_url, text= f"Requested by {ctx.author.name}")
        await ctx.send(embed = movieEmbed)

    @cog_ext.cog_slash(name="actor", description="sends info about actor or actress")
    # @commands.command(name="actor", help="sends info about actor or actress") #TODO: fix biography and filmography
    async def actor(self, ctx: SlashContext, name:str):
        # actor = self.tools.tupleUnpack(data)
        person = self.imdb.search_person(name)
        content = person[0]
        self.imdb.update(content, info= ['biography'])
        self.imdb.update(content, info= ['filmography'])
        if 'headshot' in content:
            url = content['full-size headshot']
        else:
            url = "https://i.imgur.com/jQgjBgO.png" #if something goes wrong
        bio = self.tools.shortenText(content['biography'][0], 4)
        if len(bio) > 4000:
            bio = bio[:4000-len(bio)]   
        person_embed = discord.Embed(title=content['name'], 
                            description=bio,
                            url = f"https://imdb.com/name/nm{content.personID}",
                            color = discord.Color.green())
        if 'birth date' in content:
            person_embed.add_field(name="Born", value=self.tools.formatDate(content['birth date']), inline=True)
        if 'actor' in content['filmography']:
            person_embed.add_field(name= "Filmography", value= self.tools.processFilmography(content['filmography']['actor'], 10))
        elif 'actress' in content['filmography']:
            person_embed.add_field(name= "Filmography", value= self.tools.processFilmography(content['filmography']['actress'], 10))
        person_embed.set_thumbnail(url=url)
        person_embed.set_footer(icon_url= ctx.author.avatar_url, text= f"Requested by {ctx.author.name}")        
        await ctx.send(embed=person_embed)

def setup(bot):
    bot.add_cog(Imdb(bot))
