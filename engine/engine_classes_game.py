#
from typing import Any, Optional
#
import json
#
from .engine_classes_things_rooms import Thing, Room, Player, Entity
from . import engine_classes_missions as mis
from . import engine_classes_scenes as scn
from . import engine_classes_actions as eca
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
        self.current_scene_id: str = ""
        self.current_scene_cursor: int = 0

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
    def next_event_or_entity_action(self) -> Optional[tuple[lu.PQ_Entity_and_EventsSystem, ect.GameTime]]:

        #
        return self.priority_queue_events_and_entities.pop_top()

    #
    def manage_npc_entities(self, elt: lu.PQ_Entity_and_EventsSystem) -> None:

        # TODO
        pass

    #
    def manage_event(self, elt: lu.PQ_Entity_and_EventsSystem) -> None:

        #
        event: evt.Event = self.events[elt.elt_id]
        #
        if isinstance(event, evt.EventAlways):

            #
            if event.event_condition is None or event.event_condition.verify(variables_space=self.variables_space):

                #
                self.play_scene( scene_id = event.scene_id )

        #
        if elt.repetitive:
            #
            self.priority_queue_events_and_entities.insert_with_priority(
                item=elt,
                priority=elt.current_action_time
            )

    #
    def play_scene(self, scene_id: str) -> None:

        #
        self.current_scene_id = scene_id
        self.current_scene_cursor = 0
        #
        while self.current_scene_id in self.scenes and self.current_scene_cursor >= 0 and self.current_scene_cursor < len(self.scenes[self.current_scene_id].scenes_actions):

            #
            self.play_scene_action( scene_action = self.scenes[self.current_scene_id].scenes_actions[self.current_scene_cursor] )

        #
        self.current_scene_id = ""

    #
    def play_scene_action(self, scene_action: eca.Action) -> None:

        #
        if isinstance(scene_action, eca.ActionText):
            #
            gamePlayActionText(game=self, action=scene_action)

        #
        elif isinstance(scene_action, eca.ActionLabel):
            #
            gamePlayActionLabel(game=self, action=scene_action)

        #
        elif isinstance(scene_action, eca.ActionJump):
            #
            gamePlayActionJump(game=self, action=scene_action)

        #
        elif isinstance(scene_action, eca.ActionConditionalJump):
            #
            gamePlayActionConditionalJump(game=self, action=scene_action)

        #
        elif isinstance(scene_action, eca.ActionChangeScene):
            #
            gamePlayActionChangeScene(game=self, action=scene_action)

        #
        elif isinstance(scene_action, eca.ActionConditionalChangeScene):
            #
            gamePlayActionConditionalChangeScene(game=self, action=scene_action)

        #
        elif isinstance(scene_action, eca.ActionEndScene):
            #
            gamePlayActionEndScene(game=self, action=scene_action)

        #
        elif isinstance(scene_action, eca.ActionConditionalEndScene):
            #
            gamePlayActionConditionalEndScene(game=self, action=scene_action)

        #
        elif isinstance(scene_action, eca.ActionEndGame):
            #
            gamePlayActionEndGame(game=self, action=scene_action)

        #
        elif isinstance(scene_action, eca.ActionConditionalEndGame):
            #
            gamePlayActionConditionalEndGame(game=self, action=scene_action)

        #
        elif isinstance(scene_action, eca.ActionCreateVar):
            #
            gamePlayActionCreateVar(game=self, action=scene_action)

        #
        elif isinstance(scene_action, eca.ActionEditVar):
            #
            gamePlayActionEditVar(game=self, action=scene_action)

        #
        elif isinstance(scene_action, eca.ActionDeleteVar):
            #
            gamePlayActionDeleteVar(game=self, action=scene_action)

        #
        elif isinstance(scene_action, eca.ActionBinaryOp):
            #
            gamePlayActionBinaryOp(game=self, action=scene_action)

        #
        elif isinstance(scene_action, eca.ActionUnaryOp):
            #
            gamePlayActionUnaryOp(game=self, action=scene_action)

        #
        elif isinstance(scene_action, eca.ActionChangeElt):
            #
            gamePlayActionChangeElt(game=self, action=scene_action)

        #
        elif isinstance(scene_action, eca.ActionEditAttributeOfElt):
            #
            gamePlayActionEditAttributeOfElt(game=self, action=scene_action)

        #
        elif isinstance(scene_action, eca.ActionAppendToAttributeOfElt):
            #
            gamePlayActionAppendToAttributeOfElt(game=self, action=scene_action)

        #
        elif isinstance(scene_action, eca.ActionRemoveValueToAttributeOfElt):
            #
            gamePlayActionRemoveValueToAttributeOfElt(game=self, action=scene_action)

        #
        elif isinstance(scene_action, eca.ActionSetKVAttributeOfElt):
            #
            gamePlayActionSetKVAttributeOfElt(game=self, action=scene_action)

        #
        elif isinstance(scene_action, eca.ActionThingDuplicate):
            #
            gamePlayActionThingDuplicate(game=self, action=scene_action)

        #
        elif isinstance(scene_action, eca.ActionThingDisplace):
            #
            gamePlayActionThingDisplace(game=self, action=scene_action)

        #
        elif isinstance(scene_action, eca.ActionThingAddToPlace):
            #
            gamePlayActionThingAddToPlace(game=self, action=scene_action)

        #
        elif isinstance(scene_action, eca.ActionThingRemoveFromPlace):
            #
            gamePlayActionThingRemoveFromPlace(game=self, action=scene_action)

        #
        elif isinstance(scene_action, eca.ActionPlayerAssignMission):
            #
            gamePlayActionPlayerAssignMission(game=self, action=scene_action)

        #
        self.current_scene_cursor += 1



