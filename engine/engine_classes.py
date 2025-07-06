#
from typing import Any, Optional, Callable, Tuple
#
import os
import json
#
from .engine_classes_things_rooms import Thing, Object, Entity, LifeSystem, Player, Access, Room, ALL_ATTRIBUTES
from . import engine_classes_missions as mis
from . import engine_classes_scenes as scn
from . import engine_classes_actions as act
from . import engine_classes_events as evt
from . import engine_classes_conditions as ecc
from . import engine_classes_game as ecg
#
from .lib_direction import parse_directions
from . import lib_class_fusions as lcf



#
def verify_keys_in_dict(dictionary: dict[str, Any], keys: list[str], type_: str) -> None:
    #
    k: str
    for k in keys:
        if k not in keys:
            raise KeyError(f"The key `{k}` not in the dictionary for the type_ {type_} !\n\nDictionary : {dictionary}\n\n")


#
def create_default_value(default_value: Any, attr: str, in_dict: dict[str, Any], type_: str) -> Any:
    #
    if isinstance(default_value, EmptyDict):
        #
        return {}
    #
    elif isinstance(default_value, EmptyList):
        #
        return []
    #
    elif isinstance(default_value, ClassLoadFromDict) and attr in in_dict:
        #
        return create_class_with_attributes_or_default_values_from_dict(
            class_name=default_value.class_name,
            in_dict=in_dict[attr],
            type_=default_value.type_
        )
    #
    return default_value


#
def create_classloadfromdictdependingondictvalue(clfddodv: "ClassLoadFromDictDependingOnDictValue", in_dict: dict[str, Any], attr: str, type_: str) -> Any:
    #
    if attr not in in_dict:
        #
        if isinstance(clfddodv.default_value, NoDefaultValues):
            #
            raise KeyError(f"The attribute `{attr}` not in the dictionary for the type_ {type_} !\n\nDictionary : {in_dict}\n\n")
        #
        return create_default_value(default_value=clfddodv.default_value, attr=attr, in_dict=in_dict, type_=type_)
    #
    if clfddodv.dict_key_value not in in_dict[attr]:
        #
        raise KeyError(f"The attribute `{clfddodv.dict_key_value}` not in the dictionary for the type {type_} !\n\nDictionary : {in_dict[attr]}\n\n")
    #
    if in_dict[attr][clfddodv.dict_key_value] not in clfddodv.class_names_and_types:
        #
        raise KeyError(f"The attribute `{attr}` is an unkown type for `ClassLoadFromDictDependingOnDictValue` and its following class names available : {clfddodv.class_names_and_types.keys()}")
    #
    return create_class_with_attributes_or_default_values_from_dict(
        class_name=clfddodv.class_names_and_types[in_dict[attr][clfddodv.dict_key_value]][0],
        in_dict=in_dict[attr],
        type_=clfddodv.class_names_and_types[in_dict[attr][clfddodv.dict_key_value]][1]
    )

