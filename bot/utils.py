import os
import re
import logging

def get_latest_replay(replays_folder):
    """Finds the most recent SC2Replay file."""
    try:
        if not os.path.exists(replays_folder):
            logging.error(f"Replays folder does not exist: {replays_folder}")
            return None

        files = [f for f in os.listdir(replays_folder) if f.endswith(".SC2Replay")]
        if not files:
            logging.warning("No replay files found.")
            return None

        latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(replays_folder, f)))
        logging.info(f"Latest replay file: {latest_file}")
        return os.path.join(replays_folder, latest_file)

    except Exception as e:
        logging.error(f"Error finding latest replay: {e}")
        return None

def format_unit_name(unit_name):
    """Adds spaces between words in unit names (e.g., 'SpawningPool' -> 'Spawning Pool')."""
    return re.sub(r"([A-Z])", r" \1", unit_name).strip()