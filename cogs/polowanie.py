import json
import nextcord
import sqlite3
import random
from nextcord.ext import commands

class Items(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):

        print ("Ekonomia: polowanie - Gotowa!")


    @commands.command()
    async def polowanie(self, ctx):

        animal_list = [None, "🦊lis", "🐺wilk", "🐅tygyrs", "🐻niedźwiedź", "🦌jeleń", "🦓zebra", "🦄jednorożec", "🦫bóbr", "🦝szop", "🦔jeż", "🐿️wiewiórka", "🐇królik", "🦆kaczka", "🐗dzik"]

        db = sqlite3.connect("eco.db")
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM animals WHERE user_id = {ctx.author.id}")
        animals = cursor.fetchone()

        cursor.execute(f"SELECT łuk FROM tools WHERE user_id = {ctx.author.id}")
        łuk = cursor.fetchone

        amount =  random.randrange(15)
        polowanie = random.choice(animal_list)

      
    
        if łuk[0] > 0:
            if polowanie  == animal_list[1]:
                cursor.execute("UPDATE animals SET lis = ? WHERE user_id = ?", (animals[1] + amount, ctx.author.id))
            if polowanie  == animal_list[2]:
                cursor.execute("UPDATE animals SET wilk = ? WHERE user_id = ?", (animals[2] + amount, ctx.author.id))
            if polowanie  == animal_list[3]:
                cursor.execute("UPDATE animals SET tygrys = ? WHERE user_id = ?", (animals[3] + amount, ctx.author.id))
            if polowanie  == animal_list[4]:
                cursor.execute("UPDATE animals SET niedźwiedź = ? WHERE user_id = ?", (animals[4] + amount, ctx.author.id))
            if polowanie  == animal_list[5]:
                cursor.execute("UPDATE animals SET jeleń = ? WHERE user_id = ?", (animals[5] + amount, ctx.author.id))
            if polowanie  == animal_list[6]:
                cursor.execute("UPDATE animals SET zebra = ? WHERE user_id = ?", (animals[6] + amount, ctx.author.id))
            if polowanie  == animal_list[7]:
                cursor.execute("UPDATE animals SET jednorożec = ? WHERE user_id = ?", (animals[7] + amount, ctx.author.id))
            if polowanie  == animal_list[8]:
                cursor.execute("UPDATE animals SET bóbr = ? WHERE user_id = ?", (animals[8] + amount, ctx.author.id))
            if polowanie  == animal_list[9]:
                cursor.execute("UPDATE animals SET szop = ? WHERE user_id = ?", (animals[9] + amount, ctx.author.id))
            if polowanie  == animal_list[10]:
                cursor.execute("UPDATE animals SET jeż = ? WHERE user_id = ?", (animals[10] + amount, ctx.author.id))
            if polowanie  == animal_list[11]:
                cursor.execute("UPDATE animals SET wiewórka = ? WHERE user_id = ?", (animals[11] + amount, ctx.author.id))
            if polowanie  == animal_list[12]:
                cursor.execute("UPDATE animals SET królik = ? WHERE user_id = ?", (animals[12] + amount, ctx.author.id))
            if polowanie  == animal_list[13]:
                cursor.execute("UPDATE animals SET kaczka = ? WHERE user_id = ?", (animals[13] + amount, ctx.author.id))
            if polowanie  == animal_list[14]:
                cursor.execute("UPDATE animals SET dzik = ? WHERE user_id = ?", (animals[14] + amount, ctx.author.id))
            if polowanie  == animal_list[0]:
                cursor.execute("UPDATE tools SET łuk = ? WHERE user_id = ?", (łuk[0] - 1, ctx.author.id))
                embed=nextcord.Embed(title=f"",description=f"Spróbuj następnym razem", color = nextcord.Colour.red())
                await ctx.send(embed=embed)
                return
            cursor.execute(f"UPDATE tools SET łuk = ? WHERE user_id = ?", (łuk[0] - 1, ctx.author.id))
            embed=nextcord.Embed(title=f"",description=f"Polowanie się udało! Zabiłeś x{amount} {polowanie}!", color = nextcord.Colour.green())
            await ctx.send(embed=embed)
        else:
            embed=nextcord.Embed(title="",description="Nie masz łuku!", color = nextcord.Colour.red())
            await ctx.send(embed=embed)

        
        db.commit()
        cursor.close()
        db.close()   

                
def setup(bot):
    bot.add_cog(Items(bot))