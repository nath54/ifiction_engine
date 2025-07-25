#
from typing import Callable, Optional, Any
#
import os
import json
from datetime import datetime
#
from copy import deepcopy
#
from . import engine_classes as engine
from . import engine_classes_game as ecg
from . import engine_results as er
from . import engine_classes_commands as ecc
from . import engine_classes_time as ect
from . import lib_utils as lu
from .interaction_system import InteractionSystem
from .lib_direction import parse_directions



########################################################################################
############################### SYSTEM UTILITY FUNCTIONS ###############################
########################################################################################

FOLDER_SAVE_GAMES: str = "ifiction_games_saves"


#
def traite_txt_for_filepaths(txt: str) -> str:
    #
    txt = txt.replace("\\", "")
    txt = txt.replace("/", "")
    txt = txt.replace("*", "")
    #
    while "  " in txt:
        txt = txt.replace("  ", " ")
    #
    txt = txt.replace(" ", "_")
    txt = txt.replace("\t", "_")
    txt = txt.replace("\n", "_")
    txt = txt.replace("'", "_")
    txt = txt.replace("\"", "_")
    #
    return txt


#
def get_game_savedir(game: ecg.Game) -> str:
    #
    if not os.path.exists(FOLDER_SAVE_GAMES):
        #
        os.mkdir(FOLDER_SAVE_GAMES)
    #
    elif not os.path.isdir(FOLDER_SAVE_GAMES):
        #
        raise SystemError(f"Error: path `{FOLDER_SAVE_GAMES}` exists and is not a directory !")
    #
    game_savedir: str = f"{FOLDER_SAVE_GAMES}/{traite_txt_for_filepaths(game.game_name)}"
    #
    if not os.path.exists(game_savedir):
        #
        os.mkdir(game_savedir)
    #
    elif not os.path.isdir(game_savedir):
        #
        raise SystemError(f"Error: path `{game_savedir}` exists and is not a directory !")
    #
    return game_savedir


#
def get_next_available_auto_savegame_filepath(game: ecg.Game) -> str:
    #
    game_savedir: str = get_game_savedir(game=game)
    #
    now: str = datetime.now().strftime("d-M-y-h-m-s")
    #
    game_savepath: str = f"{game_savedir}/N_TURNS_{game.nb_turns}_PLAYER_{game.current_player}_DATE_{now}.json"
    #
    if not os.path.exists(game_savepath):
        return game_savepath
    #
    i: int = 2
    game_savepath = f"{game_savedir}/N_TURNS_{game.nb_turns}_PLAYER_{game.current_player}_DATE_{now}_{i}.json"
    while os.path.exists(game_savepath):
        i += 1
        game_savepath = f"{game_savedir}/N_TURNS_{game.nb_turns}_PLAYER_{game.current_player}_DATE_{now}_{i}.json"
    #
    return game_savepath



#################################################################################
############################### UTILITY FUNCTIONS ###############################
#################################################################################

#
def get_opt_thing(game: ecg.Game, thing_id: str) -> Optional[engine.Thing]:
    #
    if thing_id in game.things:
        return game.things[thing_id]
    #
    return None


#
def get_thing(game: ecg.Game, thing_id: str) -> engine.Thing:
    #
    if thing_id in game.things:
        return game.things[thing_id]
    #
    raise RuntimeError(f"Error: There are no thing with id `{thing_id}` in the current ifiction game: {game.game_name}.")


#
def get_entity(game: ecg.Game, entity_id: str) -> engine.Entity:
    #
    if entity_id in game.things:
        thing: engine.Thing = game.things[entity_id]
        #
        if isinstance(thing, engine.Entity):
            return thing
        #
        raise RuntimeError(f"Error: Thing {thing} is not entity in the current ifiction game: {game.game_name}.")
    #
    raise RuntimeError(f"Error: There are no thing with id `{entity_id}` in the current ifiction game: {game.game_name}.")


#
def get_opt_room(game: ecg.Game, room_id: str) -> Optional[engine.Room]:
    #
    if room_id in game.rooms:
        return game.rooms[room_id]
    #
    return None


#
def get_room(game: ecg.Game, room_id: str) -> engine.Room:
    #
    if room_id in game.rooms:
        return game.rooms[room_id]
    #
    raise RuntimeError(f"Engine error: There are no room with id `{room_id}` in the current ifiction game: {game.game_name}.")


#
def get_room_of_player(game: ecg.Game, player_id: str) -> engine.Room:
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
def fusion_rec_res_things(res1: dict[engine.Thing, tuple[str, engine.Thing | engine.Room]], res2: dict[engine.Thing, tuple[str, engine.Thing | engine.Room]]) -> dict[engine.Thing, tuple[str, engine.Thing | engine.Room]]:
    #
    for k in res2:
        if k not in res1:
            res1[k] = res2[k]
    #
    return res1


#
def add_subthing_to_rec_res(game: ecg.Game, subthing_id: str, res: dict[engine.Thing, tuple[str, engine.Thing | engine.Room]], res_tuple_keyword: str, res_tuple_value: engine.Thing | engine.Room) -> dict[engine.Thing, tuple[str, engine.Thing | engine.Room]]:
    #
    subthing = get_thing(game=game, thing_id=subthing_id)
    #
    if "hidden" in subthing.attributes:
        return res
    #
    res[subthing] = (res_tuple_keyword, res_tuple_value)
    #
    if "locked" in subthing.attributes or "closed" in subthing.attributes or ("openable" in subthing.attributes and "open" not in subthing.attributes):
        return res
    #
    res = fusion_rec_res_things(
        res1=res,
        res2=get_rec_all_things_of_a_thing(game=game, thing=subthing)
    )
    #
    return res


#
def get_rec_all_things_of_a_thing(game: ecg.Game, thing: engine.Thing) -> dict[engine.Thing, tuple[str, engine.Thing | engine.Room]]:
    #
    res: dict[engine.Thing, tuple[str, engine.Thing | engine.Room]] = {}
    #
    subthing_id: str
    #
    if isinstance(thing, engine.Object):
        #
        for subthing_id in thing.parts:
            #
            res = add_subthing_to_rec_res(game=game, subthing_id=subthing_id, res=res, res_tuple_keyword="PartOf", res_tuple_value=thing)
        #
        for subthing_id in thing.contains:
            #
            res = add_subthing_to_rec_res(game=game, subthing_id=subthing_id, res=res, res_tuple_keyword="Contained", res_tuple_value=thing)
    #
    if isinstance(thing, engine.Entity):
        #
        for subthing_id in thing.inventory:
            #
            res = add_subthing_to_rec_res(game=game, subthing_id=subthing_id, res=res, res_tuple_keyword="Inventory", res_tuple_value=thing)
    #
    return res


