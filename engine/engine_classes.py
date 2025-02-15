#
from typing import Any, Optional, Callable, Tuple
#
import os
import json

# FORWARD CLASS FOR   from .engine_results import Result  (circular import else)
class Result:
    pass


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
            if isinstance(caadv, NoDefaultValues) or isinstance(caadv, NoDefaultValueDictOfClassLoadFromDict) or isinstance(caadv, NoDefaultValueDictOfClassLoadFromDictDependingOnDictValue):
                #
                raise KeyError(f"The attribute `{attr}` not in the dictionary for the type_ {type_} !\nNo default values authorized for this attribute.\n\nDictionary : {in_dict}\n\n")
            #
            kwargs[attr] = create_default_value(default_value=caadv, attr=attr, in_dict=in_dict, type_=type_)
            #
            continue
        #
        if isinstance(caadv, NoDefaultValueDictOfClassLoadFromDict):
            #
            kwargs[attr] = {}
            #
            k: str
            #
            for k in in_dict[attr]:
                #
                kwargs[attr][k] = caadv.clfd.class_name(**create_kwargs(in_dict[attr][k], type_=caadv.clfd.type_))
        #
        elif isinstance(caadv, NoDefaultValueDictOfClassLoadFromDictDependingOnDictValue):
            #
            kwargs[attr] = {}
            #
            key: str
            #
            for key in in_dict[attr]:
                #
                kwargs[attr][key] = create_classloadfromdictdependingondictvalue(clfddodv=caadv.clfddodv, in_dict=in_dict[attr], attr=key, type_=type_)
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
def create_class_with_attributes_or_default_values_from_dict(class_name: Callable, in_dict: dict, type_: str) -> Any:
    #
    kwargs: dict = create_kwargs(in_dict=in_dict, type_=type_)
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
class ClassLoadFromDictDependingOnDictValue:
    #
    def __init__(self, dict_key_value: str, class_names_and_types: dict[str, Tuple[Callable, str]], default_value: Any) -> None:
        #
        self.dict_key_value: str = dict_key_value
        self.class_names_and_types: dict[str, Tuple[Callable, str]] = class_names_and_types
        self.default_value: Any = default_value


#
class NoDefaultValueDictOfClassLoadFromDictDependingOnDictValue:
    #
    def __init__(self, clfddodv: ClassLoadFromDictDependingOnDictValue) -> None:
        #
        self.clfddodv: ClassLoadFromDictDependingOnDictValue = clfddodv


#
class NoDefaultValueDictOfClassLoadFromDict:
    #
    def __init__(self, clfd: ClassLoadFromDict) -> None:
        #
        self.clfd: ClassLoadFromDict = clfd


#
class Thing:
    #
    def __init__(
            self,
            id_: str,
            name: str,
            description: str = "",
            brief_description: str = "",
            attributes: list[str] = []
        ) -> None:
        #
        self.id: str = id_
        self.name: str = name
        self.description: str = description
        self.brief_description: str = brief_description
        self.attributes: list[str] = attributes

    #
    def to_dict(self) -> dict:
        #
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "brief_description": self.brief_description,
            "attributes": self.attributes
        }

    #
    def __str__(self) -> str:
        #
        return f"Thing({self.id}, {self.attributes})"

    #
    def __repr__(self) -> str:
        #
        return self.__str__()


#
class Object(Thing):
    #
    def __init__(
            self,
            id_: str,
            name: str,
            description: str = "",
            brief_description: str = "",
            attributes: list[str] = [],
            parts: list[str] = [],
            part_of: Optional[str] = None,
            is_open: int = 0,
            is_locked: int = 0,
            unlocks: list[str] = [],
            contains: Optional[dict[str, int]] = None
        ) -> None:
        #
        super().__init__(
                    id_=id_,
                    name=name,
                    description=description,
                    brief_description=brief_description,
                    attributes=attributes
        )
        #
        self.parts: list[str] = parts
        self.part_of: Optional[str] = part_of
        self.is_open: int = is_open
        self.is_locked: int = is_locked
        self.unlocks: list[str] = unlocks
        self.contains: dict[str, int] = {} if contains is None else contains

    #
    def to_dict(self) -> dict:
        #
        res: dict = super().to_dict()
        #
        res["parts"] = self.parts
        res["part_of"] = self.part_of
        res["is_open"] = self.is_open
        res["is_locked"] = self.is_locked
        res["unlocks"] = self.unlocks
        res["contains"] = self.contains
        #
        return res


