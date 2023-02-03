import asyncio
import aiosqlite
from cgitb import text
from configparser import MissingSectionHeaderError
from distutils.log import error
from email.mime import application, image
from ensurepip import bootstrap
import itertools
from lib2to3.pytree import convert
from nturl2path import url2pathname
from pickle import TRUE
from tkinter import N
from unicodedata import name
import nextcord
from nextcord import member
from nextcord.ext import commands, tasks
from nextcord.ext.commands import has_permissions
from nextcord.utils import get
import random
import os
import sqlite3
import time
from nextcord import ButtonStyle, SelectOption, Intents, Interaction, SlashOption
from nextcord.ui import Button, View, Select
from nextcord import Colour
import datetime
from datetime import datetime, timedelta
import json
from PIL import Image
from io import BytesIO
import urllib
from neuralintents import GenericAssistant
import itertools
from nextcord.ext.commands import MissingPermissions
from datetime import date
import json as jason

SERWER_ID = 795356386807775282


intents = Intents.default()
intents.message_content = True
intents.members = True
intents.messages = True

client = commands.Bot(command_prefix="x!", intents=intents)
client.remove_command("help")


for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        client.load_extension(f"cogs.{file[:-3]}")






@client.event
async def on_ready():
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name='/help'))
    db = sqlite3.connect("warns.db")
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS warns(guild_id INT, user_id INT, content STR, author_id INT, time INT)")
    print("Baza Danych Systemu Warnów - Gotowa!")
    print("Baza Danych Systemu Poziomów - Gotowa!")

    setattr(client, "db", await aiosqlite.connect("levelsystem.db"))
    await asyncio.sleep(delay=3)
    async with client.db.cursor() as cursor:
        await cursor.execute("CREATE TABLE IF NOT EXISTS levels (level INTEGER, xp INTEGER, user INTEGER, guild INTEGER)")

    print("Jestem Online!")


client.event
async def on_message(message):
    if message.author.bot:
        return
    author = message.author
    guild = message.guild
    async with client.db.cursor() as cursor:
        await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?", (author.id, guild.id,))
        xp = await cursor.fetchone()
        await cursor.execute("SELECT level FROM levels WHERE user = ? AND guild = ?", (author.id, guild.id,))
        level = await cursor.fetchone()

        if not xp or not level:
            await cursor.execute("INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)", (0, 0, author.id, guild.id,))
            await client.commit()

        try:
            xp = xp[0]
            level = level[0]
        except TypeError:
            xp = 0
            level = 0

        if level < 5:
            xp += random.randint(1, 3)
            await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (xp, author.id, guild.id,))
        else:
            rand = random.randint(1, (level//4))
            if rand == 1:
                xp += random.randint(1, 3)
                await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (xp, author.id, guild.id,))
        if xp >= 100:
            level += 1
            await cursor.execute("UPDATE levels SET level = ? WHERE user = ? AND guild = ?", (level, author.id, guild.id,))
            await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (0, author.id, guild.id,))
            await message.channel.send(f"Brawo {author.mention}, osiągnąłeś poziom **{level}**! 🥳")
    await client.db.commit()
    await client.process_commands(message)

@client.command(aliases=['lvl','poziom','rank'])
async def level(ctx, member: nextcord.Member = None):
    if member is None:
        member = ctx.author
    async with client.db.cursor() as cursor:
        await cursor.execute("SELECT level FROM levels WHERE user = ? AND guild = ?", (member.id, ctx.guild.id,))
        level = await cursor.fetchone()
        await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?", (member.id, ctx.guild.id,))
        xp = await cursor.fetchone()

    if not xp or not level:
        await cursor.execute("INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)", (0, 0, member.id, ctx.guild.id,))
        await client.db.commit()

    try:
        xp = xp[0]
        level = level[0]
    except TypeError:
        xp = 0
        level = 0

    embed = nextcord.Embed(title=f"Karta Poziomu {member.name}:", description=f"**Poziom**: `{level}` \n**XP**: `{xp}`", color=member.color)
    await ctx.send(embed=embed)





@client.slash_command(guild_ids=[SERWER_ID], description="Sprawdź stan swojego konta 🏦", name="bal")
async def bal(interaction: Interaction, osoba: nextcord.Member):
    if osoba is None:
        osoba = interaction.user
    

    db = sqlite3.connect("eco.db")
    cursor = db.cursor()


    cursor.execute(f"SELECT wallet, bank FROM eco WHERE user_id = {osoba.id}")
    bal = cursor.fetchone()
    try:
        wallet = bal[0]
        bank = bal[1]
    except:
        wallet = 0
        bank = 0
    suma = (wallet + bank)
    embed=nextcord.Embed(title=f"",timestamp = datetime.now(), color=0x04ec32)
    embed.add_field(name="**Portfel:**", value=f"`{wallet}`💰", inline=True)
    embed.add_field(name="**Bank:**", value=f"`{bank}`💰", inline=True)
    embed.add_field(name="**Suma:**", value=f"`{suma}`💰", inline=True)
    embed.set_author(name = osoba.name, icon_url = osoba.display_avatar)
    embed.set_thumbnail(url="https://cdn.pixabay.com/photo/2017/10/08/19/55/bank-2831361_1280.png") 
    await interaction.response.send_message(embed=embed)

    

@client.command(aliases=['bal', 'konto'])
async def balance(ctx, member: nextcord.Member = None):
    if member is None:
        member = ctx.author
    

    db = sqlite3.connect("eco.db")
    cursor = db.cursor()


    cursor.execute(f"SELECT wallet, bank FROM eco WHERE user_id = {member.id}")
    bal = cursor.fetchone()
    try:
        wallet = bal[0]
        bank = bal[1]
    except:
        wallet = 0
        bank = 0
    suma = (wallet + bank)
    embed=nextcord.Embed(title=f"",timestamp = datetime.now(), color=0x04ec32)
    embed.add_field(name="**Portfel:**", value=f"`{wallet}`💰", inline=True)
    embed.add_field(name="**Bank:**", value=f"`{bank}`💰", inline=True)
    embed.add_field(name="**Suma:**", value=f"`{suma}`💰", inline=True)
    embed.set_author(name = member.name, icon_url = member.display_avatar)
    embed.set_thumbnail(url="https://cdn.pixabay.com/photo/2017/10/08/19/55/bank-2831361_1280.png") 
    await ctx.send(embed=embed)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed=nextcord.Embed(title=f"",description=f"Tą komendę możesz użyć ponownie za:  `{round(error.retry_after, 2)}`s!", color = nextcord.Colour.red())
        await ctx.send(embed=embed)


@client.slash_command(guild_ids=[SERWER_ID], description="Pracuj by dostawać wynagrodzenie 💼", name="work")
@commands.cooldown(1,1800, commands.BucketType.user)
async def work(interaction: Interaction):
    osoba = interaction.user

    earnings = random.randint(95,195)

    zawod = ["👮Policjant","👨‍⚕️Lekarz","⛏️Górnik","🪓Drawl","🧑‍🏫Nauczyciel","🧑‍🚒Strażak","👨‍🔧Elektryk","🧑‍🔧Mechanik","🧑‍💻Programista","💻Informatyk","🧪Naukowiec","👷Budowlaniec","🧱Murarz","🛒Kasjer","🗿Rzeźbiarz","🛢️Tynkarz","🏠Architekt","⚽Piłkarz","🎾Sportowiec","🦷Dentystka","⚖️Adwokat","🎭Aktor","🦴Archeolog","🧑‍🎨Artysta","🧁Cukiernik","💇‍♂️Fryzjer","🧑‍🍳Kucharz","🧬Biolog","📚Bibliotekarz","🪨Brukarz","⛓️Kowal","🧥Choreograf","🕵️Detektyw","🛖Dekarz","🥕Dietetyk","🧮Fizyk","🧑‍🚀Astronauta","🔭Astronom","🤔Fizolof","📷Fotograf","🌍Geolog","🖌️Grafik","🤳Influencer","🤮Komornik","🎩Kominiarz","🪡Krawiec","📨Listonosz","☄️Meteorolog","🚂Maszynista","🔫Ochroniarz","🤿Nurek","📝Notariusz","📢Negocjator","🧑‍✈️Pilot Samolotu","🧑‍🌾Rolnik","♥️Psycholog","🥽Spawacz","🪑Stolarz","💃Tancerz","🚕Taksówkarz","🔌Technik","💭Tłumacz","⌚Zegarmistrz","🏢Urzędnik","🐕‍🦺Treser","🥇Trener","🎼Muzyk","📽️Youtuber","🎮Gamer","🗞️Dziennikarz","💼Polityk"]

    zawodpraca = random.choice(zawod)
    db = sqlite3.connect("eco.db")
    cursor = db.cursor()

    cursor.execute(f"SELECT wallet FROM eco WHERE user_id = {osoba.id}")
    wallet = cursor.fetchone()

    try:
        wallet = wallet[0]
    except:
        wallet = 0

    sql = ("UPDATE eco SET wallet = ? WHERE user_id = ?")
    val = (wallet + int(earnings), osoba.id)
    cursor.execute(sql, val)
    embed=nextcord.Embed(title=f"",description=f"<:tak:1020344650260807700> Pracowałeś jako `{zawodpraca}` i zarobiłeś `{earnings}`💰!", color=0x04ec32)
    await interaction.response.send_message(embed=embed)

    db.commit()
    cursor.close()
    db.close()


@client.command(aliases=['praca'])
@commands.cooldown(1,1800, commands.BucketType.user)
async def work(ctx):
    member = ctx.author

    earnings = random.randint(95,195)

    zawod = ["👮Policjant","👨‍⚕️Lekarz","⛏️Górnik","🪓Drawl","🧑‍🏫Nauczyciel","🧑‍🚒Strażak","👨‍🔧Elektryk","🧑‍🔧Mechanik","🧑‍💻Programista","💻Informatyk","🧪Naukowiec","👷Budowlaniec","🧱Murarz","🛒Kasjer","🗿Rzeźbiarz","🛢️Tynkarz","🏠Architekt","⚽Piłkarz","🎾Sportowiec","🦷Dentystka","⚖️Adwokat","🎭Aktor","🦴Archeolog","🧑‍🎨Artysta","🧁Cukiernik","💇‍♂️Fryzjer","🧑‍🍳Kucharz","🧬Biolog","📚Bibliotekarz","🪨Brukarz","⛓️Kowal","🧥Choreograf","🕵️Detektyw","🛖Dekarz","🥕Dietetyk","🧮Fizyk","🧑‍🚀Astronauta","🔭Astronom","🤔Fizolof","📷Fotograf","🌍Geolog","🖌️Grafik","🤳Influencer","🤮Komornik","🎩Kominiarz","🪡Krawiec","📨Listonosz","☄️Meteorolog","🚂Maszynista","🔫Ochroniarz","🤿Nurek","📝Notariusz","📢Negocjator","🧑‍✈️Pilot Samolotu","🧑‍🌾Rolnik","♥️Psycholog","🥽Spawacz","🪑Stolarz","💃Tancerz","🚕Taksówkarz","🔌Technik","💭Tłumacz","⌚Zegarmistrz","🏢Urzędnik","🐕‍🦺Treser","🥇Trener","🎼Muzyk","📽️Youtuber","🎮Gamer","🗞️Dziennikarz","💼Polityk"]

    zawodpraca = random.choice(zawod)
    db = sqlite3.connect("eco.db")
    cursor = db.cursor()

    cursor.execute(f"SELECT wallet FROM eco WHERE user_id = {member.id}")
    wallet = cursor.fetchone()

    try:
        wallet = wallet[0]
    except:
        wallet = 0

    sql = ("UPDATE eco SET wallet = ? WHERE user_id = ?")
    val = (wallet + int(earnings), member.id)
    cursor.execute(sql, val)
    embed=nextcord.Embed(title=f"",description=f"<:tak:1020344650260807700> Pracowałeś jako `{zawodpraca}` i zarobiłeś `{earnings}`💰!", color=0x04ec32)
    await ctx.send(embed=embed)

    db.commit()
    cursor.close()
    db.close()


@client.slash_command(guild_ids=[SERWER_ID], description="Tabelka najbogatszych ludzi na serwerze 💲", name="leaderboard")
async def leaderboard(interaction: Interaction):
    embed = nextcord.Embed(title = f"🏆 Lista Najbogatszych:", color = nextcord.Colour.yellow())
    embed.add_field(name="`[ 1 ]` : @Xajper ", value="`100💰`", inline=True)

    await interaction.response.send_message(embed=embed)


@client.command(aliases = ["lb"])
async def leaderboard(ctx):


    embed = nextcord.Embed(title = f"🏆 Lista Najbogatszych:", color = nextcord.Colour.yellow())
    embed.add_field(name="`[ 1 ]` : @Xajper ", value="`100💰`", inline=True)

    await ctx.send(embed=embed)





@commands.command()
async def kup_passat(ctx, amount:int=10000):
    member = ctx.author
    db = sqlite3.connect("eco.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT wallet FROM eco WHERE user_id = {member.id}")
    wallet = cursor.fetchone()
    Pasat = cursor.fetchone()

    try:
        wallet = wallet[0]
    except:
        wallet = wallet


    if wallet < amount:
        embed = nextcord.Embed(title = "<:nie:1020344672461262889> Nie masz wystarczająco pieniędzy!",timestamp = ctx.message.created_at, color = nextcord.Colour.red())
        return await ctx.reply(embed = embed)

    if wallet >= amount:
        cursor.execute(f"UPDATE eco SET wallet = ? WHERE user_id = ?", (wallet - amount, ctx.author.id))
        cursor.execute(f"UPDATE auta SET Pasat = ? WHERE user_id = ?", (Pasat + 1, ctx.author.id))
        db.commit()
        embed = nextcord.Embed(title = "<:tak:1020344650260807700> Pomyślnie zakupiono Passata!", timestamp = ctx.message.created_at, color = nextcord.Colour.green())
        return await ctx.reply(embed = embed)


@client.slash_command(guild_ids=[SERWER_ID], description="Sklep serwerowej ekonomii 🏪", name="sklep")
async def sklep(interaction: Interaction):
    await interaction.channel.purge(limit=1)
    
    button = Button(label="Następne", style=nextcord.ButtonStyle.blurple, emoji="↪️")

    async def button_callback(interaction):
        await interaction.channel.purge(limit=1)
        embed=nextcord.Embed(title=f"🛒Sklep",description="Żeby coś kupić wpisz `/kup_{nazwa rzeczy którą chcesz kupić}`", color = nextcord.Colour.purple())
        embed.add_field(name="══════════ PRZEDMIOTY ═════════", value="`🪚`", inline=False) 
        embed.add_field(name="🏹 Łuk", value="Koszt 1000 💰", inline=True)
        embed.add_field(name="⚔️ Scyzoryk", value="Koszt 1000 💰", inline=True)
        embed.add_field(name="⛏️ Kilof", value="Koszt 1000 💰", inline=True)
        embed.add_field(name="🎣 Wędka", value="Koszt 1000 💰", inline=True)
        embed.add_field(name="🪓 Siekiera", value="Koszt 1000 💰", inline=True)
        embed.add_field(name="══════════ INNE ═════════", value="`⭐`", inline=False)
        embed.add_field(name="🏠 Dom", value="Koszt 100000 💰", inline=True)
        embed.add_field(name="🎙️ Własny Kanał Głosowy", value="Koszt 85000 💰", inline=True)
        await interaction.response.send_message(embed=embed)

    button.callback = button_callback

    embed=nextcord.Embed(title=f"🛒Sklep",description="Żeby coś kupić wpisz `/kup_{nazwa rzeczy którą chcesz kupić}`", color = nextcord.Colour.purple())
    embed.add_field(name="══════════ TRANSPORT ═════════", value="`🚕`", inline=False)
    embed.add_field(name="🚗 Passat", value="Koszt 10000 💰", inline=True)
    embed.add_field(name="🚗 Audi", value="Koszt 50000 💰", inline=True)
    embed.add_field(name="🚗 BMW", value="Koszt 100000 💰", inline=True)
    embed.add_field(name="🏎️ Lamborghini", value="Koszt 500000 💰", inline=True)
    embed.add_field(name="🛹 Deskorolka", value="Koszt 1100 💰", inline=True)
    embed.add_field(name="🚲 Rower", value="Koszt 3000 💰", inline=True)
    embed.add_field(name="🛴 Hulajnoga", value="Koszt 2500 💰", inline=True)
    embed.add_field(name="🏍️ Motor", value="Koszt 7500 💰", inline=True)
    embed.add_field(name="🚂 Pociąg", value="Koszt 65000 💰", inline=True)
    embed.add_field(name="🛩️ Samolot", value="Koszt 75000 💰", inline=True)
    embed.add_field(name="🚀 Rakieta", value="Koszt 100000 💰", inline=True)
    embed.add_field(name="🚁 Helikopter", value="Koszt 25000 💰", inline=True)
    embed.add_field(name="🛸 UFO", value="Koszt 500000 💰", inline=True)
    embed.add_field(name="⛵ Żaglówka", value="Koszt 10000 💰", inline=True)
    embed.add_field(name="🛥️ Motorówka", value="Koszt 12000 💰", inline=True)
    embed.add_field(name="══════════ MEBLE ═════════", value="`🚿`", inline=False) 
    embed.add_field(name="🪑 Krzesło", value="Koszt 500 💰", inline=True)
    embed.add_field(name="🗃️Komoda", value="Koszt 1000 💰", inline=True)
    embed.add_field(name="🖼️ Obraz", value="Koszt 1100 💰", inline=True)
    embed.add_field(name="🛁 Wanna", value="Koszt 1360 💰", inline=True)
    embed.add_field(name="🛏️ Łóżko", value="Koszt 1750 💰", inline=True)
    embed.add_field(name="🛋️ Sofa", value="Koszt 1500 💰", inline=True)
    embed.add_field(name="🗄️ Szafa", value="Koszt 2000 💰", inline=True)
    embed.add_field(name="🔪 Aneks Kuchenny", value="Koszt 10000 💰", inline=True)

    

    view = View(timeout=120)
    view.add_item(button)

    await interaction.response.send_message(embed=embed, view=view)


@client.command(aliases=['sklep'])
async def shop(ctx):
    await ctx.channel.purge(limit=1)
    
    button = Button(label="Następne", style=nextcord.ButtonStyle.blurple, emoji="↪️")

    async def button_callback(interaction):
        await ctx.channel.purge(limit=1)
        embed=nextcord.Embed(title=f"🛒Sklep",description="Żeby coś kupić wpisz `/kup_{nazwa rzeczy którą chcesz kupić}`", color = nextcord.Colour.purple())
        embed.add_field(name="══════════ PRZEDMIOTY ═════════", value="`🪚`", inline=False) 
        embed.add_field(name="🏹 Łuk", value="Koszt 1000 💰", inline=True)
        embed.add_field(name="⚔️ Scyzoryk", value="Koszt 1000 💰", inline=True)
        embed.add_field(name="⛏️ Kilof", value="Koszt 1000 💰", inline=True)
        embed.add_field(name="🎣 Wędka", value="Koszt 1000 💰", inline=True)
        embed.add_field(name="🪓 Siekiera", value="Koszt 1000 💰", inline=True)
        embed.add_field(name="══════════ INNE ═════════", value="`⭐`", inline=False)
        embed.add_field(name="🏠 Dom", value="Koszt 100000 💰", inline=True)
        embed.add_field(name="🎙️ Własny Kanał Głosowy", value="Koszt 85000 💰", inline=True)
        await ctx.send(embed=embed)

    button.callback = button_callback

    embed=nextcord.Embed(title=f"🛒Sklep",description="Żeby coś kupić wpisz `/kup_{nazwa rzeczy którą chcesz kupić}`", color = nextcord.Colour.purple())
    embed.add_field(name="══════════ TRANSPORT ═════════", value="`🚕`", inline=False)
    embed.add_field(name="🚗 Passat", value="Koszt 10000 💰", inline=True)
    embed.add_field(name="🚗 Audi", value="Koszt 50000 💰", inline=True)
    embed.add_field(name="🚗 BMW", value="Koszt 100000 💰", inline=True)
    embed.add_field(name="🏎️ Lamborghini", value="Koszt 500000 💰", inline=True)
    embed.add_field(name="🛹 Deskorolka", value="Koszt 1100 💰", inline=True)
    embed.add_field(name="🚲 Rower", value="Koszt 3000 💰", inline=True)
    embed.add_field(name="🛴 Hulajnoga", value="Koszt 2500 💰", inline=True)
    embed.add_field(name="🏍️ Motor", value="Koszt 7500 💰", inline=True)
    embed.add_field(name="🚂 Pociąg", value="Koszt 65000 💰", inline=True)
    embed.add_field(name="🛩️ Samolot", value="Koszt 75000 💰", inline=True)
    embed.add_field(name="🚀 Rakieta", value="Koszt 100000 💰", inline=True)
    embed.add_field(name="🚁 Helikopter", value="Koszt 25000 💰", inline=True)
    embed.add_field(name="🛸 UFO", value="Koszt 500000 💰", inline=True)
    embed.add_field(name="⛵ Żaglówka", value="Koszt 10000 💰", inline=True)
    embed.add_field(name="🛥️ Motorówka", value="Koszt 12000 💰", inline=True)
    embed.add_field(name="══════════ MEBLE ═════════", value="`🚿`", inline=False) 
    embed.add_field(name="🪑 Krzesło", value="Koszt 500 💰", inline=True)
    embed.add_field(name="🗃️Komoda", value="Koszt 1000 💰", inline=True)
    embed.add_field(name="🖼️ Obraz", value="Koszt 1100 💰", inline=True)
    embed.add_field(name="🛁 Wanna", value="Koszt 1360 💰", inline=True)
    embed.add_field(name="🛏️ Łóżko", value="Koszt 1750 💰", inline=True)
    embed.add_field(name="🛋️ Sofa", value="Koszt 1500 💰", inline=True)
    embed.add_field(name="🗄️ Szafa", value="Koszt 2000 💰", inline=True)
    embed.add_field(name="🔪 Aneks Kuchenny", value="Koszt 10000 💰", inline=True)

    

    view = View(timeout=120)
    view.add_item(button)

    await ctx.send(embed=embed, view=view)


@client.slash_command(guild_ids=[SERWER_ID], description="Codzinne wynagrodzenie ⭐", name="daily")
@commands.cooldown(1,86400, commands.BucketType.user)
async def daily(interaction: Interaction):
    member = interaction.user

    daily = 500

    db = sqlite3.connect("eco.db")
    cursor = db.cursor()

    cursor.execute(f"SELECT wallet FROM eco WHERE user_id = {member.id}")
    wallet = cursor.fetchone()

    try:
        wallet = wallet[0]
    except:
        wallet = 0

    sql = ("UPDATE eco SET wallet = ? WHERE user_id = ?")
    val = (wallet + int(daily), member.id)
    cursor.execute(sql, val)
    embed=nextcord.Embed(title="🎁 `CODZIENNA NAGRODA`", description="Odbierz nagrodę ponownie za **24h**!", timestamp = datetime.now(), color = nextcord.Colour.dark_magenta())
    embed.add_field(name=f"<:tak:1020344650260807700> Do twojego portfela wpłynęło **{daily}**💰!", value=f"Zbieraj dalej!", inline=True)
    await interaction.response.send_message(embed=embed)

    db.commit()
    cursor.close()
    db.close()

@client.command()
@commands.cooldown(1,86400, commands.BucketType.user)
async def daily(ctx):
    member = ctx.author

    daily = 500

    db = sqlite3.connect("eco.db")
    cursor = db.cursor()

    cursor.execute(f"SELECT wallet FROM eco WHERE user_id = {member.id}")
    wallet = cursor.fetchone()

    try:
        wallet = wallet[0]
    except:
        wallet = 0

    sql = ("UPDATE eco SET wallet = ? WHERE user_id = ?")
    val = (wallet + int(daily), member.id)
    cursor.execute(sql, val)
    embed=nextcord.Embed(title="🎁 `CODZIENNA NAGRODA`", description="Odbierz nagrodę ponownie za **24h**!", timestamp = datetime.now(), color = nextcord.Colour.dark_magenta())
    embed.add_field(name=f"<:tak:1020344650260807700> Do twojego portfela wpłynęło **{daily}**💰!", value=f"Zbieraj dalej!", inline=True)
    await ctx.send(embed=embed)

    db.commit()
    cursor.close()
    db.close()


