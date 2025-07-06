#
from typing import Any
#
import json
#
from .engine_classes_things_rooms import Thing, Room
from . import engine_classes_missions as mis
from . import engine_classes_scenes as scn
from . import engine_classes_events as evt
from . import engine_results as er
#
from . import lib_utils as lu


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
        self.events_quick_access: dict[str, list[str]] = {}

    #
    def __str__(self) -> str:
        #
        return f"Game:\n\t-game name = {self.game_name}\n\t-game author = {self.game_author}\n\n*Things:\n\n{'\n\n'.join(t.__str__() for t in self.things.values())}\n\n*Rooms:\n\n{'\n\n'.join(t.__str__() for t in self.rooms.values())}\n\n*variables : {self.variables}\n\n*players : {self.players}\n\n*nb turns : {self.nb_turns}"

    #
    def __repr__(self) -> str:
        #
        return self.__str__()

    #
    def to_dict(self) -> dict[str, Any]:
        #
        res: dict[str, Any] = {
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
            game_dict: dict[str, Any] = self.to_dict()

            #
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(game_dict, f)
        #
        else:
            raise UserWarning(f"ERROR: Unkown IFICTION game save format : `{game_save_format}`")

    #
    def prepare_events_quick_access(self) -> None:
        #
        key: str
        evt: Any
        #
        for key, evt in self.events.items():
            #
            class_name: str = lu.get_class_name( evt )
            #
            if class_name not in self.events_quick_access:
                #
                self.events_quick_access[class_name] = []
            #
            self.events_quick_access[class_name].append( key )
