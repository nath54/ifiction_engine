#
from typing import Any, Optional
#
import os
import json


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
            is_open: int = 1,
            is_locked: int = 1,
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
        return {}


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
        # TODO
        return {}


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
        # TODO
        return {}


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
        # TODO
        return {}


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
        # TODO
        return {}


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