@client.command(aliases=['dodajpieniądze','addmoney','dodajmoney','addpieniadze','addpieniądze'])
@has_permissions(manage_messages=True)
async def dodajpieniadze(ctx, member: nextcord.User = None, ilosc=int):
    if member == None:
        member = ctx.author

    ilosc = {ilosc}

    db = sqlite3.connect("eco.db")
    cursor = db.cursor()

    cursor.execute(f"SELECT bank FROM eco WHERE user_id = {member.id}")
    bank = cursor.fetchone()

    try:
        bank = bank[0]
    except:
        bank = 0

    sql = ("UPDATE eco SET bank = ? WHERE user_id = ?")
    val = (bank + int(ilosc), member.id)
    cursor.execute(sql, val)
    embed=nextcord.Embed(title=f"💸 Dodawanie pieniędzy {member.mention}...", timestamp = datetime.now(), color = nextcord.Colour.dark_orange)
    embed.add_field(name=f"<:tak:1020344650260807700> Do banku {member.mention} dodano `{ilosc}`💰!")
    await ctx.send(embed=embed)

    db.commit()
    cursor.close()
    db.close()
 

@client.slash_command(guild_ids=[SERWER_ID], description="Pamiętaj! Hazard jest zły! 🤑", name="hazard")
async def hazard(interaction: Interaction, pieniądze:int=1000):
    member = interaction.user
    db = sqlite3.connect("eco.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT wallet FROM eco WHERE user_id = {member.id}")
    wallet = cursor.fetchone()

    try:
        wallet = wallet[0]
    except:
        wallet = 0

    if wallet < pieniądze:
        embed = nextcord.Embed(title = "<:nie:1020344672461262889> Nie masz wystarczająco pieniędzy!",timestamp = interaction.created_at, color = nextcord.Colour.red())
        return await interaction.response.send_message(embed = embed)

    user_strikes = random.randint(1,14)
    bot_strikes = random.randint(5,14)

    if user_strikes > bot_strikes:
        percentage = random.randint(50,100)
        amount_won = int(pieniądze*(percentage/100))
        cursor.execute(f"UPDATE eco SET wallet = ? WHERE user_id = ?", (wallet + amount_won, interaction.user.id))
        db.commit()
        embed=nextcord.Embed(title=f"🥇 Wygrałeś!",description=f"➕ Wygrałeś **{amount_won}**💰\n🍀 Szansa: **{percentage}%**\n🏦 Nowy Stan Portfela: **{wallet + amount_won}💰**", timestamp = datetime.now(), color=0x04ec32)
        embed.set_author(name = member.name, icon_url = member.display_avatar)
    
    elif user_strikes < bot_strikes:
        percentage = random.randint(50,100)
        amount_lost = int(pieniądze*(percentage/100))
        cursor.execute(f"UPDATE eco SET wallet = ? WHERE user_id = ?", (wallet - amount_lost, interaction.user.id))
        db.commit()
        embed=nextcord.Embed(title=f"❌ Przegrałeś!",description=f"➖ Straciłeś **{amount_lost}**💰\n🍀 Szansa: **{percentage}%**\n🏦 Nowy Stan Portfela: **{wallet - amount_lost}💰**", timestamp = datetime.now(), color = nextcord.Colour.red())
        embed.set_author(name = member.name, icon_url = member.display_avatar)
    else:
        embed=nextcord.Embed(title=f"🧨 Remis!", timestamp = datetime.now(), color = nextcord.Colour.red())
        embed.set_author(name = member.name, icon_url = member.display_avatar)

    embed.add_field(name=f"**{interaction.user.name}**", value=f"Wynik: __{user_strikes}__", inline=True)
    embed.set_thumbnail(url="https://cdn.pixabay.com/photo/2013/07/13/12/37/poker-159973_960_720.png") 
    embed.add_field(name=f"**XajperBOT**", value=f"Wynik: __{bot_strikes}__", inline=True)
    await interaction.response.send_message(embed=embed)

    cursor.close()
    db.close()

@client.command()
async def hazard(ctx, amount:int=1000):
    member = ctx.author
    db = sqlite3.connect("eco.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT wallet FROM eco WHERE user_id = {member.id}")
    wallet = cursor.fetchone()

    try:
        wallet = wallet[0]
    except:
        wallet = 0

    if wallet < amount:
        embed = nextcord.Embed(title = "<:nie:1020344672461262889> Nie masz wystarczająco pieniędzy!",timestamp = ctx.message.created_at, color = nextcord.Colour.red())
        return await ctx.reply(embed = embed)

    user_strikes = random.randint(1,14)
    bot_strikes = random.randint(5,14)

    if user_strikes > bot_strikes:
        percentage = random.randint(50,100)
        amount_won = int(amount*(percentage/100))
        cursor.execute(f"UPDATE eco SET wallet = ? WHERE user_id = ?", (wallet + amount_won, ctx.author.id))
        db.commit()
        embed=nextcord.Embed(title=f"🥇 Wygrałeś!",description=f"➕ Wygrałeś **{amount_won}**💰\n🍀 Szansa: **{percentage}%**\n🏦 Nowy Stan Portfela: **{wallet + amount_won}💰**", timestamp = datetime.now(), color=0x04ec32)
        embed.set_author(name = member.name, icon_url = member.display_avatar)
    
    elif user_strikes < bot_strikes:
        percentage = random.randint(50,100)
        amount_lost = int(amount*(percentage/100))
        cursor.execute(f"UPDATE eco SET wallet = ? WHERE user_id = ?", (wallet - amount_lost, ctx.author.id))
        db.commit()
        embed=nextcord.Embed(title=f"❌ Przegrałeś!",description=f"➖ Straciłeś **{amount_lost}**💰\n🍀 Szansa: **{percentage}%**\n🏦 Nowy Stan Portfela: **{wallet - amount_lost}💰**", timestamp = datetime.now(), color = nextcord.Colour.red())
        embed.set_author(name = member.name, icon_url = member.display_avatar)
    else:
        embed=nextcord.Embed(title=f"🧨 Remis!", timestamp = datetime.now(), color = nextcord.Colour.red())
        embed.set_author(name = member.name, icon_url = member.display_avatar)

    embed.add_field(name=f"**{ctx.author.name.title()}**", value=f"Wynik: __{user_strikes}__", inline=True)
    embed.set_thumbnail(url="https://cdn.pixabay.com/photo/2013/07/13/12/37/poker-159973_960_720.png") 
    embed.add_field(name=f"**XajperBOT**", value=f"Wynik: __{bot_strikes}__", inline=True)
    await ctx.reply(embed=embed)

    cursor.close()
    db.close()


@client.slash_command(guild_ids=[SERWER_ID], description="Zagraj w kasyno 🎰", name="kasyno")
async def kasyno(interaction: Interaction, pieniądze: int=500):
    member = interaction.user
    db = sqlite3.connect("eco.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT wallet FROM eco WHERE user_id = {member.id}")
    wallet = cursor.fetchone()

    try:
        wallet = wallet[0]
    except:
        wallet = wallet

    if pieniądze < 500:
        embed = nextcord.Embed(title = "<:nie:1020344672461262889> Musisz postawić minimalnie 500💰!",timestamp = interaction.created_at, color = nextcord.Colour.red())
        return await interaction.response.send_message(embed = embed)
    
    if wallet < pieniądze:
        embed = nextcord.Embed(title = "<:nie:1020344672461262889> Nie masz wystarczająco pieniędzy!",timestamp = interaction.created_at, color = nextcord.Colour.red())
        return await interaction.response.send_message(embed = embed)

    time_factors = random.randint(1,5)
    earning = int(pieniądze*time_factors)

    final = []
    for i in range(3):
        a =  random.choice(["🍉","💎","💸"])
        final.append(a)
    
    if final[0] == final[1] or final[0] == final[2] or final[2] == final[0]:
        cursor.execute(f"UPDATE eco SET wallet = ? WHERE user_id = ?", (wallet + earning, interaction.user.name))
        db.commit()
        
        embed=nextcord.Embed(title=f"🎰 Automat", timestamp = datetime.now(), color=0x04ec32)
        embed.set_author(name = member.name, icon_url = member.display_avatar)
        embed.add_field(name=f"Wygrałeś {earning}💰!",value=f"{final}")
        embed.add_field(name=f"════════════════════", value=f"⭕ Mnożnik: **x{time_factors}**", inline=False)
        embed.add_field(name=f"════════════════════", value=f"🏦 Nowy Stan Portfela: **{wallet + earning}**💰", inline=False)
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1055/1055823.png")
        await interaction.response.send_message(embed=embed)
    else:
        cursor.execute(f"UPDATE eco SET wallet = ? WHERE user_id = ?", (wallet - earning, interaction.user.name))
        db.commit()
        
        embed=nextcord.Embed(title=f"🎰 Automat", timestamp = datetime.now(), color = nextcord.Colour.red())
        embed.set_author(name = member.name, icon_url = member.display_avatar)
        embed.add_field(name=f"Straciłeś {earning}💰!",value=f"{final}")
        embed.add_field(name=f"════════════════════", value=f"⭕ Mnożnik: **x{time_factors}**", inline=False)
        embed.add_field(name=f"════════════════════", value=f"🏦 Nowy Stan Portfela: **{wallet - earning}**💰", inline=False)
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1055/1055823.png")
        await interaction.response.send_message(embed=embed)

        cursor.close()
        db.close()

@client.command()
async def kasyno(ctx, amount:int=500):
    member = ctx.author
    db = sqlite3.connect("eco.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT wallet FROM eco WHERE user_id = {member.id}")
    wallet = cursor.fetchone()

    try:
        wallet = wallet[0]
    except:
        wallet = wallet

    if amount < 500:
        embed = nextcord.Embed(title = "<:nie:1020344672461262889> Musisz postawić minimalnie 500💰!",timestamp = ctx.message.created_at, color = nextcord.Colour.red())
        return await ctx.reply(embed = embed)
    
    if wallet < amount:
        embed = nextcord.Embed(title = "<:nie:1020344672461262889> Nie masz wystarczająco pieniędzy!",timestamp = ctx.message.created_at, color = nextcord.Colour.red())
        return await ctx.reply(embed = embed)

    time_factors = random.randint(1,5)
    earning = int(amount*time_factors)

    final = []
    for i in range(3):
        a =  random.choice(["🍉","💎","💸"])
        final.append(a)
    
    if final[0] == final[1] or final[0] == final[2] or final[2] == final[0]:
        cursor.execute(f"UPDATE eco SET wallet = ? WHERE user_id = ?", (wallet + earning, ctx.author.id))
        db.commit()
        
        embed=nextcord.Embed(title=f"🎰 Automat", timestamp = datetime.now(), color=0x04ec32)
        embed.set_author(name = member.name, icon_url = member.display_avatar)
        embed.add_field(name=f"Wygrałeś {earning}💰!",value=f"{final}")
        embed.add_field(name=f"════════════════════", value=f"⭕ Mnożnik: **x{time_factors}**", inline=False)
        embed.add_field(name=f"════════════════════", value=f"🏦 Nowy Stan Portfela: **{wallet + earning}**💰", inline=False)
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1055/1055823.png")
        await ctx.reply(embed=embed)
    else:
        cursor.execute(f"UPDATE eco SET wallet = ? WHERE user_id = ?", (wallet - earning, ctx.author.id))
        db.commit()
        
        embed=nextcord.Embed(title=f"🎰 Automat", timestamp = datetime.now(), color = nextcord.Colour.red())
        embed.set_author(name = member.name, icon_url = member.display_avatar)
        embed.add_field(name=f"Straciłeś {earning}💰!",value=f"{final}")
        embed.add_field(name=f"════════════════════", value=f"⭕ Mnożnik: **x{time_factors}**", inline=False)
        embed.add_field(name=f"════════════════════", value=f"🏦 Nowy Stan Portfela: **{wallet - earning}**💰", inline=False)
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1055/1055823.png")
        await ctx.reply(embed=embed)

        cursor.close()
        db.close()

@client.command()
async def ruletka(ctx, amount:int=500, *, kolor):
    zarobek = int(amount*2)
    wybory = ['czerwone', 'niebieskie']
    wyborybota = random.choice(wybory)
    user_choice = user_choice.lower()
    member = ctx.author
    db = sqlite3.connect("eco.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT wallet FROM eco WHERE user_id = {member.id}")
    wallet = cursor.fetchone()

    try:
        wallet = wallet[0]
    except:
        wallet = wallet

    if amount < 100:
        embed = nextcord.Embed(title = "<:nie:1020344672461262889> Musisz postawić minimalnie 100💰!",timestamp = ctx.message.created_at, color = nextcord.Colour.red())
        return await ctx.reply(embed = embed)
    
    if wallet < amount:
        embed = nextcord.Embed(title = "<:nie:1020344672461262889> Nie masz wystarczająco pieniędzy!",timestamp = ctx.message.created_at, color = nextcord.Colour.red())
        return await ctx.reply(embed = embed)

    if wybory==wyborybota:
        cursor.execute("UPDATE eco SET bank = ? WHERE user_id = ?", (wallet + zarobek, ctx.user.id))
        embed=nextcord.Embed(title=f"🎲 Ruletka",description=f"Wygrałeś {zarobek}💰!", timestamp = datetime.now(), color = nextcord.Colour.green())
        embed.add_field(name=f"════════════════════", value=f"❓ **Gdzie wypadła kulka**? Pole {wyborybota}", inline=False)
        embed.add_field(name=f"════════════════════", value=f"🎯 **Na co postawiłeś**? {user_choice}", inline=False)
        embed.add_field(name=f"════════════════════", value=f"💸 **Nowy stan portfela**: {wallet + zarobek}💰", inline=False)
        await ctx.response.send_message(embed=embed)

    if wybory=='czerwone' and wyborybota=='niebieskie':
        cursor.execute("UPDATE eco SET bank = ? WHERE user_id = ?", (wallet - zarobek, ctx.user.id))
        embed=nextcord.Embed(title=f"🎲 Ruletka",description=f"<:tak:1020344650260807700> Straciłeś {zarobek}💰!", timestamp = datetime.now(), color = nextcord.Colour.red())
        embed.add_field(name=f"════════════════════", value=f"❓ **Gdzie wypadła kulka**? Pole {wyborybota}", inline=False)
        embed.add_field(name=f"════════════════════", value=f"🎯 **Na co postawiłeś**? {user_choice}", inline=False)
        embed.add_field(name=f"════════════════════", value=f"💸 **Nowy stan portfela**: {wallet - zarobek}💰", inline=False)
        await ctx.response.send_message(embed=embed)

    if wybory=='niebieskie' and wyborybota=='czerwone':
        cursor.execute("UPDATE eco SET bank = ? WHERE user_id = ?", (wallet - zarobek, ctx.user.id))
        embed=nextcord.Embed(title=f"🎲 Ruletka",description=f"<:tak:1020344650260807700> Straciłeś {zarobek}💰!", timestamp = datetime.now(), color = nextcord.Colour.red())
        embed.add_field(name=f"════════════════════", value=f"❓ **Gdzie wypadła kulka**? Pole {wyborybota}", inline=False)
        embed.add_field(name=f"════════════════════", value=f"🎯 **Na co postawiłeś**? {user_choice}", inline=False)
        embed.add_field(name=f"════════════════════", value=f"💸 **Nowy stan portfela**: {wallet - zarobek}💰", inline=False)
        await ctx.response.send_message(embed=embed)

    cursor.close()
    db.close()







@client.command(aliases=['roulette'])
async def ruletka1(ctx, round_id):
    round_id = str(round_id)
    round_lenght = len(round_id)
    if round_lenght == 36:
        predictions = ['red','red','red','purple','purple','purple','gold']
        prediction = random.choice(predictions)
        if prediction == 'red':
            embed_color = 0xFF0078
            color_text = 'Red'
            prediction = ":red_square:"
        elif prediction == 'purple':
            embed_color = 0xff0000
            color_text = 'Purple'
            prediction = ":purple_square:"
        elif prediction == 'gold':
            embed_color = 0xffea00
            color_text = 'Gold'
            prediction = ":yellow_square:"
        embed=nextcord.Embed(title=f"🎲 Ruletka", timestamp = datetime.now(), color = embed_color)
        embed.add_field(name="Predyktor Ruletki", value=color_text + "\n" + prediction)
        embed.set_author(name = member.name, icon_url = member.display_avatar)
        embed.set_thumbnail(url="https://sadurski.com/wp-content/uploads/2019/11/ruletka-gra-hazard-ciekawostki.jpg")
        await ctx.send(embed=embed)
    else:
        embed=nextcord.Embed(title="",description="<:nie:1020344672461262889> Niepoprawna ilość rund!", timestamp = datetime.now(), color = nextcord.Colour.red())
        await ctx.send(embed=embed)


@client.slash_command(guild_ids=[SERWER_ID], description="Wpłać pieniądze do banku 💸", name="dep")
async def dep(interaction: Interaction, pieniądze: int):
    db = sqlite3.connect("eco.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM eco WHERE user_id = {interaction.user.id}")
    data = cursor.fetchone()
    try:
        wallet = data[1]
        bank = data[2]
    except:
        embed=nextcord.Embed(title=f"",description=f"ERROR!", color = nextcord.Colour.red())
        await interaction.response.send_message(embed=embed)

    if wallet < pieniądze:
        embed=nextcord.Embed(title=f"",description=f"<:nie:1020344672461262889> Nie masz tylu środków do przelewu na konto!", timestamp = datetime.now(), color = nextcord.Colour.red())
        return await interaction.response.send_message(embed=embed)
    else:
        cursor.execute("UPDATE eco SET bank = ? WHERE user_id = ?", (bank + pieniądze, interaction.user.id))
        cursor.execute("UPDATE eco SET wallet = ? WHERE user_id = ?", (wallet - pieniądze, interaction.user.id))
        embed=nextcord.Embed(title=f"",description=f"<:tak:1020344650260807700> Pomyślnie wpłaciłeś {pieniądze}💰 `do` swojego banku!", timestamp = datetime.now(), color = nextcord.Colour.green())
        await interaction.response.send_message(embed=embed)

    db.commit()
    cursor.close()
    db.close()
    

@client.command(aliases=['deposit', 'wpłać'])
async def dep(ctx, amount:int):
    db = sqlite3.connect("eco.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM eco WHERE user_id = {ctx.author.id}")
    data = cursor.fetchone()
    try:
        wallet = data[1]
        bank = data[2]
    except:
        embed=nextcord.Embed(title=f"",description=f"ERROR!", color = nextcord.Colour.red())
        await ctx.send(embed=embed)

    if wallet < amount:
        embed=nextcord.Embed(title=f"",description=f"<:nie:1020344672461262889> Nie masz tylu środków do przelewu na konto!", timestamp = datetime.now(), color = nextcord.Colour.red())
        return await ctx.send(embed=embed)
    else:
        cursor.execute("UPDATE eco SET bank = ? WHERE user_id = ?", (bank + amount, ctx.author.id))
        cursor.execute("UPDATE eco SET wallet = ? WHERE user_id = ?", (wallet - amount, ctx.author.id))
        embed=nextcord.Embed(title=f"",description=f"<:tak:1020344650260807700> Pomyślnie wpłaciłeś {amount}💰 `do` swojego banku!", timestamp = datetime.now(), color = nextcord.Colour.green())
        await ctx.send(embed=embed)

    db.commit()
    cursor.close()
    db.close()


@client.slash_command(guild_ids=[SERWER_ID], description="Wypłać pieniądze z banku 💳", name="with")
async def wpłać(interaction: Interaction, pieniądze: int):
    db = sqlite3.connect("eco.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM eco WHERE user_id = {interaction.user.id}")
    data = cursor.fetchone()
    try:
        wallet = data[1]
        bank = data[2]
    except:
        embed=nextcord.Embed(title=f"",description=f"ERROR!", color = nextcord.Colour.red())
        await interaction.response.send_message(embed=embed)

    if bank < pieniądze:
        embed=nextcord.Embed(title=f"",description=f"<:nie:1020344672461262889> Nie masz tylu środków na koncie!", timestamp = datetime.now(), color = nextcord.Colour.red())
        return await interaction.response.send_message(embed=embed)
    else:
        cursor.execute("UPDATE eco SET wallet = ? WHERE user_id = ?", (wallet + pieniądze, interaction.user.id))
        cursor.execute("UPDATE eco SET bank = ? WHERE user_id = ?", (bank - pieniądze, interaction.user.id))
        embed=nextcord.Embed(title=f"",description=f"<:tak:1020344650260807700> Pomyślnie wypłaciłeś {pieniądze}💰 `z` swojego banku!", timestamp = datetime.now(), color = nextcord.Colour.green())
        await interaction.response.send_message(embed=embed)

    db.commit()
    cursor.close()
    db.close()        

@client.command(aliases=['with', 'withdraw'])
async def wypłać(ctx, amount:int):
    db = sqlite3.connect("eco.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM eco WHERE user_id = {ctx.author.id}")
    data = cursor.fetchone()
    try:
        wallet = data[1]
        bank = data[2]
    except:
        embed=nextcord.Embed(title=f"",description=f"ERROR!", color = nextcord.Colour.red())
        await ctx.send(embed=embed)

    if bank < amount:
        embed=nextcord.Embed(title=f"",description=f"<:nie:1020344672461262889> Nie masz tylu środków na koncie!", timestamp = datetime.now(), color = nextcord.Colour.red())
        return await ctx.send(embed=embed)
    else:
        cursor.execute("UPDATE eco SET wallet = ? WHERE user_id = ?", (wallet + amount, ctx.author.id))
        cursor.execute("UPDATE eco SET bank = ? WHERE user_id = ?", (bank - amount, ctx.author.id))
        embed=nextcord.Embed(title=f"",description=f"<:tak:1020344650260807700> Pomyślnie wypłaciłeś {amount}💰 `z` swojego banku!", timestamp = datetime.now(), color = nextcord.Colour.green())
        await ctx.send(embed=embed)

    db.commit()
    cursor.close()
    db.close()        


@client.slash_command(guild_ids=[SERWER_ID], description="Twój ekwipunek 🎒", name="inv")
async def inv(interaction: Interaction):
    animal_list = [None, "🦊lis", "🐺wilk", "🐅tygyrs", "🐻niedźwiedź", "🦌jeleń", "🦓zebra", "🦄jednorożec", "🦫bóbr", "🦝szop", "🦔jeż", "🐿️wiewiórka", "🐇królik", "🦆kaczka", "🐗dzik"]
    tools_list = [None, "🏹łuk", "⚔️scyzoryk", "⛏️kilof", "🎣wędka", "🪓siekiera"]
    ore_list = [None, "🥇złoto", "💎diament", "🦾żelazo", "🪨kamień", "🟩szmaragd", "🔴rubin"]
    auta_list = [None, "🚗BMW", "🚗Audi", "🚗Lamborghini", "🚗Pasat", "🛥️Motorówka", "⛵Żaglówka", "🛸UFO", "🚁Helikopter", "🚀Rakieta", "🛩️Samolot", "🚂Pociąg", "🏍️Motor", "🛴Hulajnoga", "🚲Rower", "🛹Deskorolka"]
    meble_list = [None, "🗃️komoda", "🛏️łóżko", "🗄️szafa", "dywan", "🪑krzesło", "🔪aneks kuchenny", "🖼️obraz", "🛁wanna", "🛋️sofa"]

    db = sqlite3.connect("eco.db")
    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM animals WHERE user_id = {interaction.user.id}")
    animals = cursor.fetchone()

    cursor.execute(f"SELECT * FROM tools WHERE user_id = {interaction.user.id}")
    tools = cursor.fetchone()

    cursor.execute(f"SELECT * FROM ore WHERE user_id = {interaction.user.id}")
    ore = cursor.fetchone()

    cursor.execute(f"SELECT * FROM auta WHERE user_id = {interaction.user.id}")
    auta = cursor.fetchone()

    cursor.execute(f"SELECT * FROM meble WHERE user_id = {interaction.user.id}")
    meble = cursor.fetchone()

    animals_ = [f"{i} x{j}" for i, j in itertools.zip_longest(animal_list, animals) if j > 0 and j < 1000000000000]
    tools_ = [f"{i} x{j}" for i, j in itertools.zip_longest(tools_list, tools) if j > 0 and j < 1000000000000]
    ore_ = [f"{i} x{j}" for i, j in itertools.zip_longest(ore_list, ore) if j > 0 and j < 1000000000000]
    auta_ = [f"{i} x{j}" for i, j in itertools.zip_longest(auta_list, auta) if j > 0 and j < 1000000000000]
    meble_ = [f"{i} x{j}" for i, j in itertools.zip_longest(meble_list, meble) if j > 0 and j < 1000000000000]

    animals_ = "\n".join(animals_) if len(animals_) > 0 else "*Nie ma zwierząt w ekwipunku*"
    tools_ = "\n".join(tools_) if len(tools_) > 0 else "*Nie ma narzędzi w ekwipunku*"
    ore_ = "\n".join(ore_) if len(ore_) > 0 else "*Nie ma rud w ekwipunku*"
    auta_ = "\n".join(auta_) if len(auta_) > 0 else "*Nie ma aut w ekwipunku*"
    meble_ = "\n".join(meble_) if len(meble_) > 0 else "*Nie ma mebli w ekwipunku*"
    

    embed=nextcord.Embed(title=f"📚 Ekwipunek",description=f"Wszystkie zebrane rzeczy", timestamp = datetime.now(), color = nextcord.Colour.blue())
    embed.add_field(name="`😺 Zwierzęta`", value=animals_, inline=True)
    embed.add_field(name="`🪛 Narzędzia`", value=tools_, inline=True)
    embed.add_field(name="`👑 Rudy`", value=ore_, inline=True)
    embed.add_field(name="`🏎️ Auta`", value=auta_, inline=True)
    embed.add_field(name="`🛋️ Meble`", value=meble_, inline=True)

    await interaction.response.send_message(embed=embed)
    

