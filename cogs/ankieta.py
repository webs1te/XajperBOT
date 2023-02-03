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
        print("Ładowanie Ankiet...")

    @commands.command()
    async def ankieta(self,ctx,choice1,choice2,*,topic):

        embed=nextcord.Embed(title="**📊 | Ankieta**", timestamp = ctx.message.created_at, color=ctx.author.colour)
        embed.add_field(name=f"> Pytanie od __{ctx.author.name}__: 📝\n", value=topic, inline=False)
        embed.add_field(name=f"➡️ {choice1}", value="*Kliknij `👍`*", inline=True)
        embed.add_field(name=f"➡️ {choice2}", value="*Kliknij `👎`*", inline=True)
        
        message = await ctx.send(embed = embed)
        await message.add_reaction("👍")
        await message.add_reaction("👎")




def setup(bot):
    bot.add_cog(Ankieta(bot))