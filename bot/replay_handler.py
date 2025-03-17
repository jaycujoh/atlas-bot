import os
import sc2reader
from collections import defaultdict
import logging
from .utils import format_unit_name

def extract_game_data(replay_path):
    """Extracts key metrics from the replay file using sc2reader."""
    try:
        if not os.path.exists(replay_path):
            logging.error(f"Replay file does not exist: {replay_path}")
            return None, None

        # Load the replay file
        replay = sc2reader.load_replay(replay_path)

        # Dictionary to store player data
        player_data = {}

        # Define units and buildings to exclude (e.g., Larva, MULE, Drones, Probes, SCVs, Creep Tumors)
        excluded_units = {"Larva", "MULE", "AutoTurret", "Broodling", "InfestedTerran", "Drone", "Probe", "SCV", "CreepTumor", "CreepTumorQueen"}

        # Iterate through players in the replay
        for player in replay.players:
            player_data[player.name] = {
                "build_order": [],  # Stores units/buildings and their creation times
                "race": player.play_race,  # Player race
                "supply": [],  # Stores supply at the time of unit creation
                "resources": [],  # Stores resource collection over time
                "combat_events": [],  # Stores combat-related events
                "unit_deaths": [],  # Stores unit deaths
                "ability_usage": [],  # Stores ability usage
            }

            logging.info(f"Processing player: {player.name} ({player.play_race})")

            # Track supply and resources over time
            supply_events = []
            resource_events = []
            current_supply = 0
            current_minerals = 0
            current_gas = 0

            # Iterate through events in the replay
            for event in replay.events:
                try:
                    # Track supply changes
                    if event.name == "PlayerStatsEvent" and event.player == player:
                        current_supply = int(event.food_used)  # Convert supply to a whole number
                        current_minerals = event.minerals_current
                        current_gas = event.vespene_current
                        supply_events.append((event.second, current_supply))
                        resource_events.append((event.second, current_minerals, current_gas))

                    # Check if the event is related to the current player
                    if hasattr(event, 'unit') and event.unit.owner == player:
                        # Handle UnitBornEvent (units created or spawned)
                        if event.name == "UnitBornEvent":
                            unit_name = event.unit_type_name
                            if (
                                unit_name
                                and unit_name not in excluded_units  # Exclude unwanted units
                                and event.second > 0  # Exclude units created at game start (time 0)
                            ):
                                # Format the unit name to include spaces
                                formatted_unit_name = format_unit_name(unit_name)
                                # Find the player's supply at the time of the event
                                supply_at_time = next((supply for time, supply in supply_events if time >= event.second), current_supply)
                                player_data[player.name]["build_order"].append((event.second, supply_at_time, formatted_unit_name))
                                logging.info(f"Unit Born: {formatted_unit_name}, Time: {event.second}, Supply: {supply_at_time}, Player: {player.name}")

                        # Handle UnitInitEvent (units or buildings that begin construction)
                        elif event.name == "UnitInitEvent":
                            unit_name = event.unit_type_name
                            if (
                                unit_name
                                and unit_name not in excluded_units  # Exclude unwanted units
                                and event.second > 0  # Exclude units created at game start (time 0)
                            ):
                                # Format the unit name to include spaces
                                formatted_unit_name = format_unit_name(unit_name)
                                # Find the player's supply at the time of the event
                                supply_at_time = next((supply for time, supply in supply_events if time >= event.second), current_supply)
                                player_data[player.name]["build_order"].append((event.second, supply_at_time, formatted_unit_name))
                                logging.info(f"Unit Init: {formatted_unit_name}, Time: {event.second}, Supply: {supply_at_time}, Player: {player.name}")

                        # Handle UnitDiedEvent (units destroyed)
                        elif event.name == "UnitDiedEvent":
                            unit_name = event.unit.name
                            player_data[player.name]["unit_deaths"].append((event.second, unit_name))
                            logging.info(f"Unit Died: {unit_name}, Time: {event.second}, Player: {player.name}")

                    # Handle Upgrade events (e.g., Glial Reconstitution, Lair, Hydralisk Speed)
                    if event.name == "UpgradeEvent" and event.player == player:
                        upgrade_name = event.upgrade_type_name
                        if upgrade_name and event.second > 0:  # Exclude upgrades at game start
                            # Format the upgrade name to include spaces
                            formatted_upgrade_name = format_unit_name(upgrade_name)
                            # Find the player's supply at the time of the event
                            supply_at_time = next((supply for time, supply in supply_events if time >= event.second), current_supply)
                            player_data[player.name]["build_order"].append((event.second, supply_at_time, formatted_upgrade_name))
                            logging.info(f"Upgrade Started: {formatted_upgrade_name}, Time: {event.second}, Supply: {supply_at_time}, Player: {player.name}")

                    # Handle Ability usage
                    if event.name == "AbilityEvent" and event.player == player:
                        ability_name = event.ability_name
                        player_data[player.name]["ability_usage"].append((event.second, ability_name))
                        logging.info(f"Ability Used: {ability_name}, Time: {event.second}, Player: {player.name}")

                except Exception as e:
                    logging.warning(f"Error processing event: {e}")

            # Add resource collection data
            player_data[player.name]["resources"] = resource_events

        return player_data, replay

    except Exception as e:
        logging.error(f"Error extracting game data: {e}")
        return None, None

def get_game_result(replay, player_name):
    """Determines if the game was a victory or defeat for the specified player."""
    try:
        for player in replay.players:
            if player.name == player_name:
                if player.result == "Win":
                    return "Victory"
                else:
                    return "Defeat"
        return "Unknown"
    except Exception as e:
        logging.error(f"Error determining game result: {e}")
        return "Unknown"