#
def create_kwargs(in_dict: dict[str, Any], type_: str) -> dict[str, Any]:
    #
    kwargs: dict[str, Any] = {}
    #
    if type_ not in CLASS_ATTRIBUTES_AND_DEFAULT_VALUES:
        raise UserWarning(f"Error: Unkown type: `{type_}`")
    #
    attr: str
    for attr in CLASS_ATTRIBUTES_AND_DEFAULT_VALUES[type_]:
        #
        if attr == "id":
            kwargs["id_"] = in_dict["id"]
            continue
        #
        if isinstance(CLASS_ATTRIBUTES_AND_DEFAULT_VALUES[type_][attr], ClassLoadFromDictDependingOnDictValue):
            #
            clfddodv: ClassLoadFromDictDependingOnDictValue = CLASS_ATTRIBUTES_AND_DEFAULT_VALUES[type_][attr]
            #
            kwargs[attr] = create_classloadfromdictdependingondictvalue(clfddodv=clfddodv, in_dict=in_dict, attr=attr, type_=type_)
            #
            continue
        #
        caadv: Any = CLASS_ATTRIBUTES_AND_DEFAULT_VALUES[type_][attr]
        #
        if attr not in in_dict:
            #
            if isinstance(caadv, NoDefaultValues):
                #
                raise KeyError(f"The attribute `{attr}` not in the dictionary for the type_ {type_} !\nNo default values authorized for this attribute.\n\nDictionary : {in_dict}\n\n")
            #
            elif isinstance(caadv, DictOfClassLoadFromDictDependingOnDictValue):
                #
                if isinstance(caadv.default_value, NoDefaultValues):
                    #
                    raise KeyError(f"The attribute `{attr}` not in the dictionary for the type_ {type_} !\nNo default values authorized for this attribute.\n\nDictionary : {in_dict}\n\n")
                else:
                    kwargs[attr] = create_default_value(default_value=caadv.default_value, attr=attr, in_dict=in_dict, type_=type_)
                    continue
            #
            elif isinstance(caadv, DictOfClassLoadFromDict):
                #
                if isinstance(caadv.default_value, NoDefaultValues):
                    #
                    raise KeyError(f"The attribute `{attr}` not in the dictionary for the type_ {type_} !\nNo default values authorized for this attribute.\n\nDictionary : {in_dict}\n\n")
                else:
                    kwargs[attr] = create_default_value(default_value=caadv.default_value, attr=attr, in_dict=in_dict, type_=type_)
                    continue
            #
            elif isinstance(caadv, ClassLoadFromDict):
                #
                kwargs[attr] = create_class_with_attributes_or_default_values_from_dict(
                    class_name=caadv.class_name,
                    type_=caadv.type_,
                    in_dict=None
                )
                continue
            #
            kwargs[attr] = create_default_value(default_value=caadv, attr=attr, in_dict=in_dict, type_=type_)
            #
            continue
        #
        if isinstance(caadv, DictOfClassLoadFromDict):
            #
            kwargs[attr] = {}
            #
            k: str
            #
            for k in in_dict[attr]:
                #
                kwargs[attr][k] = caadv.clfd.class_name(**create_kwargs(in_dict[attr][k], type_=caadv.clfd.type_))
        #
        elif isinstance(caadv, DictOfClassLoadFromDictDependingOnDictValue):
            #
            kwargs[attr] = {}
            #
            key: str
            #
            for key in in_dict[attr]:
                #
                kwargs[attr][key] = create_classloadfromdictdependingondictvalue(clfddodv=caadv.clfddodv, in_dict=in_dict[attr], attr=key, type_=type_)
        #
        elif isinstance(caadv, NoDefaultValueListOfClassLoadFromDict):
            #
            kwargs[attr] = []
            #
            i: int
            #
            for i in range(len(in_dict[attr])):
                #
                kwargs[attr].append(
                    caadv.clfd.class_name(**create_kwargs(in_dict[attr][i], type_=caadv.clfd.type_))
                )
        #
        elif hasattr(caadv, "class_name") and hasattr(caadv, "type_") and (caadv.class_name is not None) and (caadv.type_ is not None):
            #
            kwargs[attr] = create_class_with_attributes_or_default_values_from_dict(
                class_name=caadv.class_name,
                in_dict=in_dict[attr],
                type_=caadv.type_
            )
        #
        else:
            #
            kwargs[attr] = in_dict[attr]
    #
    return kwargs


#
def set_attributes_or_default_values_from_dict(obj: Any, in_dict: dict[str, Any], type_: str) -> None:
    #
    kwargs: dict[str, Any] = create_kwargs(in_dict=in_dict, type_=type_)
    #
    attr: str
    #
    for attr in kwargs:
        setattr(obj, attr, kwargs[attr])


#
def create_class_with_attributes_or_default_values_from_dict(class_name: Callable[..., Any], in_dict: Optional[dict[str, Any]], type_: str) -> Any:
    #
    if in_dict is None:
        in_dict = {}
    #
    kwargs: dict[str, Any] = create_kwargs(in_dict=in_dict, type_=type_)
    #
    return class_name(**kwargs)


#
class NoDefaultValues:
    #
    def __init__(self, have_type_: Optional[str] = None, class_name: Optional[Callable[..., Any]] = None, type_: Optional[str] = None) -> None:
        self.have_type_: Optional[str] = have_type_
        self.class_name: Optional[Callable[..., Any]] = class_name
        self.type_: Optional[str] = type_


#
class ValueOfAttribute:
    #
    def __init__(self, attr: str) -> None:
        #
        self.attr: str = attr


#
class EmptyDict:
    #
    def __init__(self) -> None:
        pass


#
class EmptyList:
    #
    def __init__(self) -> None:
        pass