@client.command(aliases=['eq', 'inventory'])
async def inv(ctx):
    animal_list = [None, "🦊lis", "🐺wilk", "🐅tygyrs", "🐻niedźwiedź", "🦌jeleń", "🦓zebra", "🦄jednorożec", "🦫bóbr", "🦝szop", "🦔jeż", "🐿️wiewiórka", "🐇królik", "🦆kaczka", "🐗dzik"]
    tools_list = [None, "🏹łuk", "⚔️scyzoryk", "⛏️kilof", "🎣wędka", "🪓siekiera"]
    ore_list = [None, "🥇złoto", "💎diament", "🦾żelazo", "🪨kamień", "🟩szmaragd", "🔴rubin"]
    auta_list = [None, "🚗BMW", "🚗Audi", "🚗Lamborghini", "🚗Pasat", "🛥️Motorówka", "⛵Żaglówka", "🛸UFO", "🚁Helikopter", "🚀Rakieta", "🛩️Samolot", "🚂Pociąg", "🏍️Motor", "🛴Hulajnoga", "🚲Rower", "🛹Deskorolka"]
    meble_list = [None, "🗃️komoda", "🛏️łóżko", "🗄️szafa", "dywan", "🪑krzesło", "🔪aneks kuchenny", "🖼️obraz", "🛁wanna", "🛋️sofa"]

    db = sqlite3.connect("eco.db")
    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM animals WHERE user_id = {ctx.author.id}")
    animals = cursor.fetchone()

    cursor.execute(f"SELECT * FROM tools WHERE user_id = {ctx.author.id}")
    tools = cursor.fetchone()

    cursor.execute(f"SELECT * FROM ore WHERE user_id = {ctx.author.id}")
    ore = cursor.fetchone()

    cursor.execute(f"SELECT * FROM auta WHERE user_id = {ctx.author.id}")
    auta = cursor.fetchone()

    cursor.execute(f"SELECT * FROM meble WHERE user_id = {ctx.author.id}")
    meble = cursor.fetchone()

    animals_ = [f"{i} x{j}" for i, j in itertools.zip_longest(animal_list, animals) if j > 0 and j < 1000000000000]
    tools_ = [f"{i} x{j}" for i, j in itertools.zip_longest(tools_list, tools) if j > 0 and j < 1000000000000]
    ore_ = [f"{i} x{j}" for i, j in itertools.zip_longest(ore_list, ore) if j > 0 and j < 1000000000000]
    auta_ = [f"{i} x{j}" for i, j in itertools.zip_longest(auta_list, auta) if j > 0 and j < 1000000000000]
    meble_ = [f"{i} x{j}" for i, j in itertools.zip_longest(meble_list, meble) if j > 0 and j < 1000000000000]

    animals_ = "\n".join(animals_) if len(animals_) > 0 else "*Nie ma zwierząt w ekwipunku*"
    tools_ = "\n".join(tools_) if len(tools_) > 0 else "*Nie ma narzędzi w ekwipunku*"
    ore_ = "\n".join(ore_) if len(ore_) > 0 else "*Nie ma rud w ekwipunku*"
    auta_ = "\n".join(auta_) if len(auta_) > 0 else "*Nie ma aut w ekwipunku*"
    meble_ = "\n".join(meble_) if len(meble_) > 0 else "*Nie ma mebli w ekwipunku*"
    

    embed=nextcord.Embed(title=f"📚 Ekwipunek",description=f"Wszystkie zebrane rzeczy", timestamp = datetime.now(), color = nextcord.Colour.blue())
    embed.add_field(name="`😺 Zwierzęta`", value=animals_, inline=True)
    embed.add_field(name="`🪛 Narzędzia`", value=tools_, inline=True)
    embed.add_field(name="`👑 Rudy`", value=ore_, inline=True)
    embed.add_field(name="`🏎️ Auta`", value=auta_, inline=True)
    embed.add_field(name="`🛋️ Meble`", value=meble_, inline=True)

    await ctx.send(embed=embed)

@client.command()
async def embed(ctx, tytul, tekst):


    if tytul == None:
        embed=nextcord.Embed(title="<:nie:1020344672461262889> Błąd", description="Nie podano `tytułu`!", timestamp = datetime.now(), color = nextcord.Colour.red())
        await ctx.send(embed=embed)

    if tekst == None:
        embed=nextcord.Embed(title="<:nie:1020344672461262889> Błąd", description="Nie podano `tekstu`!", timestamp = datetime.now(), color = nextcord.Colour.red())
        await ctx.send(embed=embed)

    else:
        embed=nextcord.Embed(title=tytul, description={tekst}, timestamp = datetime.now(), color = nextcord.Colour.green())
        await ctx.send(embed=embed)
    



@client.slash_command(guild_ids=[SERWER_ID], description="Ostrzeż użytkownika ❗", name="warn")
async def warn(interaction: Interaction, osoba: nextcord.Member, *, powód:str= None):
    if powód == None:
        powód = "brak powodu"
    db = sqlite3.connect("warns.db")
    cursor = db.cursor()
    cursor.execute("INSERT INTO warns(guild_id, user_id, content, author_id, time) VALUES(?, ?, ?, ?, ?)", (interaction.guild_id, osoba.id, powód, interaction.user.id, time.time()))
    db.commit()
    cursor.close()
    db.close()
    embed=nextcord.Embed(timestamp = datetime.now(), color = nextcord.Colour.green())
    embed.add_field(name=f"» :warning: Pomyślne zwarnowanie!", value=f"> Zwarnowano użytkownika `{osoba.name}` za `{powód}`!", inline=False)
    embed.set_footer(text=f"Komende użył {interaction.user.name}")
    await interaction.response.send_message(embed=embed)


@client.command()
@has_permissions(ban_members=True)
async def warn(ctx, member: nextcord.Member, *,reason:str= None):
    if reason == None:
        reason = "brak powodu"
    db = sqlite3.connect("warns.db")
    cursor = db.cursor()
    cursor.execute("INSERT INTO warns(guild_id, user_id, content, author_id, time) VALUES(?, ?, ?, ?, ?)", (ctx.author.guild.id, member.id, reason, ctx.author.id, time.time()))
    db.commit()
    cursor.close()
    db.close()
    embed=nextcord.Embed(timestamp = datetime.now(), color = nextcord.Colour.green())
    embed.add_field(name=f"» :warning: Pomyślne zwarnowanie!", value=f"> Zwarnowano użytkownika `{member.name}` za `{reason}`!", inline=False)
    embed.set_footer(text=f"Komende użył {ctx.author.display_name}")
    await ctx.send(embed=embed)

@warn.error
async def warn_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed=nextcord.Embed(title="<:nie:1020344672461262889> ERROR",description="Nie posiadasz permisji!",timestamp = datetime.now(), color = nextcord.Colour.red())
        await ctx.send(embed=embed)


@client.slash_command(guild_ids=[SERWER_ID], description="Sprawdź ostrzeżenia użytkownika 📑", name="warninfo")
async def warninfo(interaction: Interaction, osoba: nextcord.Member):
    db = sqlite3.connect("warns.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM warns WHERE guild_id = {interaction.guild_id} AND user_id = {osoba.id}")
    wynik = cursor.fetchall()
    nm = 1
    if wynik:
        for warn in wynik:
            embed=nextcord.Embed(timestamp = datetime.now(), color = nextcord.Colour.green())
            embed.add_field(name=f"» 📜 Lista warnów {osoba.name}:", value=f"> Warn numer `{nm}` użytkownika `{osoba.name}` za `{warn[2]}`", inline=False)
            embed.set_footer(text=f"Komende użył {interaction.user.name}")
            await interaction.response.send_message(embed=embed)
            nm += 1
    else:
        embed=nextcord.Embed(timestamp = datetime.now(), color = nextcord.Colour.green())
        embed.add_field(name=f"» 📜 Lista warnów {osoba.name}:", value=f"> Użytkownik `{osoba.name}` nie posiada warnów!", inline=False)
        embed.set_footer(text=f"Komende użył {interaction.user.name}")
        await interaction.response.send_message(embed=embed)

    cursor.close()
    db.close()
    

@client.command()
@has_permissions(ban_members=True)
async def warninfo(ctx, member: nextcord.Member):
    db = sqlite3.connect("warns.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM warns WHERE guild_id = {ctx.author.guild.id} AND user_id = {member.id}")
    wynik = cursor.fetchall()
    nm = 1
    if wynik:
        for warn in wynik:
            embed=nextcord.Embed(timestamp = datetime.now(), color = nextcord.Colour.green())
            embed.add_field(name=f"» 📜 Lista warnów {member.name}:", value=f"> Warn numer `{nm}` użytkownika `{member.name}` za `{warn[2]}`", inline=False)
            embed.set_footer(text=f"Komende użył {ctx.author.display_name}")
            await ctx.send(embed=embed)
            nm += 1
    else:
        embed=nextcord.Embed(timestamp = datetime.now(), color = nextcord.Colour.green())
        embed.add_field(name=f"» 📜 Lista warnów {member.name}:", value=f"> Użytkownik `{member.name}` nie posiada warnów!", inline=False)
        embed.set_footer(text=f"Komende użył {ctx.author.display_name}")
        await ctx.send(embed=embed)

    cursor.close()
    db.close()

@warninfo.error
async def warninfo_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed=nextcord.Embed(title="<:nie:1020344672461262889> ERROR",description="Nie posiadasz permisji!",timestamp = datetime.now(), color = nextcord.Colour.red())
        await ctx.send(embed=embed)

@client.slash_command(guild_ids=[SERWER_ID], description="Odwołaj ostrzeżenie użytkownika 🎭", name="unwarn")
async def unwarn(interaction: Interaction, osoba: nextcord.Member, numer: int):
    db = sqlite3.connect("warns.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM warns WHERE guild_id = {interaction.guild.id} AND user_id = {osoba.id}")
    wynik = cursor.fetchall()
    nm = 1
    if wynik:
        for warn in wynik:
            if nm == numer:
                cursor.execute(f"DELETE FROM warns WHERE guild_id = ? AND user_id = ? AND content = ? AND author_id = ? AND time = ?", (warn[0], warn[1], warn[2], warn[3], warn[4]))
                embed=nextcord.Embed(timestamp = datetime.now(), color = nextcord.Colour.green())
                embed.add_field(name=f"» :warning: Pomyślnie usunięto ostrzeżenie!", value=f"> Warn numer `{nm}` użytkownika `{osoba.name}`, został usunięty!", inline=False)
                await interaction.response.send_message(embed=embed)
            nm += 1
    else:
        embed=nextcord.Embed(timestamp = datetime.now(), color = nextcord.Colour.green())
        embed.add_field(name=f"» 📜 Lista warnów {osoba.name}:", value=f"> Użytkownik `{osoba.name}` nie posiada warnów!", inline=False)
        embed.set_footer(text=f"Komende użył {interaction.user.name}")
        await interaction.response.send_message(embed=embed)
    db.commit()
    cursor.close()
    db.close()


@client.command()
@has_permissions(ban_members=True)
async def unwarn(ctx, member: nextcord.Member, numer: int):
    db = sqlite3.connect("warns.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM warns WHERE guild_id = {ctx.author.guild.id} AND user_id = {member.id}")
    wynik = cursor.fetchall()
    nm = 1
    if wynik:
        for warn in wynik:
            if nm == numer:
                cursor.execute(f"DELETE FROM warns WHERE guild_id = ? AND user_id = ? AND content = ? AND author_id = ? AND time = ?", (warn[0], warn[1], warn[2], warn[3], warn[4]))
                embed=nextcord.Embed(timestamp = datetime.now(), color = nextcord.Colour.green())
                embed.add_field(name=f"» :warning: Pomyślnie usunięto ostrzeżenie!", value=f"> Warn numer `{nm}` użytkownika `{member.name}`, został usunięty!", inline=False)
                await ctx.send(embed=embed)
            nm += 1
    else:
        embed=nextcord.Embed(timestamp = datetime.now(), color = nextcord.Colour.green())
        embed.add_field(name=f"» 📜 Lista warnów {member.name}:", value=f"> Użytkownik `{member.name}` nie posiada warnów!", inline=False)
        embed.set_footer(text=f"Komende użył {ctx.author.display_name}")
        await ctx.send(embed=embed)
    db.commit()
    cursor.close()
    db.close()

@unwarn.error
async def unwarn_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed=nextcord.Embed(title="<:nie:1020344672461262889> ERROR",description="Nie posiadasz permisji!",timestamp = datetime.now(), color = nextcord.Colour.red())
        await ctx.send(embed=embed)

@client.slash_command(guild_ids=[SERWER_ID], description="Usuń wiadomości 🧹", name="clear")
async def clear(interaction: Interaction, ilość: int):
    await interaction.channel.purge(limit=ilość)
    embed=nextcord.Embed(title=f"» 🧹 Pomyślnie usunięto `{ilość}` wiadomości", timestamp = datetime.now(), color = nextcord.Colour.green())
    embed.set_footer(text=f"Komende użył {interaction.user.name}")
    await interaction.response.send_message(embed=embed, delete_after = 1)



@client.command()
@has_permissions(manage_messages=True)
async def clear(ctx, ilosc:int):
    await ctx.channel.purge(limit=ilosc)
    embed=nextcord.Embed(title=f"» 🧹 Pomyślnie usunięto `{ilosc}` wiadomości", timestamp = datetime.now(), color = nextcord.Colour.green())
    embed.set_footer(text=f"Komende użył {ctx.user.name}")
    await ctx.send(embed=embed, delete_after = 1)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed=nextcord.Embed(title="<:nie:1020344672461262889> ERROR",description="Nie posiadasz permisji!",timestamp = datetime.now(), color = nextcord.Colour.red())
        await ctx.send(embed=embed)

@client.slash_command(guild_ids=[SERWER_ID], description="Wycisz użytkownika 🔇", name="mute")
async def mute(interaction: Interaction, osoba: nextcord.Member, *, powód:str= None):
    if powód == None:
        powód = "brak powodu"

    await osoba.edit(timeout=timedelta(hours=24), reason=powód)
    embed=nextcord.Embed(timestamp = datetime.now(), color = nextcord.Colour.green())
    embed.add_field(name=f"» 🔇 Pomyślnie wyciszono `{osoba.name}` za `{powód}`!",value="> *Administratorze, użyj /unmute żeby odciszyć*", inline=False)
    await interaction.response.send_message(embed=embed)
    await osoba.send(f"» 🔇 Zostałeś wyciszony na **XajperTeam** za `{powód}`")


@client.command()
@has_permissions(manage_messages=True)
async def mute(ctx, member: nextcord.Member, *, reason:str= None):
    if reason == None:
        reason = "brak powodu"
    

    await member.edit(timeout=timedelta(hours=24), reason=reason)
    embed=nextcord.Embed(timestamp = datetime.now(), color = nextcord.Colour.green())
    embed.add_field(name=f"» 🔇 Pomyślnie wyciszono `{member.name}` za `{reason}`!", value="> *Administratorze, użyj /unmute żeby odciszyć*", inline=False)
    await ctx.send(embed=embed)
    await member.send(f"» 🔇 Zostałeś wyciszony na **XajperTeam** za `{reason}`")

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed=nextcord.Embed(title="<:nie:1020344672461262889> ERROR",description="Nie posiadasz permisji!",timestamp = datetime.now(), color = nextcord.Colour.red())
        await ctx.send(embed=embed)


@client.slash_command(guild_ids=[SERWER_ID], description="Odcisz użytkownika 🔈", name="unmute")
async def unmute(interaction: Interaction, osoba: nextcord.Member):
    
    await osoba.edit(timeout=None)
    embed=nextcord.Embed(timestamp = datetime.now(), color = nextcord.Colour.green())
    embed.add_field(name=f"» 🔈 Pomyślnie odciszono `{osoba.name}`!", value=f"> {osoba.name} przestrzegaj regulamin by nie dostać ponownie muta!", inline=False)
    await interaction.response.send_message(embed=embed)
    await osoba.send(f"» 🔈 Zostałeś odciszony na **XajperTeam**!")


@client.command()
@has_permissions(manage_messages=True)
async def unmute(ctx, osoba: nextcord.Member):

    await osoba.edit(timeout=None)
    embed=nextcord.Embed(timestamp = datetime.now(), color = nextcord.Colour.green())
    embed.add_field(name=f"» 🔈 Pomyślnie odciszono `{osoba.name}`!", value=f"> {osoba.name} przestrzegaj regulamin by nie dostać ponownie muta!", inline=False)
    await ctx.send(embed=embed)
    await osoba.send(f"» 🔈 Zostałeś odciszony na **XajperTeam**!")

@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed=nextcord.Embed(title="<:nie:1020344672461262889> ERROR",description="Nie posiadasz permisji!",timestamp = datetime.now(), color = nextcord.Colour.red())
        await ctx.send(embed=embed)


@client.slash_command(guild_ids=[SERWER_ID], description="Tymczasowo wycisz użytkownika ⌛", name="tempmute")
async def tempmute(interaction: Interaction, osoba: nextcord.Member, czas:int, *, powód:str= None):
    if powód == None:
        powód = "brak powodu"
    embed=nextcord.Embed(timestamp = datetime.now(), color = nextcord.Colour.green())
    embed.add_field(name=f"» ⌛ Pomyślnie wyciszono `{osoba.name}` na `{czas}` minut za `{powód}`!", value="> *Administratorze, użyj /unmute żeby odciszyć*", inline=False)
    await interaction.response.send_message(embed=embed)
    await osoba.edit(timeout=timedelta(minutes=czas), reason=powód)

@client.command()
@has_permissions(manage_messages=True)
async def tempmute(ctx, member: nextcord.Member = None, time:int=None, *, reason:str = None):
    if member == None:
        embed=nextcord.Embed(timestamp = datetime.now(), color = nextcord.Colour.green())
        embed.add_field(name="» 🆔 Zapomniałeś podać użytkowika!", value="‼️", inline=False)
        await ctx.send(embed=embed)
    elif time == None:
        embed=nextcord.Embed(timestamp = datetime.now(), color = nextcord.Colour.green())
        embed.add_field(name="» ⏰ Zapomniałeś podać czas - na który chcesz wyciszyć użytkownika!", value="‼️", inline=False)
        await ctx.send(embed=embed)
    elif reason == None:
        reason = "brak powodu"


    await member.edit(timeout=timedelta(minutes=time), reason=reason)
    embed=nextcord.Embed(timestamp = datetime.now(), color = nextcord.Colour.green())
    embed.add_field(name=f"» ⌛ Pomyślnie wyciszono `{member.name}` na `{time}` minut za `{reason}`!", value="> *Administratorze, użyj /unmute żeby odciszyć*", inline=False)
    await ctx.send(embed=embed)

@tempmute.error
async def tempmute_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed=nextcord.Embed(title="<:nie:1020344672461262889> ERROR",description="Nie posiadasz permisji!",timestamp = datetime.now(), color = nextcord.Colour.red())
        await ctx.send(embed=embed)
    

