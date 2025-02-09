#
from typing import Any, Optional, Callable
#
import os
import json


#
def verify_keys_in_dict(dictionary: dict, keys: list[str], type_: str) -> None:
    #
    k: str
    for k in keys:
        if k not in keys:
            raise KeyError(f"The key `{k}` not in the dictionary for the type_ {type_} !\n\nDictionary : {dictionary}\n\n")


#
def create_kwargs(in_dict: dict, type_: str) -> dict:
    #
    kwargs: dict = {}
    #
    attr: str
    for attr in CLASS_ATTRIBUTES_AND_DEFAULT_VALUES[type_]:
        #
        if attr not in in_dict:
            #
            if isinstance(CLASS_ATTRIBUTES_AND_DEFAULT_VALUES[type_][attr], NoDefaultValues):
                #
                raise KeyError(f"The attribute `{attr}` not in the dictionary for the type_ {type_} !\n\nDictionary : {in_dict}\n\n")
            #
            elif isinstance(CLASS_ATTRIBUTES_AND_DEFAULT_VALUES[type_][attr], EmptyDict):
                #
                kwargs[attr] = {}
            #
            elif isinstance(CLASS_ATTRIBUTES_AND_DEFAULT_VALUES[type_][attr], EmptyList):
                #
                kwargs[attr] = []
            #
            elif isinstance(CLASS_ATTRIBUTES_AND_DEFAULT_VALUES[type_][attr], ClassLoadFromDict):
                #
                kwargs[attr] = create_class_with_attributes_or_default_values_from_dict(
                    class_name=CLASS_ATTRIBUTES_AND_DEFAULT_VALUES[type_][attr].class_name,
                    in_dict=in_dict[attr],
                    type_=CLASS_ATTRIBUTES_AND_DEFAULT_VALUES[type_][attr].type_
                )
            #
            else:
                #
                kwargs[attr] = CLASS_ATTRIBUTES_AND_DEFAULT_VALUES[type_][attr]
        #
        else:
            #
            if hasattr(CLASS_ATTRIBUTES_AND_DEFAULT_VALUES[type_][attr], "class_name") and hasattr(CLASS_ATTRIBUTES_AND_DEFAULT_VALUES[type_][attr], "type_") and (CLASS_ATTRIBUTES_AND_DEFAULT_VALUES[type_][attr].class_name is not None) and (CLASS_ATTRIBUTES_AND_DEFAULT_VALUES[type_][attr].type_ is not None):
                #
                kwargs[attr] = create_class_with_attributes_or_default_values_from_dict(
                    class_name=CLASS_ATTRIBUTES_AND_DEFAULT_VALUES[type_][attr].class_name,
                    in_dict=in_dict[attr],
                    type_=CLASS_ATTRIBUTES_AND_DEFAULT_VALUES[type_][attr].type_
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
    pass


#
class EmptyList:
    pass


#
class ClassLoadFromDict:
    #
    def __init__(self, class_name: Callable, type_: str) -> None:
        #
        self.class_name: Callable = class_name
        self.type_: str = type_

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
            unlocks: list[str] = []
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
class Room:
    #
    def __init__(
            self,
            room_name: str,
            accesses: list[ Access ],
            description: str = ""
        ) -> None:
        #
        self.room_name: str = room_name
        self.accesses: list[ Access ] = accesses
        self.description: str = description

    #
    def to_dict(self) -> dict:
        #
        return {
            "room_name": self.room_name,
            "accesses": [
                access.to_dict() for access in self.accesses
            ],
            "description": self.description
        }


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
    def __init__(self, lst_of_ends: list[ End ]) -> None:
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
    def __init__(self, lst_of_ends: list[ End ]) -> None:
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
    def __init__(self, room_id: str) -> None:
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
    def __init__(self, entity_id: str) -> None:
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
    def __init__(self) -> None:
        #
        self.game_name: str = ""
        self.game_description: str = ""
        self.game_author: str = ""
        self.things: dict[str, Thing] = {}
        self.rooms: dict[str, Room] = {}
        self.variables: dict[str, Any] = {}
        self.end: End = End()
        self.players: list[str] = []

    #
    def load_from_dict(self, game_dict: dict) -> None:
        # TODO
        pass

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
    def load_from_filepath(self, filepath: str, game_save_format: str = "JSON") -> None:
        #
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"This file wasn't found : {filepath} !")

        #
        if game_save_format == "JSON":
            #
            game_dict: dict

            #
            with open(filepath, "r", encoding="utf-8") as f:
                game_dict = json.load(f)

            #
            self.load_from_dict(game_dict)
        #
        else:
            raise UserWarning(f"ERROR: Unkown IFICTION game save format : `{game_save_format}`")


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
    game: Game = Game()
    #
    game.load_from_filepath(filepath, game_save_format)
    #
    return game



#
def save_interactive_fiction_model_from_file(filepath: str, game_save_format: str = "JSON") -> Game:
    #
    game: Game = Game()
    #
    game.save_to_filepath(filepath, game_save_format)
    #
    return game



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
        "is_open": 0,
        "is_locked": 0,
        "unlocks": EmptyList()
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
        "life_system": ClassLoadFromDict(class_name=LifeSystem)
    },
    "Access": {
        "thing_id": NoDefaultValues(),
        "world_direction": NoDefaultValues(),
        "links_to": NoDefaultValues()
    },
    "Room": {
        "room_name": NoDefaultValues(),
        "accesses": NoDefaultValues(),
        "description": ""
    },
    "Game": {
        "game_name": NoDefaultValues(),
        "game_description": NoDefaultValues(),
        "game_author": "",
        "things": NoDefaultValues(),
        "rooms": NoDefaultValues(),
        "variables": EmptyDict(),
        "end": NoDefaultValues(),
        "players": NoDefaultValues()
    }
}
