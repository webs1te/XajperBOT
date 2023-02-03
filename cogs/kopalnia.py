from http import client
import json
import nextcord
import sqlite3
import random
from nextcord.ext import commands
from nextcord import Interaction

class Kopalnia(commands.Cog):

    client = commands.Bot(command_prefix="x!")

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):

        print ("Ekonomia: kopalnia - Gotowa!")


    @client.slash_command(guild_ids=[795356386807775282], description="Kop w kopalni ⛏️", name="kopalnia")
    async def kopalnia(interaction: Interaction):

        ore_list = [None, "🥇złoto", "💎diament", "🦾żelazo", "🪨kamień", "🟩szmaragd", "🔴rubin"]

        db = sqlite3.connect("eco.db")
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM ore WHERE user_id = {interaction.user.id}")
        ore = cursor.fetchone()

        cursor.execute(f"SELECT kilof FROM tools WHERE user_id = {interaction.user.id}")
        kilof = cursor.fetchone

        amount =  random.randrange(7)
        cave = random.choice(ore_list)

      
    
        if kilof[0] > 0:
            if cave  == ore_list[1]:
                cursor.execute("UPDATE ore SET złoto = ? WHERE user_id = ?", (ore[1] + amount, interaction.user.id))
            if cave  == ore_list[2]:
                cursor.execute("UPDATE ore SET diament = ? WHERE user_id = ?", (ore[2] + amount, interaction.user.id))
            if cave  == ore_list[3]:
                cursor.execute("UPDATE ore SET żelazo = ? WHERE user_id = ?", (ore[3] + amount, interaction.user.id))
            if cave  == ore_list[4]:
                cursor.execute("UPDATE ore SET kamień = ? WHERE user_id = ?", (ore[4] + amount, interaction.user.id))
            if cave  == ore_list[5]:
                cursor.execute("UPDATE ore SET szmaragd = ? WHERE user_id = ?", (ore[5] + amount, interaction.user.id))
            if cave  == ore_list[6]:
                cursor.execute("UPDATE ore SET rubin = ? WHERE user_id = ?", (ore[6] + amount, interaction.user.id))
            if cave  == ore_list[0]:
                cursor.execute("UPDATE ore SET kilof = ? WHERE user_id = ?", (kilof[0] - 1, interaction.user.id))
                embed=nextcord.Embed(title=f"",description=f"Spróbuj następnym razem", color = nextcord.Colour.red())
                await interaction.send(embed=embed)
                return
            cursor.execute("UPDATE tools SET kilof = ? WHERE user_id = ?", (kilof[0] - 1, interaction.user.id))
            embed=nextcord.Embed(title="",description=f"Pomyśle wykopałeś x{amount} {cave}!", color = nextcord.Colour.green())
            await interaction.send(embed=embed)
        else:
            embed=nextcord.Embed(title="",description=f"Nie masz kilofa!", color = nextcord.Colour.red())
            await interaction.send(embed=embed)

        
        db.commit() 
        cursor.close()
        db.close()   


    @client.command()
    async def kopalnia(self, ctx):

        ore_list = [None, "🥇złoto", "💎diament", "🦾żelazo", "🪨kamień", "🟩szmaragd", "🔴rubin"]

        db = sqlite3.connect("eco.db")
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM ore WHERE user_id = {ctx.author.id}")
        ore = cursor.fetchone()

        cursor.execute(f"SELECT kilof FROM tools WHERE user_id = {ctx.author.id}")
        kilof = cursor.fetchone

        amount =  random.randrange(7)
        cave = random.choice(ore_list)

      
    
        if kilof[0] > 0:
            if cave  == ore_list[1]:
                cursor.execute("UPDATE ore SET złoto = ? WHERE user_id = ?", (ore[1] + amount, ctx.author.id))
            if cave  == ore_list[2]:
                cursor.execute("UPDATE ore SET diament = ? WHERE user_id = ?", (ore[2] + amount, ctx.author.id))
            if cave  == ore_list[3]:
                cursor.execute("UPDATE ore SET żelazo = ? WHERE user_id = ?", (ore[3] + amount, ctx.author.id))
            if cave  == ore_list[4]:
                cursor.execute("UPDATE ore SET kamień = ? WHERE user_id = ?", (ore[4] + amount, ctx.author.id))
            if cave  == ore_list[5]:
                cursor.execute("UPDATE ore SET szmaragd = ? WHERE user_id = ?", (ore[5] + amount, ctx.author.id))
            if cave  == ore_list[6]:
                cursor.execute("UPDATE ore SET rubin = ? WHERE user_id = ?", (ore[6] + amount, ctx.author.id))
            if cave  == ore_list[0]:
                cursor.execute("UPDATE ore SET kilof = ? WHERE user_id = ?", (kilof[0] - 1, ctx.author.id))
                embed=nextcord.Embed(title=f"",description=f"Spróbuj następnym razem", color = nextcord.Colour.red())
                await ctx.send(embed=embed)
                return
            cursor.execute("UPDATE tools SET kilof = ? WHERE user_id = ?", (kilof[0] - 1, ctx.author.id))
            embed=nextcord.Embed(title="",description=f"Pomyśle wykopałeś x{amount} {cave}!", color = nextcord.Colour.green())
            await ctx.send(embed=embed)
        else:
            embed=nextcord.Embed(title="",description=f"Nie masz kilofa!", color = nextcord.Colour.red())
            await ctx.send(embed=embed)

        
        db.commit() 
        cursor.close()
        db.close()   

                
def setup(bot):
    bot.add_cog(Kopalnia(bot))