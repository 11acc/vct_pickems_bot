
# :purpose: Main script to run discord bot

import os
import random
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime

from db.db_instance import db
from db.queries import db_logic
from utils.emojis import get_vct_emoji, format_local
from utils.matching import find_best_event_match
from utils.bracket_id import get_bracket_id
from utils.event_assigner import star_tier_category
from services.points_for_event import points_from_event
from services.leaderboard import star_leaderboard
from services.who_voted_who import who_voted_who
from services.update import update_current_pickems, update_current_matches, update_current_votes, update_all
from services.bracket_for_event import bracket_for_event
from services.db_entries import add_new_player, update_player, add_new_star
from services.status import pickem_status


load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

REO_DEV_USER_ID = 229174776634015744
BOT_NAME = "reobot"
BOT_EMBED_POINTS_COLOUR = discord.Colour.from_rgb(48,92,222)
BOT_EMBED_LEADERBOARD_COLOUR = discord.Colour.from_rgb(234,232,111)
BOT_EMBED_WVW_COLOUR = discord.Colour.from_rgb(242,240,239)
BOT_EMBED_BRACKET_COLOUR = discord.Colour.from_rgb(207,159,255)
BOT_EMBED_E_WIN_COLOUR = discord.Colour.from_rgb(108,188,140)
BOT_EMBED_STATUS_COLOUR = discord.Colour.from_rgb(52,73,94)
BOT_AUTHOR_URL = "https://x.com/marthastewart/status/463333915739316224?mx=2"

# /// AUTO RESPONSE CONFIG
TARGET_USER_ID = 229174776634015744
AUTO_RESPONSE_ENABLED = False
CUSTOM_RESPONSE_MESSAGES = [
    "NAHHHH stfu bro you got COOKED 😭😭😭",
    "heretics fans in shambles rn 💀 this you? 🤡",
    "get absolutely rolled kiddo 💀 imagine believing in heretics LMAOOO couldn't be me fr fr",
    "hold this L, you'll need both hands 🤲💀",
    "caught in 4k lacking, career over 💀📸",
    "heretics fans in witness protection rn 😭😭",
    "that take aged like milk, rotten and stinky 😷🥛",
    "bro said 'trust me' and fumbled harder than ever 💀💀",
    "witnessing a live collapse, send help 🚑😭",
]
REACTION_EMOJIS = [
    # Regular Unicode emojisph
    "💀", "😭", "🤡",
    # Static custom emojis
    "cooked_rice", "cooked_stake", "matt40", "shut",
    # Animated custom emojis  
    "crying", "laugh_sphere", "lmao_pepe", "loop_lmao", "u_mad", "bruh"
]
# Message pool for non-repeating messages
available_messages = CUSTOM_RESPONSE_MESSAGES.copy()

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

