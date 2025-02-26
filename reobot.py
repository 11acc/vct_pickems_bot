
# :purpose: Main script to run discord bot

import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord.ui import Select, View

from database.modules import db
from database.db_utils import find_best_event_match, points_from_event, star_leaderboard
from reobot.bot_utils import get_vct_emoji


load_dotenv()
REO_DEV_USER_ID = 229174776634015744
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
BOT_NAME = "reobot"
BOT_EMBED_POINTS_COLOUR = discord.Colour.from_rgb(177,35,235)
BOT_EMBED_LEADERBOARD_COLOUR = discord.Colour.from_rgb(255,68,85)
BOT_AUTHOR_URL = "https://x.com/marthastewart/status/463333915739316224?mx=2"

# Discord connection and bot command setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!vct ", intents=intents)


@bot.event
async def on_ready() -> None:
    print(f"🪸  {bot.user} online")
    db.connect()

@bot.event
async def on_disconnect() -> None:
    print(f"🪸  {bot.user} shutting down...")
    db.close()

@bot.command()
async def hello(ctx) -> None:
    await ctx.send(f"hello {ctx.author.name}")

# /// POINTS
@bot.command()
async def points(ctx, loc:str, year: int) -> None:
    # Check input year is valid
    input_event = find_best_event_match(loc, year)
    if not input_event:
        await ctx.send("massive whiff on that event selection brosky, no event with that name and year combo")

    # Set the header and obtain the appropriate user information
    header = f"{get_vct_emoji("logo")} VCT {year} Pickem' [ {loc.capitalize()} ] Leaderboard"
    event_points = points_from_event(input_event)
    if not event_points:
        await ctx.send(f"oi <@{REO_DEV_USER_ID}> you fucked somthing up you stupid ass")
        return
    player_bullets = "\n".join(event_points)
    event_link = db.event_vlr_link_from_name(input_event)
    if not event_link:
        event_link = ""

    embed = discord.Embed(
        colour=BOT_EMBED_POINTS_COLOUR
        , description=player_bullets
        , title=header
        , url=event_link
    )
    embed.set_author(name=BOT_NAME, url=BOT_AUTHOR_URL)

    await ctx.send(embed=embed)

# /// LEADERBOARD
@bot.command()
async def leaderboard(ctx) -> None:
    # Set the header and obtain the appropriate user information
    header = f":trophy: VCT Pickem' Global Leaderboard"
    leaderboard = star_leaderboard()
    if not leaderboard:
        await ctx.send(f"oi <@{REO_DEV_USER_ID}> you fucked somthing up you stupid ass")
        return
    
    embed = discord.Embed(
        colour=BOT_EMBED_LEADERBOARD_COLOUR
        , description=leaderboard
        , title=header
    )
    embed.set_author(name=BOT_NAME, url=BOT_AUTHOR_URL)

    await ctx.send(embed=embed)


@bot.command()
async def easter_egg(ctx) -> None:
    header = f"{get_vct_emoji("miku")} testin"
    asd = """
- :flag_es:  **A** <a:champs_sparkle_1:1342202573498880115> <a:champs_sparkle_2:1342202584936747111> <a:champs_sparkle_3_6:1342202595640610997>
  - **__VCT 2049 : Champions Almeria__**

- :flag_ge:  **K** <:masters_sparkle_1:1342206382698397787> <:masters_sparkle_2:1342206390403600405> <:masters_sparkle_3:1342206396808171562>
  - **VCT 2049 : Masters Los Angeles**
    """

    embed = discord.Embed(
        colour=discord.Colour.from_rgb(19,122,127)
        , description=asd
        , title=header
    )
    embed.set_author(name=BOT_NAME, url=BOT_AUTHOR_URL)

    await ctx.send(embed=embed)

# @bot.command()
# async def test(ctx) -> None:
#     header = f"{get_vct_emoji('vct_masters')} Masters Bangkok - Swiss [ Day 2 ] - Who Voted Who"
#     desc = f"""
# - **Swiss Stage: Round 1  ·**  {get_vct_emoji('vit')} vs {get_vct_emoji('t1')}
#   - {get_vct_emoji('vit')}   `Alex`  `Ting`
#   - {get_vct_emoji('t1')}   `Qiff`  `Oliver`  `Maka`
# - **Swiss Stage: Round 1  ·**  {get_vct_emoji('g2')} vs {get_vct_emoji('te')}
#   - {get_vct_emoji('g2')}   `Alex`  `Ting`  `Qiff`
#   - {get_vct_emoji('te')}   `Oliver`  `Maka`
#     """

#     embed = discord.Embed(
#         colour=discord.Colour.from_rgb(184,180,228)
#         , description=desc
#         , title=header
#     )
#     embed.set_author(name=BOT_NAME, url=BOT_AUTHOR_URL)
#     embed.set_image(url="https://i.ytimg.com/vi/FA3f5TGNj7s/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLBt2kHJKriLP0D5XXptHurNnd7a1Q")
#     embed.set_footer(
#         text="Fri, February 21, 2025"
#     )

#     await ctx.send(embed=embed)


# /// BETS
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



bot.run(DISCORD_BOT_TOKEN)