@client.slash_command(guild_ids=[SERWER_ID], description="Lista wszystkich komend 📜", name="help")
async def help(interaction: Interaction):
    await interaction.channel.purge(limit=1)
    
    button = Button(label="Moderacyjne", style=nextcord.ButtonStyle.green, emoji="🤖")
    button1 = Button(label="4fun", style=nextcord.ButtonStyle.green, emoji="🎈")
    button2 = Button(label="Ekonomia", style=nextcord.ButtonStyle.green, emoji="💰")
    button3 = Button(label="Poziomy", style=nextcord.ButtonStyle.green, emoji="💿")
    button4 = Button(label="Muzyka", style=nextcord.ButtonStyle.green, emoji="🎶")
    button5 = Button(label="4fun 2", style=nextcord.ButtonStyle.green, emoji="✨")

    async def button_callback(interaction):
        await interaction.channel.purge(limit=1)
        embed=nextcord.Embed(title="🤖Komendy Administracyjne: 🤖", description="=-=-=-=", timestamp = datetime.now(), color = nextcord.Colour.green())
        embed.add_field(name="⛔ Ban:", value="ban {@użytkownik} {powód}", inline=True)
        embed.add_field(name="🎁 UnBan:", value="unban {użytkownik#0000}", inline=True)
        embed.add_field(name="💥 Kick:", value="kick {@użytkownik} {powód}", inline=True)
        embed.add_field(name="🔇 Mute:", value="mute {@użytkownik} {powód}", inline=True)
        embed.add_field(name="🔈 TempMute:", value="tempmute {@użytkownik} {czas w minutach} {powód}", inline=True)
        embed.add_field(name="🎤 UnMute:", value="unmute {@użytkownik}", inline=True)
        embed.add_field(name="🧹 Clear:", value="clear {ilość}", inline=True)
        embed.add_field(name="🔧 Warn:", value="warn {@użytkownik} {powód}", inline=True)
        embed.add_field(name="🔰 UnWarn:", value="unwarn {@użytkownik} {numer warna}", inline=True)
        embed.add_field(name="🧳 WarnInfo:", value="warninfo {@użytkownik}", inline=True)
        embed.add_field(name="[WKRÓTCE] 🎫 Stwórz Ticket", value="ticket", inline=True)
        embed.add_field(name="📊 Stwórz Ankietę:", value="ankieta {opcja1} {opcja2} {tytuł}", inline=True)
        embed.add_field(name="🎉 Giveaway:", value="gstart {czas} {nagroda}", inline=True)
        embed.add_field(name="[WKRÓTCE] 💸 Dodawanie Pieniędzy na Ekonomii:", value="dodajpieniadze {użytkownik} {ilość dodanych pieniędzy}", inline=True)
        embed.add_field(name="🧨 Chcesz zgłosić pewną osobe? Wpisz:", value="report {użytkownik} {powód} {wiadomość którą chcesz przekazać moderacji}", inline=True)
        await interaction.send(embed=embed)
        

    button.callback = button_callback


    async def button1_callback(interaction):
        await interaction.channel.purge(limit=1)
        embed=nextcord.Embed(title="🎉Komendy 4Fun: 🎉", description="=-=-=-=", timestamp = datetime.now(), color = nextcord.Colour.green())
        embed.add_field(name="💯 Losowanie od 0 do 100:", value="losuj", inline=True)
        embed.add_field(name="❓ Wylosuj liczbę do podanego zakresu:", value="roll {zakres}", inline=True)
        embed.add_field(name="👋 Witaj:", value="witaj", inline=True)
        embed.add_field(name="👨‍💻 Avatar:", value="avatar {@użytkownik}", inline=True)
        embed.add_field(name="🔎 Info o Użytkowniku:", value="info {@użytkownik}", inline=True)
        embed.add_field(name="🤖 Info o Bocie:", value="botinfo", inline=True)
        embed.add_field(name="💻 Serwer Info:", value="serwerinfo", inline=True)
        embed.add_field(name="🎱 Zadaj Pytanie Botu:", value="8ball/8b {pytanie}", inline=True)
        embed.add_field(name="⭕❌ Kółko i Krzyżyk:", value="ox {@ty} {@przeciwnik}", inline=True)
        embed.add_field(name="🤫 Poszukiwany:", value="wanted {@użytkownik}", inline=True)
        embed.add_field(name="🤣 Mem:", value="meme", inline=True)
        embed.add_field(name="😆 Żart:", value="zart", inline=True)
        embed.add_field(name="🐈 Zdjęcie Kota:", value="kot", inline=True)
        embed.add_field(name="🐶 Zdjęcie Psa:", value="pies", inline=True)
        embed.add_field(name="🎬 Mój Kanał:", value="xajper", inline=True)
        embed.add_field(name="🧠 IQ:", value="iq", inline=True)
        embed.add_field(name="🎲 Rzuć Kostką:", value="kostka", inline=True)
        embed.add_field(name=":coin: Rzuć Monetą:", value="moneta", inline=True)
        embed.add_field(name="[WKRÓTCE] 🥋 Walka 1vs1:", value="walka {@przeciwnik}", inline=True)
        embed.add_field(name="[WKRÓTCE] ✨ Quizy:", value="quiz", inline=True)
        embed.add_field(name="[WKRÓTCE] ♟ Szachy:", value="szachy {@ty} {@przeciwnik}", inline=True)
        embed.add_field(name="[WKRÓTCE] 🌍 Zgadywanie krajów/flag/stolic:", value="zgadywanie kraje/flagi/stolice", inline=True)
        embed.add_field(name="🏓 Ping! Pong!", value="ping", inline=True)
        embed.add_field(name="❔ Propozycja:", value="propozycja {propozycja}", inline=True)
        embed.add_field(name="💪 POLSKA GUROM!", value="polskagurom", inline=True)
        await interaction.send(embed=embed)
    
    button1.callback = button1_callback

    async def button2_callback(interaction):
        await interaction.channel.purge(limit=1)
        embed=nextcord.Embed(title="💰Komendy do Ekonomii: 💰", description="=-=-=-=", timestamp = datetime.now(), color = nextcord.Colour.green())
        embed.add_field(name=":dollar: Stan Konta:", value="konto/bal/balance", inline=True)
        embed.add_field(name="⏰ Codzienny Zarobek:", value="daily", inline=True)
        embed.add_field(name=":white_check_mark: Kup Przedmiot:", value="kup {nazwa przedmiotu}", inline=True)
        embed.add_field(name="💳 Wypłać Pieniądze:", value="with {all/ilość}", inline=True)
        embed.add_field(name="🏦 Wpłać Pieniądze:", value="dep {all/ilość}", inline=True)
        embed.add_field(name="[WKRÓTCE] ⬆ Topka Najbogatszych Ludzi:", value="topmoney", inline=True)
        embed.add_field(name="🤑 Hazard:", value="hazard {ilość pieniędzy do postawienia}", inline=True)
        embed.add_field(name="🎰 Kasyno:", value="kasyno {ilość pieniędzy do postawienia}", inline=True)
        embed.add_field(name="[WKRÓTCE] 🎣 Łowienie Ryb:", value="jezioro ", inline=True)
        embed.add_field(name="[WKRÓTCE] ⛺ Polowanie:", value="polowanie", inline=True)
        embed.add_field(name="[WKRÓTCE] ⛏️ Kopalnia:", value="kopalnia", inline=True)
        embed.add_field(name="[WKRÓTCE] 🪓 Tartak:", value="tartak", inline=True)
        embed.add_field(name="🛒 Sklep:", value="sklep", inline=True)
        embed.add_field(name="🏰 Twój Ekwipunek:", value="eq/inv/inventory", inline=True)
        embed.add_field(name="🎓 Edukacja to podstawa! Chcesz zarabiać więcej? Poucz się!", value="edukacja/nauka {ilość pieniędzy przeznaczona na edukację}", inline=True)
        
        await interaction.send(embed=embed)

    button2.callback = button2_callback


    async def button3_callback(interaction):
        await interaction.channel.purge(limit=1)
        embed=nextcord.Embed(title="🏆Komendy do Systemu Poziomów: 🏆", description="=-=-=-=", timestamp = datetime.now(), color = nextcord.Colour.green())
        embed.add_field(name="[WKRÓTCE] 💠 Twój Aktualnym Poziom:", value="rank", inline=True)
        embed.add_field(name="[WKRÓTCE] 📈 Topka Ludzi z Najwyższym Poziomem:", value="toplvl", inline=True)
        await interaction.send(embed=embed)

    button3.callback = button3_callback


    async def button4_callback(interaction):
        await interaction.channel.purge(limit=1)
        embed=nextcord.Embed(title="🎼Komendy do Muzyki: 🎼", description="=-=-=-=", timestamp = datetime.now(), color = nextcord.Colour.green())
        embed.add_field(name="[WKRÓTCE] 🎵 Start:", value="start {muzyka}", inline=True)
        await interaction.send(embed=embed)

    button4.callback = button4_callback


    async def button5_callback(interaction):
        await interaction.channel.purge(limit=1)
        embed=nextcord.Embed(title="🎉Komendy 4Fun: 🎉", description="=-=-=-=", timestamp = datetime.now(), color = nextcord.Colour.green())
        embed.add_field(name=":printer:Chcesz żeby bot napisał to co ty emotkami? Wpisz:", value="kopiuj", inline=True)
        embed.add_field(name="🪨🧻✂️ Kamień papier nożyce:", value="kpn",inline=True)
        embed.add_field(name="🔎 Ciekawostki:", value="ciekawostka",inline=True)
        embed.add_field(name="🤔 Różne żartobliwe rozkminy:", value="rozkmina",inline=True)
        await interaction.send(embed=embed)
        
    button5.callback = button5_callback


    view = View(timeout=120)
    view.add_item(button)
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)
    view.add_item(button4)
    view.add_item(button5)
    embed = nextcord.Embed(title = "» Hej! Wybierz kategorię pomocy którą chcesz zobaczyć!",timestamp = interaction.created_at, color = nextcord.Colour.green())
    await interaction.send(embed = embed, view=view)







@client.command()
async def help(ctx):
    await ctx.channel.purge(limit=1)
    
    button = Button(label="Moderacyjne", style=nextcord.ButtonStyle.green, emoji="🤖")
    button1 = Button(label="4fun", style=nextcord.ButtonStyle.green, emoji="🎈")
    button2 = Button(label="Ekonomia", style=nextcord.ButtonStyle.green, emoji="💰")
    button3 = Button(label="Poziomy", style=nextcord.ButtonStyle.green, emoji="💿")
    button4 = Button(label="Muzyka", style=nextcord.ButtonStyle.green, emoji="🎶")
    button5 = Button(label="4fun 2", style=nextcord.ButtonStyle.green, emoji="✨")

    async def button_callback(interaction):
        await ctx.channel.purge(limit=1)
        embed=nextcord.Embed(title="🤖Komendy Administracyjne: 🤖", description="=-=-=-=", timestamp = datetime.now(), color = nextcord.Colour.green())
        embed.add_field(name="⛔ Ban:", value="ban {@użytkownik} {powód}", inline=True)
        embed.add_field(name="🎁 UnBan:", value="unban {użytkownik#0000}", inline=True)
        embed.add_field(name="💥 Kick:", value="kick {@użytkownik} {powód}", inline=True)
        embed.add_field(name="🔇 Mute:", value="mute {@użytkownik} {powód}", inline=True)
        embed.add_field(name="🔈 TempMute:", value="tempmute {@użytkownik} {czas w minutach} {powód}", inline=True)
        embed.add_field(name="🎤 UnMute:", value="unmute {@użytkownik}", inline=True)
        embed.add_field(name="🧹 Clear:", value="clear {ilość}", inline=True)
        embed.add_field(name="🔧 Warn:", value="warn {@użytkownik} {powód}", inline=True)
        embed.add_field(name="🔰 UnWarn:", value="unwarn {@użytkownik} {numer warna}", inline=True)
        embed.add_field(name="🧳 WarnInfo:", value="warninfo {@użytkownik}", inline=True)
        embed.add_field(name="[WKRÓTCE] 🎫 Stwórz Ticket", value="ticket", inline=True)
        embed.add_field(name="📊 Stwórz Ankietę:", value="ankieta {opcja1} {opcja2} {tytuł}", inline=True)
        embed.add_field(name="🎉 Giveaway:", value="gstart {czas} {nagroda}", inline=True)
        embed.add_field(name="[WKRÓTCE] 💸 Dodawanie Pieniędzy na Ekonomii:", value="dodajpieniadze {użytkownik} {ilość dodanych pieniędzy}", inline=True)
        embed.add_field(name="🧨 Chcesz zgłosić pewną osobe? Wpisz:", value="report {użytkownik} {powód} {wiadomość którą chcesz przekazać moderacji}", inline=True)
        await ctx.send(embed=embed)
        

    button.callback = button_callback


    async def button1_callback(interaction):
        await ctx.channel.purge(limit=1)
        embed=nextcord.Embed(title="🎉Komendy 4Fun: 🎉", description="=-=-=-=", timestamp = datetime.now(), color = nextcord.Colour.green())
        embed.add_field(name="💯 Losowanie od 0 do 100:", value="losuj", inline=True)
        embed.add_field(name="❓ Wylosuj liczbę do podanego zakresu:", value="roll {zakres}", inline=True)
        embed.add_field(name="👋 Witaj:", value="witaj", inline=True)
        embed.add_field(name="👨‍💻 Avatar:", value="avatar {@użytkownik}", inline=True)
        embed.add_field(name="🔎 Info o Użytkowniku:", value="userinfo {@użytkownik}", inline=True)
        embed.add_field(name="🤖 Info o Bocie:", value="botinfo", inline=True)
        embed.add_field(name="💻 Serwer Info:", value="serwerinfo", inline=True)
        embed.add_field(name="🎱 Zadaj Pytanie Botu:", value="8ball/8b {pytanie}", inline=True)
        embed.add_field(name="⭕❌ Kółko i Krzyżyk:", value="ox {@ty} {@przeciwnik}", inline=True)
        embed.add_field(name="🤫 Poszukiwany:", value="wanted {@użytkownik}", inline=True)
        embed.add_field(name="🤣 Mem:", value="meme", inline=True)
        embed.add_field(name="😆 Żart:", value="zart", inline=True)
        embed.add_field(name="🐈 Zdjęcie Kota:", value="kot", inline=True)
        embed.add_field(name="🐶 Zdjęcie Psa:", value="pies", inline=True)
        embed.add_field(name="🎬 Mój Kanał:", value="xajper", inline=True)
        embed.add_field(name="🧠 IQ:", value="iq", inline=True)
        embed.add_field(name="🎲 Rzuć Kostką:", value="kostka", inline=True)
        embed.add_field(name=":coin: Rzuć Monetą:", value="moneta", inline=True)
        embed.add_field(name="[WKRÓTCE] 🥋 Walka 1vs1:", value="walka {@przeciwnik}", inline=True)
        embed.add_field(name="[WKRÓTCE] ✨ Quizy:", value="quiz", inline=True)
        embed.add_field(name="[WKRÓTCE] ♟ Szachy:", value="szachy {@ty} {@przeciwnik}", inline=True)
        embed.add_field(name="[WKRÓTCE] 🌍 Zgadywanie krajów/flag/stolic:", value="zgadywanie kraje/flagi/stolice", inline=True)
        embed.add_field(name="🏓 Ping! Pong!", value="ping", inline=True)
        embed.add_field(name="❔ Propozycja:", value="propozycja {propozycja}", inline=True)
        embed.add_field(name="💪 POLSKA GUROM!", value="polskagurom", inline=True)
        await ctx.send(embed=embed)
    
    button1.callback = button1_callback

    async def button2_callback(interaction):
        await ctx.channel.purge(limit=1)
        embed=nextcord.Embed(title="💰Komendy do Ekonomii: 💰", description="=-=-=-=", timestamp = datetime.now(), color = nextcord.Colour.green())
        embed.add_field(name=":dollar: Stan Konta:", value="konto/bal/balance", inline=True)
        embed.add_field(name="⏰ Codzienny Zarobek:", value="daily", inline=True)
        embed.add_field(name=":white_check_mark: Kup Przedmiot:", value="kup {nazwa przedmiotu}", inline=True)
        embed.add_field(name="💳 Wypłać Pieniądze:", value="with {all/ilość}", inline=True)
        embed.add_field(name="🏦 Wpłać Pieniądze:", value="dep {all/ilość}", inline=True)
        embed.add_field(name="[WKRÓTCE] ⬆ Topka Najbogatszych Ludzi:", value="topmoney", inline=True)
        embed.add_field(name="🤑 Hazard:", value="hazard {ilość pieniędzy do postawienia}", inline=True)
        embed.add_field(name="🎰 Kasyno:", value="kasyno {ilość pieniędzy do postawienia}", inline=True)
        embed.add_field(name="[WKRÓTCE] 🎣 Łowienie Ryb:", value="jezioro ", inline=True)
        embed.add_field(name="[WKRÓTCE] ⛺ Polowanie:", value="polowanie", inline=True)
        embed.add_field(name="[WKRÓTCE] ⛏️ Kopalnia:", value="kopalnia", inline=True)
        embed.add_field(name="[WKRÓTCE] 🪓 Tartak:", value="tartak", inline=True)
        embed.add_field(name="🛒 Sklep:", value="sklep", inline=True)
        embed.add_field(name="🏰 Twój Ekwipunek:", value="eq/inv/inventory", inline=True)
        embed.add_field(name="🎓 Edukacja to podstawa! Chcesz zarabiać więcej? Poucz się!", value="edukacja/nauka {ilość pieniędzy przeznaczona na edukację}", inline=True)
        
        await ctx.send(embed=embed)

    button2.callback = button2_callback


    async def button3_callback(interaction):
        await ctx.channel.purge(limit=1)
        embed=nextcord.Embed(title="🏆Komendy do Systemu Poziomów: 🏆", description="=-=-=-=", timestamp = datetime.now(), color = nextcord.Colour.green())
        embed.add_field(name="[WKRÓTCE] 💠 Twój Aktualnym Poziom:", value="rank", inline=True)
        embed.add_field(name="[WKRÓTCE] 📈 Topka Ludzi z Najwyższym Poziomem:", value="toplvl", inline=True)
        await ctx.send(embed=embed)

    button3.callback = button3_callback


    async def button4_callback(interaction):
        await ctx.channel.purge(limit=1)
        embed=nextcord.Embed(title="🎼Komendy do Muzyki: 🎼", description="=-=-=-=", timestamp = datetime.now(), color = nextcord.Colour.green())
        embed.add_field(name="[WKRÓTCE] 🎵 Start:", value="start {muzyka}", inline=True)
        await ctx.send(embed=embed)

    button4.callback = button4_callback


    async def button5_callback(interaction):
        await ctx.channel.purge(limit=1)
        embed=nextcord.Embed(title="🎉Komendy 4Fun: 🎉", description="=-=-=-=", timestamp = datetime.now(), color = nextcord.Colour.green())
        embed.add_field(name=":printer:Chcesz żeby bot napisał to co ty emotkami? Wpisz:", value="kopiuj", inline=True)
        embed.add_field(name="🪨🧻✂️ Kamień papier nożyce:", value="kpn",inline=True)
        embed.add_field(name="🔎 Ciekawostki:", value="ciekawostka",inline=True)
        embed.add_field(name="🤔 Różne żartobliwe rozkminy:", value="rozkmina",inline=True)
        await ctx.send(embed=embed)
        
    button5.callback = button5_callback


    view = View(timeout=120)
    view.add_item(button)
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)
    view.add_item(button4)
    view.add_item(button5)
    embed = nextcord.Embed(title = "» Hej! Wybierz kategorię pomocy którą chcesz zobaczyć!",timestamp = ctx.message.created_at, color = nextcord.Colour.green())
    await ctx.send(embed = embed, view=view)
    


@client.slash_command(guild_ids=[SERWER_ID], description="Napisz coś a bot skopiuje to do postaci emotek 🤪", name="kopiuj")
async def kopiuj(interaction: Interaction, tekst):
    emojis = []
    for s in tekst.lower():
        if s.isdecimal():
            num2emo = {'0':'zero','1':'one','2':'two','3':'three','4':'four','5':'five','6':'six','7':'seven','8':'eight','9':'nine'}

            emojis.append(f':{num2emo.get(s)}:')
        elif s.isalpha():
            emojis.append(f':regional_indicator_{s}:')
        else:
            emojis.append(s)
    await interaction.response.send_message(''.join(emojis))

@client.command()
async def kopiuj(ctx,*,text):
    emojis = []
    for s in text.lower():
        if s.isdecimal():
            num2emo = {'0':'zero','1':'one','2':'two','3':'three','4':'four','5':'five','6':'six','7':'seven','8':'eight','9':'nine'}

            emojis.append(f':{num2emo.get(s)}:')
        elif s.isalpha():
            emojis.append(f':regional_indicator_{s}:')
        else:
            emojis.append(s)
    await ctx.send(''.join(emojis))



@client.slash_command(guild_ids=[SERWER_ID], description="Zadaj pytanie botu 🎱", name="8ball")
async def eightball(interaction: Interaction, *, pytanie):
    responses = ["To pewne.",
                "Zdecydowanie tak.",
                "Bez wątpienia.",
                "Tak - zdecydowanie.",
                "Najprawdopodobniej.",
                "Perspektywa jest dobra.",
                "Tak.",
                "Wszystkie znaki wskazują na tak.",
                "Zapytaj ponownie później.",
                "Lepiej ci teraz nie mówić.",
                "Nie mogę teraz tego przewidzieć.",
                "Skoncentruj się i zapytaj ponownie.",
                "Nie licz na to.",
                "Moja odpowiedź brzmi nie.",
                "Według moich źródeł, nie.",
                "Najadłeś się za dużo Kocimiętki XD",
                "Bardzo wątpliwe."]
    embed = nextcord.Embed(title = f':8ball: Pytanie: __{pytanie}__\n:8ball: Odpowiedź: __{random.choice(responses)}__',timestamp = interaction.created_at, color=interaction.user.colour)
    await interaction.response.send_message(embed = embed)


@client.command(aliases=['8ball', '8b'])
async def eightball(ctx, *, pytanie):
    responses = ["To pewne.",
                "Zdecydowanie tak.",
                "Bez wątpienia.",
                "Tak - zdecydowanie.",
                "Najprawdopodobniej.",
                "Perspektywa jest dobra.",
                "Tak.",
                "Wszystkie znaki wskazują na tak.",
                "Zapytaj ponownie później.",
                "Lepiej ci teraz nie mówić.",
                "Nie mogę teraz tego przewidzieć.",
                "Skoncentruj się i zapytaj ponownie.",
                "Nie licz na to.",
                "Moja odpowiedź brzmi nie.",
                "Według moich źródeł, nie.",
                "Najadłeś się za dużo Kocimiętki XD",
                "Bardzo wątpliwe."]
    embed = nextcord.Embed(title = f':8ball: Pytanie: __{pytanie}__\n:8ball: Odpowiedź: __{random.choice(responses)}__',timestamp = ctx.message.created_at, color=ctx.author.colour)
    await ctx.send(embed = embed)


@client.slash_command(guild_ids=[SERWER_ID], description="Zmień status bota 🎮", name="graj")
async def graj(interaction: Interaction, *, gra):
    await client.change_presence(activity=nextcord.Game(name=gra))
    embed=nextcord.Embed(title="<:tak:1020344650260807700> ZMIANA STATUSU",description=f"Bot gra w `{gra}`",timestamp = datetime.now(), color = nextcord.Colour.green())
    await interaction.response.send_message(embed=embed)


@client.command()
@has_permissions(ban_members=True)
async def graj(ctx, *, game):
    await client.change_presence(activity=nextcord.Game(name=game))


@client.slash_command(guild_ids=[SERWER_ID], description="Zmień status bota 📡", name="streamuj")
async def streamuj(interaction: Interaction, *, stream):
    await client.change_presence(activity=nextcord.Streaming(name=stream, url="https://www.youtube.com/channel/UCC5Ssx_Py9yYkEpApx6Piug"))
    embed=nextcord.Embed(title="<:tak:1020344650260807700> ZMIANA STATUSU",description=f"Bot streamuje `{stream}`",timestamp = datetime.now(), color = nextcord.Colour.green())
    await interaction.response.send_message(embed=embed)


@client.command()
@has_permissions(ban_members=True)
async def streamuj(ctx, *, game):
    await client.change_presence(activity=nextcord.Streaming(name=game, url="https://www.youtube.com/channel/UCC5Ssx_Py9yYkEpApx6Piug"))


@client.slash_command(guild_ids=[SERWER_ID], description="Zmień status bota 🎵", name="słuchaj")
async def słuchaj(interaction: Interaction, *, muzyka):
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name=muzyka))
    embed=nextcord.Embed(title="<:tak:1020344650260807700> ZMIANA STATUSU",description=f"Bot słucha `{muzyka}`",timestamp = datetime.now(), color = nextcord.Colour.green())
    await interaction.response.send_message(embed=embed)


@client.command()
@has_permissions(ban_members=True)
async def sluchaj(ctx, *, music):
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name=music))


@client.slash_command(guild_ids=[SERWER_ID], description="Zmień status bota 🎦", name="oglądaj")
async def oglądaj(interaction: Interaction, *, film):
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=film))
    embed=nextcord.Embed(title="<:tak:1020344650260807700> ZMIANA STATUSU",description=f"Bot ogląda `{film}`",timestamp = datetime.now(), color = nextcord.Colour.green())
    await interaction.response.send_message(embed=embed)


@client.command()
@has_permissions(ban_members=True)
async def ogladaj(ctx, *, film):
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=film))


@client.slash_command(guild_ids=[SERWER_ID], description="Zbanuj użytkownika 🔨", name="ban")
async def ban(interaction: Interaction, osoba: nextcord.Member, powód):
    embed=nextcord.Embed(title="» ⛔ Pomyślnie zbanowanie!",timestamp = datetime.now(), color = nextcord.Colour.green())
    embed.add_field(name=f"> Zbanowano `{osoba.name}` za `{powód}`!", value="*Administratorze, użyj /unban żeby odbanować*", inline=False)
    await interaction.response.send_message(embed=embed)
    await osoba.ban(reason=powód)


@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member : nextcord.Member, reason="bez powodu"):
    embed=nextcord.Embed(title="» ⛔ Pomyślnie zbanowanie!",timestamp = datetime.now(), color = nextcord.Colour.green())
    embed.add_field(name=f"> Zbanowano `{member.name}` za `{reason}`!", value="*Administratorze, użyj /unban żeby odbanować*", inline=False)
    await ctx.send(embed=embed)
    await member.ban(reason=reason)

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed=nextcord.Embed(title="<:nie:1020344672461262889> ERROR",description="Nie posiadasz permisji!",timestamp = datetime.now(), color = nextcord.Colour.red())
        await ctx.send(embed=embed)


@client.slash_command(guild_ids=[SERWER_ID], description="Odbanuj użytkownika 😎", name="unban")
async def unban(interaction: Interaction, *, osoba: nextcord.Member):
    if "#" in osoba:
        banned = await interaction.guild.bans()
        osoba_name, osoba_discriminator = osoba.split("#")

        for ban_entry in banned:
            user = ban_entry.user

            if(user.name, user.discriminator) == (osoba_name, osoba_discriminator):
                await interaction.guild.unban(user)
                embed=nextcord.Embed(timestamp = datetime.now(), color = nextcord.Colour.green())
                embed.add_field(name=f"» <:tak:1020344650260807700> Pomyślnie odbanowano {osoba.name}!", value=f"{osoba.name} przestrzegaj regulaminu!", inline=False)
                await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("» Podaj nick w ten sposób: `@XajperBOT` lub `XajperBOT#2471`")