#
class ClassLoadFromDict:
    #
    def __init__(self, class_name: Callable[..., Any], type_: str) -> None:
        #
        self.class_name: Callable[..., Any] = class_name
        self.type_: str = type_


#
class NoDefaultValueListOfClassLoadFromDict:
    #
    def __init__(self, clfd: ClassLoadFromDict) -> None:
        #
        self.clfd: ClassLoadFromDict = clfd


#
class ClassLoadFromDictDependingOnDictValue:
    #
    def __init__(self, dict_key_value: str, class_names_and_types: dict[str, Tuple[Callable[..., Any], str]], default_value: Any) -> None:
        #
        self.dict_key_value: str = dict_key_value
        self.class_names_and_types: dict[str, Tuple[Callable[..., Any], str]] = class_names_and_types
        self.default_value: Any = default_value


#
class DictOfClassLoadFromDictDependingOnDictValue:
    #
    def __init__(self, clfddodv: ClassLoadFromDictDependingOnDictValue, default_value: Optional[Any] = NoDefaultValues()) -> None:
        #
        self.clfddodv: ClassLoadFromDictDependingOnDictValue = clfddodv
        self.default_value: Optional[Any] = default_value


#
class DictOfClassLoadFromDict:
    #
    def __init__(self, clfd: ClassLoadFromDict, default_value: Optional[Any] = NoDefaultValues()) -> None:
        #
        self.clfd: ClassLoadFromDict = clfd
        self.default_value: Optional[Any] = default_value



#
def verif_id(elt_id: str, d: dict[str, Any]) -> Any:
    #
    if elt_id == "none":
        #
        return None
    #
    if elt_id not in d:
        #
        raise KeyError(f"Error: Id `{elt_id}` points out toward unknown object !")
    #
    return d[elt_id]

#
def verif_list_ids(elt_ids: str | list[str], d: dict[str, Any]) -> None:
    #
    if isinstance(elt_ids, str):
        #
        elt_ids = [elt_ids]
    #
    elt_id: str
    for elt_id in elt_ids:
        verif_id(elt_id=elt_id, d=d)


#
def verif_scene_action_label_exists(scene: scn.Scene, label_name: str) -> None:
    #
    action: act.Action
    #
    for action in scene.scenes_actions:
        #
        if isinstance(action, act.ActionLabel) and action.label_name == label_name:
            #
            return
    #
    raise KeyError(f"Error : ActionLabel with label_name `{label_name}` not found in scene's actions of scene `{scene.scene_id}` !")


