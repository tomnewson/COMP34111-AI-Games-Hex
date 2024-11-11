import argparse
import csv
import importlib
import logging
import re
import traceback
from datetime import datetime
from glob import glob
from itertools import permutations, repeat
from multiprocessing import Pool, TimeoutError

from src.Colour import Colour
from src.Game import Game, format_result
from src.Player import Player
from src.EndState import EndState

# Set up logger
logging.basicConfig(
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# set the timeout limit in seconds
TIME_OUT_LIMIT = 1

fieldnames = [
    "player1",
    "player2",
    "winner",
    "win_method",
    "player1_move_time",
    "player2_move_time",
    "player1_turns",
    "player2_turns",
    "total_turns",
    "total_game_time",
]
time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")


def run(games: list[tuple[str, str]]):
    """Run the tournament. This uses multiprocessing to dispatch each of the game.
    The results are written to a csv file.
    The error will be written to a log file.

    Args:
        games (list[tuple[str, str]]): all the games pair that need to be played
    """
    resultFilePath = f"game_results_{time}.csv"
    errorGameListPath = f"error_game_list_{time}.log"

    with open(resultFilePath, "w", newline="") as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        writer.writeheader()

    # Run the tournament
    gameResults = []
    with Pool() as pool:
        # using apply_async to apply the game function to the player pair
        result = [
            pool.apply_async(
                run_match,
                (agentPair,),
            )
            for agentPair in games
        ]

        # gather all the results. Error of a game is captured and written to a log file.
        for i, gameResult in enumerate(result):
            try:
                r = gameResult.get(timeout=TIME_OUT_LIMIT)
                with open(resultFilePath, "a", newline="") as csvFile:
                    writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
                    writer.writerow(r)
                gameResults.append(r)

            except TimeoutError as error:
                logger.warning(f"Timed out between {games[i]}")
                with open(errorGameListPath, "a") as errFile:
                    errFile.write(f"{games[i]}, {repr(error)}\n")

            except Exception as error:
                logger.error(f"Exception occurred between {games[i]}: {repr(error)}")
                logger.error(traceback.format_exc())
                with open(errorGameListPath, "a") as errFile:
                    errFile.write(f"{games[i]}, {repr(error), {traceback.format_exc()}}\n")

    export_stats(gameResults)


def run_match(agentPair: tuple[str, str]) -> dict:
    """Run a single game between two agents. It parses the agent string pair
    and creates the player objects.
    """

    player1, player2 = agentPair
    logger.info(f"starting game between {player1} and {player2}")

    player1_class = None
    player2_class = None

    try:
        p1_path, p1_class = player1.split(" ")
        p1 = importlib.import_module(p1_path)
        # this should return the group name
        p1Name = player1.split(".")[1]
        player1_class = Player(name=p1Name, agent=getattr(p1, p1_class)(Colour.RED),)
    except ModuleNotFoundError as error:
        logger.error(f"Exception occured importing {player1}, agent file could not be imported: {repr(error)}")
        logger.error(traceback.format_exc())
    except Exception as error:
        logger.error(f"Exception occured importing {player1}: {repr(error)}")
        logger.error(traceback.format_exc())

    try:
        p2_path, p2_class = player2.split(" ")
        p2 = importlib.import_module(p2_path)
        # this should return the group name
        p2Name = player2.split(".")[1]
        player2_class = Player(name=p2Name,agent=getattr(p2, p2_class)(Colour.BLUE),)
    except ModuleNotFoundError as error:
        logger.error(f"Exception occured importing {player1}, agent file could not be imported: {repr(error)}")
        logger.error(traceback.format_exc())
    except Exception as error:
        logger.error(f"Exception occured importing {player1}: {repr(error)}")
        logger.error(traceback.format_exc())

    if player1_class is None and player2_class is None:
        logger.info(f"Both agents failed to load for game between {player1} and {player2}.")
        result = format_result(
            player1_name=player1,
            player2_name=player2,
            winner="",
            win_method=EndState.FAILED_LOAD,
            player_1_move_time="",
            player_2_move_time="",
            player_1_turn="",
            player_2_turn="",
            total_turns="",
            total_time=""
        )
    elif player1_class is None:
        logger.info(f"Agent {player1} failed to load, {player2} wins.")
        result = format_result(
            player1_name=player1,
            player2_name=player2_class.name,
            winner=player2_class.name,
            win_method=EndState.FAILED_LOAD,
            player_1_move_time="",
            player_2_move_time="",
            player_1_turn="",
            player_2_turn="",
            total_turns="",
            total_time=""
        )
    elif player2_class is None:
        logger.info(f"Agent {player2} failed to load, {player1} wins.")
        result = format_result(
            player1_name=player1_class.name,
            player2_name=player2,
            winner=player1_class.name,
            win_method=EndState.FAILED_LOAD,
            player_1_move_time="",
            player_2_move_time="",
            player_1_turn="",
            player_2_turn="",
            total_turns="",
            total_time=""
        )
    else:
        # the getattr is to get the class from the module, then instantiate it with the colour
        g = Game(
            player1=player1_class,
            player2=player2_class,
            board_size=11,
            silent=True,
        )
        result = g.run()
        logger.info(f"Game complete normally between {player1} and {player2}")

    return result


def export_stats(gameResults: list[dict]):
    playerStats = {}

    statEntry = {
        "matches": 0,
        "wins": 0,
        "win_rate": 0,
        "total_move_time": 0,
        "total_moves": 0,
        "average_move_time": 0,
        "illegal_moves_loss": 0,
        "time_out_loss": 0,
        "regular_loss": 0,
    }

    # populate the player stats dictionary
    for result in gameResults:
        for player in [result["player1"], result["player2"]]:
            if player not in playerStats:
                playerStats[player] = statEntry.copy()

    # fill in the data
    for result in gameResults:
        player1 = result["player1"]
        player2 = result["player2"]
        winner = result["winner"]

        if result["win_method"] == EndState.FAILED_LOAD:
            if winner == "":
                continue
            else:
                playerStats[winner]["matches"] += 1
                playerStats[winner]["wins"] += 1
        else:
            if winner == player1:
                loser = player2
            else:
                loser = player1

            playerStats[player1]["matches"] += 1
            playerStats[player2]["matches"] += 1
            playerStats[player1]["total_move_time"] += result["player1_move_time"]
            playerStats[player2]["total_move_time"] += result["player2_move_time"]
            playerStats[player1]["total_moves"] += result["player1_turns"]
            playerStats[player2]["total_moves"] += result["player2_turns"]

            playerStats[winner]["wins"] += 1
            playerStats[loser]["illegal_moves_loss"] += 1 if result["win_method"] == "BAD_MOVE" else 0
            playerStats[loser]["time_out_loss"] += 1 if result["win_method"] == "TIMEOUT" else 0
            playerStats[loser]["regular_loss"] += 1 if result["win_method"] == "WIN" else 0

    for player, stats in playerStats.items():
        playerStats[player]["win_rate"] = stats["wins"] / stats["matches"] if stats["matches"] > 0 else 0
        playerStats[player]["average_move_time"] = (
            stats["total_move_time"] / stats["total_moves"] if stats["total_moves"] > 0 else 0
        )

    with open(f"game_stat_{time}.csv", "w", newline="") as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(["player"] + list(statEntry.keys()))
        for player, stats in playerStats.items():
            writer.writerow([player] + list(stats.values()))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the Hex Tournament. Will create the game stat file and all the game log. In the event of crashing, the error event will go into the error log"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-p",
        "--partialTournament",
        type=str,
        help="Path to a newline separated list of int, which are the group number. Each line will play against every other group",
    )

    args = parser.parse_args()

    def extract_group_number(path):
        if match := re.search(r"Group(\d+)", path):
            return int(match.group(1))
        else:
            raise ValueError(f"Invalid path {path}")

    agents = {}
    for p in sorted(glob("agents/Group*/cmd.txt"), key=extract_group_number):
        with open(p, "r") as f:
            agent = f.read().split("\n")[0].strip()
            if p.split('/')[1] != agent.split('.')[1]:
                print(f"Agent location {agent} does not match group number for path {p}, agent will not be loaded.")
            else:
                agents[extract_group_number(p)] = agent

    games = []
    games = list(permutations(agents.values(), 2))

    # if running a partial tournament, the following will overwrite the games list
    # Each item on the partial list will play against every agent in the agents directory
    if args.partialTournament:
        with open(args.partialTournament) as f:
            for line in f:
                # the given line as player A
                games.extend(zip(repeat(agents[int(line)]), list(agents.values()), strict=False))
                # the given line as player B
                games.extend(zip(agents.values(), repeat(agents[int(line)]), strict=False))

        # remove all repeat and self play
        games = [(i, j) for i, j in list(set(games)) if i != j]

    run(games)