#
def get_rec_all_things_of_a_room(game: ecg.Game, room: engine.Room) -> dict[engine.Thing, tuple[str, engine.Thing | engine.Room]]:
    #
    res: dict[engine.Thing, tuple[str, engine.Thing | engine.Room]] = {}
    #
    subthing_id: str
    for subthing_id in room.things_inside:
        #
        res = add_subthing_to_rec_res(game=game, subthing_id=subthing_id, res=res, res_tuple_keyword="InsideRoom", res_tuple_value=room)
    #
    return res


#
def get_all_thing_of_a_room(game: ecg.Game, room: engine.Room) -> list[engine.Thing]:
    #
    return [get_thing(game=game, thing_id=thing_id) for thing_id in room.things_inside]


#
def describe_room(game: ecg.Game, room: engine.Room, player_id: str = "") -> dict[engine.Thing, tuple[str, engine.Thing | engine.Room]]:
    #
    things_in_room: dict[engine.Thing, tuple[str, engine.Thing | engine.Room]] = get_rec_all_things_of_a_room(game=game, room=room)
    #
    thing: engine.Thing
    for thing in list(things_in_room.keys()):
        #
        if things_in_room[thing][0] == "Inventory":
            del(things_in_room[thing])
        #
        elif thing.id == player_id:
            del(things_in_room[thing])
    #
    return things_in_room


#
def is_designing_thing(text: str, thing: engine.Thing) -> bool:
    #
    if text in thing.name:
        return True
    #
    if text in thing.id:
        return True
    #
    return False


#
def get_designed_thing(game: ecg.Game, text: str, player_id: str) -> Optional[engine.Thing]:
    #
    current_player_room: engine.Room = get_room_of_player(game=game, player_id=player_id)

    #
    things_in_room: list[engine.Thing] = get_all_thing_of_a_room(game=game, room=current_player_room)

    #
    possible_things: list[engine.Thing] = []

    #
    thing: engine.Thing
    for thing in things_in_room:
        #
        if is_designing_thing(text=text, thing=thing):
            #
            possible_things.append( thing )

    #
    if len(possible_things) == 1:
        #
        return possible_things[0]
    #
    return None


#
def remove_thing_from_thing(game: ecg.Game, thing_to_remove_id: str, thing: engine.Thing, quantity: int = 1) -> None:
    #
    if isinstance(thing, engine.Object):
        #
        if thing_to_remove_id not in thing.contains:
            return
        #
        if thing.contains[thing_to_remove_id] > quantity:
            thing.contains[thing_to_remove_id] -= quantity
        #
        else:
            del thing.contains[thing_to_remove_id]
    #
    elif isinstance(thing, engine.Entity):
        #
        if thing_to_remove_id not in thing.inventory:
            return
        #
        if thing.inventory[thing_to_remove_id] > quantity:
            thing.inventory[thing_to_remove_id] -= quantity
        #
        else:
            del thing.inventory[thing_to_remove_id]


#
def add_thing_to_thing(game: ecg.Game, thing_to_add_id: str, thing: engine.Thing, quantity: int = 1) -> None:
    #
    if isinstance(thing, engine.Object):
        #
        if thing_to_add_id not in thing.contains:
            thing.contains[thing_to_add_id] = quantity
        return
        #
        thing.contains[thing_to_add_id] += quantity
    #
    elif isinstance(thing, engine.Entity):
        #
        if thing_to_add_id not in thing.inventory:
            thing.inventory[thing_to_add_id] = quantity
        return
        #
        thing.inventory[thing_to_add_id] += quantity


#
def move_thing_from_thing_to_thing(game: ecg.Game, thing_id: str, thing_from: engine.Thing, thing_to: engine.Thing, quantity: int = 1) -> None:
    #
    remove_thing_from_thing(game=game, thing_to_remove_id=thing_id, thing=thing_from, quantity=quantity)
    add_thing_to_thing(game=game, thing_to_add_id=thing_id, thing=thing_to, quantity=quantity)


#
def remove_thing_from_room(game: ecg.Game, thing_id: str, room: engine.Room, quantity: int = 1) -> None:
    #
    if thing_id not in room.things_inside:
        return
    #
    if room.things_inside[thing_id] > quantity:
        room.things_inside[thing_id] -= quantity
    #
    else:
        del room.things_inside[thing_id]


#
def add_thing_to_room(game: ecg.Game, thing_id: str, room: engine.Room, quantity: int = 1) -> None:
    #
    if thing_id not in room.things_inside:
        room.things_inside[thing_id] = quantity
        return
    #
    room.things_inside[thing_id] += quantity


#
def remove_thing_from_inventory(game: ecg.Game, thing_id: str, entity: engine.Entity, quantity: int = 1) -> None:
    #
    if thing_id not in entity.inventory:
        return
    #
    if entity.inventory[thing_id] > quantity:
        entity.inventory[thing_id] -= quantity
    #
    else:
        del entity.inventory[thing_id]


#
def add_thing_to_inventory(game: ecg.Game, thing_id: str, entity: engine.Entity, quantity: int = 1) -> None:
    #
    if thing_id not in entity.inventory:
        entity.inventory[thing_id] = quantity
        return
    #
    entity.inventory[thing_id] += quantity


#
def move_thing_from_room_to_room(game: ecg.Game, thing_id: str, room_from: engine.Room, room_to: engine.Room, quantity: int = 1) -> None:
    #
    remove_thing_from_room(game=game, thing_id=thing_id, room=room_from, quantity=quantity)
    add_thing_to_room(game=game, thing_id=thing_id, room=room_to, quantity=quantity)


#
def get_thing_designed(game: ecg.Game, text: str, list_of_things: list[engine.Thing]) -> Optional[engine.Thing]:
    #
    thing: engine.Thing
    #
    for thing in list_of_things:
        #
        if is_designing_thing(text=text, thing=thing):
            return thing
    #
    return None