# /// AUTO RESPONSE
@bot.event
async def on_message(message):
    # Don't respond to the bot's own messages
    if message.author == bot.user:
        return

    # Check if the message is from the target user and auto response is enabled
    if message.author.id == TARGET_USER_ID and AUTO_RESPONSE_ENABLED:
        try:
            global available_messages

            # If we've used all messages, refill the pool
            if not available_messages:
                available_messages = CUSTOM_RESPONSE_MESSAGES.copy()

            # Pick a random message from available ones and remove it
            random_message = random.choice(available_messages)
            available_messages.remove(random_message)

            await message.channel.send(random_message)

            # Add 4-5 random reactions to the user's message
            num_reactions = random.randint(4, 5)
            selected_emojis = random.sample(REACTION_EMOJIS, min(num_reactions, len(REACTION_EMOJIS)))

            for emoji_name in selected_emojis:
                # Check if it's a regular Unicode emoji or custom emoji
                if emoji_name in ["💀", "😭", "🤡"]:
                    # Regular Unicode emoji
                    await message.add_reaction(emoji_name)
                else:
                    # Custom server emoji
                    emoji = discord.utils.get(message.guild.emojis, name=emoji_name)
                    if emoji:
                        await message.add_reaction(emoji)
                    else:
                        print(f"Custom emoji '{emoji_name}' not found in server")

        except discord.HTTPException as e:
            print(f"Failed to respond to {message.author}: {e}")

    # Process commands (important to keep this)
    await bot.process_commands(message)


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
            f"{get_vct_emoji('chillin')} massive whiff on that event selection brosky, no event with that name and year combo"
        )
        return

    # Set the header and obtain the appropriate user information
    header = f"{get_vct_emoji('vct_masters')} VCT {year} Pickem' [ {event.capitalize()} ] Leaderboard"
    event_points = points_from_event(input_event)
    if not event_points:
        await interaction.response.send_message(
            f"{get_vct_emoji('miku_what')} oi <@{REO_DEV_USER_ID}> you fucked somthing up you stupid ass"
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


# /// LEADERBOARD
@bot.tree.command(name="leaderboard", description="Global Pickem leaderboard")
async def leaderboard(interaction: discord.Interaction) -> None:
    # Set the header and obtain the appropriate user information
    header = f":trophy: VCT Pickem' Global Leaderboard"
    leaderboard = star_leaderboard()
    if not leaderboard:
        await interaction.response.send_message(
            f"{get_vct_emoji('miku_what')} oi <@{REO_DEV_USER_ID}> you fucked somthing up you stupid ass"
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
                f"{get_vct_emoji('chillin')} nice typo, region has to be one of: {', '.join(valid_regions)}"
            )
            return

    date_lookup, upcoming_formatted = who_voted_who(region, skip_amount)
    if not upcoming_formatted:
        await interaction.response.send_message(f"{get_vct_emoji('miku_what')} oi <@{REO_DEV_USER_ID}> you fucked somthing up you stupid ass")
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


# /// BRACKET PREP
async def execute_bracket_with_progress(interaction: discord.Interaction, match_ev_id: int, input_event: str, year: int, region: str = None):
    # Send the initial progress message
    await interaction.response.send_message(f"{get_vct_emoji('miku_loading')} generating bracket...")

    # Retrieve the message sent as the initial response
    progress_message = await interaction.original_response()

    try:
        # Generate bracket image
        bracket_for_event(match_ev_id, year, region)

        # Locate and build paths for the image
        bracket_file_name = f'{get_bracket_id(match_ev_id, region, year)}.png'
        bracket_dir = os.path.join(os.path.dirname(__file__), "bracket")
        imgs_dir = os.path.join(bracket_dir, "generated_imgs")
        file_path = os.path.join(imgs_dir, bracket_file_name)

        file = discord.File(file_path, filename=bracket_file_name)

        # Prepare the embed
        h_region = f"{get_vct_emoji(region)}" if region else ""
        header = f"{get_vct_emoji("pain")} VCT {year} [ {input_event} ] {h_region} Bracket"
        event_link = db.pickem_link_from_event_name(input_event)
        if not event_link:
            event_link = ""

        embed = discord.Embed(
            colour=BOT_EMBED_BRACKET_COLOUR,
            title=header,
            url=event_link
        )
        embed.set_author(name=BOT_NAME, url=BOT_AUTHOR_URL)
        embed.set_image(url=f"attachment://{bracket_file_name}")

        # Delete the progress message and send the bracket
        await progress_message.delete()
        await interaction.followup.send(file=file, embed=embed)

    except Exception as e:
        # Delete the progress message and send an error follow-up
        await progress_message.delete()
        await interaction.followup.send(
            f"{get_vct_emoji('miku_what')} <@{REO_DEV_USER_ID}> you fucking suck brosky:\n```{str(e)}```"
        )

# /// BRACKET COMMAND
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
            f"{get_vct_emoji('chillin')} massive whiff on that event selection brosky, no event with that name"
        )
        return
    match_ev_id = db.get_event_id_from_name(input_event)

    # Validate region if provided
    if region:
        region = region.capitalize()
        valid_regions = ["China", "Americas", "Emea", "Pacific"]
        if region not in valid_regions:
            await interaction.response.send_message(
                f"{get_vct_emoji('chillin')} nice typo, region has to be one of: {', '.join(valid_regions)}"
            )
            return
    # If region wasn't provided but event requires it, throw error
    if db_logic.check_event_subs(match_ev_id) and not region:
        await interaction.response.send_message(
            f"{get_vct_emoji('chillin')} specify which region for selected event, or don't and read this again"
        )
        return

    # Validate year
    if not year:
        year = datetime.now().year

    # Execute bracket generation with progress
    await execute_bracket_with_progress(interaction, match_ev_id, input_event, year, region)


# /// ADD PLAYER
@bot.tree.command(name="add_player", description="Add a new player to the database")
@app_commands.describe(
    name="The visaul name",
    vlr_user="VLR username",
    local="Choose a country",
    icon_url="URL for your profile icon"
)
async def add_player(interaction: discord.Interaction, name: str, vlr_user: str, local: str, icon_url: str):
    # Validate local
    formatted_local = format_local(local)
    if not formatted_local:
        await interaction.response.send_message(
            f"{get_vct_emoji('chillin')} have no idea where that local is buddy"
        )
        return

    # Add new player to db
    if not add_new_player(name, vlr_user, formatted_local, icon_url):
        await interaction.response.send_message(
            f"{get_vct_emoji('miku_what')} oi <@{REO_DEV_USER_ID}> you fucked somthing up you stupid ass"
        )
        return

    await interaction.response.send_message(
        f"{get_vct_emoji('yay')} successfully added new player to active db"
    )
    # print active users


# /// UPDATE PLAYER
@bot.tree.command(name="update_player", description="Update a player's info")
@app_commands.describe(
    existing_player="Name of player to change",
    new_name="The visaul name",
    local="A country",
    icon_url="URL for a profile icon"
)
async def update_player_command(interaction: discord.Interaction, existing_player: str, new_name: str = None, local: str = None, icon_url: str = None):
    # Really?
    if not new_name and not local and not icon_url:
        await interaction.response.send_message(
            f"{get_vct_emoji('bruh')} really? lmao"
        )
        return

    # Find existing player
    existing_player_id = db.get_player_id_from_name(existing_player)
    if not existing_player_id:
        print(f"Failed to identify existing player")
        return False

    # Validate local
    if local:
        local = format_local(local)
        if not local:
            await interaction.response.send_message(
                f"{get_vct_emoji('chillin')} have no idea where that local is buddy"
            )
            return

    # Update player in db
    if not update_player(existing_player_id, new_name, local, icon_url):
        await interaction.response.send_message(
            f"{get_vct_emoji('madge_time')} failed to update player '{existing_player}', probably <@{REO_DEV_USER_ID}>'s fault"
        )
        return

    await interaction.response.send_message(
        f"{get_vct_emoji('yay')} successfully did the thing to '{existing_player}' and now became the new thing you did at some point in time"
    )
    # print active users


