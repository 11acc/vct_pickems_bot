
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

from database.db_utils import format_player_info
from bot.bot_utils import EventYears, EventTypes, get_vct_emoji


load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
# Other global variables
BOT_NAME = "reobot"
BOT_EMBED_COLOUR = discord.Colour.from_rgb(177,35,235)
BOT_AUTHOR_URL = "https://x.com/marthastewart/status/463333915739316224?mx=2"

# Discord connection and bot command setup
intents = discord.Intents.default()
intents.message_content = True  # needed for msg commands
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🐙 {bot.user} online")

@bot.command()
async def hello(ctx):
    await ctx.send(f"hello {ctx.author.name}")

@bot.command()
async def vct(ctx, year: int, event: str):
    # Check input year is valid
    if not EventYears.validate(year):
        await ctx.send(f"massive whiff on that year brosky\nvalid years: [{', '.join(EventYears.VALID_YEARS)}]")

    # Check input event is valid
    if not EventTypes.validate(event):
        await ctx.send(f"massive whiff on that event selection\nvalid events: [{', '.join(EventTypes.VALID_EVENTS.keys()).lower()}]")
        return None
    
    # Set the header and obtain the appropriate user information
    header = f"{get_vct_emoji("logo")} VCT {year} Pickem' [ {event.capitalize()} ] Leaderboard"
    player_bullets = "\n".join(format_player_info(year, event))

    embed = discord.Embed(
        colour=BOT_EMBED_COLOUR
        , description=player_bullets
        , title=header
        # , url=""
    )
    embed.set_author(name=BOT_NAME, url=BOT_AUTHOR_URL)

    await ctx.send(embed=embed)



bot.run(DISCORD_BOT_TOKEN)