############################################################################
############################### ALL COMMANDS ###############################
############################################################################

#
def execute_C_LOOKAROUND(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    #
    current_player_room: engine.Room = get_room_of_player(game=game, player_id=player_id)

    #
    interaction_system.add_result(
        result=er.ResultLookAround(
                    room=current_player_room,
                    things_in_room=describe_room(game=game, room=current_player_room, player_id=game.players[game.current_player])
        )
    )

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime()
        ),
        priority=ect.GameTime()
    )

    #
    return game


#
def execute_C_RECAP(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime()
        ),
        priority=ect.GameTime()
    )

    #
    return game


#
def execute_C_BRIEF(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    #
    designed_thing: Optional[engine.Thing] = get_designed_thing(game=game, text=command.elt, player_id=player_id)

    #
    if designed_thing is not None:
        #
        interaction_system.add_result( result=er.ResultBrief( thing=er.ThingShow(thing=designed_thing) ) )
    #
    else:
        #
        interaction_system.add_result( result=er.ResultErrorThingNotFound( text_designing_thing=command.elt ) )

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime()
        ),
        priority=ect.GameTime()
    )

    #
    return game


#
def execute_C_DESCRIBE(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    #
    designed_thing: Optional[engine.Thing] = get_designed_thing(game=game, text=command.elt, player_id=player_id)

    #
    if designed_thing is not None:
        #
        interaction_system.add_result( result=er.ResultDescribe( thing=er.ThingShow(thing=designed_thing) ) )
    #
    else:
        #
        interaction_system.add_result( result=er.ResultErrorThingNotFound( text_designing_thing=command.elt ) )

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime()
        ),
        priority=ect.GameTime()
    )

    #
    return game


#
def execute_C_EXAMINE(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    #
    designed_thing: Optional[engine.Thing] = get_designed_thing(game=game, text=command.elt, player_id=player_id)

    #
    if designed_thing is not None:
        #
        interaction_system.add_result( result=er.ResultExamine( thing=er.ThingShow(thing=designed_thing) ) )
    #
    else:
        #
        interaction_system.add_result( result=er.ResultErrorThingNotFound( text_designing_thing=command.elt ) )

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=5)
        ),
        priority=ect.GameTime()
    )

    #
    return game


#
def execute_C_RUMMAGE(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=10)
        ),
        priority=ect.GameTime()
    )
    #
    return game


#
def execute_C_READ(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt_OKw_OElt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=10)
        ),
        priority=ect.GameTime()
    )
    #
    return game


#
def execute_C_GO(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    #
    parsed_direc: Optional[str] = parse_directions(command.elt)

    #
    if parsed_direc is None:
        #
        interaction_system.add_result( result=er.ResultErrorDirection(input_txt=command.elt) )
        #
        game.priority_queue_events_and_entities.insert_with_priority(
            item=lu.PQ_Entity_and_EventsSystem(
                elt_type="entity",
                elt_id=game.players[game.current_player],
                current_action=None,
                current_action_time=ect.GameTime()
            ),
            priority=ect.GameTime()
        )
        #
        return game

    #
    current_player_room: engine.Room = get_room_of_player(game=game, player_id=player_id)
    #
    choosen_access: Optional[engine.Access] = None
    #
    access: engine.Access
    for access in current_player_room.accesses:
        #
        if access.direction == parsed_direc:
            #
            choosen_access = access
            break
    #
    if choosen_access is not None:
        #
        access_thing: engine.Thing
        #
        if choosen_access.thing_id != "none":

            #
            access_thing = get_thing(game=game, thing_id=choosen_access.thing_id)
            #
            if "locked" in access_thing.attributes:
                #
                interaction_system.add_result(
                    result=er.ResultErrorAccessLocked(
                        direction=choosen_access.direction,
                        access_thing=er.ThingShow(thing=access_thing)
                    )
                )
                #
                game.priority_queue_events_and_entities.insert_with_priority(
                    item=lu.PQ_Entity_and_EventsSystem(
                        elt_type="entity",
                        elt_id=game.players[game.current_player],
                        current_action=None,
                        current_action_time=ect.GameTime()
                    ),
                    priority=ect.GameTime()
                )
                #
                return game
            #
            if "openable" in access_thing.attributes and "open" not in access_thing.attributes:
                #
                interaction_system.add_result(
                    result=er.ResultErrorAccessClosed(
                        direction=choosen_access.direction,
                        access_thing=er.ThingShow(thing=access_thing)
                    )
                )
                #
                game.priority_queue_events_and_entities.insert_with_priority(
                    item=lu.PQ_Entity_and_EventsSystem(
                        elt_type="entity",
                        elt_id=game.players[game.current_player],
                        current_action=None,
                        current_action_time=ect.GameTime()
                    ),
                    priority=ect.GameTime()
                )
                #
                return game
        #
        else:
            #
            access_thing = engine.Thing(id_="none", name="none")
        #
        remove_thing_from_room(game=game, thing_id=player_id, room=current_player_room)
        #
        add_thing_to_room(game=game, thing_id=player_id, room=get_room(game=game, room_id=choosen_access.links_to))
        #
        player: engine.Entity = get_entity(game=game, entity_id=player_id)
        #
        player.room = choosen_access.links_to
        #
        interaction_system.add_result(
            result=er.ResultGo(
                direction=choosen_access.direction,
                access_thing=er.ThingShow(thing=access_thing)
            )
        )
        #
        game.priority_queue_events_and_entities.insert_with_priority(
            item=lu.PQ_Entity_and_EventsSystem(
                elt_type="entity",
                elt_id=game.players[game.current_player],
                current_action="moving",
                current_action_time=ect.GameTime(minute=5)
            ),
            priority=ect.GameTime()
        )
        #
        return execute_C_LOOKAROUND(game=game, interaction_system=interaction_system, command=ecc.Command(command_name="C_LOOKAROUDN"), player_id=player_id, copy_game=copy_game)
    #
    else:
        #
        interaction_system.add_result( result=er.ResultErrorCannotGoDirection( direction=parsed_direc ) )
    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime()
        ),
        priority=ect.GameTime()
    )
    #
    return game


#
def execute_C_PUT(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt_Kw_Elt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=5)
        ),
        priority=ect.GameTime()
    )
    #
    return game


