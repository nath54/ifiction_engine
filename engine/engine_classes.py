#
from typing import Any, Optional, Callable, Tuple
#
import os
import json
#
from .engine_classes_things_rooms import Thing, Object, LifeSystem, Entity, Player, Access, Room
from . import missions as mis
from . import scenes as scn
from . import actions as act
from . import events as evt
from . import engine_results as er
#
from .lib_direction import parse_directions

#
def verify_keys_in_dict(dictionary: dict, keys: list[str], type_: str) -> None:
    #
    k: str
    for k in keys:
        if k not in keys:
            raise KeyError(f"The key `{k}` not in the dictionary for the type_ {type_} !\n\nDictionary : {dictionary}\n\n")


#
def create_default_value(default_value: Any, attr: str, in_dict: dict, type_: str) -> Any:
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
def create_classloadfromdictdependingondictvalue(clfddodv: "ClassLoadFromDictDependingOnDictValue", in_dict: dict, attr: str, type_: str) -> Any:
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
def create_kwargs(in_dict: dict, type_: str) -> dict:
    #
    kwargs: dict = {}
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
def set_attributes_or_default_values_from_dict(obj: Any, in_dict: dict, type_: str) -> None:
    #
    kwargs: dict = create_kwargs(in_dict=in_dict, type_=type_)
    #
    attr: str
    #
    for attr in kwargs:
        setattr(obj, attr, kwargs[attr])


#
def create_class_with_attributes_or_default_values_from_dict(class_name: Callable, in_dict: Optional[dict], type_: str) -> Any:
    #
    if in_dict is None:
        in_dict = {}
    #
    kwargs: dict = create_kwargs(in_dict=in_dict, type_=type_)
    #
    print(f"DEBUG | create_class_with_attributes_or_default_values_from_dict\n\t- class_name: {class_name}\n\t- type_: {type_}\n\t- in_dict: {in_dict}\n\t- kwargs = {kwargs}")
    #
    return class_name(**kwargs)


#
class NoDefaultValues:
    #
    def __init__(self, have_type_: Optional[str] = None, class_name: Optional[Callable] = None, type_: Optional[str] = None) -> None:
        self.have_type_: Optional[str] = have_type_
        self.class_name: Optional[Callable] = class_name
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
    def __init__(self, class_name: Callable, type_: str) -> None:
        #
        self.class_name: Callable = class_name
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
    def __init__(self, dict_key_value: str, class_names_and_types: dict[str, Tuple[Callable, str]], default_value: Any) -> None:
        #
        self.dict_key_value: str = dict_key_value
        self.class_names_and_types: dict[str, Tuple[Callable, str]] = class_names_and_types
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
class Game:
    #
    def __init__(
            self,
            game_name: str,
            game_description: str,
            game_author: str,
            things: dict[str, Thing],
            rooms: dict[str, Room],
            variables: dict[str, Any],
            scenes: dict[str, scn.Scene],
            events: dict[str, evt.Event],
            missions: dict[str, mis.Mission],
            players: list[str],
            nb_turns: int = 0,
            imports: list[str] = []
        ) -> None:
        #
        self.game_name: str = game_name
        self.game_description: str = game_description
        self.game_author: str = game_author
        self.things: dict[str, Thing] = things
        self.rooms: dict[str, Room] = rooms
        self.variables: dict[str, Any] = variables
        self.scenes: dict[str, scn.Scene] = scenes
        self.events: dict[str, evt.Event] = events
        self.missions: dict[str, mis.Mission] = missions
        self.nb_turns: int = nb_turns
        self.players: list[str] = players
        self.nb_players: int = len(self.players)
        self.imports: list[str] = imports
        self.current_player: int = 0
        self.history: list[er.Result] = []

    #
    def __str__(self) -> str:
        #
        return f"Game:\n\t-game name = {self.game_name}\n\t-game author = {self.game_author}\n\n*Things:\n\n{'\n\n'.join(t.__str__() for t in self.things.values())}\n\n*Rooms:\n\n{'\n\n'.join(t.__str__() for t in self.rooms.values())}\n\n*variables : {self.variables}\n\n*players : {self.players}\n\n*nb turns : {self.nb_turns}"

    #
    def __repr__(self) -> str:
        #
        return self.__str__()

    #
    def to_dict(self) -> dict:
        #
        res: dict = {
            "game_name": self.game_name,
            "game_author": self.game_author,
            "things": {},
            "rooms": {},
            "variables": self.variables,
            "scenes": {},
            "events": {},
            "missions": {},
            "players": self.players,
            "current_player": self.current_player,
            "nb_turns": self.nb_turns,
            "history": [
                r.to_dict() for r in self.history
            ]
        }

        #
        k: str
        for k in self.things:
            res["things"][k] = self.things[k].to_dict()
        #
        for k in self.rooms:
            res["rooms"][k] = self.rooms[k].to_dict()
        #
        for k in self.scenes:
            res["scenes"][k] = self.scenes[k].to_dict()
        #
        for k in self.events:
            res["events"][k] = self.events[k].to_dict()
        #
        for k in self.missions:
            res["missions"][k] = self.missions[k].to_dict()

        #
        return res


    #
    def save_to_filepath(self, filepath: str, game_save_format: str = "JSON") -> None:
        #
        if game_save_format == "JSON":
            #
            game_dict: dict = self.to_dict()

            #
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(game_dict, f)
        #
        else:
            raise UserWarning(f"ERROR: Unkown IFICTION game save format : `{game_save_format}`")


