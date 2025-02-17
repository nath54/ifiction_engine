#
from typing import Optional
#
import sys
#
from engine.interaction_system import BasicTerminalInteractionSystem
from engine.engine_classes import load_interactive_fiction_model_from_file, Game, Room
from engine.command_parsing import parse_command
import engine.engine_classes_commands as ecc
from engine.engine_commands import ALL_COMMANDS_FUNCTIONS, introduce_game, after_each_player_turn, after_all_players_turn, execute_C_LOOKAROUND, get_room_of_player


#
if __name__ == "__main__":

    #
    if len(sys.argv) != 2:
        raise SyntaxError(f"Error: bad arguments given to this application !\n\nMust be used like that : \n\t`python {sys.argv[0]} path_to_game_or_save_file.json`\n\n")

    #
    game: Game = load_interactive_fiction_model_from_file(filepath=sys.argv[1])
    interaction_system: BasicTerminalInteractionSystem = BasicTerminalInteractionSystem(game=game)

    #
    introduce_game(game=game, interaction_system=interaction_system)

    #
    if game.nb_players == 0:
        raise RuntimeError(f"Error: No player for the game : `{game.game_name}` from `{game.game_author}`")

    #
    player_id: str
    for player_id in game.players:
        #
        room: Room = get_room_of_player(game=game, player_id=player_id)
        #
        if player_id not in room.things_inside:
            room.things_inside[player_id] = 1

    #
    while interaction_system.running:
        #
        if game.nb_players > 1:
            #
            interaction_system.write_to_output(txt=f"\n\n### Player: {game.players[game.current_player]}\n\n")
            #
            if game.nb_turns == 0:
                #
                execute_C_LOOKAROUND(game=game, interaction_system=interaction_system, command=ecc.Command(command_name="C_LOOKAROUND"), player_id=game.players[game.current_player])
        #
        elif game.nb_turns == 0:
                #
                execute_C_LOOKAROUND(game=game, interaction_system=interaction_system, command=ecc.Command(command_name="C_LOOKAROUND"), player_id=game.players[game.current_player])

        #
        command_input: str = interaction_system.ask_input()

        #
        parsed_command: Optional[ecc.Command] = parse_command(command_input=command_input)

        #
        if not parsed_command or parsed_command.command_name not in ALL_COMMANDS_FUNCTIONS:
            #
            interaction_system.write_to_output(txt="Unkown Command\n")
            continue

        #
        ALL_COMMANDS_FUNCTIONS[parsed_command.command_name](game, interaction_system, parsed_command, game.players[game.current_player], False)

        #
        if parsed_command.command_name == "C_QUIT":
            break

        #
        after_each_player_turn(game=game, interaction_system=interaction_system)

        #
        if game.nb_players > 1:
            #
            game.current_player = (game.current_player + 1)
            #
            while game.current_player >= game.nb_players:
                #
                game.nb_players -= game.nb_players
                #
                after_all_players_turn(game=game, interaction_system=interaction_system)
        else:
            after_all_players_turn(game=game, interaction_system=interaction_system)

    #
    interaction_system.write_to_output(txt="\nSystem Exit\nGoodbye.")
    #
    if hasattr(interaction_system, "flush_output"):
        interaction_system.flush_output()