#
def execute_C_ATTACH(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt_Kw_Elt_OKw_OElt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=5)
        ),
        priority=ect.GameTime()
    )
    #
    return game


#
def execute_C_THROW(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt_OKw_OElt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=5)
        ),
        priority=ect.GameTime()
    )
    #
    return game


#
def execute_C_DROP(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    #
    current_player: engine.Entity = get_entity(game=game, entity_id=player_id)
    #
    current_room: engine.Room = get_room(game=game, room_id=current_player.room)

    #
    designated_thing: Optional[engine.Thing] = get_thing_designed(game=game, text=command.elt, list_of_things=[get_thing(game=game, thing_id=thing_id) for thing_id in current_player.inventory])

    #
    if designated_thing is None:
        #
        interaction_system.add_result( result=er.ResultErrorThingNotFound(text_designing_thing=command.elt) )
        return game

    #
    remove_thing_from_inventory(game=game, thing_id=designated_thing.id, entity=current_player)
    add_thing_to_room(game=game, thing_id=designated_thing.id, room=current_room)

    #
    interaction_system.add_result(
        result=er.ResultDrop(
            thing=er.ThingShow(thing=designated_thing),
            room=current_room
        )
    )

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=5)
        ),
        priority=ect.GameTime()
    )
    #
    return game


#
def execute_C_USE(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt_OKw_OElt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    #
    current_player: engine.Entity = get_entity(game=game, entity_id=player_id)
    #
    current_room: engine.Room = get_room(game=game, room_id=current_player.room)
    #
    dict_of_things: dict[engine.Thing, tuple[str, engine.Thing | engine.Room]] = get_rec_all_things_of_a_room(game=game, room=current_room)
    #
    list_of_things: list[engine.Thing] = list(dict_of_things.keys())
    #
    elt1: Optional[engine.Thing] = get_thing_designed(game=game, text=command.elt1, list_of_things=list_of_things)

    #
    if elt1 is None:
        #
        interaction_system.add_result(result=er.ResultErrorThingNotFound(command.elt1))
        #
        game.priority_queue_events_and_entities.insert_with_priority(
            item=lu.PQ_Entity_and_EventsSystem(
                elt_type="entity",
                elt_id=game.players[game.current_player],
                current_action=None,
                current_action_time=ect.GameTime(minute=10)
            ),
            priority=ect.GameTime()
        )
        #
        return game

    #
    possessor: engine.Thing | engine.Room = dict_of_things[elt1][1]
    #
    if dict_of_things[elt1][0] == "Inventory" and isinstance(possessor, engine.Thing) and possessor != current_player:
        #
        interaction_system.add_result(result=er.ResultErrorAnotherPossessThing(thing=er.ThingShow(elt1), possessor=er.ThingShow(possessor)))
        #
        game.priority_queue_events_and_entities.insert_with_priority(
            item=lu.PQ_Entity_and_EventsSystem(
                elt_type="entity",
                elt_id=game.players[game.current_player],
                current_action=None,
                current_action_time=ect.GameTime(minute=10)
            ),
            priority=ect.GameTime()
        )
        #
        return game

    #
    if command.elt2 is None:

        #
        accesses_idxs: list[int] = [i for i in range(len(current_room.accesses)) if current_room.accesses[i].thing_id == elt1.id]
        access_idx: int = accesses_idxs[-1] if accesses_idxs else -1
        #
        if access_idx != -1:

            # For doors
            if "open" in elt1.attributes:
                #
                return execute_C_GO(game=game, interaction_system=interaction_system, command=ecc.Command_Elt(command_name="C_GO", elt=current_room.accesses[access_idx].direction), player_id=player_id, copy_game=copy_game)

        # TODO
        interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

        #
        game.priority_queue_events_and_entities.insert_with_priority(
            item=lu.PQ_Entity_and_EventsSystem(
                elt_type="entity",
                elt_id=game.players[game.current_player],
                current_action=None,
                current_action_time=ect.GameTime(minute=10)
            ),
            priority=ect.GameTime()
        )
        #
        return game

    #
    elt2: Optional[engine.Thing] = get_thing_designed(game=game, text=command.elt2, list_of_things=list_of_things)

    #
    if elt2 is None:
        #
        interaction_system.add_result(result=er.ResultErrorThingNotFound(command.elt2))
        #
        game.priority_queue_events_and_entities.insert_with_priority(
            item=lu.PQ_Entity_and_EventsSystem(
                elt_type="entity",
                elt_id=game.players[game.current_player],
                current_action=None,
                current_action_time=ect.GameTime(minute=10)
            ),
            priority=ect.GameTime()
        )
        #
        return game

    #
    possessor = dict_of_things[elt2][1]
    if dict_of_things[elt2][0] == "Inventory" and isinstance(possessor, engine.Thing) and possessor != current_player:
        #
        interaction_system.add_result(result=er.ResultErrorAnotherPossessThing(thing=er.ThingShow(elt2), possessor=er.ThingShow(possessor)))
        #
        game.priority_queue_events_and_entities.insert_with_priority(
            item=lu.PQ_Entity_and_EventsSystem(
                elt_type="entity",
                elt_id=game.players[game.current_player],
                current_action=None,
                current_action_time=ect.GameTime(minute=10)
            ),
            priority=ect.GameTime()
        )
        #
        return game

    #
    if command.kw in ["on", "onto"]:

        #
        if dict_of_things[elt1][0] != "Inventory" or dict_of_things[elt1][1] != current_player:
            #
            interaction_system.add_result(result=er.ResultErrorDoesntPossessThing(er.ThingShow(elt1)))
            #
            game.priority_queue_events_and_entities.insert_with_priority(
                item=lu.PQ_Entity_and_EventsSystem(
                    elt_type="entity",
                    elt_id=game.players[game.current_player],
                    current_action=None,
                    current_action_time=ect.GameTime(minute=10)
                ),
                priority=ect.GameTime()
            )
            #
            return game


        # Unlocks
        if isinstance(elt1, engine.Object) and elt2.id in elt1.unlocks:
            #
            if "locked" in elt2.attributes:
                #
                elt2.attributes.remove("locked")
                #
                interaction_system.add_result( result=er.ResultUnlock(thing1=er.ThingShow(elt2), thing2=er.ThingShow(elt1)) )
            #
            else:
                #
                elt2.attributes.append("locked")
                #
                interaction_system.add_result( result=er.ResultLock(thing1=er.ThingShow(elt2), thing2=er.ThingShow(elt1)) )
            #
            game.priority_queue_events_and_entities.insert_with_priority(
                item=lu.PQ_Entity_and_EventsSystem(
                    elt_type="entity",
                    elt_id=game.players[game.current_player],
                    current_action=None,
                    current_action_time=ect.GameTime(minute=10)
                ),
                priority=ect.GameTime(minute=5)
            )
            #
            return game


    # TODO
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=10)
        ),
        priority=ect.GameTime()
    )
    #
    return game


