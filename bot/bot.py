import discord
from discord.ext import commands
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import asyncio
import logging
import os
from collections import defaultdict
from config.settings import TOKEN, DISCORD_CHANNEL_ID, REPLAYS_FOLDER
from .replay_handler import extract_game_data, get_game_result
from .openai_integration import generate_analysis_with_openai
from .utils import get_latest_replay

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Configure bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

async def upload_replay(file_path):
    """Uploads the replay file and posts the build order and game result."""
    try:
        channel = bot.get_channel(DISCORD_CHANNEL_ID)
        if not channel:
            logging.error(f"Discord channel with ID {DISCORD_CHANNEL_ID} not found.")
            return

        if not os.path.exists(file_path):
            logging.error(f"Replay file does not exist: {file_path}")
            return

        # Upload the replay file
        try:
            with open(file_path, "rb") as file:
                replay_message = await channel.send(file=discord.File(file, filename=os.path.basename(file_path)))
        except discord.HTTPException as e:
            logging.error(f"Failed to upload replay file: {e}")
            return

        # Extract game data
        player_data, replay = extract_game_data(file_path)
        if not player_data or not replay:
            logging.error("Failed to extract game data.")
            return

        # Ensure exactly two players are displayed
        players = list(player_data.keys())
        if len(players) < 2:
            # Post staged "analyzing replay" messages with delays
            analysis_message = await channel.send("```>>> ANALYSIS INITIATED...```")
            await asyncio.sleep(2)  # Wait for 2 seconds

            await analysis_message.edit(content="```>>> ANALYSIS INITIATED...\n>>> PROCESSING DATA STREAM... COMPLETE.```")
            await asyncio.sleep(2)  # Wait for 2 seconds

            # Post the error message
            error_message = (
                ">>> ANALYSIS INITIATED...\n"
                ">>> PROCESSING DATA STREAM... COMPLETE.\n\n"
                ">>> ERROR: REPLAY ANALYSIS FAILED.\n"
                ">>> REASON: REPLAY CONTAINS ONLY ONE PLAYER. ATLAS AI REQUIRES A 1V1 REPLAY FOR ANALYSIS.\n"
                ">>> END OF REPORT."
            )
            await analysis_message.edit(content=f"```diff\n{error_message}\n```")
            return

        player1, player2 = players
        order1 = player_data[player1]["build_order"]
        order2 = player_data[player2]["build_order"]

        # Group identical units created at the same time
        def group_units(units):
            grouped = defaultdict(list)
            for time, supply, unit in units:
                if supply > 200:  # Stop adding units once supply reaches 200
                    break
                grouped[(time, supply, unit)].append((time, supply, unit))
            return grouped

        grouped_order1 = group_units(order1)
        grouped_order2 = group_units(order2)

        # Prepare the table rows
        formatted_rows = []
        max_length = max(len(grouped_order1), len(grouped_order2))

        for i in range(max_length):
            # Player 1
            if i < len(grouped_order1):
                key1 = list(grouped_order1.keys())[i]
                time1, supply1, unit1 = key1
                count1 = len(grouped_order1[key1])
                unit1_display = f"{unit1} x {count1}" if count1 > 1 else unit1
                row1 = f"{time1//60:02}:{time1%60:02}   {supply1:>3}   {unit1_display}"
            else:
                row1 = ""

            # Player 2
            if i < len(grouped_order2):
                key2 = list(grouped_order2.keys())[i]
                time2, supply2, unit2 = key2
                count2 = len(grouped_order2[key2])
                unit2_display = f"{unit2} x {count2}" if count2 > 1 else unit2
                row2 = f"{time2//60:02}:{time2%60:02}   {supply2:>3}   {unit2_display}"
            else:
                row2 = ""

            formatted_rows.append(f"{row1:<40}   {row2}")

        # Create the final message
        map_name = replay.map_name
        result = get_game_result(replay, 'jaycujoh')  # Use your in-game name here
        table = (
            f"Map: {map_name} ({result})\n\n"
            f"{player1} ({player_data[player1]['race']}){' ' * (40 - len(player1) - len(player_data[player1]['race']))}   {player2} ({player_data[player2]['race']})\n"
            f"{'-' * 40}   {'-' * 40}\n"
            + "\n".join(formatted_rows)
        )

        # Save the build order to a .txt file
        txt_file_path = os.path.join(REPLAYS_FOLDER, "build_order.txt")
        with open(txt_file_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(table)

        # Upload the .txt file
        with open(txt_file_path, "rb") as txt_file:
            await channel.send(file=discord.File(txt_file, filename="build_order.txt"))

        # Post staged "analyzing replay" messages with delays
        analysis_message = await channel.send("```>>> ANALYSIS INITIATED...```")
        await asyncio.sleep(2)  # Wait for 2 seconds

        await analysis_message.edit(content="```>>> ANALYSIS INITIATED...\n>>> PROCESSING DATA STREAM... COMPLETE.```")
        await asyncio.sleep(2)  # Wait for 2 seconds

        await analysis_message.edit(content="```>>> ANALYSIS INITIATED...\n>>> PROCESSING DATA STREAM... COMPLETE.\n>>> COMMENCING REPORT GENERATION...```")
        await asyncio.sleep(2)  # Wait for 2 seconds

        # Generate and post the analysis using OpenAI
        analysis = generate_analysis_with_openai(player_data, replay, 'jaycujoh')  # Use your in-game name here

        # If the analysis failed after retries, notify the user
        if "ERROR: ANALYSIS FAILED. REBOOTING ATLAS AI..." in analysis:
            await analysis_message.edit(content=analysis)
            return

        # Split the analysis into chunks of 2000 characters or less
        chunk_size = 2000
        analysis_chunks = [analysis[i:i + chunk_size] for i in range(0, len(analysis), chunk_size)]

        # Edit the original message with the first chunk
        await analysis_message.edit(content=analysis_chunks[0])

        # Send the remaining chunks as new messages
        for chunk in analysis_chunks[1:]:
            await channel.send(chunk)

        # Clean up the .txt file
        os.remove(txt_file_path)

    except Exception as e:
        logging.error(f"Error uploading replay: {e}")

# File watcher class
class ReplayHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".SC2Replay"):
            logging.info(f"New replay detected: {event.src_path}")
            bot.loop.create_task(upload_replay(event.src_path))

@bot.event
async def on_ready():
    logging.info(f"Logged in as {bot.user}")

    # Start monitoring for replays
    try:
        event_handler = ReplayHandler()
        observer = Observer()
        observer.schedule(event_handler, REPLAYS_FOLDER, recursive=True)
        observer.start()
        logging.info("Watching for new replays...")
    except Exception as e:
        logging.error(f"Error starting file watcher: {e}")
        logging.basicConfig(level=logging.DEBUG)