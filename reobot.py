
# :purpose: Main script to run discord bot

import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord.ui import Select, View

from db.db_instance import db
from utils.emojis import get_vct_emoji
from utils.matching import find_best_event_match
from services.points_for_event import points_from_event
from services.leaderboard import star_leaderboard
from services.who_voted_who import who_voted_who


load_dotenv()
REO_DEV_USER_ID = 229174776634015744
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
BOT_NAME = "reobot"
BOT_EMBED_POINTS_COLOUR = discord.Colour.from_rgb(48,92,222)
BOT_EMBED_LEADERBOARD_COLOUR = discord.Colour.from_rgb(234,232,111)
BOT_EMBED_WVW_COLOUR = discord.Colour.from_rgb(64,130,109)  # 168,220,171
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
    # Check if the input is valid
    input_event = find_best_event_match(loc, year)
    if not input_event:
        await ctx.send("massive whiff on that event selection brosky, no event with that name and year combo")
        return

    # Set the header and obtain the appropriate user information
    header = f"{get_vct_emoji("logo")} VCT {year} Pickem' [ {loc.capitalize()} ] Leaderboard"
    event_points = points_from_event(input_event)
    if not event_points:
        await ctx.send(f"oi <@{REO_DEV_USER_ID}> you fucked somthing up you stupid ass")
        return
    player_bullets = "\n".join(event_points)
    event_link = db.get_event_vlr_link_from_name(input_event)
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

# /// WHO VOTED WHO
@bot.command()
async def wvw(ctx, next_param: int = None) -> None:
    header = f"{get_vct_emoji("who")} VCT Who Voted Who"
    upcoming_formatted = who_voted_who(next_param)
    if not upcoming_formatted:
        await ctx.send(f"oi <@{REO_DEV_USER_ID}> you fucked somthing up you stupid ass")
        return
    
    embed = discord.Embed(
        colour=BOT_EMBED_WVW_COLOUR
        , description=upcoming_formatted
        , title=header
    )
    embed.set_author(name=BOT_NAME, url=BOT_AUTHOR_URL)

    await ctx.send(embed=embed)

"""
    embed.set_image(url="https://i.ytimg.com/vi/FA3f5TGNj7s/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLBt2kHJKriLP0D5XXptHurNnd7a1Q")
    embed.set_footer(
        text="Fri, February 21, 2025"
    )
"""


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

@bot.command()
async def test_emojis(ctx) -> None:
    from utils.emojis import VCT_EMOJIS
    lines = [f"{name}: {emoji}" for name, emoji in VCT_EMOJIS.items()]
    
    messages = []
    current_message = ""
    for line in lines:
        new_line = line + "\n"
        if len(current_message) + len(new_line) > 2000:
            messages.append(current_message)
            current_message = new_line
        else:
            current_message += new_line
    
    if current_message:
        messages.append(current_message)
    
    for message in messages:
        await ctx.send(message)

@bot.command()
async def test_emoji_lookup(ctx) -> None:
    from utils.emojis import VCT_EMOJIS, ALIASES
    results = []

    # Test direct lookups using the VCT_EMOJIS keys
    results.append("**Testing direct VCT_EMOJIS keys:**")
    for key, emoji in VCT_EMOJIS.items():
        found = get_vct_emoji(key)
        results.append(f"Input: `{key}` -> Expected: {emoji} | Got: {found}")

    # Test using the aliases
    results.append("\n**Testing ALIASES:**")
    for alias, direct_key in ALIASES.items():
        expected = VCT_EMOJIS.get(direct_key, "❓")
        found = get_vct_emoji(alias)
        results.append(f"Input: `{alias}` -> Expected: {expected} | Got: {found}")

    # Optionally, add some fuzzy match tests
    fuzzy_tests = ["Team Vtlty", "G2", "Sentinel", "Talon", "FURIA", "Navi"]
    results.append("\n**Testing Fuzzy Matches:**")
    for test in fuzzy_tests:
        found = get_vct_emoji(test)
        results.append(f"Input: `{test}` -> Got: {found}")

    # Discord messages have a character limit, so split into chunks if necessary
    output = "\n".join(results)
    if len(output) > 1900:
        for chunk in [output[i:i+1900] for i in range(0, len(output), 1900)]:
            await ctx.send(chunk)
    else:
        await ctx.send(output)


bot.run(DISCORD_BOT_TOKEN)