#
def execute_C_CLIMB(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=10)
        ),
        priority=ect.GameTime(minute=0)
    )
    #
    return game


#
def execute_C_OPEN(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    #
    current_player: engine.Entity = get_entity(game=game, entity_id=player_id)
    #
    current_room: engine.Room = get_room(game=game, room_id=current_player.room)
    #
    things_in_room: dict[engine.Thing, tuple[str, Any]] = get_rec_all_things_of_a_room(game=game, room=current_room)
    #
    designated_thing: Optional[engine.Thing] = get_thing_designed(game=game, text=command.elt, list_of_things=list(things_in_room.keys()))

    #
    if designated_thing is None:
        #
        interaction_system.add_result( result=er.ResultErrorThingNotFound(text_designing_thing=command.elt) )
        return game

    #
    possessor: engine.Thing | engine.Room = things_in_room[designated_thing][1]
    if things_in_room[designated_thing][0] == "Inventory" and isinstance(possessor, engine.Thing) and possessor != current_player:
        #
        interaction_system.add_result(result=er.ResultErrorAnotherPossessThing(thing=er.ThingShow(designated_thing), possessor=er.ThingShow(possessor)))
        return game

    #
    if "openable" not in designated_thing.attributes:
        #
        interaction_system.add_result(result=er.ResultErrorCannotActionThing(action="open", thing=er.ThingShow(designated_thing), reason=". It is not openable"))
        return game

    #
    if "locked" in designated_thing.attributes:
        #
        interaction_system.add_result(result=er.ResultErrorCannotActionThing(action="open", thing=er.ThingShow(designated_thing), reason=". It is locked"))
        return game

    #
    if "open" in designated_thing.attributes:
        #
        interaction_system.add_result(result=er.ResultErrorCannotActionThing(action="open", thing=er.ThingShow(designated_thing), reason=". It is already open"))
        return game

    #
    designated_thing.attributes.append("open")
    interaction_system.add_result(result=er.ResultOpen(thing=er.ThingShow(designated_thing)))

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=10)
        ),
        priority=ect.GameTime(minute=5)
    )
    #
    return game


#
def execute_C_CLOSE(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    #
    current_player: engine.Entity = get_entity(game=game, entity_id=player_id)
    #
    current_room: engine.Room = get_room(game=game, room_id=current_player.room)
    #
    things_in_room: dict[engine.Thing, tuple[str, Any]] = get_rec_all_things_of_a_room(game=game, room=current_room)
    #
    designated_thing: Optional[engine.Thing] = get_thing_designed(game=game, text=command.elt, list_of_things=list(things_in_room.keys()))

    #
    if designated_thing is None:
        #
        interaction_system.add_result( result=er.ResultErrorThingNotFound(text_designing_thing=command.elt) )
        return game

    #
    possessor: engine.Thing | engine.Room = things_in_room[designated_thing][1]
    if things_in_room[designated_thing][0] == "Inventory" and isinstance(possessor, engine.Thing) and possessor != current_player:
        #
        interaction_system.add_result(result=er.ResultErrorAnotherPossessThing(thing=er.ThingShow(designated_thing), possessor=er.ThingShow(possessor)))
        return game

    #
    if "openable" not in designated_thing.attributes:
        #
        interaction_system.add_result(result=er.ResultErrorCannotActionThing(action="open", thing=er.ThingShow(designated_thing), reason=". It is not closable."))
        return game

    #
    if "open" not in designated_thing.attributes:
        #
        interaction_system.add_result(result=er.ResultErrorCannotActionThing(action="open", thing=er.ThingShow(designated_thing), reason=". It is already closed."))
        return game

    #
    designated_thing.attributes.remove("open")
    interaction_system.add_result(result=er.ResultClose(thing=er.ThingShow(designated_thing)))

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=10)
        ),
        priority=ect.GameTime(minute=5)
    )
    #
    return game


#
def execute_C_LOCK(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt_OKw_OElt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    #
    current_player: engine.Entity = get_entity(game=game, entity_id=player_id)
    current_room: engine.Room = get_room(game=game, room_id=current_player.room)
    #
    all_things_in_room: dict[engine.Thing, tuple[str, engine.Thing | engine.Room]] = get_rec_all_things_of_a_room(game=game, room=current_room)
    #
    elt_to_lock_: Optional[engine.Thing] = get_thing_designed(game=game, text=command.elt1, list_of_things=list(all_things_in_room.keys()))

    #
    if elt_to_lock_ is None:
        #
        interaction_system.add_result( result=er.ResultErrorThingNotFound(text_designing_thing=command.elt1) )
        return game

    #
    if not isinstance(elt_to_lock_, engine.Object):
        #
        interaction_system.add_result( result=er.ResultErrorCannotActionThingSolo(action="lock", thing=er.ThingShow(elt_to_lock_), reason=". It is not an object !") )
        return game

    #
    elt_to_lock: engine.Object = elt_to_lock_

    #
    if "locked" in elt_to_lock.attributes:
        #
        interaction_system.add_result( result=er.ResultErrorCannotActionThingSolo(action="lock", thing=er.ThingShow(elt_to_lock), reason=". It is already locked !") )
        return game

    #
    if "open" in elt_to_lock.attributes:
        #
        interaction_system.add_result( result=er.ResultErrorCannotActionThingSolo(action="lock", thing=er.ThingShow(elt_to_lock), reason=". It is still open !") )
        return game

    #
    if command.elt2 is None:
        #
        if current_room.room_name not in elt_to_lock.easy_to_unlock_from:
            #
            interaction_system.add_result( result=er.ResultErrorCannotActionThingSolo(action="lock", thing=er.ThingShow(elt_to_lock), reason=". It is not easily lockable from this room !") )
            return game
        #
        elt_to_lock.attributes.append("locked")
        #
        interaction_system.add_result( result=er.ResultLock(thing1=er.ThingShow(elt_to_lock)) )
        return game

    #
    elt_that_lock: Optional[engine.Thing] = get_thing_designed(game=game, text=command.elt2, list_of_things=list(all_things_in_room.keys()))
    #
    if elt_that_lock is None:
        #
        interaction_system.add_result( result=er.ResultErrorThingNotFound(text_designing_thing=command.elt2) )
        return game

    #
    if not isinstance(elt_that_lock, engine.Object):
        #
        interaction_system.add_result( result=er.ResultErrorThingNotFound(text_designing_thing=command.elt2) )
        return game

    #
    if elt_to_lock.id not in elt_that_lock.unlocks:
        #
        interaction_system.add_result( result=er.ResultErrorCannotActionThingWithThing(action="lock", thing1=er.ThingShow(elt_to_lock), thing2=er.ThingShow(elt_that_lock)) )
        return game

    #
    elt_to_lock.attributes.append("locked")
    #
    interaction_system.add_result( result=er.ResultLock(thing1=er.ThingShow(elt_to_lock), thing2=er.ThingShow(elt_that_lock)) )

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=10)
        ),
        priority=ect.GameTime(minute=5)
    )
    #
    return game


