#
from typing import Optional, cast
#
import sys
import copy
#
from engine.interaction_system import BasicTerminalInteractionSystem
from engine.engine_classes import load_interactive_fiction_model_from_file, Room, Player
from engine.engine_classes_game import Game
from engine.command_parsing import parse_command
import engine.engine_classes_commands as ecc
import engine.engine_classes_time as ect
import engine.lib_utils as lu
from engine.engine_commands import ALL_COMMANDS_FUNCTIONS, introduce_game, execute_C_LOOKAROUND, get_room_of_player


#
if __name__ == "__main__":

    #
    if len(sys.argv) != 2:
        #
        raise SyntaxError(f"Error: bad arguments given to this application !\n\nMust be used like that : \n\t`python {sys.argv[0]} path_to_game_or_save_file.json`\n\n")

    #
    generic_kws: dict[str, str] = {
        "to": "KW_TO",
        "in": "KW_IN",
        "inside": "KW_IN",
        "into": "KW_IN",
        "on": "KW_ON",
        "with": "KW_WITH"
    }

    #
    game: Game = load_interactive_fiction_model_from_file(filepath=sys.argv[1])
    game.prepare_events_quick_access()
    game.prepare_priority_queue_entities()

    #
    print(f"DEBUG | priority_queue_events_and_entities = {game.priority_queue_events_and_entities._queue}")  # type: ignore

    #
    interaction_system: BasicTerminalInteractionSystem = BasicTerminalInteractionSystem(game=game)

    #
    introduce_game(game=game, interaction_system=interaction_system)

    #
    if game.nb_players == 0:
        #
        raise RuntimeError(f"Error: No player for the game : `{game.game_name}` from `{game.game_author}`")

    #
    player_id: str
    #
    for player_id in game.players:
        #
        room: Room = get_room_of_player(game=game, player_id=player_id)
        #
        if player_id not in room.things_inside:
            room.things_inside[player_id] = 1

    #
    next_entity_event: Optional[lu.PQ_Entity_and_EventsSystem] = None
    next_time_shift: Optional[ect.GameTime] = None

    #
    res: Optional[ tuple[lu.PQ_Entity_and_EventsSystem, ect.GameTime] ] = game.next_event_or_entity_action()

    #
    if res is not None:
        #
        next_entity_event = res[0]
        next_time_shift = copy.deepcopy(res[1])

    #
    while next_entity_event is not None and next_time_shift is not None and interaction_system.running:

        #
        # print(f"DEBUG | next_entity_event.elt_type = {next_entity_event.elt_type}")

        #
        if next_entity_event.elt_type == "entity":

            #
            if next_entity_event.elt_id in game.players:
                #
                interaction_system.write_to_output(txt=f"\n\n### Player: {game.players[game.current_player]}\n\n")
                #
                if next_entity_event.elt_id not in game.players_first_description:
                    #
                    execute_C_LOOKAROUND(game=game, interaction_system=interaction_system, command=ecc.Command(command_name="C_LOOKAROUND"), player_id=game.players[game.current_player])
                    #
                    game.players_first_description.add( next_entity_event.elt_id )

                #
                command_input: str = interaction_system.ask_input()

                #
                parsed_command: Optional[ecc.Command] = parse_command(command_input=command_input, generic_kws=generic_kws)

                #
                if parsed_command is None or parsed_command.command_name not in ALL_COMMANDS_FUNCTIONS:  # type: ignore
                    #
                    interaction_system.write_to_output(txt="Unkown Command\n")
                    continue

                #
                game.check_and_apply_events_from_command(command=parsed_command, player=cast(Player, game.things[game.players[game.current_player]]))

                #
                ALL_COMMANDS_FUNCTIONS[parsed_command.command_name](game, interaction_system, parsed_command, game.players[game.current_player], False)  # type: ignore

                #
                if parsed_command.command_name == "C_QUIT":  # type: ignore
                    #
                    break

            #
            else:

                #
                game.manage_npc_entities(elt=next_entity_event, interaction_system=interaction_system)

        #
        else:

            #
            game.manage_event(elt=next_entity_event, interaction_system=interaction_system)


        #
        # print(f"DEBUG 1 | priority_queue_events_and_entities = {game.priority_queue_events_and_entities._queue}")  # type: ignore

        #
        game.priority_queue_events_and_entities.shift_all_times(time_shift=next_time_shift)
        game.global_time += next_time_shift

        #
        # print(f"DEBUG 2 | priority_queue_events_and_entities = {game.priority_queue_events_and_entities._queue}")  # type: ignore

        #
        res = game.next_event_or_entity_action()

        #
        if res is not None:
            #
            next_entity_event = res[0]
            next_time_shift = copy.deepcopy(res[1])
        #
        else:
            #
            next_entity_event = None
            next_time_shift = None
        #
        if hasattr(interaction_system, "flush_output"):
            #
            interaction_system.flush_output()  # type: ignore

        #
        # print(f"DEBUG 3 | priority_queue_events_and_entities = {game.priority_queue_events_and_entities._queue}")  # type: ignore


    #
    interaction_system.write_to_output(txt="\nSystem Exit\nGoodbye.")
    #
    if hasattr(interaction_system, "flush_output"):
        #
        interaction_system.flush_output()  # type: ignore