@client.command()
@has_permissions(ban_members=True)
async def unban(ctx, *, member):
    if "#" in member:
        banned = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned:
            user = ban_entry.user

            if(user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                embed=nextcord.Embed(timestamp = datetime.now(), color = nextcord.Colour.green())
                embed.add_field(name=f"» <:tak:1020344650260807700> Pomyślnie odbanowano {member.name}!", value=f"{member.name} przestrzegaj regulaminu!", inline=False)
                await ctx.send(embed=embed)
    else:
        await ctx.send("» Podaj nick w ten sposób: `@XajperBOT` lub `XajperBOT#2471`")

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed=nextcord.Embed(title="<:nie:1020344672461262889> ERROR",description="Nie posiadasz permisji!",timestamp = datetime.now(), color = nextcord.Colour.red())
        await ctx.send(embed=embed)

@client.slash_command(guild_ids=[SERWER_ID], description="Wyświetl avatar użytkownika 🎩", name="avatar")
async def avatar(interaction: Interaction, *, osoba: nextcord.Member):
    if osoba is None or osoba == "":
        osoba = interaction.user

    avatarUrl = osoba.avatar.url
    avatarEmbed = nextcord.Embed(title=f"» 🎩 Avatar `{osoba.name}` :",timestamp = interaction.created_at, colour=nextcord.Colour.gold())
    avatarEmbed.set_image(url=avatarUrl)
    avatarEmbed.set_footer(text=f"Komende użył {interaction.user.name}")

    await interaction.response.send_message(embed=avatarEmbed)


@client.command()
async def avatar(ctx, *, uzytkownik: nextcord.Member = ""):
    if uzytkownik is None or uzytkownik == "":
        uzytkownik = ctx.author

    avatarUrl = uzytkownik.avatar.url
    avatarEmbed = nextcord.Embed(title=f"» 🎩 Avatar `{uzytkownik.mention}` :",timestamp = ctx.message.created_at, colour=nextcord.Colour.gold())
    avatarEmbed.set_image(url=avatarUrl)
    avatarEmbed.set_footer(text=f"Komende użył {ctx.author.name}")

    await ctx.send(embed=avatarEmbed)


@client.slash_command(guild_ids=[SERWER_ID], description="Wyświetl informacje o użytkowniku 🥸", name="userinfo")
async def userinfo(interaction: Interaction, osoba: nextcord.Member):
    if osoba is None or osoba == "":
        osoba = interaction.user
    infoEmbed = nextcord.Embed(title=f"Informacje o: `{osoba.name}`",timestamp = interaction.created_at, color=osoba.colour)
    infoEmbed.add_field(name=f"`🎩Nazwa`", value=osoba.name)
    infoEmbed.add_field(name=f"`🪧ID`", value=osoba.id)
    infoEmbed.add_field(name=f"`🕶️Nick`", value=osoba.display_name)
    infoEmbed.add_field(name=f"`✨Stworzono`", value=osoba.created_at.strftime("%b %d %Y"))
    infoEmbed.add_field(name=f"`📨Dołączono`", value=osoba.joined_at.strftime("%b %d %Y"))
    infoEmbed.add_field(name=f"`👑Najwyższa Rola`", value=osoba.top_role.mention)
    infoEmbed.set_footer(text=f"Komende użył {interaction.user.name}")
    infoEmbed.add_field(name=f"`🎭Ilość Roli`", value=str(len(osoba.roles)-1))
    await interaction.response.send_message(embed=infoEmbed)


@client.command()
async def userinfo(ctx, uzytkownik: nextcord.Member = ""):
    if uzytkownik is None or uzytkownik == "":
        uzytkownik = ctx.author
    infoEmbed = nextcord.Embed(title=f"Informacje o: `{uzytkownik.name}`",timestamp = ctx.message.created_at, color=uzytkownik.colour)
    infoEmbed.add_field(name=f"`🎩Nazwa`", value=uzytkownik.name)
    infoEmbed.add_field(name=f"`🪧ID`", value=uzytkownik.id)
    infoEmbed.add_field(name=f"`🕶️Nick`", value=uzytkownik.display_name)
    infoEmbed.add_field(name=f"`✨Stworzono`", value=uzytkownik.created_at.strftime("%b %d %Y"))
    infoEmbed.add_field(name=f"`📨Dołączono`", value=uzytkownik.joined_at.strftime("%b %d %Y"))
    infoEmbed.add_field(name=f"`👑Najwyższa Rola`", value=uzytkownik.top_role.mention)
    infoEmbed.set_footer(text=f"Komende użył {ctx.author.name}")
    infoEmbed.add_field(name=f"`🎭Ilość Roli`", value=str(len(uzytkownik.roles)-1))
    await ctx.send(embed=infoEmbed)


@client.slash_command(guild_ids=[SERWER_ID], description="Wyświetl informacje o serwerze 🧑‍💻", name="serwerinfo")
async def serwerinfo(interaction: Interaction):
    role_count = len(interaction.guild.roles)
    list_of_bots = [bot.mention for bot in interaction.guild.members if bot.bot]

    embed = nextcord.Embed(title=f"Informacje o Serwerze:",timestamp = interaction.created_at, colour=nextcord.Colour.dark_magenta())

    embed.add_field(name=f"`💼Nazwa`", value=interaction.guild.name)
    embed.add_field(name=f"`👥Użytkownicy`", value=interaction.guild.member_count)
    embed.add_field(name=f"`💍Poziom Weryfikacji`", value=str(interaction.guild.verification_level))
    embed.add_field(name=f"`👑Najwyższa Rola`", value=interaction.guild.roles[-2])
    embed.add_field(name=f"`🎭Ilość Roli`", value=str(role_count))
    embed.add_field(name=f"`🤖Boty`", value=', '.join(list_of_bots))
    embed.set_footer(text=f"Komende użył {interaction.user.name}")


    await interaction.response.send_message(embed=embed)


@client.command()
async def serwerinfo(ctx):
    role_count = len(ctx.guild.roles)
    list_of_bots = [bot.mention for bot in ctx.guild.members if bot.bot]

    serverinfoEmbed = nextcord.Embed(title=f"Informacje o Serwerze:",timestamp = ctx.message.created_at, colour=nextcord.Colour.dark_magenta())

    serverinfoEmbed.add_field(name=f"`💼Nazwa`", value=ctx.guild.name)
    serverinfoEmbed.add_field(name=f"`👥Użytkownicy`", value=ctx.guild.member_count)
    serverinfoEmbed.add_field(name=f"`💍Poziom Weryfikacji`", value=str(ctx.guild.verification_level))
    serverinfoEmbed.add_field(name=f"`👑Najwyższa Rola`", value=ctx.guild.roles[-2])
    serverinfoEmbed.add_field(name=f"`🎭Ilość Roli`", value=str(role_count))
    serverinfoEmbed.add_field(name=f"`🤖Boty`", value=', '.join(list_of_bots))
    embed.set_footer(text=f"Komende użył {ctx.author.name}")


    await ctx.send(embed=serverinfoEmbed)


@client.slash_command(guild_ids=[SERWER_ID], description="Wyrzuć użytkownika 📤", name="kick")
async def kick(interaction: Interaction, osoba: nextcord.Member, powód):
    embed=nextcord.Embed(timestamp = datetime.now(), color = nextcord.Colour.green())
    embed.add_field(name=f"» Pomyślnie wyrzucono {osoba.name} za {powód}!", value="Kick to nie ban - użytkownik może jeszcze wrócić na serwer", inline=False)
    await interaction.response.send_message(embed=embed)
    await osoba.kick(reason=powód)


@client.command()
@has_permissions(ban_members=True)
async def kick(ctx, member : nextcord.Member, reason="bez powodu"):
    embed=nextcord.Embed(timestamp = datetime.now(), color = nextcord.Colour.green())
    embed.add_field(name=f"» Pomyślnie wyrzucono {member.name} za {reason}!", value="Kick to nie ban - użytkownik może jeszcze wrócić na serwer", inline=False)
    await ctx.send(embed=embed)
    await member.kick(reason=reason)

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed=nextcord.Embed(title="<:nie:1020344672461262889> ERROR",description="Nie posiadasz permisji!",timestamp = datetime.now(), color = nextcord.Colour.red())
        await ctx.send(embed=embed)


@client.slash_command(guild_ids=[SERWER_ID], description="Wylosuj liczbę od 1 do 100 🍀", name="losuj")
async def losuj(interaction: Interaction):
    numer = random.randrange(0, 100)
    embed=nextcord.Embed(description=numer, color = nextcord.Colour.dark_teal())
    await interaction.response.send_message(embed=embed)


@client.command()
async def losuj(ctx):
    numer = random.randrange(0, 100)
    embed=nextcord.Embed(description=numer, color = nextcord.Colour.dark_teal())
    await ctx.send(embed=embed)


@client.slash_command(guild_ids=[SERWER_ID], description="Wylosuj liczbę do podanego zakresu 🔢", name="roll")
async def roll(interaction: Interaction, zakres: int):
    if(0 < zakres):
        numer = random.randrange(0, zakres)
        embed=nextcord.Embed(description=numer, color = nextcord.Colour.dark_teal())
        await interaction.response.send_message(embed=embed)
    else:
        embed=nextcord.Embed(description="Podano złe liczby!", color = nextcord.Colour.red())
        await interaction.response.send_message(embed=embed)
    

@client.command()
async def roll(ctx, max : int):
    if(0 < max):
        numer = random.randrange(0, max)
        embed=nextcord.Embed(description=numer, color = nextcord.Colour.dark_teal())
        await ctx.send(embed=embed)
    else:
        embed=nextcord.Embed(description="Podano złe liczby!", color = nextcord.Colour.red())
        await ctx.send(embed=embed)


@client.slash_command(guild_ids=[SERWER_ID], description="Przywitaj się z botem 👋", name="witaj")
async def witaj(interaction: Interaction):
    tablica = ["Cześć!", "Witaj!", "Siema!", "Siemanko!", "Elo!", "Siemano!", "Hej!"]
    embed=nextcord.Embed(description=random.choice(tablica), color = nextcord.Colour.dark_teal())
    await interaction.response.send_message(embed=embed)


@client.command()
async def witaj(ctx):
    tablica = ["Cześć!", "Witaj!", "Siema!", "Siemanko!", "Elo!", "Siemano!", "Hej!"]
    embed=nextcord.Embed(description=random.choice(tablica), color = nextcord.Colour.dark_teal())
    await ctx.send(embed=embed)



@client.event
async def on_message(message):
    slowa = ['kurwa', 'jebac', 'jebać', 'niger', 'nigger', 'ruchacz', 'ruchać', 'ruchac', 'cipa', 'cipka']
    for i in slowa:
        if i in message.content:
            await message.channel.send("» Nie pisz tak!", after_delete=2)
            await message.delete()

    await client.process_commands(message)




@client.event
async def on_message_delete(message):
    embed = nextcord.Embed(title=f":wastebasket: {message.author.name} usunął wiadomość! :wastebasket: | ID Użytkownika: {message.author.id}", description=f"{message.content}", timestamp = datetime.now(), color = nextcord.Colour.red())
    embed.add_field(name="Lokalizacja:", value=f"{message.channel.mention}", inline=False)
    embed.set_author(name = message.author, icon_url = message.author.display_avatar)
    channel = client.get_channel(797177705304424518)
    await channel.send(embed=embed)

@client.event
async def on_message_edit(message_before, message_after):
    embed = nextcord.Embed(title=f":pencil2: {message_before.author.name} edytował wiadomość! :pencil2: | ID Użytkownika: {message_before.author.id}", timestamp = datetime.now(), color = nextcord.Colour.red())
    embed.add_field(name="Przed:", value=f"{message_before.content}", inline=False)
    embed.add_field(name="Po:", value=f"{message_after.content}", inline=False)
    embed.add_field(name="Lokalizacja:", value=f"{message_before.channel.mention}", inline=False)
    embed.set_author(name = message_after.author, icon_url = message_after.author.display_avatar)
    channel = client.get_channel(797177705304424518)
    await channel.send(embed=embed)

@client.event
async def on_member_update(before, after):
    if len(before.roles) > len(after.roles):
        role = next(role for role in before.roles if role not in after.roles)
        embed = nextcord.Embed(title = f":outbox_tray:  Usunięta rola dla {before.name}! :outbox_tray:", description = f"{role.mention} została usunięta dla {before.mention}", timestamp = datetime.now(), color = nextcord.Colour.red())
    elif len(after.roles) > len(before.roles):
        role = next(role for role in after.roles if role not in before.roles)
        embed = nextcord.Embed(title = f":inbox_tray: Nowa rola dla {before.name}! :inbox_tray:", description = f"{role.mention} została dodana dla {before.mention}", timestamp = datetime.now(), color = nextcord.Colour.green())
    elif before.nick != after.nick:
        embed = nextcord.Embed(title = f"🎩 Pseudonim {before.name} został zmieniony!", timestamp = datetime.now(), color = nextcord.Colour.blue())
        embed.add_field(name="Stary pseudonim:", value=f"{before.nick}", inline=False)
        embed.add_field(name="Nowy pseudonim:", value=f"{after.nick}", inline=False)
    else:
        return
    embed.set_author(name = after, icon_url = after.display_avatar)
    channel = client.get_channel(797177705304424518)
    await channel.send(embed=embed)

@client.event
async def on_member_join(member):
    kanal = nextcord.utils.get(member.guild.channels, id=797177705304424518)
    embed=nextcord.Embed(title="🥳Nowy użytkownik🎉", timestamp = datetime.now(), color = nextcord.Colour.green())
    embed.add_field(name=f"Nowy użytkownik:", value=f"{member.name}", inline=False)
    await kanal.send(embed=embed)

@client.event
async def on_member_remove(member):
    kanal = nextcord.utils.get(member.guild.channels, id=797177705304424518)
    embed=nextcord.Embed(title=f"⛔Użytkowik wyszedł⛔", value=f"{member.name}", timestamp = datetime.now(), color = nextcord.Colour.yellow())
    await kanal.send(embed=embed)


@client.event
async def on_guild_channel_create(channel):
    kanal = client.get_channel(797177705304424518)
    embed = nextcord.Embed(title=f"🆕Nowy kanał!🆕", description = f"{channel.mention}", timestamp = datetime.now(), color = nextcord.Colour.green())
    await kanal.send(embed=embed)

@client.event
async def on_guild_channel_delete(channel):
    kanal = client.get_channel(797177705304424518)
    embed = nextcord.Embed(title=f"🧨Usunięty kanał!🧨", description = f"{channel}", timestamp = datetime.now(), color = nextcord.Colour.red())
    await kanal.send(embed=embed)


@client.slash_command(guild_ids=[795356386807775282], description="Stwórz system weryfikacji ✅", name="weryfikacja")
async def weryfikacja(interaction: Interaction):
    embed=nextcord.Embed(title="WERYFIKACJA", color=0x7740dd)
    embed.add_field(name="Zaznacz reakcję pod tą wiadomością,", value="aby się zweryfikować.", inline=False)
    msg = await interaction.response.send_message(embed=embed)
    await msg.add_reaction('✅')


@client.command()
async def weryfikacja(ctx):
    embed=nextcord.Embed(title="WERYFIKACJA", color=0x7740dd)
    embed.add_field(name="Zaznacz reakcję pod tą wiadomością,", value="aby się zweryfikować.", inline=False)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('✅')

@client.event
async def on_raw_reaction_add(payload):
    if payload.message_id == 1002617815976652800:
        if payload.emoji.name == '✅':
            guild = client.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            rola = nextcord.utils.get(guild.roles, id=909492534328324096)
            await member.add_roles(rola)

@client.event
async def on_raw_reaction_remove(payload):
    if payload.message_id == 1002617815976652800:
        if payload.emoji.name == '✅':
            guild = client.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            rola = nextcord.utils.get(guild.roles, id=909492534328324096)
            await member.remove_roles(rola)




@client.event
async def on_member_join(member):
    kanal = nextcord.utils.get(member.guild.channels, id=901449970547306506)
    rola = nextcord.utils.get(member.guild.roles, id=940571010640527370)
    embed=nextcord.Embed(title="🥳Nowy użytkownik🎉", timestamp = datetime.now(), color = nextcord.Colour.green())
    embed.add_field(name=f"Hej {member.name}, witaj na `Xajper Team`.", value="Zapoznaj się **regulaminem**. Baw się dobrze! 🙂", inline=False)
    await kanal.send(embed=embed)
    await member.add.roles(rola)

@client.event
async def on_member_remove(member):
    kanal = nextcord.utils.get(member.guild.channels, id=901449970547306506)
    embed=nextcord.Embed(title=f"{member.name} opuścił nasze grono, będziemy mieli o nim miłe wspomnienia :(", timestamp = datetime.now(), color = nextcord.Colour.yellow())
    embed.set_footer(text=f"Żegnaj {member.name}.")
    await kanal.send(embed=embed)


@client.event
async def on_messages(message):
    db = sqlite3.connect("levelsystem.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM info WHERE guild_id = {message.author.guild.id} AND user_id = {message.author.id}")
    wynik = cursor.fetchone()
    axp = random.randrange(1, 10)
    if wynik is None:
        cursor.execute("INSERT INTO info(guild_id, user_id, xp, lvl) VALUES(?, ?, ?, ?)", (message.author.guild.id, message.author.id, axp, 1))
    else:
        cursor.execute("UPDATE info SET xp = ? WHERE guild_id = ? AND user_id = ?", (wynik[2] + axp, message.author.guild.id, message.author.id))


    cursor.close()
    db.commit()
    db.close()


    await client.process_commands(message)



@client.command()
@has_permissions(manage_messages=True)
async def giveaway(ctx):
    await ctx.send("Zaczyna się giveaway! Odpowiedz na 3 pytania w ciągu 15 sekund!")

    questions = ["Na jakim kanale ma się odbyć giveaway?",
                "Ile ma trwać? (s|m|h|d)",
                "Jaka ma być nagroda?"]   

    answers = []

    def check (m):
        return m.author == ctx.author and m.channel == ctx.channel

    for i in questions:
        await ctx.send(i)

        try:
            msg = await client.wait_for('message', timeout = 15.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('Nie zdążyłeś odpowiedzieć na wszystkie pytania w ciągu 15 sekund! Proszę być szybszym następnym razem!')
            return
        else:
            answers.append(msg.content)

#  id
    try:
        c_id = int(answers[0][2:-1])
    except:
        await ctx.send(f"Nie wspomniałeś właściwie o kanale! Zrób to tak: {ctx.channel.mention}")
        return

    channel = client.get_channel(c_id)

    time = convert(answers[1])
    if time == -1:
        await ctx.send(f"Nie odpowiedziałeś na czas odpowiednią jednostką! Wykorzystaj: (s|m|h|d)")
        return
    elif time == -2:
        await ctx.send(f"Czas musi być liczbą całkowitą!")
        return

    prize = answers[2]

    await ctx.send(f"Giveaway rozpoczął się na: {channel.mention} i potrwa {answers[1]}!")


    embed = nextcord.Embed(title = "🎉 __Konkurs!__ 🎉", description = f"{prize}", color = nextcord.Colour.blue())

    embed.add_field(name = "Stworzony przez:", value = ctx.author.mention)

    embed.set_footer(text = f"Koniec za {answers[1]} od teraz!")

    
    message = await ctx.send(embed=embed)
    await message.add_reaction('🎉')


    await asyncio.sleep(time)

    
    new_msg = await channel.fetch_message(message.id)


    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))


    winner = random.choice(users)

    await channel.send(f"Gratulacje! {winner.mention} wygrałeś **{prize}**!")

@giveaway.error
async def giveaway_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed=nextcord.Embed(title="<:nie:1020344672461262889> ERROR",description="Nie posiadasz permisji!",timestamp = datetime.now(), color = nextcord.Colour.red())
        await ctx.send(embed=embed)

def convert (time):
    pos = ["s", "m", "h", "d"]

    time_dict = {"s" : 1, "m" : 60, "h" : 3600, "d": 86400}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2


    return val * time_dict[unit]



@client.slash_command(guild_ids=[SERWER_ID], description="Stwórz konkurs 🎉", name="gstart")
async def gstart(interaction: Interaction, czas, *, nagorda):

    embed = nextcord.Embed(title='🎉 __Konkurs!__ 🎉', description=f'`Nagroda`\n{nagorda}', color = nextcord.Colour.blue())
    embed.add_field(name = 'Stworzony przez:', value = interaction.user.mention)
    embed.set_footer(text=f'Giveaway skończy się za {czas}')
    gaw_msg = await interaction.response.send_message(embed = embed)

    await gaw_msg.add_reaction("🎉")
    await asyncio.sleep(int(czas))

    new_gaw_msg = await interaction.channel.fetch_message(gaw_msg.id)

    print(new_gaw_msg.reactions)
    users = await new_gaw_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await interaction.response.send_message(f"Gratulacje! {winner.mention} wygrałeś **{nagorda}**!")


@client.command()
async def gstart(ctx, time=None, *, prize=None):
    if time == None:
        await ctx.send('Odpowiedz na to pytanie!')
    elif prize == None:
        await ctx.send('Odpowiedz na to pytanie! Jaka ma być nagroda?')
    embed = nextcord.Embed(title='🎉 __Konkurs!__ 🎉', description=f'{prize}', color = nextcord.Colour.blue())
    embed.add_field(name = 'Stworzony przez:', value = ctx.author.mention)
    embed.set_footer(text=f'Giveaway skończy się za {time}')
    gaw_msg = await ctx.send(embed = embed)

    await gaw_msg.add_reaction("🎉")
    await asyncio.sleep(int(time))

    new_gaw_msg = await ctx.channel.fetch_message(gaw_msg.id)

    print(new_gaw_msg.reactions)
    users = await new_gaw_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await ctx.send(f"Gratulacje! {winner.mention} wygrałeś **{prize}**!")

@gstart.error
async def gstart_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed=nextcord.Embed(title="<:nie:1020344672461262889> ERROR",description="Nie posiadasz permisji!",timestamp = datetime.now(), color = nextcord.Colour.red())
        await ctx.send(embed=embed)



@client.slash_command(guild_ids=[SERWER_ID], description="Losowa ciekawostka 🔎", name="ciekawostka")
async def ciekawostka(interaction: Interaction):
    ciekawostka = ["W Chinach zakazane jest przytulanie drzew","Od 1945r. wszystkie brytyjskie czołgi są wyposażone w zestaw do patrzenia herbaty","2 dzień września to międzynarodowy dzień lodów o smaku borówki","Leonardo da Vinci potrafił malować jedną ręką i jednocześnie pisać drugą","Ziemia jest jedyną planetą w naszym układzie słonecznym, której nazwa nie pochodzi od imienia boga","W Singapurze zabronione jest rzucie gumy","Podczas oddychania jedno płuco wykorzystuje tylko 5% wdychanego tlenu","Dolar amerykański zawiera 25% lnu i 75% bawełny","Cienie na księżycu są ciemniejsze niż na Ziemi","3 najbogatsze rodziny na świecie mają w sumie więcej środków i zasobów niż 48 najbiedniejszych krajów łącznie","W trakcie oddychania żebra poruszają sie 5 milionów razy rocznie","Wieża Eiffela została w 1967 roku czasowo przeniesiona do Kanady","Tylko 15% powierzchni Sahary pokryte jest piaskiem"]

    embed=nextcord.Embed(title="🔎 Losowa Ciekawostka!", description=random.choice(ciekawostka), timestamp = datetime.now(), color = nextcord.Colour.blue())
    await interaction.response.send_message(embed=embed)


@client.command()
async def ciekawostka(ctx):
    
    ciekawostka = ["W Chinach zakazane jest przytulanie drzew","Od 1945r. wszystkie brytyjskie czołgi są wyposażone w zestaw do patrzenia herbaty","2 dzień września to międzynarodowy dzień lodów o smaku borówki","Leonardo da Vinci potrafił malować jedną ręką i jednocześnie pisać drugą","Ziemia jest jedyną planetą w naszym układzie słonecznym, której nazwa nie pochodzi od imienia boga","W Singapurze zabronione jest rzucie gumy","Podczas oddychania jedno płuco wykorzystuje tylko 5% wdychanego tlenu","Dolar amerykański zawiera 25% lnu i 75% bawełny","Cienie na księżycu są ciemniejsze niż na Ziemi","3 najbogatsze rodziny na świecie mają w sumie więcej środków i zasobów niż 48 najbiedniejszych krajów łącznie","W trakcie oddychania żebra poruszają sie 5 milionów razy rocznie","Wieża Eiffela została w 1967 roku czasowo przeniesiona do Kanady","Tylko 15% powierzchni Sahary pokryte jest piaskiem"]

    embed=nextcord.Embed(title="🔎 Losowa Ciekawostka!", description=random.choice(ciekawostka), timestamp = datetime.now(), color = nextcord.Colour.blue())
    await ctx.send(embed=embed)