#
def execute_C_UNLOCK(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt_OKw_OElt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    #
    current_player: engine.Entity = get_entity(game=game, entity_id=player_id)
    current_room: engine.Room = get_room(game=game, room_id=current_player.room)
    #
    all_things_in_room: dict[engine.Thing, tuple[str, engine.Thing | engine.Room]] = get_rec_all_things_of_a_room(game=game, room=current_room)
    #
    elt_to_unlock_: Optional[engine.Thing] = get_thing_designed(game=game, text=command.elt1, list_of_things=list(all_things_in_room.keys()))

    #
    if elt_to_unlock_ is None:
        #
        interaction_system.add_result( result=er.ResultErrorThingNotFound(text_designing_thing=command.elt1) )
        return game

    #
    if not isinstance(elt_to_unlock_, engine.Object):
        #
        interaction_system.add_result( result=er.ResultErrorCannotActionThingSolo(action="unlock", thing=er.ThingShow(elt_to_unlock_), reason=". It is not an object !") )
        return game

    #
    elt_to_unlock: engine.Object = elt_to_unlock_

    #
    if "locked" not in elt_to_unlock.attributes:
        #
        interaction_system.add_result( result=er.ResultErrorCannotActionThingSolo(action="unlock", thing=er.ThingShow(elt_to_unlock), reason=". It is already unlocked !") )
        return game

    #
    if command.elt2 is None:
        #
        if current_room.room_name not in elt_to_unlock.easy_to_unlock_from:
            #
            interaction_system.add_result( result=er.ResultErrorCannotActionThingSolo(action="unlock", thing=er.ThingShow(elt_to_unlock), reason=". It is not easily unlockable from this room !") )
            return game
        #
        elt_to_unlock.attributes.remove("locked")
        #
        interaction_system.add_result( result=er.ResultUnlock(thing1=er.ThingShow(elt_to_unlock)) )
        return game

    #
    elt_that_unlock: Optional[engine.Thing] = get_thing_designed(game=game, text=command.elt2, list_of_things=list(all_things_in_room.keys()))
    #
    if elt_that_unlock is None:
        #
        interaction_system.add_result( result=er.ResultErrorThingNotFound(text_designing_thing=command.elt2) )
        return game

    #
    if not isinstance(elt_that_unlock, engine.Object):
        #
        interaction_system.add_result( result=er.ResultErrorThingNotFound(text_designing_thing=command.elt2) )
        return game

    #
    if elt_to_unlock.id not in elt_that_unlock.unlocks:
        #
        interaction_system.add_result( result=er.ResultErrorCannotActionThingWithThing(action="unlock", thing1=er.ThingShow(elt_to_unlock), thing2=er.ThingShow(elt_that_unlock)) )
        return game

    #
    elt_to_unlock.attributes.remove("locked")
    #
    interaction_system.add_result( result=er.ResultUnlock(thing1=er.ThingShow(elt_to_unlock), thing2=er.ThingShow(elt_that_unlock)) )

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=10)
        ),
        priority=ect.GameTime(minute=5)
    )
    #
    return game


#
def execute_C_INSERT(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt_Kw_Elt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=0)
        ),
        priority=ect.GameTime(minute=0)
    )
    #
    return game


#
def execute_C_REMOVE(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt_Kw_Elt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=0)
        ),
        priority=ect.GameTime(minute=0)
    )
    #
    return game


#
def execute_C_SET(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt_Kw_Elt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=0)
        ),
        priority=ect.GameTime(minute=0)
    )
    #
    return game


#
def execute_C_EAT(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=0)
        ),
        priority=ect.GameTime(minute=0)
    )
    #
    return game


#
def execute_C_DRINK(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=0)
        ),
        priority=ect.GameTime(minute=0)
    )
    #
    return game


#
def execute_C_AWAKE(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=0)
        ),
        priority=ect.GameTime(minute=0)
    )
    #
    return game


#
def execute_C_ATTACK(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt_OKw_OElt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=0)
        ),
        priority=ect.GameTime(minute=0)
    )
    #
    return game


#
def execute_C_BUY(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt_Kw_Elt_Kw_Elt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=0)
        ),
        priority=ect.GameTime(minute=0)
    )
    #
    return game


#
def execute_C_SHOW(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt_Kw_Elt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=0)
        ),
        priority=ect.GameTime(minute=0)
    )
    #
    return game


#
def execute_C_EMBRACE(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=0)
        ),
        priority=ect.GameTime(minute=0)
    )
    #
    return game


#
def execute_C_FEED(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt_Kw_Elt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=0)
        ),
        priority=ect.GameTime(minute=0)
    )
    #
    return game


#
def execute_C_GIVE(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt_Kw_Elt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=0)
        ),
        priority=ect.GameTime(minute=0)
    )
    #
    return game


#
def execute_C_SAY(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt_OKw_OElt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=0)
        ),
        priority=ect.GameTime(minute=0)
    )
    #
    return game


#
def execute_C_ASK(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt_Kw_Elt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=0)
        ),
        priority=ect.GameTime(minute=0)
    )
    #
    return game


