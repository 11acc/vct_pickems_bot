
# :purpose: Main script to run discord bot

import os
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands

from db.db_instance import db
from db.queries import db_logic
from utils.emojis import get_vct_emoji
from utils.matching import find_best_event_match
from services.points_for_event import points_from_event
from services.leaderboard import star_leaderboard
from services.who_voted_who import who_voted_who
from services.update import update_current_pickems, update_current_matches, update_current_votes, update_all
from services.bracket_for_event import bracket_for_event


load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

REO_DEV_USER_ID = 229174776634015744
BOT_NAME = "reobot"
BOT_EMBED_POINTS_COLOUR = discord.Colour.from_rgb(48,92,222)
BOT_EMBED_LEADERBOARD_COLOUR = discord.Colour.from_rgb(234,232,111)
BOT_EMBED_WVW_COLOUR = discord.Colour.from_rgb(242,240,239)
BOT_EMBED_BRACKET_COLOUR = discord.Colour.from_rgb(232,49,85)
BOT_AUTHOR_URL = "https://x.com/marthastewart/status/463333915739316224?mx=2"

# Discord connection and bot command setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!vct ", intents=intents)

# /// SETUP
@bot.event
async def on_ready():
    print(f"🐙 {bot.user} online")
    db.connect()
    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

@bot.event
async def on_disconnect():
    print(f"🐙 {bot.user} shutting down...")
    db.close()


# /// POINTS
@bot.tree.command(name="points", description="Points leaderboard for a specific event")
@app_commands.describe(
    event="Event name (Kickoff, Bangkok, Stage1, etc.)",
    year="The number thing we keep track of every earth spin"
)
async def points(interaction: discord.Interaction, event: str, year: int):
    # Check if the input is valid
    input_event = find_best_event_match(event, year)
    if not input_event:
        await interaction.response.send_message(
            "massive whiff on that event selection brosky, no event with that name and year combo"
        )
        return

    # Set the header and obtain the appropriate user information
    header = f"{get_vct_emoji('logo')} VCT {year} Pickem' [ {event.capitalize()} ] Leaderboard"
    event_points = points_from_event(input_event)
    if not event_points:
        await interaction.response.send_message(
            f"oi <@{REO_DEV_USER_ID}> you fucked somthing up you stupid ass"
        )
        return

    player_bullets = "\n".join(event_points)
    event_link = db.pickem_link_from_event_name(input_event)
    if not event_link:
        event_link = ""

    embed = discord.Embed(
        colour=BOT_EMBED_POINTS_COLOUR
        , description=player_bullets
        , title=header
        , url=event_link
    )
    embed.set_author(name=BOT_NAME, url=BOT_AUTHOR_URL)

    await interaction.response.send_message(embed=embed)


# /// POINTS
@bot.tree.command(name="leaderboard", description="Global Pickem leaderboard")
async def leaderboard(interaction: discord.Interaction) -> None:
    # Set the header and obtain the appropriate user information
    header = f":trophy: VCT Pickem' Global Leaderboard"
    leaderboard = star_leaderboard()
    if not leaderboard:
        await interaction.response.send_message(
            "oi <@{REO_DEV_USER_ID}> you fucked somthing up you stupid ass"
        )
        return
    
    embed = discord.Embed(
        colour=BOT_EMBED_LEADERBOARD_COLOUR
        , description=leaderboard
        , title=header
    )
    embed.set_author(name=BOT_NAME, url=BOT_AUTHOR_URL)

    await interaction.response.send_message(embed=embed)


# /// WHO VOTED WHO
@bot.tree.command(name="wvw", description="Who voted for who today or tomorrow or sometime in the future")
@app_commands.describe(
    region="Region for the matches (China, Americas, Emea, Pacific)",
    skip_amount="Number of days to skip into the future"
)
async def wvw(interaction: discord.Interaction, region: str = None, skip_amount: int = 0):
    # Validate region if provided
    if region:
        region = region.capitalize()
        valid_regions = ["China", "Americas", "Emea", "Pacific"]
        if region not in valid_regions:
            await interaction.response.send_message(
                f"nice typo, region has to be one of: {', '.join(valid_regions)}"
            )
            return

    date_lookup, upcoming_formatted = who_voted_who(region, skip_amount)
    if not upcoming_formatted:
        await interaction.response.send_message(f"oi <@{REO_DEV_USER_ID}> you fucked somthing up you stupid ass")
        return

    header = f"{get_vct_emoji("who")} VCT Who Voted Who — {date_lookup}"

    embed = discord.Embed(
        colour=BOT_EMBED_WVW_COLOUR,
        description=upcoming_formatted,
        title=header
    )
    embed.set_author(name=BOT_NAME, url=BOT_AUTHOR_URL)

    await interaction.response.send_message(embed=embed)