@client.slash_command(guild_ids=[SERWER_ID], description="Zagraj z botem w kamień, papier, nożyce 🪨🧻✂️", name="kpn")
async def kpn(interaction: Interaction, wybór, *,arg:str='None'):
    wybory = ['kamień','papier','nożyce']
    wyborbota = random.choice(wybory)
    wybór = wybór.lower()

    if wyborbota == wybór:
        embed=nextcord.Embed(title="🪄 Remis!", description=f"Twój Wybór: **{wybór}**\nWybór Bota: **{wyborbota}**", timestamp = datetime.now(), color = nextcord.Colour.blue())
        await interaction.send(embed=embed)
    elif wyborbota == 'kamień' and wybór == 'papier':
        embed=nextcord.Embed(title="🥇 Wygrałeś!", description=f"Twój Wybór: **{wybór}**\nWybór Bota: **{wyborbota}**", timestamp = datetime.now(), color = nextcord.Colour.green())
        await interaction.send(embed=embed)
    elif wyborbota == 'kamień' and wybór == 'nożyce':
        embed=nextcord.Embed(title="❌ Przegrałeś!", description=f"Twój Wybór: **{wybór}**\nWybór Bota: **{wyborbota}**", timestamp = datetime.now(), color = nextcord.Colour.red())
        await interaction.send(embed=embed)
    elif wyborbota == 'papier' and wybór == 'kamień':
        embed=nextcord.Embed(title="❌ Przegrałeś!", description=f"Twój Wybór: **{wybór}**\nWybór Bota: **{wyborbota}**", timestamp = datetime.now(), color = nextcord.Colour.red())
        await interaction.send(embed=embed)
    elif wyborbota == 'papier' and wybór == 'nożyce':
        embed=nextcord.Embed(title="🥇 Wygrałeś!", description=f"Twój Wybór: **{wybór}**\nWybór Bota: **{wyborbota}**", timestamp = datetime.now(), color = nextcord.Colour.green())
        await interaction.send(embed=embed)
    elif wyborbota == 'nożyce' and wybór == 'papier':
        embed=nextcord.Embed(title="❌ Przegrałeś!", description=f"Twój Wybór: **{wybór}**\nWybór Bota: **{wyborbota}**", timestamp = datetime.now(), color = nextcord.Colour.red())
        await interaction.send(embed=embed)
    elif wyborbota == 'nożyce' and wybór == 'kamień':
        embed=nextcord.Embed(title="🥇 Wygrałeś!", description=f"Twój Wybór: **{wybór}**\nWybór Bota: **{wyborbota}**", timestamp = datetime.now(), color = nextcord.Colour.green())
        await interaction.send(embed=embed)
    else:
        embed=nextcord.Embed(title="❌ Błąd!", description=f"Przepraszam, ale pojawił się problem podczas uruchamiania polecenia! Upewnij się, że wybrałeś jedną z poniższych opcji.\n**{wybory[0]}**, **{wybory[1]}** lub **{wybory[2]}**", timestamp = datetime.now(), color = nextcord.Colour.red())
        await interaction.send(embed=embed)

@client.command()
async def kpn(ctx, user_choice, *,arg:str='None'):
    wybory = ['kamień','papier','nożyce']
    wyborbota = random.choice(wybory)
    user_choice = user_choice.lower()

    if wyborbota == user_choice:
        embed=nextcord.Embed(title="🪄 Remis!", description=f"Twój Wybór: **{user_choice}**\nWybór Bota: **{wyborbota}**", timestamp = datetime.now(), color = nextcord.Colour.blue())
        await ctx.send(embed=embed)
    elif wyborbota == 'kamień' and user_choice == 'papier':
        embed=nextcord.Embed(title="🥇 Wygrałeś!", description=f"Twój Wybór: **{user_choice}**\nWybór Bota: **{wyborbota}**", timestamp = datetime.now(), color = nextcord.Colour.green())
        await ctx.send(embed=embed)
    elif wyborbota == 'kamień' and user_choice == 'nożyce':
        embed=nextcord.Embed(title="❌ Przegrałeś!", description=f"Twój Wybór: **{user_choice}**\nWybór Bota: **{wyborbota}**", timestamp = datetime.now(), color = nextcord.Colour.red())
        await ctx.send(embed=embed)
    elif wyborbota == 'papier' and user_choice == 'kamień':
        embed=nextcord.Embed(title="❌ Przegrałeś!", description=f"Twój Wybór: **{user_choice}**\nWybór Bota: **{wyborbota}**", timestamp = datetime.now(), color = nextcord.Colour.red())
        await ctx.send(embed=embed)
    elif wyborbota == 'papier' and user_choice == 'nożyce':
        embed=nextcord.Embed(title="🥇 Wygrałeś!", description=f"Twój Wybór: **{user_choice}**\nWybór Bota: **{wyborbota}**", timestamp = datetime.now(), color = nextcord.Colour.green())
        await ctx.send(embed=embed)
    elif wyborbota == 'nożyce' and user_choice == 'papier':
        embed=nextcord.Embed(title="❌ Przegrałeś!", description=f"Twój Wybór: **{user_choice}**\nWybór Bota: **{wyborbota}**", timestamp = datetime.now(), color = nextcord.Colour.red())
        await ctx.send(embed=embed)
    elif wyborbota == 'nożyce' and user_choice == 'kamień':
        embed=nextcord.Embed(title="🥇 Wygrałeś!", description=f"Twój Wybór: **{user_choice}**\nWybór Bota: **{wyborbota}**", timestamp = datetime.now(), color = nextcord.Colour.green())
        await ctx.send(embed=embed)
    else:
        embed=nextcord.Embed(title="❌ Błąd!", description=f"Przepraszam, ale pojawił się problem podczas uruchamiania polecenia! Upewnij się, że wybrałeś jedną z poniższych opcji.\n**{wybory[0]}**, **{wybory[1]}** lub **{wybory[2]}**", timestamp = datetime.now(), color = nextcord.Colour.red())
        await ctx.send(embed=embed)


@kpn.error
async def kpn_error(ctx, error):
    wybory = ['kamień','papier','nożyce']
    if isinstance(error, commands.MissingRequireArgument):
        embed=nextcord.Embed(title="❌ Błąd!", description=f"Przepraszam, ale pojawił się problem podczas uruchamiania polecenia! Upewnij się, że wybrałeś jedną z poniższych opcji.\n**{wybory[0]}**, **{wybory[1]}** lub **{wybory[2]}**", timestamp = datetime.now(), color = nextcord.Colour.red())
        await ctx.send(embed=embed)




player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []


winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]    



@client.slash_command(guild_ids=[SERWER_ID], description="Kółko i krzyżyk ⭕❌", name="ox")
async def ox(interaction: Interaction, gracz1 : nextcord.Member, gracz2 : nextcord.Member):
    global player1
    global player2
    global turn
    global gameOver
    global count

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                ":white_large_square:", ":white_large_square:", ":white_large_square:",
                ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = gracz1
        player2 = gracz2

        # print th board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await interaction.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            embed = nextcord.Embed(title=f"Kolej {player1.name}!", color = nextcord.Colour.green())
            await interaction.send(embed=embed)
        elif num == 2:
            turn = player2
            embed = nextcord.Embed(title=f"Kolej {player2.name}!", color = nextcord.Colour.green())
            await interaction.send(embed=embed)
    else:
        embed = nextcord.Embed(title='Gra już trwa! Zakończ ją przed rozpoczęciem nowej!', color = nextcord.Colour.yellow())
        await interaction.send(embed=embed)


@client.slash_command(guild_ids=[SERWER_ID], description="Kółko i krzyżyk ⭕❌ | Wybór postawienia kółka/krzyżyka", name="miejsce")
async def miejsce(interaction: Interaction, pozycja : int):
    global turn
    global player1
    global player2
    global board
    global count

    if not gameOver:
        mark = ""
        if turn == interaction.user:
            if turn == player1:
                mark = ":x:"
            elif turn == player2:
                mark = ":o:"
            if 0 < pozycja < 10 and board [pozycja -1] == ":white_large_square:":
                board[pozycja - 1] = mark
                count += 1

                # print board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await interaction.send(line)
                        line = ""
                    else:
                        line += " " + board[x]
                
                checkWinner(winningConditions, mark)
                if gameOver:
                    embed = nextcord.Embed(title=mark + " **wygrywa!**", color = nextcord.Colour.green())
                    await interaction.send(embed=embed)
                elif count >= 9:
                    embed = nextcord.Embed(title="**Remis!**", color = nextcord.Colour.yellow())
                    await interaction.send(embed=embed)

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1



            else:
                embed = nextcord.Embed(title="<:nie:1020344672461262889> | Pamiętaj, aby wybrać liczbę całkowitą od 1 do 9 (włącznie) oraz nieoznaczoną płytkę", color = nextcord.Colour.red())
                await interaction.send(embed=embed)
        else:
            embed = nextcord.Embed(title="<:nie:1020344672461262889> | Poczekaj na swoją kolej!", color = nextcord.Colour.red())
            await interaction.send(embed=embed)
    else:
        embed = nextcord.Embed(title="Rozpocznij nową grę za pomocą komendy `/ox`!", color = nextcord.Colour.green())
        await interaction.send(embed=embed)


@client.command()
async def ox(ctx, p1 : nextcord.Member, p2 : nextcord.Member):
    global player1
    global player2
    global turn
    global gameOver
    global count

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",":white_large_square:", ":white_large_square:", ":white_large_square:",":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print th board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            embed = nextcord.Embed(title=f"Kolej {player1.name}!", color = nextcord.Colour.green())
            await ctx.send(embed=embed)
        elif num == 2:
            turn = player2
            embed = nextcord.Embed(title=f"Kolej {player2.name}!", color = nextcord.Colour.green())
            await ctx.send(embed=embed)
    else:
        embed = nextcord.Embed(title='<:nie:1020344672461262889> | Gra już trwa! Zakończ ją przed rozpoczęciem nowej!', color = nextcord.Colour.yellow())
        await ctx.send(embed=embed)

    
@client.command()
async def miejsce(ctx, pos : int):
    global turn
    global player1
    global player2
    global board
    global count

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":x:"
            elif turn == player2:
                mark = ":o:"
            if 0 < pos < 10 and board [pos -1] == ":white_large_square:":
                board[pos - 1] = mark
                count += 1

                # print board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]
                
                checkWinner(winningConditions, mark)
                if gameOver:
                    embed = nextcord.Embed(title=mark + " **wygrywa!**", color = nextcord.Colour.green())
                    await ctx.send(embed=embed)
                elif count >= 9:
                    embed = nextcord.Embed(title="**Remis!**", color = nextcord.Colour.yellow())
                    await ctx.send(embed=embed)

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1



            else:
                embed = nextcord.Embed(title="Pamiętaj, aby wybrać liczbę całkowitą od 1 do 9 (włącznie) oraz nieoznaczoną płytkę", color = nextcord.Colour.red())
                await ctx.send(embed=embed)
        else:
            embed = nextcord.Embed(title="Poczekaj na swoją kolej!", color = nextcord.Colour.red())
            await ctx.send(embed=embed)
    else:
        embed = nextcord.Embed(title="Rozpocznij nową grę za pomocą komendy `/ox`!", color = nextcord.Colour.green())
        await ctx.send(embed=embed)


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver= True

@ox.error
async def ox_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = nextcord.Embed(title="Proszę wspomnieć o `2` graczach dla tego polecenia!", color = nextcord.Colour.red())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BadArgument):
        embed = nextcord.Embed(title="Pamiętaj, aby wspomnieć/pingować graczy (np. <@999288244476850236>).", color = nextcord.Colour.red())
        await ctx.send(embed=embed)


@miejsce.error
async def miejsce_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = nextcord.Embed(title="Podaj pozycję, którą chcesz oznaczyć!", color = nextcord.Colour.red())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BadArgument):
        embed = nextcord.Embed(title="Upewnij się, że wpiszesz liczbę całkowitą!", color = nextcord.Colour.red())
        await ctx.send(embed=embed)


@client.slash_command(guild_ids=[SERWER_ID], description="List gończy 📰", name="wanted")
async def wanted(interaction: Interaction, osoba: nextcord.Member):
    if osoba == None:
        osoba = interaction.user
 
    wanted = Image.open(".\\assets\\wanted.png")

    data = BytesIO(await osoba.display_avatar.read())
    pfp = Image.open(data)

    pfp = pfp.resize((300, 300))

    wanted.paste(pfp, (100, 200))

    wanted.save(".\\assets\\profile.png")

    await interaction.send(file=nextcord.File(".\\assets\\profile.png"))


@client.command()
async def wanted(ctx, user: nextcord.User = None):
    if user == None:
        user = ctx.author
 
    wanted = Image.open(".\\assets\\wanted.png")

    data = BytesIO(await user.display_avatar.read())
    pfp = Image.open(data)

    pfp = pfp.resize((300, 300))

    wanted.paste(pfp, (100, 200))

    wanted.save(".\\assets\\profile.png")

    await ctx.reply(file=nextcord.File(".\\assets\\profile.png"))

@client.slash_command(guild_ids=[SERWER_ID], description="Losowy polski mem 🤣", name="mem")
async def mem(interaction: Interaction):
    memy = ["https://media.discordapp.net/attachments/901377998471696416/1034898918695248032/unknown.png","https://media.discordapp.net/attachments/901377998471696416/1034898918280015912/unknown.png","https://media.discordapp.net/attachments/901377998471696416/1034898917785084064/unknown.png","https://media.discordapp.net/attachments/901377998471696416/1025657449400774656/unknown.png","https://media.discordapp.net/attachments/901377998471696416/1023487218590961754/4069065.jpg?width=452&height=581","https://media.discordapp.net/attachments/901377998471696416/1020760605633806487/unknown-235.png?width=558&height=581","https://media.discordapp.net/attachments/901377998471696416/1018039728509046874/xd.png?width=520&height=582","https://media.discordapp.net/attachments/901377998471696416/1017416006261559306/unknown.png","https://media.discordapp.net/attachments/901377998471696416/1006430426560200744/unknown-1-1.jpg?width=291&height=581","https://media.discordapp.net/attachments/901377998471696416/1006287415268352050/received_555751202306902.gif","https://media.discordapp.net/attachments/901377998471696416/994479270934085652/unknown.png","https://media.discordapp.net/attachments/901377998471696416/989524577547853825/unknown.png","https://media.discordapp.net/attachments/901377998471696416/986662020088733717/unknown.png","https://media.discordapp.net/attachments/901377998471696416/965538641667584040/unknown.png","https://media.discordapp.net/attachments/901377998471696416/959158534111625266/FB_IMG_16476738967777932.png","https://media.discordapp.net/attachments/901377998471696416/953373345309683832/IMG_20220315_202010.png?width=528&height=582","https://bi.im-g.pl/im/61/f1/19/z27202145Q,Memy-po-porazce-Polakow-ze-Slowakami-na-Euro-2020.jpg","https://i.pinimg.com/736x/79/2a/08/792a08abfc0153df4b34a5f9f539f8c0.jpg","https://img.besty.pl/images/404/72/4047205.jpg","https://media.discordapp.net/attachments/797833316551229460/1034926379961155624/6229d7c674097_o_large.jpg?width=529&height=581","https://media.discordapp.net/attachments/797833316551229460/1034361512619421736/unknown.png","https://media.discordapp.net/attachments/797833316551229460/1034345288686645299/unknown-80-1.png","https://media.discordapp.net/attachments/999660337370505226/1024399343073112106/received_539532414070813-1.jpg","https://bi.im-g.pl/im/24/ae/1b/z29024804Q,Smieszne-memy-o-tesciowej--10-zdjec--ktore-rozbawi.jpg","https://media.discordapp.net/attachments/797833316551229460/1036016082231754852/770646_dzieki-pomoglo.jpg?width=528&height=582","https://media.discordapp.net/attachments/797833316551229460/1039215844544221284/Screenshot_20221107_140352.jpg?width=378&height=582","https://media.discordapp.net/attachments/797833316551229460/1044148574587473970/830833_przyganial-kociol-garnkowi.jpg?width=364&height=581","https://media.discordapp.net/attachments/797833316551229460/1044220937991626762/1669026888216.jpg","https://media.discordapp.net/attachments/797833316551229460/1044148345108709386/Screenshot_2021-11-20-18-31-54-01.png","https://media.discordapp.net/attachments/797833316551229460/1044148487429832704/16687665957606558223903410924705.jpg","image.png","https://media.discordapp.net/attachments/797833316551229460/1043425877284888628/20221117_195331.jpg","https://media.discordapp.net/attachments/797833316551229460/1043425394445013003/895897_ulubiony-avenger-maszynisty-thor.jpg?width=481&height=581","https://media.discordapp.net/attachments/797833316551229460/1043204824453369876/Screenshot_20221118-142031_Instagram.jpg?width=466&height=581","https://media.discordapp.net/attachments/797833316551229460/1043054973459648542/faceci.jpg?width=630&height=581"]
    embed = nextcord.Embed(title="POLSKI MEM 🤣", colour=nextcord.Colour.orange())
    embed.set_image(url=random.choice(memy))
    await interaction.response.send_message(embed=embed)



@client.slash_command(guild_ids=[SERWER_ID], description="Losowy zagraniczny mem 🤣", name="meme")
async def meme(interaction: Interaction):
    memeApi = urllib.request.urlopen('https://meme-api.herokuapp.com/gimme')

    memeData = json.load(memeApi)

    memeUrl = memeData['url']
    memeName = memeData['title']
    memePoster = memeData['author']
    memeLink = memeData['postLink']


    embed = nextcord.Embed(title=memeName, colour=nextcord.Colour.orange())
    embed.set_image(url=memeUrl)
    embed.set_footer(text=f"Twórca: {memePoster} | Link: {memeLink}")
    await interaction.response.send_message(embed=embed)


@client.command()
async def meme(ctx):
    memeApi = urllib.request.urlopen('https://meme-api.herokuapp.com/gimme')

    memeData = json.load(memeApi)

    memeUrl = memeData['url']
    memeName = memeData['title']
    memePoster = memeData['author']
    memeLink = memeData['postLink']


    embed = nextcord.Embed(title=memeName, colour=nextcord.Colour.orange())
    embed.set_image(url=memeUrl)
    embed.set_footer(text=f"Twórca: {memePoster} | Link: {memeLink}")
    await ctx.send(embed=embed)


@client.slash_command(guild_ids=[SERWER_ID], description="💪 POLSKA GUROM 🔥", name="polskagurom")
async def polskagurom(interaction: Interaction):
    polskagurom = ["https://tenor.com/view/pudzian-polska-gurom-gif-22944047","https://tenor.com/view/polska-gurom-polska-gurom-pudzian-pudzianowski-gif-18323120"]
    embed = nextcord.Embed(title=":fire: POLSKA GUROM!!! :fire:", colour=nextcord.Colour.gold())
    embed.set_image(url=random.choice(polskagurom))
    await interaction.send(embed=embed)


@client.command()
async def polskagurom(ctx):
    polskagurom = ["https://tenor.com/view/pudzian-polska-gurom-gif-22944047","https://tenor.com/view/polska-gurom-polska-gurom-pudzian-pudzianowski-gif-18323120"]
    embed = nextcord.Embed(title=":fire: POLSKA GUROM!!! :fire:", colour=nextcord.Colour.gold())
    embed.set_image(url=random.choice(polskagurom))
    await ctx.send(embed=embed)


@client.slash_command(guild_ids=[SERWER_ID], description="Zdjęcie psa 🐶", name="pies")
async def pies(interaction: Interaction):
    gpies = ["https://tenor.com/view/dogs-cute-all-you-need-is-love-gif-13111410",
        "https://tenor.com/view/puppy-high-five-cute-fluffy-gif-10903022",
        "https://media.discordapp.net/attachments/730945069711884289/808982584280350730/image0.gif",
        "https://tenor.com/view/puppies-silly-puppy-cute-puppy-doggys-dogs-gif-17639683",
        "https://tenor.com/view/golden-retriever-dog-did-you-call-me-mirame-perrito-golden-gif-17047579",
        "https://tenor.com/view/bedtime-sleepy-good-night-sleep-well-go-to-bed-gif-15801983",
        "https://tenor.com/view/look-puppy-hi-hello-gif-5047026",
        "https://tenor.com/view/dog-getting-frustrated-stop-it-annoyed-gif-15192974"
        ]
    embed = nextcord.Embed(title="Piesek 🐶", colour=nextcord.Colour.green())
    embed.set_image(url=random.choice(gpies))
    await interaction.send(embed=embed)


@client.command()
async def pies(ctx):

    gpies = ["https://tenor.com/view/dogs-cute-all-you-need-is-love-gif-13111410",
        "https://tenor.com/view/puppy-high-five-cute-fluffy-gif-10903022",
        "https://media.discordapp.net/attachments/730945069711884289/808982584280350730/image0.gif",
        "https://tenor.com/view/puppies-silly-puppy-cute-puppy-doggys-dogs-gif-17639683",
        "https://tenor.com/view/golden-retriever-dog-did-you-call-me-mirame-perrito-golden-gif-17047579",
        "https://tenor.com/view/bedtime-sleepy-good-night-sleep-well-go-to-bed-gif-15801983",
        "https://tenor.com/view/look-puppy-hi-hello-gif-5047026",
        "https://tenor.com/view/dog-getting-frustrated-stop-it-annoyed-gif-15192974"
        ]
    embed = nextcord.Embed(title="Piesek 🐶", colour=nextcord.Colour.green())
    embed.set_image(url=random.choice(gpies))
    await ctx.send(embed=embed)


@client.slash_command(guild_ids=[SERWER_ID], description="Zdjęcie kota 😺", name="kot")
async def kot(interaction: Interaction):
    gkot = ["https://media.tenor.com/gVCgzpv0B7AAAAPo/cat-cute.gif",
        "https://media.tenor.com/ZhfMGWrmCTcAAAPo/cute-kitty-best-kitty.gif",
        "https://media.tenor.com/hLJJl7NjpN4AAAPo/jenminismo.gif",
        "https://media.tenor.com/K_75XqYil5MAAAPo/cat-kitten.gif",
        "https://media.tenor.com/XjnZVoMpvfoAAAPo/kawaii-cat.gif",
        "https://media.tenor.com/6ywDINZvw6oAAAPo/koopagode.gif",
        "https://media.tenor.com/eH-L7uAQ7ZUAAAPo/hello-hi.gif",
        "https://media.tenor.com/TcYTfeJkbmcAAAPo/%D0%BA%D0%BE%D1%82.gif"
        ]
    embed = nextcord.Embed(title="Kotek 🐈", colour=nextcord.Colour.green())
    embed.set_image(url=random.choice(gkot))
    await interaction.send(embed=embed)


@client.command()
async def kot(ctx):

    gkot = ["https://media.tenor.com/gVCgzpv0B7AAAAPo/cat-cute.gif",
        "https://media.tenor.com/ZhfMGWrmCTcAAAPo/cute-kitty-best-kitty.gif",
        "https://media.tenor.com/hLJJl7NjpN4AAAPo/jenminismo.gif",
        "https://media.tenor.com/K_75XqYil5MAAAPo/cat-kitten.gif",
        "https://media.tenor.com/XjnZVoMpvfoAAAPo/kawaii-cat.gif",
        "https://media.tenor.com/6ywDINZvw6oAAAPo/koopagode.gif",
        "https://media.tenor.com/eH-L7uAQ7ZUAAAPo/hello-hi.gif",
        "https://media.tenor.com/TcYTfeJkbmcAAAPo/%D0%BA%D0%BE%D1%82.gif"
        ]
    embed = nextcord.Embed(title="Kotek 🐈", colour=nextcord.Colour.green())
    embed.set_image(url=random.choice(gkot))
    await ctx.channel.send(embed=embed)