#
def execute_C_WRITE(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt_Kw_Elt_OKw_OElt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=0)
        ),
        priority=ect.GameTime(minute=0)
    )
    #
    return game


#
def execute_C_ERASE(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt_OKw_OElt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=0)
        ),
        priority=ect.GameTime(minute=0)
    )
    #
    return game


#
def execute_C_WEAR(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=0)
        ),
        priority=ect.GameTime(minute=0)
    )
    #
    return game


#
def execute_C_UNDRESS(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=0)
        ),
        priority=ect.GameTime(minute=0)
    )
    #
    return game


#
def execute_C_INVENTORY(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    #
    player: engine.Entity = get_entity(game=game, entity_id=player_id)

    #
    inv_dict: dict[er.ThingShow, int] = {}

    #
    thing_id: str
    for thing_id in player.inventory:
        inv_dict[er.ThingShow(thing=get_thing(game=game, thing_id=thing_id))] = player.inventory[thing_id]

    #
    interaction_system.add_result( result=er.ResultInventory(inventory=inv_dict) )
    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=5)
        ),
        priority=ect.GameTime(minute=5)
    )
    #
    return game


#
def execute_C_WAIT(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_OElt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    #
    interaction_system.write_to_output(txt="You wait 30 minutes doing nothing.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action="waiting",
            current_action_time=ect.GameTime(minute=30)
        ),
        priority=ect.GameTime(minute=30)
    )
    #
    return game


#
def execute_C_SLEEP(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=0)
        ),
        priority=ect.GameTime(minute=0)
    )
    #
    return game


#
def execute_C_SIT_DOWN(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=0)
        ),
        priority=ect.GameTime(minute=0)
    )
    #
    return game


#
def execute_C_LIE_DOWN(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=0)
        ),
        priority=ect.GameTime(minute=0)
    )
    #
    return game


#
def execute_C_STAND_UP(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=0)
        ),
        priority=ect.GameTime(minute=0)
    )
    #
    return game


#
def execute_C_TAKE(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        #
        game = deepcopy(game)

    #
    current_player_room: engine.Room = get_room_of_player(game=game, player_id=player_id)
    #
    player: engine.Entity = get_entity(game=game, entity_id=player_id)
    #
    things_in_room: dict[engine.Thing, tuple[str, Any]] = get_rec_all_things_of_a_room(game=game, room=current_player_room)
    #
    designated_thing: Optional[engine.Thing] = get_thing_designed(game=game, text=command.elt, list_of_things=list(things_in_room.keys()))

    #
    if designated_thing is None:
        #
        interaction_system.add_result( result=er.ResultErrorThingNotFound(text_designing_thing=command.elt) )
        #
        game.priority_queue_events_and_entities.insert_with_priority(
            item=lu.PQ_Entity_and_EventsSystem(
                elt_type="entity",
                elt_id=game.players[game.current_player],
                current_action=None,
                current_action_time=ect.GameTime(minute=0)
            ),
            priority=ect.GameTime(minute=0)
        )
        #
        return game

    #
    if things_in_room[designated_thing][0] == "Inventory":
        #
        interaction_system.add_result( result=er.ResultErrorCannotActionThing(action="take", thing=er.ThingShow(thing=designated_thing), reason=". It is already in an inventory.") )
        #
        game.priority_queue_events_and_entities.insert_with_priority(
            item=lu.PQ_Entity_and_EventsSystem(
                elt_type="entity",
                elt_id=game.players[game.current_player],
                current_action=None,
                current_action_time=ect.GameTime(minute=0)
            ),
            priority=ect.GameTime(minute=0)
        )
        #
        return game

    #
    elif things_in_room[designated_thing][0] == "PartOf":
        #
        interaction_system.add_result( result=er.ResultErrorCannotActionThing(action="take", thing=er.ThingShow(thing=designated_thing), reason=f". It is a part of {things_in_room[designated_thing][1]}.") )
        #
        game.priority_queue_events_and_entities.insert_with_priority(
            item=lu.PQ_Entity_and_EventsSystem(
                elt_type="entity",
                elt_id=game.players[game.current_player],
                current_action=None,
                current_action_time=ect.GameTime(minute=0)
            ),
            priority=ect.GameTime(minute=0)
        )
        #
        return game

    #
    elif "item" not in designated_thing.attributes:
        #
        interaction_system.add_result( result=er.ResultErrorCannotActionThing(action="take", thing=er.ThingShow(thing=designated_thing), reason=". It is not an item to take.") )
        #
        game.priority_queue_events_and_entities.insert_with_priority(
            item=lu.PQ_Entity_and_EventsSystem(
                elt_type="entity",
                elt_id=game.players[game.current_player],
                current_action=None,
                current_action_time=ect.GameTime(minute=0)
            ),
            priority=ect.GameTime(minute=0)
        )
        #
        return game

    #
    if things_in_room[designated_thing][0] == "Contained":
        #
        remove_thing_from_thing(game=game, thing_to_remove_id=designated_thing.id, thing=things_in_room[designated_thing][1])
    #
    elif things_in_room[designated_thing][0] == "InsideRoom":
        #
        remove_thing_from_room(game=game, thing_id=designated_thing.id, room=current_player_room)
    #
    add_thing_to_inventory(game=game, thing_id=designated_thing.id, entity=player)

    #
    interaction_system.add_result( result=er.ResultTake(thing=er.ThingShow(thing=designated_thing)) )
    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action="taking something",
            current_action_time=ect.GameTime(minute=5)
        ),
        priority=ect.GameTime(minute=5)
    )
    #
    return game


#
def execute_C_QUIT(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=0)
        ),
        priority=ect.GameTime(minute=0)
    )

    #
    return game


