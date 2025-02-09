#
import sys
#
from engine.interaction_system import BasicTerminalInteractionSystem
from engine.engine_classes import load_interactive_fiction_model_from_file, Game
from command_parsing.command_parsing import parse_command
from engine.engine_commands import ALL_COMMANDS_FUNCTIONS, introduce_game


#
if __name__ == "__main__":

    #
    if len(sys.argv) != 2:
        raise SyntaxError(f"Error: bad arguments given to this application !\n\nMust be used like that : \n\t`python {sys.argv[0]} path_to_game_or_save_file.json`\n\n")

    #
    game: Game = load_interactive_fiction_model_from_file(filepath=sys.argv[1])
    interaction_system: BasicTerminalInteractionSystem = BasicTerminalInteractionSystem()

    #
    introduce_game(game=game, interaction_system=interaction_system)

    #
    nb_players: int = len(game.players)

    #
    if nb_players == 0:
        raise RuntimeError(f"Error: No player for the game : `{game.game_name}` from `{game.game_author}`")

    #
    current_player: int = 0

    #
    while interaction_system.running:
        #
        if nb_players > 1:
            interaction_system.write_to_output(txt=f"\n\nPlayer: {game.players[current_player]}\n\n")
        #
        command_input: str = interaction_system.ask_input()

        #
        parsed_command: list[str] = parse_command(command_input=command_input)

        #
        if not parsed_command or parsed_command[0] not in ALL_COMMANDS_FUNCTIONS:
            #
            interaction_system.write_to_output(txt="Unkown Command\n")
            continue

        #
        ALL_COMMANDS_FUNCTIONS[parsed_command[0]](game, interaction_system, parsed_command, game.players[current_player], False)

        #
        if parsed_command[0] == "QUIT":
            break

        #
        if nb_players > 1:
            current_player = (current_player + 1) % nb_players

    #
    interaction_system.write_to_output(txt="\nSystem Exit\nGoodbye.")
    #
    if hasattr(interaction_system, "flush_output"):
        interaction_system.flush_output()