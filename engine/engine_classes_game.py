#
from typing import Any, Optional
#
import json
#
from .engine_classes_things_rooms import Thing, Room, Player, Entity
from . import engine_classes_missions as mis
from . import engine_classes_scenes as scn
from . import engine_classes_events as evt
from . import engine_results as er
from . import engine_classes_commands as ecc
from . import engine_classes_time as ect
#
from . import lib_utils as lu



#
class GameSettings:

    #
    def __init__(
        self,
        display_time_at_player_turn: bool = True,
        time_multiplier: float = 1,
    ) -> None:

        #
        self.display_time_at_player_turn: bool = display_time_at_player_turn
        self.time_multiplier: float = time_multiplier


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
        imports: list[str] = [],
        global_time: ect.GameTime = ect.GameTime(),
        game_settings: GameSettings = GameSettings()
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
        self.global_time: ect.GameTime = global_time
        #
        self.events_quick_access: dict[str, list[str]] = {}
        #
        self.priority_queue_events_and_entities: lu.PriorityQueue = lu.PriorityQueue()
        #
        self.variables_space: dict[str, Any] = {}
        #
        self.game_settings: GameSettings = game_settings
        #
        self.players_first_description: set[str] = set()

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
        event_id: str
        event: Any
        #
        for event_id, event in self.events.items():
            #
            class_name: str = lu.get_class_name( event )
            #
            if class_name not in self.events_quick_access:
                #
                self.events_quick_access[class_name] = []
            #
            self.events_quick_access[class_name].append( event_id )
            #
            if isinstance(event, evt.EventAlways):
                #
                self.priority_queue_events_and_entities.insert_with_priority(
                    item = lu.PQ_Entity_and_EventsSystem(
                        elt_id="event",
                        elt_type=event_id,
                        current_action=None,
                        current_action_time=event.time_delay,
                        can_be_interrupted=False,
                        repetitive=True
                    ),
                    priority=event.time_delay
                )

        #
        print(f"DEBUG | self.events_quick_access = {self.events_quick_access}")

    #
    def prepare_priority_queue_entities(self) -> None:

        #
        thing_id: str
        thing: Thing
        #
        for thing_id, thing in self.things.items():
            #
            if isinstance(thing, Entity):
                #
                self.priority_queue_events_and_entities.insert_with_priority(
                    item=lu.PQ_Entity_and_EventsSystem(
                        elt_type="entity",
                        elt_id=thing_id,
                        current_action=None,
                        current_action_time=ect.GameTime(),
                        can_be_interrupted=True,
                        repetitive=False
                    ),
                    priority=ect.GameTime()  # Time left before able to do something new
                )

    #
    def check_and_apply_events_from_command(self, command: ecc.Command, player: Player) -> None:
        #
        pass

    #
    def check_event(self, event: evt.Event) -> None:
        #
        pass

    #
    def next_event_or_entity_action(self) -> Optional[tuple[lu.PQ_Entity_and_EventsSystem, ect.GameTime]]:

        #
        return self.priority_queue_events_and_entities.pop_top()