# /// STATUS
@bot.tree.command(name="status", description="What event is happening? Who is playing?")
async def status(interaction: discord.Interaction) -> None:
    ongoing_title, status_players = pickem_status()
    if not status_players:
        await interaction.response.send_message(
            f"{get_vct_emoji('miku_what')} oi <@{REO_DEV_USER_ID}> you fucked somthing up you stupid ass"
        )
        return

    embed = discord.Embed(
        colour=BOT_EMBED_STATUS_COLOUR
        , description=status_players
        , title=ongoing_title
    )
    embed.set_author(name=BOT_NAME, url=BOT_AUTHOR_URL)

    await interaction.response.send_message(embed=embed)


# /// AUTO RESPONSE
@bot.tree.command(name="dev_msgtarget", description="Set the user to auto-respond to (only me mf don't try)")
@app_commands.describe(user="The user to target for auto-responses")
async def set_target_user(interaction: discord.Interaction, user: discord.Member):
    if interaction.user.id != REO_DEV_USER_ID:
        await interaction.response.send_message("stop trying lil bro, you can't use this")
        return

    global TARGET_USER_ID
    TARGET_USER_ID = user.id
    await interaction.response.send_message(f"Target user set to {user.mention}", ephemeral=True)

@bot.tree.command(name="dev_msgstop", description="Toggle auto response service on/off (only me mf don't try)")
async def toggle_auto_response(interaction: discord.Interaction):
    if interaction.user.id != REO_DEV_USER_ID:
        await interaction.response.send_message("stop trying lil bro, you can't use this")
        return

    global AUTO_RESPONSE_ENABLED, available_messages
    AUTO_RESPONSE_ENABLED = not AUTO_RESPONSE_ENABLED

    # Reset message pool when toggling
    available_messages = CUSTOM_RESPONSE_MESSAGES.copy()

    status = "enabled" if AUTO_RESPONSE_ENABLED else "disabled"
    await interaction.response.send_message(f"Auto response service is now **{status}**")



# /// EVENT WINNER
@bot.tree.command(name="dev_event_winner", description="Finalise event winner")
@app_commands.describe(
    event_name="Event in question",
    year="The number of spinny things thing",
    player_name="Winner player name"
)
async def event_winner(interaction: discord.Interaction, event_name: str, year: int, player_name: str):
    if interaction.user.id != REO_DEV_USER_ID:
        await interaction.response.send_message("stop trying lil bro, you can't use this")
        return

    # Check if the event is valid
    input_event = find_best_event_match(event_name, year)
    if not input_event:
        await interaction.response.send_message(
            f"{get_vct_emoji('chillin')} massive whiff on that event selection brosky, no event with that name and year combo"
        )
        return
    match_ev_id = db.get_event_id_from_name(input_event)

    # Check if event has already been won
    if not db.check_event_star(match_ev_id):
        await interaction.response.send_message(
            f"{get_vct_emoji('bruh')} event's already won... awkward"
        )
        return

    # Validate player
    player_id = db.get_player_id_from_name(player_name)
    if not player_id:
        await interaction.response.send_message(
            f"{get_vct_emoji('chillin')} massive whiff on that player name, doesn't exist"
        )
        return

    # Add new star to db
    if not add_new_star(player_id, match_ev_id):
        await interaction.response.send_message(
            f"{get_vct_emoji('miku_what')} oi <@{REO_DEV_USER_ID}> you fucked somthing up you stupid ass"
        )
        return

    # Check for event star tier
    star_tier = star_tier_category(match_ev_id)
    # Gif location
    BASE_DIR = os.path.dirname(__file__)
    gif_file = f"congrats_{star_tier}.gif"
    gif_path = os.path.join(BASE_DIR, "assets", "congrats_gifs", gif_file)
    file = discord.File(gif_path, filename=gif_file)

    header = f"{get_vct_emoji('celebrate')} Congratulations **{player_name.capitalize()}**!!"
    description = f"You won {get_vct_emoji(f"vct_{star_tier}")} VCT {star_tier.capitalize()} {event_name.capitalize()}, here is your glorified star png"
    embed = discord.Embed(
        colour=BOT_EMBED_E_WIN_COLOUR,
        description=description,
        title=header
    )
    embed.set_author(name=BOT_NAME, url=BOT_AUTHOR_URL)
    embed.set_image(url=f"attachment://{gif_file}")

    await interaction.response.send_message(embed=embed, file=file)


bot.run(DISCORD_BOT_TOKEN)