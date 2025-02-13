
# :purpose: Main script to run discord bot

import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord.ui import Select, View

from database.sql_tables import tuple_event_into_class, get_event, get_points_from_event


load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
BOT_NAME = "reobot"
BOT_EMBED_COLOUR = discord.Colour.from_rgb(177,35,235)
BOT_AUTHOR_URL = "https://x.com/marthastewart/status/463333915739316224?mx=2"

# Discord connection and bot command setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!vct ", intents=intents)


@bot.event
async def on_ready():
    print(f"🐙 {bot.user} online")

@bot.command()
async def hello(ctx):
    await ctx.send(f"hello {ctx.author.name}")


# /// POINTS
@bot.command()
async def points(ctx, kind: str, loc:str, year: int):
    pass



# @bot.command()
# async def points(ctx, year: int, event: str):
#     # Check input year is valid
#     if not EventYears.validate(year):
#         await ctx.send(f"massive whiff on that year brosky\nvalid years: [{', '.join(EventYears.VALID_YEARS)}]")

#     # Check input event is valid
#     event = event.upper()
#     if not EventTypes.validate(event):
#         await ctx.send(f"massive whiff on that event selection\nvalid events: [{', '.join(EventTypes.VALID_EVENTS.keys()).lower()}]")
#         return None
    
#     # Set the header and obtain the appropriate user information
#     header = f"{get_vct_emoji("logo")} VCT {year} Pickem' [ {event.capitalize()} ] Leaderboard"
#     player_bullets = "\n".join(format_player_info(year, event))

#     embed = discord.Embed(
#         colour=BOT_EMBED_COLOUR
#         , description=player_bullets
#         , title=header
#         # , url=""
#     )
#     embed.set_author(name=BOT_NAME, url=BOT_AUTHOR_URL)

#     await ctx.send(embed=embed)



# class Bet_Select_View(View):
#     @discord.ui.select()
#     async def callback(self, interaction):
#         await interaction.response.send_message(f"You chose: {self.values[0]}")

# class Bet_Select(Select):
#     def __init__(self, placeholder, min_values, max_values, options, row) -> None:
#         super().__init__(
#             placeholder=placeholder
#             , min_values=min_values
#             , max_values=max_values
#             , options=options
#             , row=row)

# @bot.command()
# async def test(ctx):

#     # getting matches

#     matches = [
#         {"match": "Upper Final", "team1": "VIT", "team2": "TH"}
#         , {"match": "Lower Round 4", "team1": "FUT", "team2": "TL"}
#     ]

#     select = Bet_Select(
#         placeholder="Choose match"
#         , min_values=1
#         , max_values=1
#         , options=[
#             discord.SelectOption(label=f"{m['team1']} vs {m['team2']} : {m['match']}") for m in matches
#         ]
#         , row=1
#     )
#     view = View()
#     view.add_item(select)

#     await ctx.send(f"hello {ctx.author.name}", view=view)


# /// BETS
# @bot.group()
# async def bets(ctx):
#     pass

# @bets.command(name="active")
# async def active_bets(ctx):
#     # Receive all active bets
#     asd

#     embed = discord.Embed(
#         colour=BOT_EMBED_COLOUR
#         , description=player_bullets
#         , title=header
#         # , url=""
#     )
#     embed.set_author(name=BOT_NAME, url=BOT_AUTHOR_URL)

#     await ctx.send(embed=embed)


# @bets.command(name="history")
# async def history_bets(ctx):
#     # Receive all past bets

#     # 

#     await ctx.send(embed=embed)



# /// TEST





bot.run(DISCORD_BOT_TOKEN)