#
def execute_C_SAVE(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_OElt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    #
    savegame_filepath: str = ""

    #
    if command.elt is not None:
        #
        c_elt: str = traite_txt_for_filepaths(command.elt)
        #
        if not c_elt.endswith(".json"):
            interaction_system.add_result(result=er.ResultSystemError(f"Le fichier de sauvegarde demandé ne finit pas par `.json` ! (rappel fichier demandé: `{c_elt}`)"))
        #
        game_savedir: str = get_game_savedir(game=game)
        #
        if os.path.exists(f"{game_savedir}/{c_elt}"):
            interaction_system.add_result(result=er.ResultSystemError(f"Le fichier de sauvegarde demandé existe déjà, sauvegarde annulée ! (rappel fichier demandé: `{c_elt}`)"))
        #
        savegame_filepath = command.elt
    #
    else:
        savegame_filepath = get_next_available_auto_savegame_filepath(game=game)

    #
    game_dict: dict[str, Any] = game.to_dict()

    #
    with open(savegame_filepath, "w", encoding="utf-8") as f:
        json.dump(game_dict, f)

    #
    interaction_system.write_to_output(txt=f"File saved to `{savegame_filepath}`")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=0)
        ),
        priority=ect.GameTime(minute=0)
    )
    #
    return game


#
def execute_C_LOAD(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_Elt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=0)
        ),
        priority=ect.GameTime(minute=0)
    )
    #
    return game


#
def execute_C_SCORE(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=0)
        ),
        priority=ect.GameTime(minute=0)
    )
    #
    return game


#
def execute_C_HELP(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_OElt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    #
    with open("command_list.md", "r", encoding="utf-8") as f:
        #
        interaction_system.write_to_output(txt=f"\nCommand list:\n{f.read()}\n\n")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=0)
        ),
        priority=ect.GameTime(minute=0)
    )
    #
    return game


#
def execute_C_GENERIC_ACTION(game: ecg.Game, interaction_system: InteractionSystem, command: ecc.Command_OElt, player_id: str, copy_game: bool = False) -> ecg.Game:
    #
    if copy_game:
        game = deepcopy(game)

    # TODO
    pass

    #
    interaction_system.write_to_output(txt="Warning: This command hasn't been implemented yet.")

    #
    game.priority_queue_events_and_entities.insert_with_priority(
        item=lu.PQ_Entity_and_EventsSystem(
            elt_type="entity",
            elt_id=game.players[game.current_player],
            current_action=None,
            current_action_time=ect.GameTime(minute=0)
        ),
        priority=ect.GameTime(minute=0)
    )
    #
    return game


###########################################################################################
############################### GAME INTRODUCTION FUNCTIONS ###############################
###########################################################################################


#
def introduce_game(game: ecg.Game, interaction_system: InteractionSystem) -> None:
    #
    if game.nb_turns == 0:
        #
        print(f"""

    ############################################################
    #                                                          #
    #  {game.game_name} {(54 - len(game.game_name)) * ' '} #
    #                                                          #
    #  by {game.game_author} {(51 - len(game.game_author)) * ' '} #
    #                                                          #
    ############################################################

        """)


###################################################################################
############################### ALL COMMANDS LINKED ###############################
###################################################################################


#
ALL_COMMANDS_FUNCTIONS: dict[str, Callable[[ecg.Game, InteractionSystem, ecc.Command, str, bool], ecg.Game]] = {
    "C_LOOKAROUND": execute_C_LOOKAROUND,       # type: ignore
    "C_RECAP": execute_C_RECAP,                 # type: ignore
    "C_BRIEF": execute_C_BRIEF,                 # type: ignore
    "C_DESCRIBE": execute_C_DESCRIBE,           # type: ignore
    "C_EXAMINE": execute_C_EXAMINE,             # type: ignore
    "C_RUMMAGE": execute_C_RUMMAGE,             # type: ignore
    "C_READ": execute_C_READ,                   # type: ignore
    "C_GO": execute_C_GO,                       # type: ignore
    "C_PUT": execute_C_PUT,                     # type: ignore
    "C_ATTACH": execute_C_ATTACH,               # type: ignore
    "C_THROW": execute_C_THROW,                 # type: ignore
    "C_DROP": execute_C_DROP,                   # type: ignore
    "C_USE": execute_C_USE,                     # type: ignore
    "C_CLIMB": execute_C_CLIMB,                 # type: ignore
    "C_OPEN": execute_C_OPEN,                   # type: ignore
    "C_CLOSE": execute_C_CLOSE,                 # type: ignore
    "C_LOCK": execute_C_LOCK,                   # type: ignore
    "C_UNLOCK": execute_C_UNLOCK,               # type: ignore
    "C_INSERT": execute_C_INSERT,               # type: ignore
    "C_REMOVE": execute_C_REMOVE,               # type: ignore
    "C_SET": execute_C_SET,                     # type: ignore
    "C_EAT": execute_C_EAT,                     # type: ignore
    "C_DRINK": execute_C_DRINK,                 # type: ignore
    "C_AWAKE": execute_C_AWAKE,                 # type: ignore
    "C_ATTACK": execute_C_ATTACK,               # type: ignore
    "C_BUY": execute_C_BUY,                     # type: ignore
    "C_SHOW": execute_C_SHOW,                   # type: ignore
    "C_EMBRACE": execute_C_EMBRACE,             # type: ignore
    "C_FEED": execute_C_FEED,                   # type: ignore
    "C_GIVE": execute_C_GIVE,                   # type: ignore
    "C_SAY": execute_C_SAY,                     # type: ignore
    "C_ASK": execute_C_ASK,                     # type: ignore
    "C_WRITE": execute_C_WRITE,                 # type: ignore
    "C_ERASE": execute_C_ERASE,                 # type: ignore
    "C_WEAR": execute_C_WEAR,                   # type: ignore
    "C_UNDRESS": execute_C_UNDRESS,             # type: ignore
    "C_INVENTORY": execute_C_INVENTORY,         # type: ignore
    "C_WAIT": execute_C_WAIT,                   # type: ignore
    "C_SLEEP": execute_C_SLEEP,                 # type: ignore
    "C_SIT_DOWN": execute_C_SIT_DOWN,           # type: ignore
    "C_LIE_DOWN": execute_C_LIE_DOWN,           # type: ignore
    "C_STAND_UP": execute_C_STAND_UP,           # type: ignore
    "C_TAKE": execute_C_TAKE,                   # type: ignore
    "C_QUIT": execute_C_QUIT,                   # type: ignore
    "C_SAVE": execute_C_SAVE,                   # type: ignore
    "C_LOAD": execute_C_LOAD,                   # type: ignore
    "C_SCORE": execute_C_SCORE,                 # type: ignore
    "C_HELP": execute_C_HELP,                   # type: ignore
    "generic_action": execute_C_GENERIC_ACTION, # type: ignore
}
