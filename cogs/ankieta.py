from asyncio.futures import _set_concurrent_future_state
from ast import alias
from unittest import result
import nextcord
from nextcord.ext import commands
import asyncio
import datetime

class Ankieta(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print("Εadowanie Ankiet...")

    @commands.command()
    async def ankieta(self,ctx,choice1,choice2,*,topic):

        embed=nextcord.Embed(title="**π | Ankieta**", timestamp = ctx.message.created_at, color=ctx.author.colour)
        embed.add_field(name=f"> Pytanie od __{ctx.author.name}__: π\n", value=topic, inline=False)
        embed.add_field(name=f"β‘οΈ {choice1}", value="*Kliknij `π`*", inline=True)
        embed.add_field(name=f"β‘οΈ {choice2}", value="*Kliknij `π`*", inline=True)
        
        message = await ctx.send(embed = embed)
        await message.add_reaction("π")
        await message.add_reaction("π")




def setup(bot):
    bot.add_cog(Ankieta(bot))