# /// UPDATE
update_funcs = {
    'pickems': update_current_pickems
    , 'matches': update_current_matches
    , 'votes': update_current_votes
    , 'all': update_all
}
async def execute_with_progress(interaction: discord.Interaction, update_function):
    # Send the initial progress message
    # Using interaction.response.send_message to immediately respond
    await interaction.response.send_message(f"{get_vct_emoji('miku_loading')} refreshing...")

    # Retrieve the message sent as the initial response.
    progress_message = await interaction.original_response()

    try:
        # Run the provided update function. If your update_function is async, add "await".
        update_function()

        # Delete the progress message and send a success follow-up.
        await progress_message.delete()
        await interaction.followup.send(f"{get_vct_emoji('miku_yay')} the fresh has been re ✅ for: {update_function.__name__.split("_")[-1]}")

    except Exception as e:
        # Delete the progress message and send an error follow-up.
        await progress_message.delete()
        await interaction.followup.send(
            f"{get_vct_emoji('miku_what')} <@{REO_DEV_USER_ID}> you fucking suck brosky:\n```{str(e)}```"
        )

@bot.tree.command(name="refresh", description="Update the database with fresh vlr data")
@app_commands.describe(
    update_func="Which dataset to refresh: 'pickems', 'matches', 'votes', or 'all' of them",
)
async def refresh(interaction: discord.Interaction, update_func: str):
    if update_func not in update_funcs:
        await interaction.response.send_message(
            "nice try jackass, update something sensible pls"
        )
        return

    func = update_funcs[update_func]
    await execute_with_progress(interaction, func)


# /// BRACKET
@bot.tree.command(name="bracket", description="View an event's bracket with player votes")
@app_commands.describe(
    event="Event name (Kickoff, Bangkok, Stage1, etc.)",
    region="Region for the matches (China, Americas, Emea, Pacific)",
    year="The number thing we keep track of every earth spin"
)
async def bracket(interaction: discord.Interaction, event: str, region: str = None, year: int = None):
    # Validate event input
    input_event = find_best_event_match(event)
    if not input_event:
        await interaction.response.send_message(
            "massive whiff on that event selection brosky, no event with that name"
        )
        return
    match_ev_id = db.get_event_id_from_name(input_event)

    # Validate region if provided
    if region:
        region = region.capitalize()
        valid_regions = ["China", "Americas", "Emea", "Pacific"]
        if region not in valid_regions:
            await interaction.response.send_message(
                f"nice typo, region has to be one of: {', '.join(valid_regions)}"
            )
            return
    # If region wasn't provided but event requires it, throw error
    if not db_logic.check_event_subs(match_ev_id):
        await interaction.response.send_message(
            "specify which region for selected event, or don't and read this again"
        )
        return

    ### BRACKET STUFF
    ### ???
    bracket_formatted = None  # bracket_for_event(match_ev_id, region, year)
    if not bracket_formatted:
        await interaction.response.send_message(
            f"oi <@{REO_DEV_USER_ID}> you fucked somthing up you stupid ass"
        )
        return
    ### i11

    header = f"{get_vct_emoji("pain")} VCT {year} [ {event.capitalize()} ] Bracket"
    event_link = db.pickem_link_from_event_name(input_event)
    if not event_link:
        event_link = ""

    embed = discord.Embed(
        colour=BOT_EMBED_BRACKET_COLOUR
        , description=bracket_formatted
        , title=header
        , url=event_link
    )
    embed.set_author(name=BOT_NAME, url=BOT_AUTHOR_URL)

    await interaction.response.send_message(embed=embed)



bot.run(DISCORD_BOT_TOKEN)