@client.slash_command(guild_ids=[SERWER_ID], description="Xajper - Kanał youtube 🎥", name="xajper")
async def xajper(interaction: Interaction):
    embed = nextcord.Embed(title="Mój Kanał", colour=nextcord.Colour.og_blurple())
    embed.description = "Xajper jest yotuberem, chcesz zobaczyć kanał? Kliknij [tutaj](https://www.youtube.com/channel/UCC5Ssx_Py9yYkEpApx6Piug)."
    await interaction.send(embed=embed, delete_after=10)


@client.command()
async def xajper(ctx):
    embed = nextcord.Embed(title="Mój Kanał", colour=nextcord.Colour.og_blurple())
    embed.description = "Xajper jest yotuberem, chcesz zobaczyć kanał? Kliknij [tutaj](https://www.youtube.com/channel/UCC5Ssx_Py9yYkEpApx6Piug)."
    await ctx.send(embed=embed, delete_after=10)


@client.slash_command(guild_ids=[SERWER_ID], description="Rzut kostką 🎲", name="kostka")
async def kostka(interaction: Interaction):
    tablica = ["`1`!", "`2`!", "`3`!", "`4`!", "`5`!", "`6`!"]
    embed = nextcord.Embed(title="🎲 | Rzuciłeś kostką i wylosowałeś... " + random.choice(tablica), colour=nextcord.Colour.green())
    await interaction.send(embed=embed)

@client.command()
async def kostka(ctx):
    tablica = ["`1`!", "`2`!", "`3`!", "`4`!", "`5`!", "`6`!"]
    embed = nextcord.Embed(title="🎲 | Rzuciłeś kostką i wylosowałeś... " + random.choice(tablica), colour=nextcord.Colour.green())
    await ctx.send(embed=embed)


@client.slash_command(guild_ids=[SERWER_ID], description="Sprawdź ile masz IQ 🧠", name="iq")
async def iq(interaction: Interaction):
    tablica = ["0!","1!", "2!", "3!", "4!", "5!", "6!","7!","8!","9!","10!","11!","12!","13!","14!","15!","16!","17!","18!","19!","20!","21!","22!","23!","24!","25!","26!","27!","28!","29!","30!","31!","32!","33!","34!","35!","36!","37!","38!","39!","40!","41!","42!","43!","44!","45!","46!","47!","48!","49!","50!","51!","52!","53!","54!","55!","56!","57!","58!","59!","60!","61!","62!","63!","64!","65!","65!","66!","67!","68!","69!","70!","71!","72!","73!","74!","75!","76!","77!","78!","79!","80!","81!","82!","83!","84!","85!","86!","87!","88!","89!","90!","91!","92!","93!","94!","95!","96!","97!","98!","99!",":exclamation: 100 :exclamation:",]
    embed = nextcord.Embed(title="🧠 | Twoje IQ wynosi " + random.choice(tablica), colour=nextcord.Colour.green())
    await interaction.send(embed=embed)

@client.command()
async def iq(ctx):
    tablica = ["0!","1!", "2!", "3!", "4!", "5!", "6!","7!","8!","9!","10!","11!","12!","13!","14!","15!","16!","17!","18!","19!","20!","21!","22!","23!","24!","25!","26!","27!","28!","29!","30!","31!","32!","33!","34!","35!","36!","37!","38!","39!","40!","41!","42!","43!","44!","45!","46!","47!","48!","49!","50!","51!","52!","53!","54!","55!","56!","57!","58!","59!","60!","61!","62!","63!","64!","65!","65!","66!","67!","68!","69!","70!","71!","72!","73!","74!","75!","76!","77!","78!","79!","80!","81!","82!","83!","84!","85!","86!","87!","88!","89!","90!","91!","92!","93!","94!","95!","96!","97!","98!","99!",":exclamation: 100 :exclamation:",]
    embed = nextcord.Embed(title="🧠 | Twoje IQ wynosi " + random.choice(tablica), colour=nextcord.Colour.green())
    await ctx.send(embed=embed)


@client.slash_command(guild_ids=[SERWER_ID], description="Rzut monetą 🪙", name="moneta")
async def moneta(interaction: Interaction):
    tablica = ["`orła`!", "`reszke`!"]
    embed = nextcord.Embed(title="🪙 | Rzuciłeś monetą i wylosowałeś... " + random.choice(tablica), colour=nextcord.Colour.green())
    await interaction.send(embed=embed)

@client.command()
async def moneta(ctx):
    tablica = ["`orła`!", "`reszke`!"]
    embed = nextcord.Embed(title="🪙 | Rzuciłeś monetą i wylosowałeś... " + random.choice(tablica), colour=nextcord.Colour.green())
    await ctx.send(embed=embed)



@client.slash_command(guild_ids=[SERWER_ID], description="Informacje o XajperBOT 🤖", name="botinfo")
async def botinfo(interaction: Interaction):
    botembed = nextcord.Embed(title=f"Informacje o XajperBOT",description="`•` Bot Autorstwa Xajper `•`",timestamp = interaction.created_at, colour=nextcord.Colour.og_blurple())
    botembed.add_field(name=f"`💼Nazwa`", value="XajperBOT")
    botembed.add_field(name=f"`🪧ID`", value=999288244476850236)
    botembed.add_field(name=f"`🌻Stworzono`", value="2022-07-20")
    botembed.set_footer(text=f"Komende użył {interaction.user.name}")
    await interaction.send(embed=botembed)
    
@client.command()
async def botinfo(ctx):
    botembed = nextcord.Embed(title=f"Informacje o XajperBOT",description="`•` Bot Autorstwa Xajper `•`",timestamp = ctx.message.created_at, colour=nextcord.Colour.og_blurple())
    botembed.add_field(name=f"`💼Nazwa`", value="XajperBOT")
    botembed.add_field(name=f"`🪧ID`", value=999288244476850236)
    botembed.add_field(name=f"`🌻Stworzono`", value="2022-07-20")
    botembed.set_footer(text=f"Komende użył {ctx.author.name}")
    await ctx.send(embed=botembed)


@client.slash_command(guild_ids=[SERWER_ID], description="Losowy żart 😂", name="żart")
async def żart(interaction: Interaction):
    zart1 = ["__Jasiu mówi do taty__: Tato, tato, mam dwie jedynki dwie dwójki dwie trójki chyba cztery czwórki i piątki.\n__Tata się pyta__: Tak a skąd?\n__A Jasiu na to__: Jedynki dwójki i trójki z przodu a czwórki i piątki po bokach.","Jak się czuje ogórek w towarzystwie śmietany?\nMizernie.","Pani pyta się Jasia: Ile masz lat ? Niewiem. Ile jest gwiazd na niebie? Niewiem. Czym twoja babcia sprząta kuże? Niewiem. Czym twój dziadek wojował na wojnie? Niewiem. Jasiu wraca do domu i pyta się mamy: Ile mam lat? 9. Ile jest gwiazd na niebie? Tego jeszcze nie obliczono. Czym moja babcia sprząta kuże? Miotełką do kużu. Czym mój dziadek wojował na wojnie? Karabinem maszynowym. Następnego dnia pani się pyta Jasia: Ile masz lat ? Tego jeszcze nie obliczono. Ile jest gwiazd na niebie? 9. Czym twoja babcia sprząta kuże? Karabinem maszynowym. Czym twój dziadek wojował na wojnie? Miotełką do kużu.","__Pacjent__: Panie doktorze, codziennie o piatej rano oddaje mocz.\n__Lekarz__: W zasadzie to bardzo dobrze, w czym problem?\n__Pacjent__: Bo ja budze sie o siódmej.","__Nauczycielka__: Krzysiu czemu wczoraj nie byłeś w szkole?\n__Krzysiu__: Bo wczoraj umarł mój dziadek\n__Nauczycielka__: Nie kłam Krzysiu, przecież wczoraj widziałam twojego dziadka w oknie\n__Krzysiu__: Nie kłamię! Tatuś wystawił go wczoraj przy oknie, bo szedł listonosz z rentą!"]


    embed = nextcord.Embed(title=f"`Żart`",timestamp = interaction.created_at, colour=nextcord.Colour.gold())
    embed.add_field(name=random.choice(zart1), value="🤣")
    embed.set_footer(text=f"Komende użył {interaction.user.name}")
    await interaction.send(embed=embed)

@client.command()
async def zart(ctx):    

    zart1 = ["__Jasiu mówi do taty__: Tato, tato, mam dwie jedynki dwie dwójki dwie trójki chyba cztery czwórki i piątki.\n__Tata się pyta__: Tak a skąd?\n__A Jasiu na to__: Jedynki dwójki i trójki z przodu a czwórki i piątki po bokach.","Jak się czuje ogórek w towarzystwie śmietany?\nMizernie.","Pani pyta się Jasia: Ile masz lat ? Niewiem. Ile jest gwiazd na niebie? Niewiem. Czym twoja babcia sprząta kuże? Niewiem. Czym twój dziadek wojował na wojnie? Niewiem. Jasiu wraca do domu i pyta się mamy: Ile mam lat? 9. Ile jest gwiazd na niebie? Tego jeszcze nie obliczono. Czym moja babcia sprząta kuże? Miotełką do kużu. Czym mój dziadek wojował na wojnie? Karabinem maszynowym. Następnego dnia pani się pyta Jasia: Ile masz lat ? Tego jeszcze nie obliczono. Ile jest gwiazd na niebie? 9. Czym twoja babcia sprząta kuże? Karabinem maszynowym. Czym twój dziadek wojował na wojnie? Miotełką do kużu.","__Pacjent__: Panie doktorze, codziennie o piatej rano oddaje mocz.\n__Lekarz__: W zasadzie to bardzo dobrze, w czym problem?\n__Pacjent__: Bo ja budze sie o siódmej.","__Nauczycielka__: Krzysiu czemu wczoraj nie byłeś w szkole?\n__Krzysiu__: Bo wczoraj umarł mój dziadek\n__Nauczycielka__: Nie kłam Krzysiu, przecież wczoraj widziałam twojego dziadka w oknie\n__Krzysiu__: Nie kłamię! Tatuś wystawił go wczoraj przy oknie, bo szedł listonosz z rentą!"]


    embed = nextcord.Embed(title=f"`Żart`",timestamp = ctx.message.created_at, colour=nextcord.Colour.gold())
    embed.add_field(name=random.choice(zart1), value="🤣")
    embed.set_footer(text=f"Komende użył {ctx.author.name}")
    await ctx.send(embed=embed)



class CreateTicket(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="Stwórz Ticket",style=nextcord.ButtonStyle.blurple,emoji="📨", custom_id="createticket:blurple")
    async def create_ticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        msg = await interaction.response.send_message("Ticket został stworzony", ephemeral=True)

        overwrites = {
            interaction.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            interaction.guild.me: nextcord.PermissionOverwrite(read_messages=True, view_channel=True),
            interaction.user: nextcord.PermissionOverwrite(read_messages=True, view_channel=True),
            interaction.guild.get_role(1026173495794729030): nextcord.PermissionOverwrite(read_messages=True, view_channel=True)
        }


        channel = await interaction.guild.create_text_channel(f"🎫{interaction.user.name}-ticket🎫",
        overwrites=overwrites)

        await msg.edit(f"Kanał został pomyślnie stworzony | {channel.mention}")
        embed = nextcord.Embed(title=f"Tiket został stworzony!", description=f"{interaction.user.mention} stworzył ticket! Kliknij jeden z poniższych przycisków, aby zmienić ustawienia.", colour=nextcord.Colour.gold())
        await channel.send(embed=embed, view=TicketSettings())

            

class TicketSettings(nextcord.ui.View):  
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="Zamknij Ticket",style=nextcord.ButtonStyle.red,emoji="🔐", custom_id="ticket_settings:red")
    async def close_ticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("**🎫 | Ticket został zamknięty pomyśłnie!**", ephemeral=True)
        await interaction.channel.delete()
        await interaction.user.send(f"**🎫 | Ticket został zamknięty pomyśłnie!**")

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.persistent_views_added = False

    async def on_ready(self):
        if not self.persistent_views_added:
            self.add_view(CreateTicket())
            self.persistent_views_added = True
        
        print("System Ticketów - Gotowy")



@client.command()
@commands.has_permissions(manage_guild=True)
async def ticket(ctx: commands.Context):
    embed = nextcord.Embed(title="Potrzebujesz pomocy?", description="Kliknij reakcje pod tą wiadomością, aby ją uzyskać. Administracja serwera niedługo się do ciebie odezwie, czekaj cierpliwie!", colour=nextcord.Colour.blue())
    await ctx.send(embed=embed, view=CreateTicket())

@ticket.error
async def ticket_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed=nextcord.Embed(title="<:nie:1020344672461262889> ERROR",description="Nie posiadasz permisji!",timestamp = datetime.now(), color = nextcord.Colour.red())
        await ctx.send(embed=embed)


@client.slash_command(guild_ids=[SERWER_ID], description="System ticketów 🎫", name="ticket")
async def ticket(interaction: Interaction):
    embed = nextcord.Embed(title="Potrzebujesz pomocy?", description="Kliknij reakcje pod tą wiadomością, aby ją uzyskać. Administracja serwera niedługo się do ciebie odezwie, czekaj cierpliwie!", colour=nextcord.Colour.blue())
    await interaction.response.send_message(embed=embed, view=CreateTicket())
    



@client.slash_command(guild_ids=[SERWER_ID], description="Stwórz ankietę 📊", name="ankieta")
async def ankieta(interaction: Interaction, wybór1, wybór2, *, tytuł):

        embed=nextcord.Embed(title="**📊 | Ankieta**", timestamp = interaction.created_at, color=interaction.user.color)
        embed.add_field(name=f"> Pytanie od __{interaction.user.name}__: 📝\n", value=tytuł, inline=False)
        embed.add_field(name=f"➡️ {wybór1}", value="*Kliknij `👍`*", inline=True)
        embed.add_field(name=f"➡️ {wybór2}", value="*Kliknij `👎`*", inline=True)
        
        message = await interaction.send(embed = embed)
        await message.add_reaction("👍")
        await message.add_reaction("👎")


@client.slash_command(guild_ids=[SERWER_ID], description="Stwórz propozycję 📃", name="propozycja")
async def propozycja(interaction: Interaction, propozycja):
        embed = nextcord.Embed(title = f"📃 | Propozycja __{interaction.user.id}__:\n", description = f"{propozycja}\n",timestamp = interaction.created_at, color=interaction.user.colour)
        
        message = await interaction.send(embed = embed)
        await message.add_reaction("<:tak:1020344650260807700>")
        await message.add_reaction("<:neutralny:1020344687959224330>")
        await message.add_reaction("<:nie:1020344672461262889>")
        
        await interaction.response.send_message(embed=embed)