#
def verif_game(game: Game) -> None:

    #
    ids_to_verify: list[tuple[str, dict]] = []

    # Trucs à vérifier:
    #    - les ids des trucs désignés, il faut vérifier que les ids pointent vers des choses existantes

    #
    thing: Thing
    thing_id: str
    for thing_id in game.things:

        #
        thing = game.things[thing_id]

        # TODO: Vérifier les pointages des unlock, parts, part_of, contains, inventory, missions, ...
        pass

        #
        if isinstance(thing, Object):
            #
            pass

        #
        elif isinstance(thing, Entity):
            #
            pass

            #
            if isinstance(thing, Player):
                #
                pass

    #
    room: Room
    room_id: str
    direct: Optional[str]
    for room_id in game.rooms:

        #
        room = game.rooms[room_id]

        # TODO: Vérifier les pointages des accès, et le world-direction
        pass

        #
        access: Access
        for access in room.accesses:
            #
            ids_to_verify.append( (access.links_to, game.rooms) )
            ids_to_verify.append( (access.thing_id, game.things) )
            #
            direct = parse_directions(access.direction)
            #
            if direct is None:
                #
                raise SyntaxError(f"Access direction is not a direction : `{access.direction}` from access : {access} from room : {room}")

    #
    scene: scn.Scene
    scene_id: str
    for scene_id in game.scenes:

        #
        scene = game.scenes[scene_id]

        # TODO: Selon les types d'evenements, vérifier les pointages
        pass

    #
    event: evt.Event
    event_id: str
    for event_id in game.events:

        #
        event = game.events[event_id]

        # TODO: Selon les types d'evenements, vérifier les pointages
        pass

    #
    mission: mis.Mission
    mission_id: str
    for mission_id in game.missions:

        #
        mission = game.missions[mission_id]

        # TODO: Selon le type des missions, vérifier les pointages
        pass

    #
    player_id: str
    for player_id in game.players:
        #

        # TODO: Vérifier que l'id existe et que c'est bien un type Player
        pass

    # TODO
    pass


#
def apply_presets(game: Game) -> Game:

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

            # TODO
            pass

    #
    return game


#
def fusion_games(games: list[Game]) -> Game:
    #
    if len(games) == 0:
        raise SystemError("There are no games to fusion !")
    #
    game: Game = games[0]
    #
    attr: str
    elt_id: str
    #
    other_game: Game
    i: int
    for i in range(1, len(games)):
        #
        other_game = games[i]

        #
        for attr in ["game_name", "game_description", "game_author"]:
            #
            if getattr(game, attr) == "":
                setattr(game, attr, getattr(other_game, attr))

        #
        for attr in ["things", "rooms", "scenes", "events", "missions"]:
            #
            other_game_dict: dict = getattr(other_game, attr)
            game_dict: dict = getattr(game, attr)
            #
            for elt_id in other_game_dict:
                #
                if elt_id not in game_dict:
                    game_dict[elt_id] = other_game_dict[elt_id]

        # TODO: Add the other things to fusion
        pass

    #
    return game


#
def load_interactive_fiction_model_from_file(filepath: str, game_save_format: str = "JSON", already_imported: set[str] = set()) -> Game:
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
        dict_: dict = json.load(f)

    #
    game: Game = create_class_with_attributes_or_default_values_from_dict(
        class_name=Game,
        in_dict=dict_,
        type_="Game"
    )

    #
    print(f"DEBUG | game = {game}")

    #
    already_imported.add(filepath)

    #
    import_filepath: str
    import_path: str
    imported_games: list[Game] = []
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
    return game



#
def save_interactive_fiction_model_to_file(game: Game, filepath: str, game_save_format: str = "JSON") -> Game:
    #
    game.save_to_filepath(filepath, game_save_format)
    #
    return game


#
things_classes: ClassLoadFromDictDependingOnDictValue = ClassLoadFromDictDependingOnDictValue(
    dict_key_value="type",
    class_names_and_types={
        "entity": (Entity, "Entity"),
        "object": (Object, "Object")
    },
    default_value=None
)

#
actions_classes: ClassLoadFromDictDependingOnDictValue = ClassLoadFromDictDependingOnDictValue(
    dict_key_value="action_type",
    class_names_and_types={
        "action": (act.Action, "Action")
    },
    default_value=None
)

#
missions_classes: ClassLoadFromDictDependingOnDictValue = ClassLoadFromDictDependingOnDictValue(
    dict_key_value="mission_type",
    class_names_and_types={
        "mission": (mis.Mission, "Mission")
    },
    default_value=None
)

#
events_classes: ClassLoadFromDictDependingOnDictValue = ClassLoadFromDictDependingOnDictValue(
    dict_key_value="event_type",
    class_names_and_types={
        "event": (evt.Event, "Event")
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
CLASS_ATTRIBUTES_AND_DEFAULT_VALUES: dict = {
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
    "Game": {
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
    }
}
