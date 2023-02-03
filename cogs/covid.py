import nextcord
import pandas as pd
from datetime import datetime
from matplotlib import pyplot
from nextcord.ext import commands
from apis.covid_api import covid_api_request


class Covid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def covid(self, ctx, country):
        request_result = covid_api_request(f'dayone/country/{country}')

        data_set = [(datetime.strptime(date_index['Date'], '%Y-%m-%dT%H:%M:%SZ').strftime('%b'), death_index['Deaths'])
                    for date_index, death_index in zip(request_result, request_result)]

        # Plot
        data_frame = pd.DataFrame(data_set)
        data_frame.plot(x=0, y=1, color='#00012C', label='Miesiące')

        # Label
        pyplot.title(f'Pokazuje zgony w {country}')
        pyplot.xlabel('Miesiące')
        pyplot.ylabel('Liczba zgonów')

        # Legend
        pyplot.legend(loc='upper left')

        # Color
        pyplot.axes().set_facecolor('#9A1622')

        pyplot.savefig('.\\assets\\tabelka_covid', bbox_inches='tight')

        await ctx.send(file=nextcord.File('.\\assets\\tabelka_covid.png'))


def setup(bot):
    bot.add_cog(Covid(bot))