#
def verif_game(game: ecg.Game) -> None:

    # Trucs à vérifier:
    #    - les ids des trucs désignés, il faut vérifier que les ids pointent vers des choses existantes

    #
    attr: str
    #
    thing: Thing
    thing_id: str
    for thing_id in game.things:

        #
        thing = game.things[thing_id]

        #
        if thing.id != thing_id:
            #
            raise IndexError(f"Error : Thing has different id that indexed from ! thing.id = `{thing.id}` != thing_id = {thing_id}")

        # TODO: Vérifier les pointages des unlock, parts, part_of, contains, inventory, missions, ...

        #
        verif_list_ids(thing.presets, game.things)

        # Verif attributes
        for attr in thing.attributes:
            #
            if attr not in ALL_ATTRIBUTES:
                #
                raise AttributeError(f"Error, unknown attribute `{attr}` for thing of id `{thing.id}`, the list of known attributes are : {ALL_ATTRIBUTES} ")

        #
        if isinstance(thing, Object):

            #
            verif_list_ids(thing.parts, game.things)
            verif_list_ids(thing.unlocks, game.things)
            verif_list_ids(list(thing.contains.keys()), game.things)
            verif_list_ids(thing.easy_to_unlock_from, game.rooms)

            #
            if thing.part_of is not None:
                #
                verif_id(thing.part_of, game.things)

        #
        elif isinstance(thing, Entity):
            #
            verif_list_ids(list(thing.inventory.keys()), game.things)

            #
            if isinstance(thing, Player):
                #
                verif_list_ids(thing.missions, game.missions)

    #
    room: Room
    room_id: str
    direct: Optional[str]
    for room_id in game.rooms:

        #
        room = game.rooms[room_id]

        # DONE: Vérifier les pointages des accès, et le world-direction

        #
        access: Access
        for access in room.accesses:
            #
            verif_id(access.links_to, game.rooms)
            verif_id(access.thing_id, game.things)
            #
            direct = parse_directions(access.direction)
            #
            if direct is None:
                #
                raise SyntaxError(f"Access direction is not a direction : `{access.direction}` from access : {access} from room : {room}")

    #
    action: act.Action
    #
    scene: scn.Scene
    scene_id: str
    for scene_id in game.scenes:

        #
        scene = game.scenes[scene_id]

        #
        if scene.scene_id != scene_id:
            #
            raise IndexError(f"Error : Scene has different id that indexed from ! scene.scene_id = `{scene.scene_id}` != scene_id = {scene_id}")

        #
        for action in scene.scenes_actions:

            #
            if isinstance(action, act.ActionJump) or isinstance(action, act.ActionConditionalJump):
                #
                verif_scene_action_label_exists(scene=scene, label_name=action.label_name)
            #
            elif isinstance(action, act.ActionChangeScene):
                #
                verif_id(action.scene_id, game.scenes)
            #
            elif isinstance(action, act.ActionChangeElt):
                #
                if action.elt_type in ["thing", "entity", "object", "player"]:
                    verif_id(action.elt_id, game.things)
                #
                elif action.elt_type == "room":
                    verif_id(action.elt_id, game.rooms)
                #
                elif action.elt_type == "scene":
                    verif_id(action.elt_id, game.scenes)
                #
                elif action.elt_type == "events":
                    verif_id(action.elt_id, game.events)
                #
                elif action.elt_type == "missions":
                    verif_id(action.elt_id, game.missions)

    #
    event: evt.Event
    event_id: str
    for event_id in game.events:

        #
        event = game.events[event_id]

        # DONE: Selon les types d'evenements, vérifier les pointages

        if isinstance(event, evt.EventMission):
            #
            verif_list_ids(event.mission_id, game.missions)
        #
        elif isinstance(event, evt.EventRoom):
            #
            verif_list_ids(event.room_id, game.rooms)
        #
        elif isinstance(event, evt.EventActionThing):
            #
            verif_list_ids(event.thing_id, game.things)
            verif_list_ids(event.entity_id, game.things)

    #
    mission: mis.Mission
    mission_id: str
    for mission_id in game.missions:

        #
        mission = game.missions[mission_id]

        # DONE: Selon le type des missions, vérifier les pointages

        #
        if isinstance(mission, mis.MissionRoom):
            #
            verif_list_ids(mission.room_id, game.rooms)

        #
        elif isinstance(mission, mis.MissionKillEntity):
            #
            verif_list_ids(mission.entity_id, game.things)


    # DONE: vérifier qu'il y a au moins 1 joueur
    if not game.players:
        #
        raise ValueError("Error: Empty player list !")

    #
    res: Any
    player_id: str
    for player_id in game.players:
        #

        # DONE: Vérifier que l'id existe et que c'est bien un type Player

        #
        res = verif_id(player_id, game.things)
        #
        if not isinstance(res, Player):
            #
            raise TypeError(f"Error: thing with id `{player_id}`, marked as player, is not of type Player !")



#
def apply_presets(game: ecg.Game) -> ecg.Game:

    #
    preset: Thing
    preset_id: str
    thing: Thing
    thing_id: str
    for thing_id in game.things:

        #
        thing = game.things[thing_id]

        #
        for preset_id in thing.presets:

            #
            if preset_id not in game.things:
                #
                raise IndexError(f"Preset not found in game.things : `{preset_id}` !")

            #
            preset = game.things[preset_id]

            #
            lcf.fusion_elts_str_or_None(
                obj_A=thing,
                obj_B=preset,
                lst_attr=["name", "description", "brief_description"]
            )

            #
            lcf.fusion_lists_str(
                obj_A=thing,
                obj_B=preset,
                lst_attr=["attributes"]
            )

            #
            if isinstance(thing, Object) and isinstance(preset, Object):

                #
                lcf.fusion_lists_str(
                    obj_A=thing,
                    obj_B=preset,
                    lst_attr=["parts", "unlocks", "easy_to_unlock_from"]
                )

                #
                lcf.fusion_dict_str(
                    obj_A=thing,
                    obj_B=preset,
                    lst_attr=["contains"]
                )

            #
            elif isinstance(thing, Entity) and isinstance(preset, Entity):

                #
                lcf.fusion_elts_str_or_None(
                    obj_A=thing,
                    obj_B=preset,
                    lst_attr=["room"]
                )

                #
                lcf.fusion_dict_str(
                    obj_A=thing,
                    obj_B=preset,
                    lst_attr=["inventory"]
                )

                if isinstance(thing, Player) and isinstance(preset, Player):

                    #
                    lcf.fusion_dict_str(
                        obj_A=thing,
                        obj_B=preset,
                        lst_attr=["missions"]
                    )

    #
    return game