#
def gamePlayActionText(game: Game, action: eca.ActionText) -> None:

    #
    pass

#
def gamePlayActionLabel(game: Game, action: eca.ActionLabel) -> None:

    #
    pass

#
def gamePlayActionJump(game: Game, action: eca.ActionJump) -> None:

    #
    pass

#
def gamePlayActionConditionalJump(game: Game, action: eca.ActionConditionalJump) -> None:

    #
    pass

#
def gamePlayActionChangeScene(game: Game, action: eca.ActionChangeScene) -> None:

    #
    pass

#
def gamePlayActionConditionalChangeScene(game: Game, action: eca.ActionConditionalChangeScene) -> None:

    #
    pass

#
def gamePlayActionEndScene(game: Game, action: eca.ActionEndScene) -> None:

    #
    pass

#
def gamePlayActionConditionalEndScene(game: Game, action: eca.ActionConditionalEndScene) -> None:

    #
    pass

#
def gamePlayActionEndGame(game: Game, action: eca.ActionEndGame) -> None:

    #
    pass

#
def gamePlayActionConditionalEndGame(game: Game, action: eca.ActionConditionalEndGame) -> None:

    #
    pass

#
def gamePlayActionCreateVar(game: Game, action: eca.ActionCreateVar) -> None:

    #
    pass

#
def gamePlayActionEditVar(game: Game, action: eca.ActionEditVar) -> None:

    #
    pass

#
def gamePlayActionDeleteVar(game: Game, action: eca.ActionDeleteVar) -> None:

    #
    pass

#
def gamePlayActionBinaryOp(game: Game, action: eca.ActionBinaryOp) -> None:

    #
    pass

#
def gamePlayActionUnaryOp(game: Game, action: eca.ActionUnaryOp) -> None:

    #
    pass

#
def gamePlayActionChangeElt(game: Game, action: eca.ActionChangeElt) -> None:

    #
    pass

#
def gamePlayActionEditAttributeOfElt(game: Game, action: eca.ActionEditAttributeOfElt) -> None:

    #
    pass

#
def gamePlayActionAppendToAttributeOfElt(game: Game, action: eca.ActionAppendToAttributeOfElt) -> None:

    #
    pass

#
def gamePlayActionRemoveValueToAttributeOfElt(game: Game, action: eca.ActionRemoveValueToAttributeOfElt) -> None:

    #
    pass

#
def gamePlayActionSetKVAttributeOfElt(game: Game, action: eca.ActionSetKVAttributeOfElt) -> None:

    #
    pass

#
def gamePlayActionThingDuplicate(game: Game, action: eca.ActionThingDuplicate) -> None:

    #
    pass

#
def gamePlayActionThingDisplace(game: Game, action: eca.ActionThingDisplace) -> None:

    #
    pass

#
def gamePlayActionThingAddToPlace(game: Game, action: eca.ActionThingAddToPlace) -> None:

    #
    pass

#
def gamePlayActionThingRemoveFromPlace(game: Game, action: eca.ActionThingRemoveFromPlace) -> None:

    #
    pass

#
def gamePlayActionPlayerAssignMission(game: Game, action: eca.ActionPlayerAssignMission) -> None:

    #
    pass