#
class LifeSystem:
    #
    def __init__(
            self,
            max_pv: int = 100,
            current_pv: Optional[int] = None,
            state: Optional[dict[str, Any]] = None
        ) -> None:
        #
        self.max_pv: int = max_pv
        self.current_pv: int = current_pv if isinstance(current_pv, int) else self.max_pv
        self.state: dict[str, Any] = state if isinstance(state, dict) else {}

    #
    def to_dict(self) -> dict:
        #
        return {
            "max_pv": self.max_pv,
            "current_pv": self.current_pv,
            "state": self.state
        }

    #
    def __str__(self) -> str:
        #
        return f"[{self.current_pv}/{self.max_pv}pv]"

    #
    def __repr__(self) -> str:
        #
        return self.__str__()


#
class Entity(Thing):
    #
    def __init__(
            self,
            id_: str,
            name: str,
            room: str,
            description: str = "",
            brief_description: str = "",
            attributes: list[str] = [],
            inventory: Optional[dict[str, int]] = None,
            life_system: LifeSystem = LifeSystem()
        ) -> None:
        #
        super().__init__(
                    id_=id_,
                    name=name,
                    description=description,
                    brief_description=brief_description,
                    attributes=attributes
        )
        #
        self.room: str = room
        self.inventory: dict[str, int] = inventory if isinstance(inventory, dict) else {}
        self.life_system: LifeSystem = life_system

    #
    def to_dict(self) -> dict:
        #
        res: dict = super().to_dict()
        #
        res["room"] = self.room
        res["inventory"] = self.inventory
        res["life_system"] = self.life_system.to_dict()
        #
        return res

    #
    def __str__(self) -> str:
        #
        return f"Entity({self.id}, in {self.room}, {self.life_system}, {self.attributes})"

    #
    def __repr__(self) -> str:
        #
        return self.__str__()


#
class Access:
    #
    def __init__(
            self,
            thing_id: str,
            world_direction: str,
            links_to: str
        ) -> None:
        #
        self.thing_id: str = thing_id
        self.world_direction: str = world_direction
        self.links_to: str = links_to

    #
    def to_dict(self) -> dict:
        #
        return {
            "thing_id": self.thing_id,
            "world_direction": self.world_direction,
            "links_to": self.links_to
        }

    #
    def __str__(self) -> str:
        #
        return f"You can go to {self.links_to} by {self.thing_id} [{self.world_direction}]"

    #
    def __repr__(self) -> str:
        #
        return self.__str__()


#
class Room:
    #
    def __init__(
            self,
            room_name: str,
            accesses: list[ Access ],
            description: str = "",
            things_inside: Optional[dict[str, int]] = None
        ) -> None:
        #
        self.room_name: str = room_name
        self.accesses: list[ Access ] = accesses
        self.description: str = description
        self.things_inside: dict[str, int] = {} if things_inside is None else things_inside

    #
    def to_dict(self) -> dict:
        #
        return {
            "room_name": self.room_name,
            "accesses": [
                access.to_dict() for access in self.accesses
            ],
            "description": self.description,
            "things_inside": self.things_inside
        }

    #
    def __str__(self) -> str:
        #
        return f"\n\nRoom:\n  + Room name = {self.room_name}\n{'  + Inside the room:\n\t-' if self.things_inside else ''}{'\n\t-'.join(self.things_inside)}"

    #
    def __repr__(self) -> str:
        #
        return self.__str__()


#
class End:
    #
    def to_dict(self) -> dict:
        #
        return {
            "end_type_": "End"
        }


#
class EndOneOf(End):
    #
    def __init__(self, end_type: str, lst_of_ends: list[ End ]) -> None:
        #
        super().__init__()
        #
        self.lst: list[ End ] = lst_of_ends

    #
    def to_dict(self) -> dict:
        #
        return {
            "end_type_": "EndOneOf",
            "lst": [
                end.to_dict() for end in self.lst
            ]
        }


#
class EndAllOf(End):
    #
    def __init__(self, end_type: str, lst_of_ends: list[ End ]) -> None:
        #
        super().__init__()
        #
        self.lst: list[ End ] = lst_of_ends

    #
    def to_dict(self) -> dict:
        #
        return {
            "end_type_": "EndAllOf",
            "lst": [
                end.to_dict() for end in self.lst
            ]
        }