#
def fusion_games(games: list[ecg.Game]) -> ecg.Game:
    #
    if len(games) == 0:
        raise SystemError("There are no games to fusion !")
    #
    game: ecg.Game = games[0]
    #
    other_game: ecg.Game
    i: int
    for i in range(1, len(games)):
        #
        other_game = games[i]

        #
        lcf.fusion_elts_str_or_None(
            obj_A=game,
            obj_B=other_game,
            lst_attr=["game_name", "game_description", "game_author"]
        )

        #
        lcf.fusion_dict_str(
            obj_A=game,
            obj_B=other_game,
            lst_attr=["things", "rooms", "scenes", "events", "missions"]
        )

        # TODO: Add the other things to fusion
        pass

    #
    return game


#
def load_interactive_fiction_model_from_file(filepath: str, game_save_format: str = "JSON", already_imported: set[str] = set()) -> ecg.Game:
    #
    if not os.path.isabs(filepath):
        filepath = os.path.abspath(filepath)

    #
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Error: file not found : `{filepath}`")

    #
    is_root: bool = len(already_imported) == 0

    #
    with open(filepath, "r", encoding="utf-8") as f:
        dict_: dict[str, Any] = json.load(f)

    #
    game: ecg.Game = create_class_with_attributes_or_default_values_from_dict(
        class_name=ecg.Game,
        in_dict=dict_,
        type_="ecg.Game"
    )

    #
    already_imported.add(filepath)

    #
    import_filepath: str
    import_path: str
    imported_games: list[ecg.Game] = []
    for import_path in game.imports:
        #
        import_filepath = os.path.join( os.path.dirname(filepath), import_path )
        #
        if import_filepath in already_imported:
            continue

        #
        already_imported.add(import_filepath)

        #
        imported_games.append(
            load_interactive_fiction_model_from_file(
                filepath=import_filepath,
                game_save_format=game_save_format,
                already_imported=already_imported
            )
        )

    #
    if imported_games:
        game = fusion_games([game] + imported_games)

    #
    if is_root:
        #
        game = apply_presets(game=game)
        #
        verif_game(game=game)

    #
    game.prepare_events_quick_access()

    #
    return game



#
def save_interactive_fiction_model_to_file(game: ecg.Game, filepath: str, game_save_format: str = "JSON") -> ecg.Game:
    #
    game.save_to_filepath(filepath, game_save_format)
    #
    return game


#
things_classes: ClassLoadFromDictDependingOnDictValue = ClassLoadFromDictDependingOnDictValue(
    dict_key_value="type",
    class_names_and_types={
        "entity": (Entity, "Entity"),
        "object": (Object, "Object"),
        "player": (Player, "Player")
    },
    default_value=None
)

#
actions_classes: ClassLoadFromDictDependingOnDictValue = ClassLoadFromDictDependingOnDictValue(
    dict_key_value="action_type",
    class_names_and_types={
        "Action": (act.Action, "Action"),
        "ActionText": (act.ActionText, "ActionText"),
        "ActionLabel": (act.ActionLabel, "ActionLabel"),
        "ActionJump": (act.ActionJump, "ActionJump"),
        "ActionConditionalJump": (act.ActionConditionalJump, "ActionConditionalJump"),
        "ActionChangeScene": (act.ActionChangeScene, "ActionChangeScene"),
        "ActionEndScene": (act.ActionEndScene, "ActionEndScene"),
        "ActionEndGame": (act.ActionEndGame, "ActionEndGame"),
        "ActionCreateVar": (act.ActionCreateVar, "ActionCreateVar"),
        "ActionEditVar": (act.ActionEditVar, "ActionEditVar"),
        "ActionDeleteVar": (act.ActionDeleteVar, "ActionDeleteVar"),
        "ActionBinaryOp": (act.ActionBinaryOp, "ActionBinaryOp"),
        "ActionUnaryOp": (act.ActionUnaryOp, "ActionUnaryOp"),
        "ActionChangeElt": (act.ActionChangeElt, "ActionChangeElt"),
        "ActionEditAttributeOfElt": (act.ActionEditAttributeOfElt, "ActionEditAttributeOfElt"),
        "ActionAppendToAttributeOfElt": (act.ActionAppendToAttributeOfElt, "ActionAppendToAttributeOfElt"),
        "ActionRemoveValueToAttributeOfElt": (act.ActionRemoveValueToAttributeOfElt, "ActionRemoveValueToAttributeOfElt"),
        "ActionSetKVAttributeOfElt": (act.ActionSetKVAttributeOfElt, "ActionSetKVAttributeOfElt"),
        "ActionThingDuplicate": (act.ActionThingDuplicate, "ActionThingDuplicate"),
        "ActionThingDisplace": (act.ActionThingDisplace, "ActionThingDisplace"),
        "ActionThingAddToPlace": (act.ActionThingAddToPlace, "ActionThingAddToPlace"),
        "ActionThingRemoveFromPlace": (act.ActionThingRemoveFromPlace, "ActionThingRemoveFromPlace"),
        "ActionPlayerAssignMission": (act.ActionPlayerAssignMission, "ActionPlayerAssignMission")
    },
    default_value=None
)

