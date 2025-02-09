#
from typing import Callable, Optional
#
from copy import deepcopy
#
from . import engine_classes as engine
from .interaction_system import InteractionSystem



#################################################################################
############################### UTILITY FUNCTIONS ###############################
#################################################################################

#
def get_opt_thing(game: engine.Game, thing_id: str) -> Optional[engine.Thing]:
    #
    if thing_id in game.things:
        return game.things[thing_id]
    #
    return None


#
def get_thing(game: engine.Game, thing_id: str) -> engine.Thing:
    #
    if thing_id in game.things:
        return game.things[thing_id]
    #
    raise RuntimeError(f"Error: There are no thing with id `{thing_id}` in the current ifiction game: {game.game_name}.")


#
def get_opt_room(game: engine.Game, room_id: str) -> Optional[engine.Room]:
    #
    if room_id in game.rooms:
        return game.rooms[room_id]
    #
    return None


#
def get_room(game: engine.Game, room_id: str) -> engine.Room:
    #
    if room_id in game.rooms:
        return game.rooms[room_id]
    #
    raise RuntimeError(f"Engine error: There are no room with id `{room_id}` in the current ifiction game: {game.game_name}.")


#
def get_room_of_player(game: engine.Game, player_id: str) -> engine.Room:
    #
    player_thing: engine.Thing = get_thing(game=game, thing_id=player_id)
    #
    if not isinstance(player_thing, engine.Entity):
        raise RuntimeError(f"Engine error: The thing with id `{player_id}` is no entity (so no player) !\n{player_id} = {player_thing}")
    #
    player: engine.Entity = player_thing
    #
    return get_room(game=game, room_id=player.room)


#
def get_all_thing_of_a_room(game: engine.Game, room: engine.Room) -> list[engine.Thing]:
    #
    pass
    #
    return []

#
def describe_room(game: engine.Game, room: engine.Room, player_id: str = "") -> str:
    #
    text = f"""
You are in {room.room_name}.

{room.description}
    """
    #
    thing: engine.Thing
    for thing in get_all_thing_of_a_room(game=game, room=room):
        #
        if thing.id == player_id:
            continue
        #
        text += f"\nYou can see {thing.name}. {thing.brief_description}"
    #
    return text


############################################################################
############################### ALL COMMANDS ###############################
############################################################################

#
def execute_C_LOOKAROUND(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    #
    current_player_room: engine.Room = get_room_of_player(game=game, player_id=player_id)

    #
    interaction_system.write_to_output(txt=describe_room(game=game, room=current_player_room, player_id=player_id))

    #
    return game


#
def execute_C_RECAP(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_BRIEF(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_DESCRIBE(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_EXAMINE(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_RUMMAGE(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_LISTEN(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_TOUCH(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_READ(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_TASTE(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_SMELL(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_GO(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_PUT(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_PUSH(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_PULL(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_ATTACH(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_BREAK(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_THROW(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_DROP(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_CLEAN(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_USE(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_CLIMB(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_OPEN(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_CLOSE(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_LOCK(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_UNLOCK(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_FILL(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_POUR(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_INSERT(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_REMOVE(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_SET(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_SPREAD(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_SQUEEZE(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_EAT(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_DRINK(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_AWAKE(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_ATTACK(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_BUY(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_SHOW(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_EMBRACE(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_FEED(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_GIVE(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_SAY(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_ASK(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_WRITE(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_ERASE(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_WEAR(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_UNDRESS(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_INVENTORY(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_WAIT(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_SLEEP(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_SIT_DOWN(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_LIE_DOWN(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_STAND_UP(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_TAKE(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_DANCE(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_SING(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_JUMP(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_THINK(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_QUIT(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_SAVE(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_LOAD(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_RESTART(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_SCORE(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


#
def execute_C_HELP(game: engine.Game, interaction_system: InteractionSystem, command: list[str], player_id: str, copy_game: bool = False) -> engine.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    return game


###########################################################################################
############################### GAME INTRODUCTION FUNCTIONS ###############################
###########################################################################################


def introduce_game(game: engine.Game, interaction_system: InteractionSystem) -> None:
    #
    pass


###################################################################################
############################### ALL COMMANDS LINKED ###############################
###################################################################################


#
ALL_COMMANDS_FUNCTIONS: dict[str, Callable[[engine.Game, InteractionSystem, list[str], str, bool], engine.Game]] = {
    "C_LOOKAROUND": execute_C_LOOKAROUND,
    "C_RECAP": execute_C_RECAP,
    "C_BRIEF": execute_C_BRIEF,
    "C_DESCRIBE": execute_C_DESCRIBE,
    "C_EXAMINE": execute_C_EXAMINE,
    "C_RUMMAGE": execute_C_RUMMAGE,
    "C_LISTEN": execute_C_LISTEN,
    "C_TOUCH": execute_C_TOUCH,
    "C_READ": execute_C_READ,
    "C_TASTE": execute_C_TASTE,
    "C_SMELL": execute_C_SMELL,
    "C_GO": execute_C_GO,
    "C_PUT": execute_C_PUT,
    "C_PUSH": execute_C_PUSH,
    "C_PULL": execute_C_PULL,
    "C_ATTACH": execute_C_ATTACH,
    "C_BREAK": execute_C_BREAK,
    "C_THROW": execute_C_THROW,
    "C_DROP": execute_C_DROP,
    "C_CLEAN": execute_C_CLEAN,
    "C_CLIMB": execute_C_CLIMB,
    "C_OPEN": execute_C_OPEN,
    "C_CLOSE": execute_C_CLOSE,
    "C_LOCK": execute_C_LOCK,
    "C_UNLOCK": execute_C_UNLOCK,
    "C_FILL": execute_C_FILL,
    "C_POUR": execute_C_POUR,
    "C_INSERT": execute_C_INSERT,
    "C_REMOVE": execute_C_REMOVE,
    "C_SET": execute_C_SET,
    "C_SPREAD": execute_C_SPREAD,
    "C_SQUEEZE": execute_C_SQUEEZE,
    "C_EAT": execute_C_EAT,
    "C_DRINK": execute_C_DRINK,
    "C_AWAKE": execute_C_AWAKE,
    "C_ATTACK": execute_C_ATTACK,
    "C_BUY": execute_C_BUY,
    "C_SHOW": execute_C_SHOW,
    "C_EMBRACE": execute_C_EMBRACE,
    "C_FEED": execute_C_FEED,
    "C_GIVE": execute_C_GIVE,
    "C_SAY": execute_C_SAY,
    "C_ASK": execute_C_ASK,
    "C_WRITE": execute_C_WRITE,
    "C_ERASE": execute_C_ERASE,
    "C_WEAR": execute_C_WEAR,
    "C_UNDRESS": execute_C_UNDRESS,
    "C_INVENTORY": execute_C_INVENTORY,
    "C_WAIT": execute_C_WAIT,
    "C_SLEEP": execute_C_SLEEP,
    "C_SIT_DOWN": execute_C_SIT_DOWN,
    "C_LIE_DOWN": execute_C_LIE_DOWN,
    "C_STAND_UP": execute_C_STAND_UP,
    "C_TAKE": execute_C_TAKE,
    "C_DANCE": execute_C_DANCE,
    "C_SING": execute_C_SING,
    "C_JUMP": execute_C_JUMP,
    "C_THINK": execute_C_THINK,
    "C_QUIT": execute_C_QUIT,
    "C_SAVE": execute_C_SAVE,
    "C_LOAD": execute_C_LOAD,
    "C_RESTART": execute_C_RESTART,
    "C_SCORE": execute_C_SCORE,
    "C_HELP": execute_C_HELP
}