class Dropdown(nextcord.ui.Select):
    def __init__(self):

        options = [
            nextcord.SelectOption(
                label="Napastnicy", emoji="⚽"
            ),
            nextcord.SelectOption(
                label="Pomocnicy", emoji="🎯"
            ),
            nextcord.SelectOption(
                label="Obrońcy", emoji="🛡️"
            ),
            nextcord.SelectOption(
                label="Bramkarze", emoji="🥅"
            ),
        ]


        super().__init__(
            placeholder="Wybierz grupę 🗂️",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: nextcord.Interaction):

        if self.values[0] == "Napastnicy":
            await interaction.channel.purge(limit=1)
    
            button = Button(style=nextcord.ButtonStyle.blurple, emoji="➡️")
            button1 = Button(style=nextcord.ButtonStyle.blurple, emoji="➡️")
            button2 = Button(style=nextcord.ButtonStyle.blurple, emoji="➡️")
            button3 = Button(style=nextcord.ButtonStyle.blurple, emoji="➡️")
            button4 = Button(style=nextcord.ButtonStyle.blurple, emoji="➡️")

            async def button_callback(interaction):
                await interaction.channel.purge(limit=1)
                embed = nextcord.Embed(title=":flag_pl: Arkadiusz Milik", colour=nextcord.Colour.greyple())
                embed.add_field(name="`Pozycja`", value="Napastnik ⚽")
                embed.set_image(url="https://sport.wprost.pl/_thumb/a1/cf/0ae362b1f114a32f7dec164922ae.jpeg")
                await interaction.response.send_message(embed=embed, view=view1)

            button.callback = button_callback

            async def button1_callback(interaction):
                await interaction.channel.purge(limit=1)
                embed = nextcord.Embed(title=":flag_pl: Karol Świderski", colour=nextcord.Colour.greyple())
                embed.add_field(name="`Pozycja`", value="Napastnik ⚽")
                embed.set_image(url="https://transfery.info/img/photos/84046/1500xauto/karol-swiderski.jpg")
                await interaction.response.send_message(embed=embed, view=view2)

            button1.callback = button1_callback

            async def button2_callback(interaction):
                await interaction.channel.purge(limit=1)
                embed = nextcord.Embed(title=":flag_pl: Krzysztof Piątek", colour=nextcord.Colour.greyple())
                embed.add_field(name="`Pozycja`", value="Napastnik ⚽")
                embed.set_image(url="https://img.wprost.pl/_thumb/b9/52/a4c7661c42eb061bb0edaxxe3ffd.jpeg")
                await interaction.response.send_message(embed=embed, view=view3)

            button2.callback = button2_callback

            async def button3_callback(interaction):
                await interaction.channel.purge(limit=1)
                embed = nextcord.Embed(title=":flag_pl: Adam Buksa", colour=nextcord.Colour.greyple())
                embed.add_field(name="`Pozycja`", value="Napastnik ⚽")
                embed.set_image(url="https://img.wprost.pl/img/adam-buksa/5d/62/98b23fe1df10d7b06d7f6c9f7de5.jpeg")
                await interaction.response.send_message(embed=embed, view=view4)

            button3.callback = button3_callback

            async def button4_callback(interaction):
                await interaction.channel.purge(limit=1)
                embed = nextcord.Embed(title=":flag_pl: Dawid Kownacki", colour=nextcord.Colour.greyple())
                embed.add_field(name="`Pozycja`", value="Napastnik ⚽")
                embed.set_image(url="https://bi.im-g.pl/im/09/1f/19/z26343177Q,Dawid-Kownacki-strzelil-pierwszego-gola-dla-Fortun.jpg")
                await interaction.response.send_message(embed=embed)

            button4.callback = button4_callback


            view = View(timeout=120)
            view1 = View(timeout=120)
            view2 = View(timeout=120)
            view3 = View(timeout=120)
            view4 = View(timeout=120)

            view.add_item(button)
            view1.add_item(button1)
            view2.add_item(button2)
            view3.add_item(button3)
            view4.add_item(button4)
 
            embed = nextcord.Embed(title=":flag_pl: Robert Lewandowski",description="KAPITAN REPREZENTACJI POLSKI 👑" ,colour=nextcord.Colour.greyple())
            embed.add_field(name="`Pozycja`", value="Napastnik ⚽")
            embed.set_image(url="https://s3.tvp.pl/images2/3/4/c/uid_34c3e6415f375692ba0c881b114e4f281666366215317_width_1200_play_0_pos_0_gs_0_height_678_robert-lewandowski-fot-getty-images.jpg")
            await interaction.response.send_message(embed=embed, view=view)

          
        if self.values[0] == "Pomocnicy":
            await interaction.channel.purge(limit=1)
            button = Button(style=nextcord.ButtonStyle.blurple, emoji="➡️")
            button1 = Button(style=nextcord.ButtonStyle.blurple, emoji="➡️")
            button2 = Button(style=nextcord.ButtonStyle.blurple, emoji="➡️")
            button3 = Button(style=nextcord.ButtonStyle.blurple, emoji="➡️")
            button4 = Button(style=nextcord.ButtonStyle.blurple, emoji="➡️")
            button5 = Button(style=nextcord.ButtonStyle.blurple, emoji="➡️")
            button6 = Button(style=nextcord.ButtonStyle.blurple, emoji="➡️")
            button7 = Button(style=nextcord.ButtonStyle.blurple, emoji="➡️")
            button8 = Button(style=nextcord.ButtonStyle.blurple, emoji="➡️")
            button9 = Button(style=nextcord.ButtonStyle.blurple, emoji="➡️")
            button10 = Button(style=nextcord.ButtonStyle.blurple, emoji="➡️")


            async def button_callback(interaction):
                await interaction.channel.purge(limit=1)
                embed = nextcord.Embed(title=":flag_pl: Nicola Zalewski", colour=nextcord.Colour.greyple())
                embed.add_field(name="`Pozycja`", value="Pomocnik 🎯")
                embed.set_image(url="https://d-art.ppstatic.pl/kadry/k/r/1/d5/05/609a5c6dea864_o_large.jpg")
                await interaction.response.send_message(embed=embed, view=view1)

            button.callback = button_callback

            async def button1_callback(interaction):
                await interaction.channel.purge(limit=1)
                embed = nextcord.Embed(title=":flag_pl: Sebastian Szymański", colour=nextcord.Colour.greyple())
                embed.add_field(name="`Pozycja`", value="Pomocnik 🎯")
                embed.set_image(url="https://s6.tvp.pl/images2/6/6/6/uid_6660ee2098abb4f84844b22d023f63411635793622492_width_1200_play_0_pos_0_gs_0_height_678_sebastian-szymanski-w-bialo-czerwonych-barwach-fot-getty-images.jpg")
                await interaction.response.send_message(embed=embed, view=view2)

            button1.callback = button1_callback

            async def button2_callback(interaction):
                await interaction.channel.purge(limit=1)
                embed = nextcord.Embed(title=":flag_pl: Jakub Kamiński", colour=nextcord.Colour.greyple())
                embed.add_field(name="`Pozycja`", value="Pomocnik 🎯")
                embed.set_image(url="https://i.iplsc.com/-/000FI472E0T7HVWY-C321-F4.webp")
                await interaction.response.send_message(embed=embed, view=view3)

            button2.callback = button2_callback

            async def button3_callback(interaction):
                await interaction.channel.purge(limit=1)
                embed = nextcord.Embed(title=":flag_pl: Kamil Grosicki", colour=nextcord.Colour.greyple())
                embed.add_field(name="`Pozycja`", value="Pomocnik 🎯")
                embed.set_image(url="https://cdn.galleries.smcloud.net/t/galleries/gf-ZNHW-7yiJ-YDHb_kamil-grosicki-reprezentacja-664x442.JPG")
                await interaction.response.send_message(embed=embed, view=view4)

            button3.callback = button3_callback

            async def button4_callback(interaction):
                await interaction.channel.purge(limit=1)
                embed = nextcord.Embed(title=":flag_pl: Szymon Żurkowski", colour=nextcord.Colour.greyple())
                embed.add_field(name="`Pozycja`", value="Pomocnik 🎯")
                embed.set_image(url="https://s2.tvp.pl/images2/2/d/2/uid_2d247e32e3feef6d178e6ce87b0307d31655451997492_width_1200_play_0_pos_0_gs_0_height_678_szymon-zurkowski-wkrotce-pozna-swoja-najblizsza-przyszlosc-fot-getty.jpg")
                await interaction.response.send_message(embed=embed, view=view5)

            button4.callback = button4_callback

            async def button5_callback(interaction):
                await interaction.channel.purge(limit=1)
                embed = nextcord.Embed(title=":flag_pl: Grzegorz Krychowiak", colour=nextcord.Colour.greyple())
                embed.add_field(name="`Pozycja`", value="Pomocnik 🎯")
                embed.set_image(url="https://www.goal.pl/wp-content/uploads/2022/05/krychowiak-2-960x640.jpg")
                await interaction.response.send_message(embed=embed, view=view6)

            button5.callback = button5_callback

            async def button6_callback(interaction):
                await interaction.channel.purge(limit=1)
                embed = nextcord.Embed(title=":flag_pl: Mateusz Klich", colour=nextcord.Colour.greyple())
                embed.add_field(name="`Pozycja`", value="Pomocnik 🎯")
                embed.set_image(url="https://ocdn.eu/sport-images-transforms/1/Hvnk9lBaHR0cHM6Ly9vY2RuLmV1L3B1bHNjbXMvTURBXy9jYWEwM2RmZGY5MzFlOTllNTcxMTgwNzE4OTA3NDA5ZS5qcGeTlQMAzOnNHSPNEGOVAs0EsADCw5MJpmM5ZjUyZAbeAAKhMAGhMQE/mateusz-klich.jpg")
                await interaction.response.send_message(embed=embed, view=view7)

            button6.callback = button6_callback

            async def button7_callback(interaction):
                await interaction.channel.purge(limit=1)
                embed = nextcord.Embed(title=":flag_pl: Karol Linetty", colour=nextcord.Colour.greyple())
                embed.add_field(name="`Pozycja`", value="Pomocnik 🎯")
                embed.set_image(url="https://oknonawagrowiec.pl/wp-content/uploads/2020/01/Karol-Linetty.jpg")
                await interaction.response.send_message(embed=embed, view=view8)

            button7.callback = button7_callback

            async def button8_callback(interaction):
                await interaction.channel.purge(limit=1)
                embed = nextcord.Embed(title=":flag_pl: Przemyslaw Frankowski", colour=nextcord.Colour.greyple())
                embed.add_field(name="`Pozycja`", value="Pomocnik 🎯")
                embed.set_image(url="https://sf-administracja.wpcdn.pl/storage2/featured_original/613336f8bac086_37714948.jpg")
                await interaction.response.send_message(embed=embed, view=view9)
                
            button8.callback = button8_callback

            async def button9_callback(interaction):
                await interaction.channel.purge(limit=1)
                embed = nextcord.Embed(title=":flag_pl: Michał Skóraś", colour=nextcord.Colour.greyple())
                embed.add_field(name="`Pozycja`", value="Pomocnik 🎯")
                embed.set_image(url="https://d-art.ppstatic.pl/kadry/k/r/1/19/64/632d7e584069f_o_medium.jpg")
                await interaction.response.send_message(embed=embed, view=view10)

            button9.callback = button9_callback

            async def button10_callback(interaction):
                await interaction.channel.purge(limit=1)
                embed = nextcord.Embed(title=":flag_pl: Mateusz Łęgowski", colour=nextcord.Colour.greyple())
                embed.add_field(name="`Pozycja`", value="Pomocnik 🎯")
                embed.set_image(url="https://www.cmsmazurska.pl/wp-content/uploads/2022/03/CMS-rep-mateusz-legowski-2.jpg")
                await interaction.response.send_message(embed=embed)

            button10.callback = button10_callback


            view = View(timeout=120)
            view1 = View(timeout=120)
            view2 = View(timeout=120)
            view3 = View(timeout=120)
            view4 = View(timeout=120)
            view5 = View(timeout=120)
            view6 = View(timeout=120)
            view7 = View(timeout=120)
            view8 = View(timeout=120)
            view9 = View(timeout=120)
            view10 = View(timeout=120)

            view.add_item(button)
            view1.add_item(button1)
            view2.add_item(button2)
            view3.add_item(button3)
            view4.add_item(button4)
            view5.add_item(button5)
            view6.add_item(button6)
            view7.add_item(button7)
            view8.add_item(button8)
            view9.add_item(button9)
            view10.add_item(button10)

            embed = nextcord.Embed(title=":flag_pl: Piotr Zieliński", colour=nextcord.Colour.greyple())
            embed.add_field(name="`Pozycja`", value="Pomocnik 🎯")
            embed.set_image(url="https://s3.tvp.pl/images2/3/b/7/uid_3b75a27f8aeb42d4a2efb762e7145194_width_1200_play_0_pos_0_gs_0_height_678_piotr-zielinski-gwiazda-meczu-z-liverpoolem-fot-getty-images.png")
            await interaction.response.send_message(embed=embed, view=view)


        if self.values[0] == "Obrońcy":
            await interaction.channel.purge(limit=1)
            button = Button(style=nextcord.ButtonStyle.blurple, emoji="➡️")
            button1 = Button(style=nextcord.ButtonStyle.blurple, emoji="➡️")
            button2 = Button(style=nextcord.ButtonStyle.blurple, emoji="➡️")
            button3 = Button(style=nextcord.ButtonStyle.blurple, emoji="➡️")
            button4 = Button(style=nextcord.ButtonStyle.blurple, emoji="➡️")
            button5 = Button(style=nextcord.ButtonStyle.blurple, emoji="➡️")
            button6 = Button(style=nextcord.ButtonStyle.blurple, emoji="➡️")
            button7 = Button(style=nextcord.ButtonStyle.blurple, emoji="➡️")
            button8 = Button(style=nextcord.ButtonStyle.blurple, emoji="➡️")
            button9 = Button(style=nextcord.ButtonStyle.blurple, emoji="➡️")


            async def button_callback(interaction):
                    await interaction.channel.purge(limit=1)
                    embed = nextcord.Embed(title=":flag_pl: Jakub Kiwior", colour=nextcord.Colour.greyple())
                    embed.add_field(name="`Pozycja`", value="Obrońca 🛡️")
                    embed.set_image(url="https://www.goal.pl/wp-content/uploads/2022/08/20220614xPF_MB4891-960x640.jpg")
                    await interaction.response.send_message(embed=embed, view=view1)

            button.callback = button_callback


            async def button1_callback(interaction):
                await interaction.channel.purge(limit=1)
                embed = nextcord.Embed(title=":flag_pl: Kamil Glik", colour=nextcord.Colour.greyple())
                embed.add_field(name="`Pozycja`", value="Obrońca 🛡️")
                embed.set_image(url="https://ocdn.eu/sport-images-transforms/1/8gfk9lCaHR0cHM6Ly9vY2RuLmV1L3B1bHNjbXMvTURBXy9lODI5MDI3MTRiYjI1NWQ5MzcyY2Q2N2NiNjBmYTM0Yi5qcGVnk5UDAcxgzQX-zQNekwXNBLDNAnSTCaZkNDFkOGMG3gACoTABoTEB")
                await interaction.response.send_message(embed=embed, view=view2)

            button1.callback = button1_callback

            async def button2_callback(interaction):
                await interaction.channel.purge(limit=1)
                embed = nextcord.Embed(title=":flag_pl: Bartosz Bereszyński", colour=nextcord.Colour.greyple())
                embed.add_field(name="`Pozycja`", value="Obrońca 🛡️")
                embed.set_image(url="https://ipla.pluscdn.pl/dituel/cp/xb/xbbkqu1amgu6s2ncvcvunurip9qpfjgd.JPG")
                await interaction.response.send_message(embed=embed, view=view3)

            button2.callback = button2_callback

            async def button3_callback(interaction):
                await interaction.channel.purge(limit=1)
                embed = nextcord.Embed(title=":flag_pl: Arkadiusz Reca", colour=nextcord.Colour.greyple())
                embed.add_field(name="`Pozycja`", value="Obrońca 🛡️")
                embed.set_image(url="https://ipla.pluscdn.pl/dituel/cp/4p/4phr9rqgm55gu5pq1tcx2fbqs1mic4kq.JPG")
                await interaction.response.send_message(embed=embed, view=view4)

            button3.callback = button3_callback

            async def button4_callback(interaction):
                await interaction.channel.purge(limit=1)
                embed = nextcord.Embed(title=":flag_pl: Tomasz Kędziora", colour=nextcord.Colour.greyple())
                embed.add_field(name="`Pozycja`", value="Obrońca 🛡️")
                embed.set_image(url="https://www.goal.pl/wp-content/uploads/2021/08/kedziora-tomasz-1.jpg")
                await interaction.response.send_message(embed=embed, view=view5)

            button4.callback = button4_callback
            
            async def button5_callback(interaction):
                await interaction.channel.purge(limit=1)
                embed = nextcord.Embed(title=":flag_pl: Mateusz Wieteska", colour=nextcord.Colour.greyple())
                embed.add_field(name="`Pozycja`", value="Obrońca 🛡️")
                embed.set_image(url="https://s5.tvp.pl/images2/5/0/1/uid_501bf6b5ee1c6077e967ed27bcbe714e1647441619455_width_1200_play_0_pos_0_gs_0_height_678_mateusz-wieteska-wpisal-sie-juz-w-legijny-krajobraz-fot-getty.jpg")
                await interaction.response.send_message(embed=embed, view=view6)

            button5.callback = button5_callback

            async def button6_callback(interaction):
                await interaction.channel.purge(limit=1)
                embed = nextcord.Embed(title=":flag_pl: Paweł Dawidowicz", colour=nextcord.Colour.greyple())
                embed.add_field(name="`Pozycja`", value="Obrońca 🛡️")
                embed.set_image(url="https://img.wprost.pl/img/pawel-dawidowicz/54/b8/fed4edce5ff2a07ba0d87890d3dc.jpeg")
                await interaction.response.send_message(embed=embed, view=view7)

            button6.callback = button6_callback

            async def button7_callback(interaction):
                await interaction.channel.purge(limit=1)
                embed = nextcord.Embed(title=":flag_pl: Robert Gumny", colour=nextcord.Colour.greyple())
                embed.add_field(name="`Pozycja`", value="Obrońca 🛡️")
                embed.set_image(url="https://transfery.info/img/photos/80513/1500xauto/robert-gumny.jpg")
                await interaction.response.send_message(embed=embed)

            button7.callback = button7_callback


            view = View(timeout=120)
            view1 = View(timeout=120)
            view2 = View(timeout=120)
            view3 = View(timeout=120)
            view4 = View(timeout=120)
            view5 = View(timeout=120)
            view6 = View(timeout=120)
            view7 = View(timeout=120)

            view.add_item(button)
            view1.add_item(button1)
            view2.add_item(button2)
            view3.add_item(button3)
            view4.add_item(button4)
            view5.add_item(button5)
            view6.add_item(button6)
            view7.add_item(button7)

            embed = nextcord.Embed(title=":flag_pl: Jan Bednarek", colour=nextcord.Colour.greyple())
            embed.add_field(name="`Pozycja`", value="Obrońca 🛡️")
            embed.set_image(url="https://ocdn.eu/sport-images-transforms/1/xedk9lCaHR0cHM6Ly9vY2RuLmV1L3B1bHNjbXMvTURBXy8wMmNhOTcyMTdiMzRmZDNjZjY5MjhkNjVjODA5MzlhYy5qcGVnk5UDAMx0zQV6zQMUlQLNBLAAwsOTCaZlZTU5ZWEG3gACoTABoTEB/jan-bednarek.jpg")
            await interaction.response.send_message(embed=embed, view=view)


        if self.values[0] == "Bramkarze":
            await interaction.channel.purge(limit=1)
            button = Button(style=nextcord.ButtonStyle.blurple, emoji="➡️")
            button1 = Button(style=nextcord.ButtonStyle.blurple, emoji="➡️")
            button2 = Button(style=nextcord.ButtonStyle.blurple, emoji="➡️")
            button3 = Button(style=nextcord.ButtonStyle.blurple, emoji="➡️")
            button4 = Button(style=nextcord.ButtonStyle.blurple, emoji="➡️")
            button5 = Button(style=nextcord.ButtonStyle.blurple, emoji="➡️")

            async def button_callback(interaction):
                await interaction.channel.purge(limit=1)
                embed = nextcord.Embed(title=":flag_pl: Łukasz Fabiański", colour=nextcord.Colour.greyple())
                embed.add_field(name="`Pozycja`", value="Bramkarz 🥅")
                embed.set_image(url="https://s4.tvp.pl/images2/d/7/a/uid_d7aafc00589b0b1b3d20a1522a798aed1641976791456_width_1200_play_0_pos_0_gs_0_height_678_lukasz-fabianski-fot-getty-images.jpg")
                await interaction.response.send_message(embed=embed, view=view1)

            button.callback = button_callback

            async def button1_callback(interaction):
                await interaction.channel.purge(limit=1)
                embed = nextcord.Embed(title=":flag_pl: Łukasz Skorupski", colour=nextcord.Colour.greyple())
                embed.add_field(name="`Pozycja`", value="Bramkarz 🥅")
                embed.set_image(url="https://cdn.galleries.smcloud.net/t/galleries/gf-uikP-7LmA-wz9Y_lukasz-skorupski-w-reprezentacji-polski-1920x1080-nocrop.JPG")
                await interaction.response.send_message(embed=embed, view=view2)

            button1.callback = button1_callback

            async def button2_callback(interaction):
                await interaction.channel.purge(limit=1)
                embed = nextcord.Embed(title=":flag_pl: Bartłomiej Drągowski", colour=nextcord.Colour.greyple())
                embed.add_field(name="`Pozycja`", value="Bramkarz 🥅")
                embed.set_image(url="https://pilkarskiswiat.com/wp-content/uploads/2020/06/Bartlomiej-Dragowski-Fiorentina-e1591599923809.jpg")
                await interaction.response.send_message(embed=embed, view=view3)

            button2.callback = button2_callback

            async def button3_callback(interaction):
                await interaction.channel.purge(limit=1)
                embed = nextcord.Embed(title=":flag_pl: Kamil Grabara", colour=nextcord.Colour.greyple())
                embed.add_field(name="`Pozycja`", value="Bramkarz 🥅")
                embed.set_image(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTFz1PKPZ70BaeusoaAnFNIH3uwU-E40a1mcg&usqp=CAU")
                await interaction.response.send_message(embed=embed, view=view4)

            button3.callback = button3_callback

            async def button4_callback(interaction):
                await interaction.channel.purge(limit=1)
                embed = nextcord.Embed(title=":flag_pl: Radosław Majecki", colour=nextcord.Colour.greyple())
                embed.add_field(name="`Pozycja`", value="Bramkarz 🥅")
                embed.set_image(url="https://www.goal.pl/wp-content/uploads/2021/08/majecki-radoslaw.jpg")
                await interaction.response.send_message(embed=embed)

            button4.callback = button4_callback




            view = View(timeout=120)
            view1 = View(timeout=120)
            view2 = View(timeout=120)
            view3 = View(timeout=120)
            view4 = View(timeout=120)

            view.add_item(button)
            view1.add_item(button1)
            view2.add_item(button2)
            view3.add_item(button3)
            view4.add_item(button4)

            embed = nextcord.Embed(title=":flag_pl: Wojciech Szczęsny", colour=nextcord.Colour.greyple())
            embed.add_field(name="`Pozycja`", value="Bramkarz 🥅")
            embed.set_image(url="https://s5.tvp.pl/images2/e/9/5/uid_e95a03909b171d0e9399ebe077bc4f341623702991532_width_1200_play_0_pos_0_gs_0_height_678_wojciech-szczesny-fot-getty-images.jpg")
            await interaction.response.send_message(embed=embed, view=view)

class DropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__()


        self.add_item(Dropdown())



@client.slash_command(guild_ids=[SERWER_ID], description="Polscy reprezentanci piłki nożnej ⚽", name="reprezentacja")
async def reprezentacja(interaction: Interaction):



    view = DropdownView()


    await interaction.send(view=view)

@client.slash_command(guild_ids=[SERWER_ID], description="Różne żartobliwe rozkminy 🤔", name="rozkmina")
async def rozkmina(interaction: Interaction):
    
    rozkmina=["Jeśli w Krakowie otwiera się okno to świerze powietrze się wpuszcza czy wypuszcza?","Skoro w winnicy jest wino, to czy w piwnicy jest piwo?","Jeżeli karaluchy potrafią przeżyć wybuch atomowy, to co jest w spreju na owady?","Ktoś ma najwięcej wygranych w kamień papier nożyce i nawet o tym nie wie","Dlaczego super klej nie przykleja się do tubki od środka?","Czy życząc Polakowi żyjącemu w Polsce na urodziny 100 lat, to tak na prawde życzymy mu dobrze, czy źle?","Czy psy nas liżą bo wiedzą, że w środku mamy kości?","Czy jeśli rozlejesz środek czyszczący to czy zrobiłeś bałagan?","Ludzkość, to jedyna cywilizacja która musi płacić, by żyć na swojej planecie","Czy jeśli uczeń obłał test, to czy to wina ucznia, czy nauczyciela?","Dwie kobiety w ciąży które walczą ze sobą, to tak jakby dwójka noworodków walczyła ze sobą w mechach?","Czy jeśli czas to pieniądz, to bankomat to wehikuł czasu?","Czy naprawa auta nie powinna nazywać się autokorektą?","Dlaczego mówimy plecy skoro mamy jeden plec?","Gdyby zegar był kompasem to północ i południe byłyby w tym samym miejscu","Czy jeśli bym był pijany i wsiadł do Tesli, która była by na autopilicie, to czy dostałbym za to mandat?","Dlaczego mucha potrafi wlecieć przez małą szczelinę a nie potrafi wylecieć przez otwarte okno?"]

    embed = nextcord.Embed(title=f"`Rozkmina`",timestamp = interaction.created_at, colour=nextcord.Colour.gold())
    embed.add_field(name=random.choice(rozkmina), value="🤔")
    embed.set_footer(text=f"Komende użył {interaction.user.name}")
    await interaction.response.send_message(embed=embed)

@client.command()
async def rozkmina(ctx):
    
    rozkmina=["Jeśli w Krakowie otwiera się okno to świerze powietrze się wpuszcza czy wypuszcza?","Skoro w winnicy jest wino, to czy w piwnicy jest piwo?","Jeżeli karaluchy potrafią przeżyć wybuch atomowy, to co jest w spreju na owady?","Ktoś ma najwięcej wygranych w kamień papier nożyce i nawet o tym nie wie","Dlaczego super klej nie przykleja się do tubki od środka?","Czy życząc Polakowi żyjącemu w Polsce na urodziny 100 lat, to tak na prawdę życzymy mu dobrze, czy źle?","Czy psy nas liżą bo wiedzą, że w środku mamy kości?","Czy jeśli rozlejesz środek czyszczący to czy zrobiłeś bałagan?","Ludzkość, to jedyna cywilizacja która musi płacić, by żyć na swojej planecie","Czy jeśli uczeń obłał test, to czy to wina ucznia, czy nauczyciela?","Dwie kobiety w ciąży które walczą ze sobą, to tak jakby dwójka noworodków walczyła ze sobą w mechach?","Czy jeśli czas to pieniądz, to bankomat to wehikuł czasu?","Czy naprawa auta nie powinna nazywać się autokorektą?","Dlaczego mówimy plecy skoro mamy jeden plec?","Gdyby zegar był kompasem to północ i południe byłyby w tym samym miejscu","Czy jeśli bym był pijany i wsiadł do Tesli, która była by na autopilicie, to czy dostałbym za to mandat?","Dlaczego mucha potrafi wlecieć przez małą szczelinę a nie potrafi wylecieć przez otwarte okno?"]

    embed = nextcord.Embed(title=f"`Rozkmina`",timestamp = ctx.message.created_at, colour=nextcord.Colour.gold())
    embed.add_field(name=random.choice(rozkmina), value="🤔")
    embed.set_footer(text=f"Komende użył {ctx.author.name}")
    await ctx.send(embed=embed)



@client.slash_command(guild_ids=[SERWER_ID], description="Zgłoś użytkownika tego serwera 📨", name="zgłoszenie")
async def zgłoszenie(interaction: Interaction, osoba: nextcord.Member, *, powód, wiadomość="brak wiadomości"):

    embed=nextcord.Embed(timestamp = datetime.now(), color = nextcord.Colour.green())
    embed.add_field(name=f"<:tak:1020344650260807700> | ZGŁOSZENIE!", value=f"📨 Twoje zgłoszenie zostało wysłane do administracji!", inline=False)
    await interaction.response.send_message(embed=embed)
    embed=nextcord.Embed(timestamp = datetime.now(), color = nextcord.Colour.yellow())
    embed.add_field(name=f"⛔ | NOWE ZGŁOSZENIE!", value=f"`{interaction.user.name}` zgłosił `{osoba.name}` za `{powód}`!", inline=False)
    embed.add_field(name=f"`💭 Wiadomośc od {interaction.user.name}`", value=f"*{wiadomość}*", inline=False)
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/OOjs_UI_icon_alert_destructive.svg/1200px-OOjs_UI_icon_alert_destructive.svg.png")
    kanal = client.get_channel(901453029411258399)
    await kanal.send(embed=embed)

@client.command()
async def report(ctx, osoba: nextcord.Member, *, powód, wiadomość="brak wiadomości"):

    embed=nextcord.Embed(timestamp = datetime.now(), color = nextcord.Colour.green())
    embed.add_field(name=f"<:tak:1020344650260807700> | ZGŁOSZENIE!", value=f"📨 Twoje zgłoszenie zostało wysłane do administracji!", inline=False)
    await ctx.send(embed=embed)
    embed=nextcord.Embed(timestamp = datetime.now(), color = nextcord.Colour.yellow())
    embed.add_field(name=f"⛔ | NOWE ZGŁOSZENIE!", value=f"`{ctx.author.name}` zgłosił `{osoba.name}` za `{powód}`!", inline=False)
    embed.add_field(name=f"`💭 Wiadomośc od {ctx.author.name}`", value=f"*{wiadomość}*", inline=False)
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/OOjs_UI_icon_alert_destructive.svg/1200px-OOjs_UI_icon_alert_destructive.svg.png")
    kanal = client.get_channel(901453029411258399)
    await kanal.send(embed=embed)

    

@tasks.loop(minutes=2)
async def check():
    today = date.today()
    if today := "2022-07-10":
        for guild in client.guilds:
            if str(guild.id) == 795356386807775282:
                for channel in guild.channels:
                    if str(channel.id) == "1049365716035444826":
                        await channel.send("Gratulacje ..., to twój dzień urodzin")





async def check_for_birthday(self):
    guild = member.guild
    await self.wait_until_ready()
    now = datetime.datetime.now()
    curmonth = now.month
    curday = now.day
    
    while not self.is_closed():
        with open('birthdays.json', 'r') as f:
            var = jason.load(f)
            for member in var:
                if member['month'] == curmonth:
                    if member['day'] == curday:
                        try:
                            await client.get_user(member).send("Szczęśliwych urodzin!")
                        except:
                            pass
                        success = False
                        index = 0
                        while not success:
                            try:
                                await guild.channels[index].send(f"Szczęśliwych urodzin! <@{member}>!")
                            except nextcord.Forbidden:
                                                    index += 1
                            except AttributeError:
                                index += 1
                            except IndexError:

                                pass
                            else:
                                success = True
        await asyncio.sleep(86400) 


@client.event
async def on_guild_join(guild):

    success = False
    index = 0
    while not success:
        try:
            await guild.channels[index].send("**👋Hej! Jestem __XajperBOT__ | Moje prefixy: `x!` `/`**")
        except nextcord.Forbidden:
            index += 1
        except AttributeError:
            index += 1
        except IndexError:

            pass
        else:
            success = True
        


class Report(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            "Twoje zgłoszenie",
            timeout=5 * 60,
        )

        self.name = nextcord.ui.TextInput(
            label="Przedstaw się",
            min_length=2,
            max_length=50,
        )
        self.add_item(self.name)

        self.description = nextcord.ui.TextInput(
            label="Kogo zgłaszasz i za co",
            style=nextcord.TextInputStyle.paragraph,
            placeholder="...",
            required=True,
            max_length=200,
        )
        self.add_item(self.description)

    async def callback(self, interaction: nextcord.Interaction) -> None:

        embed=nextcord.Embed(timestamp = datetime.now(), color = nextcord.Colour.green())
        embed.add_field(name=f"<:tak:1020344650260807700> | ZGŁOSZENIE!", value=f"📨 Twoje zgłoszenie zostało wysłane do administracji!", inline=False)
        await interaction.user.send(embed=embed)

        embed=nextcord.Embed(timestamp = datetime.now(), color = nextcord.Colour.yellow())
        embed.add_field(name=f"⛔ | NOWE ZGŁOSZENIE!", value=f"Treść zgłoszenia od {interaction.user.mention}:\n\n> {self.name.value}\n> {self.description.value}", inline=False)
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/OOjs_UI_icon_alert_destructive.svg/1200px-OOjs_UI_icon_alert_destructive.svg.png")
        kanal = client.get_channel(901453029411258399)
        await kanal.send(embed=embed)

@client.slash_command(
    name="report",
    description="Zgłoś kogoś 🙋",
    guild_ids=[SERWER_ID],
)
async def send(interaction: nextcord.Interaction):
    modal = Report()
    await interaction.response.send_modal(modal)


























client.run("OTk5Mjg4MjQ0NDc2ODUwMjM2.GXWf7M.XDZoGguDHliKFp4v_zydlRAu4dGr-QQsxmUlkM")