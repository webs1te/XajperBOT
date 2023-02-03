import asyncio
from errno import ESHUTDOWN
import nextcord
from nextcord.ext import commands
import sqlite3
import random
from PIL import ImageDraw, ImageFont, Image
from io import BytesIO

 
 
class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        db = sqlite3.connect("eco.db")
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS eco (
            user_id INTEGER, wallet INTEGER, bank INTEGER
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS animals (
            user_id, lis, wilk, tygyrs, niedźwiedź, jeleń, zebra, jednorożec, bóbr, szop, jeż, wiewiórka, królik, kaczka, dzik
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS tools (

            user_id, łuk, scyzoryk, kilof, wędka, siekiera
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS ore (

            user_id, złoto, diament, żelazo, kamień, szmaragd, rubin
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS meble (

            user_id, komoda, łóżko, szafa, dywan, krzesło, anekskuchenny, obraz, wanna, sofa
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS auta (

            user_id, BMW, Audi, Lamborghini, Pasat, Motorówka, Żaglówka, UFO, Helikopter, Rakieta, Samolot, Pociąg, Motor, Hulajnoga, Rower, Deskorolka
        )''')



        print ("Baza Danych Systemu Ekonomii - Gotowa!")


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        author =  message.author
        db = sqlite3.connect("eco.db")
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM eco WHERE user_id = {author.id}")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO eco(user_id, wallet, bank) VALUES (?, ?, ?)")
            val = (author.id, 100, 0)
            cursor.execute(sql, val)


        cursor.execute(f"SELECT user_id FROM tools WHERE user_id = {author.id}")
        result = cursor.fetchone()
        if result is None:
            cursor.execute("INSERT INTO tools(user_id, łuk, scyzoryk, kilof, wędka, siekiera) VALUES (?, ?, ?, ?, ?, ?)", (author.id, 1, 1, 1, 1, 1))


        cursor.execute(f"SELECT user_id FROM animals WHERE user_id = {author.id}")
        result = cursor.fetchone()
        if result is None:
            cursor.execute("INSERT INTO animals(user_id, lis, wilk, tygyrs, niedźwiedź, jeleń, zebra, jednorożec, bóbr, szop, jeż, wiewiórka, królik, kaczka, dzik) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))


        cursor.execute(f"SELECT user_id FROM ore WHERE user_id = {author.id}")
        result = cursor.fetchone()
        if result is None:
            cursor.execute("INSERT INTO ore(user_id, złoto, diament, żelazo, kamień, szmaragd, rubin) VALUES (?, ?, ?, ?, ?, ?, ?)", (author.id, 1, 1, 1, 1, 1, 1))

        
        cursor.execute(f"SELECT user_id FROM meble WHERE user_id = {author.id}")
        result = cursor.fetchone()
        if result is None:
            cursor.execute("INSERT INTO meble(user_id, komoda, łóżko, szafa, dywan, krzesło, anekskuchenny, obraz, wanna, sofa) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0))

        
        cursor.execute(f"SELECT user_id FROM auta WHERE user_id = {author.id}")
        result = cursor.fetchone()
        if result is None:
            cursor.execute("INSERT INTO auta(user_id, BMW, Audi, Lamborghini, Pasat, Motorówka, Żaglówka, UFO, Helikopter, Rakieta, Samolot, Pociąg, Motor, Hulajnoga, Rower, Deskorolka) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        
        db.commit()
        cursor.close()
        db.close()
    



  
def setup(bot):
    bot.add_cog(Economy(bot))