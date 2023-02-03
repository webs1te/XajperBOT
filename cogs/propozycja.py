from asyncio.futures import _set_concurrent_future_state
from ast import alias
from unittest import result
import nextcord
from nextcord.ext import commands
import asyncio
import datetime

class Propozycja(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print("Ładowanie Propozycji...")

    @commands.command()
    async def propozycja(self,ctx,choice1):
        embed = nextcord.Embed(title = f"📃 | Propozycja __{ctx.author.name}__:\n", description = f"{choice1}\n",timestamp = ctx.message.created_at, color=ctx.author.colour)
        
        message = await ctx.send(embed = embed)
        await message.add_reaction("<:tak:1020344650260807700>")
        await message.add_reaction("<:neutralny:1020344687959224330>")
        await message.add_reaction("<:nie:1020344672461262889>")
        
        await ctx.send(embed=embed)

        





def setup(bot):
    bot.add_cog(Propozycja(bot))