#
missions_classes: ClassLoadFromDictDependingOnDictValue = ClassLoadFromDictDependingOnDictValue(
    dict_key_value="mission_type",
    class_names_and_types={
        "Mission": (mis.Mission, "Mission"),
        "MissionEnterRoom": (mis.MissionEnterRoom, "MissionEnterRoom"),
        "MissionLeaveRoom": (mis.MissionLeaveRoom, "MissionLeaveRoom"),
        "MissionVariableCondition": (mis.MissionVariableCondition, "MissionVariableCondition"),
        "MissionKillEntity": (mis.MissionKillEntity, "MissionKillEntity")
    },
    default_value=None
)

#
events_classes: ClassLoadFromDictDependingOnDictValue = ClassLoadFromDictDependingOnDictValue(
    dict_key_value="event_type",
    class_names_and_types={
        "Event": (evt.Event, "Event"),
        "EventMissionGot": (evt.EventMissionGot, "EventMissionGot"),
        "EventMissionInProgress": (evt.EventMissionInProgress, "EventMissionInProgress"),
        "EventMissionDone": (evt.EventMissionDone, "EventMissionDone"),
        "EventEnterRoom": (evt.EventEnterRoom, "EventEnterRoom"),
        "EventLeaveRoom": (evt.EventLeaveRoom, "EventLeaveRoom"),
        "EventInsideRoom": (evt.EventInsideRoom, "EventInsideRoom"),
        "EventVariableCondition": (evt.EventVariableCondition, "EventVariableCondition"),
        "EventActionThing": (evt.EventActionThing, "EventActionThing"),
        "EventAlways": (evt.EventAlways, "EventAlways")
    },
    default_value=None
)

#
condition_classes: ClassLoadFromDictDependingOnDictValue = ClassLoadFromDictDependingOnDictValue(
    dict_key_value="condition_type",
    class_names_and_types={
        "ConditionVariable": (ecc.ConditionVariable, "ConditionVariable"),
        "ConditionAnd": (ecc.ConditionAnd, "ConditionAnd"),
        "ConditionOr": (ecc.ConditionOr, "ConditionOr")
    },
    default_value=None
)

#
things_dict: DictOfClassLoadFromDictDependingOnDictValue = DictOfClassLoadFromDictDependingOnDictValue(
    clfddodv=things_classes,
    default_value=EmptyDict()
)

#
rooms_dict: DictOfClassLoadFromDict = DictOfClassLoadFromDict(
    clfd=ClassLoadFromDict(
        class_name=Room,
        type_="Room"
    ),
    default_value=EmptyDict()
)

#
scenes_dict: DictOfClassLoadFromDict = DictOfClassLoadFromDict(
    clfd=ClassLoadFromDict(
        class_name=scn.Scene,
        type_="Scene"
    ),
    default_value=EmptyDict()
)

#
events_dict: DictOfClassLoadFromDictDependingOnDictValue = DictOfClassLoadFromDictDependingOnDictValue(
    clfddodv=events_classes,
    default_value=EmptyDict()
)

#
missions_dict: DictOfClassLoadFromDictDependingOnDictValue = DictOfClassLoadFromDictDependingOnDictValue(
    clfddodv=missions_classes,
    default_value=EmptyDict()
)