#
class EndInsideRoom(End):
    #
    def __init__(self, end_type: str, room_id: str) -> None:
        #
        super().__init__()
        #
        self.room_id: str = room_id

    #
    def to_dict(self) -> dict:
        #
        return {
            "end_type_": "EndInsideRoom",
            "room_id": self.room_id
        }


#
class EndEntityDead(End):
    #
    def __init__(self, end_type: str, entity_id: str) -> None:
        #
        super().__init__()
        #
        self.entity_id: str = entity_id

    #
    def to_dict(self) -> dict:
        #
        return {
            "end_type_": "EndEntityDead",
            "entity_id": self.entity_id
        }


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
            end: End,
            players: list[str],
            nb_turns: int = 0
        ) -> None:
        #
        self.game_name: str = game_name
        self.game_description: str = game_description
        self.game_author: str = game_author
        self.things: dict[str, Thing] = things
        self.rooms: dict[str, Room] = rooms
        self.variables: dict[str, Any] = variables
        self.end: End = end
        self.nb_turns: int = nb_turns
        self.players: list[str] = players
        self.nb_players: int = len(self.players)
        self.current_player: int = 0
        self.history: list[Result] = []

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
            "end": self.end.to_dict(),
            "players": self.players
        }

        #
        k: str
        for k in self.things:
            res["things"][k] = self.things[k].to_dict()
        #
        for k in self.rooms:
            res["rooms"][k] = self.rooms[k].to_dict()

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
def load_interactive_fiction_model_from_file(filepath: str, game_save_format: str = "JSON") -> Game:
    #
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Error: file not found : `{filepath}`")
    #
    with open(filepath, "r", encoding="utf-8") as f:
        dict_: dict = json.load(f)
    #
    return create_class_with_attributes_or_default_values_from_dict(
        class_name=Game,
        in_dict=dict_,
        type_="Game"
    )



#
def save_interactive_fiction_model_to_file(game: Game, filepath: str, game_save_format: str = "JSON") -> Game:
    #
    game.save_to_filepath(filepath, game_save_format)
    #
    return game


#
end_classes: ClassLoadFromDictDependingOnDictValue = ClassLoadFromDictDependingOnDictValue(
    dict_key_value="end_type",
    class_names_and_types={
        "EndAllOf": (EndAllOf, "EndAllOf"),
        "EndOneOf": (EndOneOf, "EndOneOf"),
        "EndInsideRoom": (EndInsideRoom, "EndInsideRoom"),
        "EndEntityDead": (EndEntityDead, "EndEntityDead")
    },
    default_value=End()
)


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
things_dict: NoDefaultValueDictOfClassLoadFromDictDependingOnDictValue = NoDefaultValueDictOfClassLoadFromDictDependingOnDictValue(
    clfddodv=things_classes
)


#
rooms_dict: NoDefaultValueDictOfClassLoadFromDict = NoDefaultValueDictOfClassLoadFromDict(
    clfd=ClassLoadFromDict(
        class_name=Room,
        type_="Room"
    )
)


#
CLASS_ATTRIBUTES_AND_DEFAULT_VALUES: dict = {
    "Thing": {
        "id": NoDefaultValues(),
        "name": NoDefaultValues(),
        "description": "",
        "brief_description": "",
        "attributes": EmptyList()
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
        "contains": EmptyDict()
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
        "world_direction": NoDefaultValues(),
        "links_to": NoDefaultValues()
    },
    "Room": {
        "room_name": NoDefaultValues(),
        "accesses": NoDefaultValues(),
        "things_inside": EmptyDict(),
        "description": ""
    },
    "Game": {
        "game_name": NoDefaultValues(),
        "game_description": NoDefaultValues(),
        "game_author": "",
        "things": things_dict,
        "rooms": rooms_dict,
        "variables": EmptyDict(),
        "end": end_classes,
        "players": NoDefaultValues()
    },
    "EndInsideRoom": {
        "end_type": NoDefaultValues(),
        "room_id": NoDefaultValues()
    },
    "EndEntityDead": {
        "end_type": NoDefaultValues(),
        "entity_id": NoDefaultValues()
    },
    "EndAllOf": {
        "end_type": NoDefaultValues(),
        "lst": EmptyList()
    },
    "EndAnyOf": {
        "end_type": NoDefaultValues(),
        "lst": EmptyList()
    }
}