#
CLASS_ATTRIBUTES_AND_DEFAULT_VALUES: dict[str, Any] = {
    "Thing": {
        "id": NoDefaultValues(),
        "name": NoDefaultValues(),
        "description": "",
        "brief_description": "",
        "attributes": EmptyList(),
        "presets": EmptyList()
    },
    "Object": {
        "id": NoDefaultValues(),
        "name": NoDefaultValues(),
        "description": "",
        "brief_description": "",
        "attributes": EmptyList(),
        "parts": EmptyList(),
        "part_of": None,
        "unlocks": EmptyList(),
        "contains": EmptyDict(),
        "easy_to_unlock_from": EmptyList()
    },
    "LifeSystem": {
        "max_pv": 100,
        "current_pv": ValueOfAttribute(attr="max_pv"),
        "state": None
    },
    "Entity": {
        "id": NoDefaultValues(),
        "name": NoDefaultValues(),
        "description": "",
        "brief_description": "",
        "attributes": EmptyList(),
        "room": NoDefaultValues(),
        "inventory": EmptyDict(),
        "life_system": ClassLoadFromDict(class_name=LifeSystem, type_="LifeSystem")
    },
    "Player": {
        "id": NoDefaultValues(),
        "name": NoDefaultValues(),
        "description": "",
        "brief_description": "",
        "attributes": EmptyList(),
        "room": NoDefaultValues(),
        "inventory": EmptyDict(),
        "life_system": ClassLoadFromDict(class_name=LifeSystem, type_="LifeSystem"),
        "missions": EmptyList()
    },
    "Access": {
        "thing_id": NoDefaultValues(),
        "direction": NoDefaultValues(),
        "links_to": NoDefaultValues()
    },
    "Room": {
        "room_name": NoDefaultValues(),
        "accesses": NoDefaultValueListOfClassLoadFromDict(clfd=ClassLoadFromDict(class_name=Access, type_="Access")),
        "things_inside": EmptyDict(),
        "description": ""
    },
    "ecg.Game": {
        "game_name": "",
        "game_description": "",
        "game_author": "",
        "things": things_dict,
        "rooms": rooms_dict,
        "variables": EmptyDict(),
        "scenes": scenes_dict,
        "events": events_dict,
        "missions": missions_dict,
        "players": EmptyList(),
        "imports": EmptyList()
    },

    "ConditionVariable": {
        "variable_name": NoDefaultValues(),
        "cond_op": NoDefaultValues(),
        "operand_type": NoDefaultValues(),
        "operand_value": NoDefaultValues()
    },
    "ConditionAnd": {
        "conditions": NoDefaultValues()
    },
    "ConditionOr": {
        "conditions": NoDefaultValues()
    },

    "EventMissionGot": {
        "scene_id": NoDefaultValues(),
        "event_condition": condition_classes,
        "mission_id": NoDefaultValues()
    },
    "EventMissionInProgress": {
        "scene_id": NoDefaultValues(),
        "event_condition": condition_classes,
        "mission_id": NoDefaultValues()
    },
    "EventMissionDone": {
        "scene_id": NoDefaultValues(),
        "event_condition": condition_classes,
        "mission_id": NoDefaultValues()
    },
    "EventEnterRoom": {
        "scene_id": NoDefaultValues(),
        "event_condition": condition_classes,
        "room_id": NoDefaultValues()
    },
    "EventLeaveRoom": {
        "scene_id": NoDefaultValues(),
        "event_condition": condition_classes,
        "room_id": NoDefaultValues()
    },
    "EventInsideRoom": {
        "scene_id": NoDefaultValues(),
        "event_condition": condition_classes,
        "room_id": NoDefaultValues()
    },
    "EventInsideRoom": {
        "scene_id": NoDefaultValues(),
        "event_condition": condition_classes
    },
    "EventActionThing": {
        "scene_id": NoDefaultValues(),
        "event_condition": condition_classes,
        "thing_id": NoDefaultValues(),
        "action_type": NoDefaultValues(),
        "entity_id": NoDefaultValues()
    },
    "EventAlways": {
        "scene_id": NoDefaultValues(),
        "event_condition": condition_classes
    },

    "ActionText": {
        "text": NoDefaultValues()
    },
    "ActionLabel": {
        "label_name": NoDefaultValues()
    },
    "ActionJump": {
        "label_name": NoDefaultValues()
    },
    "ActionConditionalJump": {
        "label_name": NoDefaultValues(),
        "condition": condition_classes
    },
    "ActionChangeScene": {
        "scene_id": NoDefaultValues()
    },
    "ActionEndScene": {},
    "ActionEndGame": {
        "final_score": NoDefaultValues()
    },
    "ActionCreateVar": {
        "var_name": NoDefaultValues(),
        "var_value": NoDefaultValues()
    },
    "ActionEditVar": {
        "var_name": NoDefaultValues(),
        "var_value": NoDefaultValues()
    },
    "ActionDeleteVar": {
        "var_name": NoDefaultValues()
    },
    "ActionBinaryOp": {
        "var_output_name": NoDefaultValues(),
        "elt1_type": NoDefaultValues(),
        "elt1_value": NoDefaultValues(),
        "elt2_type": NoDefaultValues(),
        "elt2_value": NoDefaultValues(),
        "op": NoDefaultValues()
    },
    "ActionUnaryOp": {
        "var_output_name": NoDefaultValues(),
        "elt_type": NoDefaultValues(),
        "elt_value": NoDefaultValues(),
        "op": NoDefaultValues()
    },
    "ActionChangeElt": {
        "elt_id": NoDefaultValues(),
        "elt_type": NoDefaultValues(),
        "elt_attr_name": NoDefaultValues()
    },
    "ActionEditAttributeOfElt": {
        "elt_id": NoDefaultValues(),
        "elt_type": NoDefaultValues(),
        "elt_attr_name": NoDefaultValues(),
        "elt_attr_new_value": NoDefaultValues()
    },
    "ActionAppendToAttributeOfElt": {
        "elt_id": NoDefaultValues(),
        "elt_type": NoDefaultValues(),
        "elt_attr_name": NoDefaultValues(),
        "elt_attr_new_value_to_append": NoDefaultValues()
    },
    "ActionRemoveValueToAttributeOfElt": {
        "elt_id": NoDefaultValues(),
        "elt_type": NoDefaultValues(),
        "elt_attr_name": NoDefaultValues(),
        "elt_attr_value_to_remove": NoDefaultValues()
    },
    "ActionSetKVAttributeOfElt": {
        "elt_id": NoDefaultValues(),
        "elt_type": NoDefaultValues(),
        "elt_attr_name": NoDefaultValues(),
        "elt_attr_key": NoDefaultValues(),
        "elt_attr_value": NoDefaultValues()
    },
    "ActionThingDuplicate": {
        "src_elt_id": NoDefaultValues(),
        "dst_elt_id": NoDefaultValues()
    },
    "ActionThingDisplace": {
        "thing_id": NoDefaultValues(),
        "src_place_type": NoDefaultValues(),
        "src_place_id": NoDefaultValues(),
        "dst_place_type": NoDefaultValues(),
        "dst_place_id": NoDefaultValues(),
        "quantity": 1
    },
    "ActionThingAddToPlace": {
        "thing_id": NoDefaultValues(),
        "place_type": NoDefaultValues(),
        "place_id": NoDefaultValues(),
        "quantity": 1
    },
    "ActionThingRemoveFromPlace": {
        "thing_id": NoDefaultValues(),
        "place_type": NoDefaultValues(),
        "place_id": NoDefaultValues(),
        "quantity": 1
    },
    "ActionPlayerAssignMission": {
        "player_id": NoDefaultValues(),
        "mission_id": NoDefaultValues()
    },

    "MissionEnterRoom": {
        "mission_id": NoDefaultValues(),
        "room_id": NoDefaultValues(),
        "scene_mission_success": "",
        "scene_mission_failure": "",
        "failure_condition": condition_classes
    },
    "MissionLeaveRoom": {
        "mission_id": NoDefaultValues(),
        "room_id": NoDefaultValues(),
        "scene_mission_success": "",
        "scene_mission_failure": "",
        "failure_condition": condition_classes
    },
    "MissionVariableCondition": {
        "mission_id": NoDefaultValues(),
        "condition": condition_classes,
        "scene_mission_success": "",
        "scene_mission_failure": "",
        "failure_condition": condition_classes
    },
    "MissionKillEntity": {
        "mission_id": NoDefaultValues(),
        "entity_id": NoDefaultValues(),
        "scene_mission_success": "",
        "scene_mission_failure": "",
        "failure_condition": condition_classes
    }

}
