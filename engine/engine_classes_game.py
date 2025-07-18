#
from typing import Any, Optional, cast
#
import json
import math
import copy
#
from .engine_classes_things_rooms import Thing, Room, Player, Entity, Object
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
        self.variables_space: dict[str, Any] = variables
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
        self.game_settings: GameSettings = game_settings
        #
        self.players_first_description: set[str] = set()
        #
        self.current_scene_id: str = ""
        self.current_scene_cursor: int = 0
        #
        self.variables_space["GLOBAL_TIME"] = self.get_global_time

    #
    @property
    def get_global_time(self) -> ect.GameTime:
        #
        return self.global_time

    #
    def __str__(self) -> str:
        #
        return f"Game:\n\t-game name = {self.game_name}\n\t-game author = {self.game_author}\n\n*Things:\n\n{'\n\n'.join(t.__str__() for t in self.things.values())}\n\n*Rooms:\n\n{'\n\n'.join(t.__str__() for t in self.rooms.values())}\n\n*variables : {self.variables_space}\n\n*players : {self.players}\n\n*nb turns : {self.nb_turns}"

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
            "variables": self.variables_space,
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
                        elt_type="event",
                        elt_id=event_id,
                        current_action=None,
                        current_action_time=copy.deepcopy(event.time_delay),
                        can_be_interrupted=False,
                        repetitive=True
                    ),
                    priority=copy.deepcopy(event.time_delay)
                )

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
    def manage_npc_entities(self, elt: lu.PQ_Entity_and_EventsSystem, interaction_system: Any) -> None:

        # TODO
        pass

    #
    def manage_event(self, elt: lu.PQ_Entity_and_EventsSystem, interaction_system: Any) -> None:

        #
        event: evt.Event = self.events[elt.elt_id]
        #
        if isinstance(event, evt.EventAlways):

            #
            if event.event_condition is None or event.event_condition.verify(variables_space=self.variables_space):

                #
                self.play_scene( scene_id = event.scene_id, interaction_system=interaction_system )

        #
        if elt.repetitive:
            #
            self.priority_queue_events_and_entities.insert_with_priority(
                item=copy.deepcopy(elt),
                priority=elt.current_action_time
            )

    #
    def play_scene(self, scene_id: str, interaction_system: Any) -> None:

        #
        self.current_scene_id = scene_id
        self.current_scene_cursor = 0
        #
        while self.current_scene_id in self.scenes and self.current_scene_cursor >= 0 and self.current_scene_cursor < len(self.scenes[self.current_scene_id].scenes_actions):

            #
            self.play_scene_action( scene_action = self.scenes[self.current_scene_id].scenes_actions[self.current_scene_cursor], interaction_system=interaction_system )

        #
        self.current_scene_id = ""
        self.current_scene_cursor = 0

    #
    def play_scene_action(self, scene_action: eca.Action, interaction_system: Any) -> None:

        #
        if isinstance(scene_action, eca.ActionText):
            #
            gamePlayActionText(game=self, action=scene_action, interaction_system=interaction_system)

        #
        elif isinstance(scene_action, eca.ActionLabel):
            #
            gamePlayActionLabel(game=self, action=scene_action, interaction_system=interaction_system)

        #
        elif isinstance(scene_action, eca.ActionJump):
            #
            gamePlayActionJump(game=self, action=scene_action, interaction_system=interaction_system)

        #
        elif isinstance(scene_action, eca.ActionConditionalJump):
            #
            gamePlayActionConditionalJump(game=self, action=scene_action, interaction_system=interaction_system)

        #
        elif isinstance(scene_action, eca.ActionChangeScene):
            #
            gamePlayActionChangeScene(game=self, action=scene_action, interaction_system=interaction_system)

        #
        elif isinstance(scene_action, eca.ActionConditionalChangeScene):
            #
            gamePlayActionConditionalChangeScene(game=self, action=scene_action, interaction_system=interaction_system)

        #
        elif isinstance(scene_action, eca.ActionEndScene):
            #
            gamePlayActionEndScene(game=self, action=scene_action, interaction_system=interaction_system)

        #
        elif isinstance(scene_action, eca.ActionConditionalEndScene):
            #
            gamePlayActionConditionalEndScene(game=self, action=scene_action, interaction_system=interaction_system)

        #
        elif isinstance(scene_action, eca.ActionEndGame):
            #
            gamePlayActionEndGame(game=self, action=scene_action, interaction_system=interaction_system)

        #
        elif isinstance(scene_action, eca.ActionConditionalEndGame):
            #
            gamePlayActionConditionalEndGame(game=self, action=scene_action, interaction_system=interaction_system)

        #
        elif isinstance(scene_action, eca.ActionCreateVar):
            #
            gamePlayActionCreateVar(game=self, action=scene_action, interaction_system=interaction_system)

        #
        elif isinstance(scene_action, eca.ActionEditVar):
            #
            gamePlayActionEditVar(game=self, action=scene_action, interaction_system=interaction_system)

        #
        elif isinstance(scene_action, eca.ActionDeleteVar):
            #
            gamePlayActionDeleteVar(game=self, action=scene_action, interaction_system=interaction_system)

        #
        elif isinstance(scene_action, eca.ActionBinaryOp):
            #
            gamePlayActionBinaryOp(game=self, action=scene_action, interaction_system=interaction_system)

        #
        elif isinstance(scene_action, eca.ActionUnaryOp):
            #
            gamePlayActionUnaryOp(game=self, action=scene_action, interaction_system=interaction_system)

        #
        elif isinstance(scene_action, eca.ActionEditAttributeOfElt):
            #
            gamePlayActionEditAttributeOfElt(game=self, action=scene_action, interaction_system=interaction_system)

        #
        elif isinstance(scene_action, eca.ActionAppendToAttributeOfElt):
            #
            gamePlayActionAppendToAttributeOfElt(game=self, action=scene_action, interaction_system=interaction_system)

        #
        elif isinstance(scene_action, eca.ActionRemoveValueToAttributeOfElt):
            #
            gamePlayActionRemoveValueToAttributeOfElt(game=self, action=scene_action, interaction_system=interaction_system)

        #
        elif isinstance(scene_action, eca.ActionSetKVAttributeOfElt):
            #
            gamePlayActionSetKVAttributeOfElt(game=self, action=scene_action, interaction_system=interaction_system)

        #
        elif isinstance(scene_action, eca.ActionThingDuplicate):
            #
            gamePlayActionThingDuplicate(game=self, action=scene_action, interaction_system=interaction_system)

        #
        elif isinstance(scene_action, eca.ActionThingDisplace):
            #
            gamePlayActionThingDisplace(game=self, action=scene_action, interaction_system=interaction_system)

        #
        elif isinstance(scene_action, eca.ActionThingAddToPlace):
            #
            gamePlayActionThingAddToPlace(game=self, action=scene_action, interaction_system=interaction_system)

        #
        elif isinstance(scene_action, eca.ActionThingRemoveFromPlace):
            #
            gamePlayActionThingRemoveFromPlace(game=self, action=scene_action, interaction_system=interaction_system)

        #
        elif isinstance(scene_action, eca.ActionPlayerAssignMission):
            #
            gamePlayActionPlayerAssignMission(game=self, action=scene_action, interaction_system=interaction_system)

        #
        self.current_scene_cursor += 1


#
def gamePlayActionText(game: Game, action: eca.ActionText, interaction_system: Any) -> None:

    #
    final_text_to_display: str = action.text
    #
    i: int = 0
    j: int = final_text_to_display.find("@", i)
    #
    while j != -1:
        #
        jj: int = final_text_to_display.find(" ", j)
        #
        if jj != -1:
            #
            jj = len(final_text_to_display)
        #
        var_name: str = final_text_to_display[j+1:jj]
        #
        if var_name in game.variables_space:
            #
            final_text_to_display = final_text_to_display.replace(f"@{var_name}", str(game.variables_space[var_name]))
        #
        i = (j + 1) if jj == -1 else (jj + 1)
        #
        j = final_text_to_display.find("@", i)

    #
    if hasattr(interaction_system, "write_to_output"):
        #
        interaction_system.write_to_output(final_text_to_display)

#
def gamePlayActionLabel(game: Game, action: eca.ActionLabel, interaction_system: Any) -> None:

    #
    pass

#
def go_to_label_cursor(game: Game, label_name: str) -> None:
    #
    ### Search for the label to jump to. ###
    #
    label_cursor: int = -1
    #
    act: eca.Action
    #
    for i, act in enumerate( game.scenes[game.current_scene_id].scenes_actions ):
        #
        if isinstance(act, eca.ActionLabel) and act.label_name == label_name:
            #
            label_cursor = i
            #
            break

    #
    if label_cursor == -1:
        #
        raise UserWarning(f"Error: LABEL NOT FOUND IN SCENE ACTIONS : `{label_name}`")

    #
    game.current_scene_cursor = label_cursor

#
def gamePlayActionJump(game: Game, action: eca.ActionJump, interaction_system: Any) -> None:

    #
    go_to_label_cursor(game=game, label_name=action.label_name)

#
def gamePlayActionConditionalJump(game: Game, action: eca.ActionConditionalJump, interaction_system: Any) -> None:

    #
    if action.condition.verify(variables_space=game.variables_space):
        #
        go_to_label_cursor(game=game, label_name=action.label_name)

#
def gamePlayActionChangeScene(game: Game, action: eca.ActionChangeScene, interaction_system: Any) -> None:

    #
    game.current_scene_id = action.scene_id
    game.current_scene_cursor = -1

#
def gamePlayActionConditionalChangeScene(game: Game, action: eca.ActionConditionalChangeScene, interaction_system: Any) -> None:

    #
    if action.condition.verify(variables_space=game.variables_space):
        #
        game.current_scene_id = action.scene_id
        game.current_scene_cursor = -1

#
def gamePlayActionEndScene(game: Game, action: eca.ActionEndScene, interaction_system: Any) -> None:

    #
    game.current_scene_id = ""
    game.current_scene_cursor = -1

#
def gamePlayActionConditionalEndScene(game: Game, action: eca.ActionConditionalEndScene, interaction_system: Any) -> None:

    #
    if action.condition.verify(variables_space=game.variables_space):
        #
        game.current_scene_id = ""
        game.current_scene_cursor = -1

#
def gamePlayActionEndGame(game: Game, action: eca.ActionEndGame, interaction_system: Any) -> None:

    #
    setattr(interaction_system, "running", False)

#
def gamePlayActionConditionalEndGame(game: Game, action: eca.ActionConditionalEndGame, interaction_system: Any) -> None:

    #
    if action.condition.verify(variables_space=game.variables_space):
        #
        setattr(interaction_system, "running", False)

#
def gamePlayActionCreateVar(game: Game, action: eca.ActionCreateVar, interaction_system: Any) -> None:

    #
    if all([l >= "A" and l <= "Z" for l in action.var_name]):
        #
        raise UserWarning(f"Error: cannot create variable name that have not lower characters in their name !\nVariables in upper characters are READ ONLY variables !\nBAD VARIABLE NAME : `{action.var_name}`")
    #
    game.variables_space[action.var_name] = action.var_value

#
def gamePlayActionEditVar(game: Game, action: eca.ActionEditVar, interaction_system: Any) -> None:

    #
    game.variables_space[action.var_name] = action.var_value

#
    if all([l >= "A" and l <= "Z" for l in action.var_name]):
        #
        raise UserWarning(f"Error: cannot edit variable name that have not lower characters in their name !\nVariables in upper characters are READ ONLY variables !\nBAD VARIABLE NAME : `{action.var_name}`")
    #

#
def gamePlayActionDeleteVar(game: Game, action: eca.ActionDeleteVar, interaction_system: Any) -> None:

    #
    if all([l >= "A" and l <= "Z" for l in action.var_name]):
        #
        raise UserWarning(f"Error: cannot delete variable name that have not lower characters in their name !\nVariables in upper characters are READ ONLY variables !\nBAD VARIABLE NAME : `{action.var_name}`")
    #
    del(game.variables_space[action.var_name])

#
def gamePlayActionBinaryOp(game: Game, action: eca.ActionBinaryOp, interaction_system: Any) -> None:

    #
    if all([l >= "A" and l <= "Z" for l in action.var_output_name]):
        #
        raise UserWarning(f"Error: cannot edit variable name that have not lower characters in their name !\nVariables in upper characters are READ ONLY variables !\nBAD VARIABLE NAME : `{action.var_output_name}`")

    #
    value_1: Optional[Any] = None
    value_2: Optional[Any] = None

    #
    ### Check elt1. ###
    #
    if action.elt1_type == "variable":
        #
        if action.elt1_value not in game.variables_space:
            #
            raise UserWarning(f"Error: unknown variable name `{action.elt1_value}` in global game variables space !")
        #
        value_1 = game.variables_space[action.elt1_value]
    #
    else:
        #
        value_1 = action.elt1_value
    #
    if value_1 is None:
        #
        raise UserWarning(f"Error : operand 1 of binary operation is None !\n{action}")

    #
    ### Check elt2. ###
    #
    if action.elt2_type == "variable":
        #
        if action.elt2_value not in game.variables_space:
            #
            raise UserWarning(f"Error: unknown variable name `{action.elt2_value}` in global game variables space !")
        #
        value_2 = game.variables_space[action.elt2_value]
    #
    else:
        #
        value_2 = action.elt2_value
    #
    if value_2 is None:
        #
        raise UserWarning(f"Error : operand 2 of binary operation is None !\n{action}")

    #
    ### Apply operation. ###
    #
    if action.op in ["+", "add", "sum", "addition"]:
        #
        game.variables_space[action.var_output_name] = value_1 + value_2
    #
    elif action.op in ["-", "sub", "substract", "substraction"]:
        #
        game.variables_space[action.var_output_name] = value_1 - value_2
    #
    elif action.op in ["*", "mul", "mult", "multiply", "multiplication", "product", "prod"]:
        #
        game.variables_space[action.var_output_name] = value_1 * value_2
    #
    elif action.op in ["/", "div", "division", "quotient"]:
        #
        game.variables_space[action.var_output_name] = value_1 / value_2 if value_2 / 0 else 0
    #
    elif action.op in ["%", "mod", "modulo", "rest"]:
        #
        game.variables_space[action.var_output_name] = value_1 % value_2
    #
    elif action.op == "and":
        #
        game.variables_space[action.var_output_name] = bool(value_1) and bool(value_2)
    #
    elif action.op == "or":
        #
        game.variables_space[action.var_output_name] = bool(value_1) or bool(value_2)
    #
    elif action.op == "xor":
        #
        game.variables_space[action.var_output_name] = (bool(value_1) and not bool(value_2)) or (bool(value_2) and not bool(value_1))
    #
    else:
        #
        raise UserWarning(f"Error: unknown operation : `{action.op}`")

#
def gamePlayActionUnaryOp(game: Game, action: eca.ActionUnaryOp, interaction_system: Any) -> None:

    #
    if all([l >= "A" and l <= "Z" for l in action.var_output_name]):
        #
        raise UserWarning(f"Error: cannot edit variable name that have not lower characters in their name !\nVariables in upper characters are READ ONLY variables !\nBAD VARIABLE NAME : `{action.var_output_name}`")

    #
    value: Optional[Any] = None

    #
    ### Check elt1. ###
    #
    if action.elt_type == "variable":
        #
        if action.elt_value not in game.variables_space:
            #
            raise UserWarning(f"Error: unknown variable name `{action.elt_value}` in global game variables space !")
        #
        value = game.variables_space[action.elt_value]
    #
    else:
        #
        value = action.elt_value
    #
    if value is None:
        #
        raise UserWarning(f"Error : operand 1 of binary operation is None !\n{action}")

    #
    ### Apply operation. ###
    #
    if action.op in ["++", "incr", "increment"]:
        #
        game.variables_space[action.var_output_name] = value + 1
    #
    elif action.op in ["--", "decr", "decrement"]:
        #
        game.variables_space[action.var_output_name] = value - 1
    #
    elif action.op in ["-", "neg", "negation", "opp", "opposite"]:
        #
        game.variables_space[action.var_output_name] = - value
    #
    elif action.op == "not":
        #
        game.variables_space[action.var_output_name] = not bool(value)
    #
    elif action.op in ["floor", "round floor"]:
        #
        game.variables_space[action.var_output_name] = math.floor(value)
    #
    elif action.op in ["ceil", "round ceil"]:
        #
        game.variables_space[action.var_output_name] = math.ceil(value)
    #
    elif action.op in ["round"]:
        #
        game.variables_space[action.var_output_name] = round(value)
    #
    elif action.op in ["int", "integer", "to_int", "to int"]:
        #
        game.variables_space[action.var_output_name] = int(value)
    #
    elif action.op in ["str", "string", "to_string", "to string"]:
        #
        game.variables_space[action.var_output_name] = str(value)
    #
    elif action.op in ["bool", "boolean", "to_boolean", "to boolean"]:
        #
        game.variables_space[action.var_output_name] = str(value)
    #
    elif action.op in ["mean", "average"]:
        #
        game.variables_space[action.var_output_name] = 0 if len(value) == 0 else sum(value)/len(value)
    #
    elif action.op in ["min", "minimum"]:
        #
        game.variables_space[action.var_output_name] = min(value)
    #
    elif action.op in ["max", "maximum"]:
        #
        game.variables_space[action.var_output_name] = max(value)
    #
    else:
        #
        raise UserWarning(f"Error: unknown operation : `{action.op}`")

#
def get_elt_to_edit(game: Game, elt_type: str, elt_id: str, elt_attr_name: str | list[str]) -> Optional[Any]:

    #
    UNEDITABLE_ATTRS: list[str] = []

    #
    elt_to_edit: Optional[Any] = None

    #
    if elt_type == "thing":
        #
        if elt_id not in game.things:
            #
            raise UserWarning(f"Error: Unknown thing id : `{elt_id}` !")
        #
        elt_to_edit = game.things[elt_id]
    #
    elif elt_type == "room":
        #
        if elt_id not in game.rooms:
            #
            raise UserWarning(f"Error: Unknown room id : `{elt_id}` !")
        #
        elt_to_edit = game.rooms[elt_id]
    #
    elif elt_type == "scene":
        #
        if elt_id not in game.scenes:
            #
            raise UserWarning(f"Error: Unknown scene id : `{elt_id}` !")
        #
        elt_to_edit = game.scenes[elt_id]
    #
    elif elt_type == "event":
        #
        if elt_id not in game.events:
            #
            raise UserWarning(f"Error: Unknown event id : `{elt_id}` !")
        #
        elt_to_edit = game.events[elt_id]
    #
    elif elt_type == "mission":
        #
        if elt_id not in game.missions:
            #
            raise UserWarning(f"Error: Unknown mission id : `{elt_id}` !")
        #
        elt_to_edit = game.missions[elt_id]

    #
    if isinstance(elt_attr_name, str):
        #
        if elt_attr_name in UNEDITABLE_ATTRS:
            #
            raise UserWarning(f"Error: cannot modify thing attribute `{elt_attr_name}` !")
    #
    elif isinstance(elt_attr_name, list):  # type: ignore
        #
        elt_attr_name_: str
        #
        for i, elt_attr_name_ in enumerate(elt_attr_name):
            #
            if elt_attr_name_[i] in UNEDITABLE_ATTRS:
                #
                raise UserWarning(f"Error: cannot modify thing attribute `{elt_attr_name_[i]}` !")
    #
    return elt_to_edit

#
def gamePlayActionEditAttributeOfElt(game: Game, action: eca.ActionEditAttributeOfElt, interaction_system: Any) -> None:

    #
    elt_to_edit: Optional[Any] = get_elt_to_edit(game=game, elt_type=action.elt_type, elt_id=action.elt_id, elt_attr_name=action.elt_attr_name)
    #
    if elt_to_edit is None:
        #
        print(f"Error action elt attr name edit elt is None : `{action}`")
        #
        return

    #
    if isinstance(action.elt_attr_name, str):
        #
        setattr(elt_to_edit, action.elt_attr_name, action.elt_attr_new_value)
    #
    elif isinstance(action.elt_attr_name, list):  # type: ignore
        #
        elt_attr_name: str
        #
        for i, elt_attr_name in enumerate(action.elt_attr_name):
            #
            if isinstance(action.elt_attr_new_value, list):  # type: ignore
                #
                setattr(elt_to_edit, elt_attr_name, action.elt_attr_new_value[i])  # type: ignore
            #
            else:
                #
                setattr(elt_to_edit, elt_attr_name, action.elt_attr_new_value)
    #
    else:
        #
        print(f"Error action elt attr name : `{action.elt_attr_name}`")

#
def gamePlayActionAppendToAttributeOfElt(game: Game, action: eca.ActionAppendToAttributeOfElt, interaction_system: Any) -> None:

    #
    elt_to_edit: Optional[Any] = get_elt_to_edit(game=game, elt_type=action.elt_type, elt_id=action.elt_id, elt_attr_name=action.elt_attr_name)

    #
    if elt_to_edit is None:
        #
        print(f"Error action elt attr name edit elt is None : `{action}`")
        #
        return

    #
    if isinstance(action.elt_attr_name, str):
        #
        if hasattr(elt_to_edit, action.elt_attr_name):
            #
            lst: list[Any] = getattr(elt_to_edit, action.elt_attr_name)
            #
            lst.append(action.elt_attr_new_value_to_append)
    #
    elif isinstance(action.elt_attr_name, list):  # type: ignore
        #
        _elt_attr_name: str
        #
        for i, _elt_attr_name in enumerate(action.elt_attr_name):
            #
            if isinstance(action.elt_attr_new_value_to_append, list) and len(action.elt_attr_new_value_to_append) == len(action.elt_attr_name):  # type: ignore
                #
                if hasattr(elt_to_edit, action.elt_attr_name[i]):
                    #
                    lst: list[Any] = getattr(elt_to_edit, action.elt_attr_name[i])
                    #
                    lst.append(action.elt_attr_new_value_to_append[i])  # type: ignore
            #
            else:
                #
                if hasattr(elt_to_edit, action.elt_attr_name[i]):
                    #
                    lst: list[Any] = getattr(elt_to_edit, action.elt_attr_name[i])
                    #
                    lst.append(action.elt_attr_new_value_to_append)  # type: ignore
    #
    else:
        #
        print(f"Error action elt attr name : `{action.elt_attr_name}`")

#
def gamePlayActionRemoveValueToAttributeOfElt(game: Game, action: eca.ActionRemoveValueToAttributeOfElt, interaction_system: Any) -> None:

    #
    elt_to_edit: Optional[Any] = get_elt_to_edit(game=game, elt_type=action.elt_type, elt_id=action.elt_id, elt_attr_name=action.elt_attr_name)

    #
    if elt_to_edit is None:
        #
        print(f"Error action elt attr name edit elt is None : `{action}`")
        #
        return

    #
    if isinstance(action.elt_attr_name, str):
        #
        if hasattr(elt_to_edit, action.elt_attr_name):
            #
            lst: list[Any] = getattr(elt_to_edit, action.elt_attr_name)
            #
            lst.remove(action.elt_attr_value_to_remove)
    #
    elif isinstance(action.elt_attr_name, list):  # type: ignore
        #
        _elt_attr_name: str
        #
        for i, _elt_attr_name in enumerate(action.elt_attr_name):
            #
            if isinstance(action.elt_attr_value_to_remove, list) and len(action.elt_attr_value_to_remove) == len(action.elt_attr_name):  # type: ignore
                #
                if hasattr(elt_to_edit, action.elt_attr_name[i]):
                    #
                    lst: list[Any] = getattr(elt_to_edit, action.elt_attr_name[i])
                    #
                    lst.remove(action.elt_attr_value_to_remove[i])  # type: ignore
            #
            else:
                #
                if hasattr(elt_to_edit, action.elt_attr_name[i]):
                    #
                    lst: list[Any] = getattr(elt_to_edit, action.elt_attr_name[i])
                    #
                    lst.remove(action.elt_attr_value_to_remove)  # type: ignore
    #
    else:
        #
        print(f"Error action elt attr name : `{action.elt_attr_name}`")

#
def gamePlayActionSetKVAttributeOfElt(game: Game, action: eca.ActionSetKVAttributeOfElt, interaction_system: Any) -> None:

    #
    elt_to_edit: Optional[Any] = get_elt_to_edit(game=game, elt_type=action.elt_type, elt_id=action.elt_id, elt_attr_name=action.elt_attr_name)

    #
    if elt_to_edit is None:
        #
        print(f"Error action elt attr name edit elt is None : `{action}`")
        #
        return

    #
    if isinstance(action.elt_attr_name, str):
        #
        if hasattr(elt_to_edit, action.elt_attr_name):
            #
            dicti: dict[Any, Any] = getattr(elt_to_edit, action.elt_attr_name)
            #
            if action.elt_attr_value == "@DELETE":
                #
                del dicti[action.elt_attr_key]
            #
            else:
                #
                dicti[action.elt_attr_key] = action.elt_attr_value
    #
    elif isinstance(action.elt_attr_name, list):  # type: ignore
        #
        _elt_attr_name: str
        #
        for i, _elt_attr_name in enumerate(action.elt_attr_name):
            #
            if isinstance(action.elt_attr_key, list) and len(action.elt_attr_key) == len(action.elt_attr_name) and isinstance(action.elt_attr_value, list) and len(action.elt_attr_value) == len(action.elt_attr_name):  # type: ignore
                #
                if hasattr(elt_to_edit, action.elt_attr_name[i]):
                    #
                    dicti: dict[Any, Any] = getattr(elt_to_edit, action.elt_attr_name[i])
                    #
                    if action.elt_attr_value[i] == "@DELETE":  # type: ignore
                        #
                        del dicti[action.elt_attr_key[i]]
                    #
                    else:
                        #
                        dicti[action.elt_attr_key[i]] = action.elt_attr_value[i]  # type: ignore
            #
            else:
                #
                if hasattr(elt_to_edit, action.elt_attr_name[i]):
                    #
                    dicti: dict[Any, Any] = getattr(elt_to_edit, action.elt_attr_name[i])
                    #
                    if action.elt_attr_value == "@DELETE":  # type: ignore
                        #
                        del dicti[action.elt_attr_key]
                    #
                    else:
                        #
                        dicti[action.elt_attr_key] = action.elt_attr_value  # type: ignore
    #
    else:
        #
        print(f"Error action elt attr name : `{action.elt_attr_name}`")

#
def gamePlayActionThingDuplicate(game: Game, action: eca.ActionThingDuplicate, interaction_system: Any) -> None:

    #
    if action.src_elt_id not in game.things:
        #
        raise UserWarning(f"Error: thing id NOT FOUND in game things : ``{action.src_elt_id} !")

    #
    if action.dst_elt_id not in game.things:
        #
        raise UserWarning(f"Error: thing id ALREADY FOUND in game things : ``{action.dst_elt_id} !\nSO CANNOT DUPLICATE !")

    #
    new_thing: Thing = copy.deepcopy( game.things[action.src_elt_id] )

    #
    new_thing.id = action.dst_elt_id
    #
    game.things[new_thing.id] = new_thing

#
def gamePlayActionThingDisplace(game: Game, action: eca.ActionThingDisplace, interaction_system: Any) -> None:

    #
    if action.thing_id not in game.things:
        #
        raise UserWarning(f"Error: thing id NOT FOUND in game things : `{action.thing_id}` !")

    #
    if action.src_place_type == "room":
        #
        if action.src_place_id not in game.rooms:
            #
            raise UserWarning(f"Error: Room id NOT FOUDN in game rooms : `{action.src_place_id}`")
        #
        if action.thing_id not in game.rooms[action.src_place_id].things_inside:
            #
            game.rooms[action.src_place_id].things_inside[action.thing_id] = 0
        #
        game.rooms[action.src_place_id].things_inside[action.thing_id] += action.quantity
    #
    elif action.src_place_type == "inventory":
        #
        if action.src_place_id not in game.things:
            #
            raise UserWarning(f"Error: Thing id NOT FOUND in game things : `{action.src_place_id}`")
        #
        if not isinstance( game.things[action.src_place_id], Entity ):
            #
            raise UserWarning(f"Error: Thing id IS NOT ENTITY in game things : `{action.src_place_id}`, `{game.things[action.src_place_id]}`")
        #
        ent: Entity = cast(Entity, game.things[action.src_place_id] )
        #
        if action.thing_id in ent.inventory:
            #
            ent.inventory[action.thing_id] -= action.quantity
            #
            if ent.inventory[action.thing_id] <= 0:
                #
                del ent.inventory[action.thing_id]
    #
    elif action.src_place_type == "container":
        #
        if action.src_place_id not in game.things:
            #
            raise UserWarning(f"Error: Thing id NOT FOUND in game things : `{action.src_place_id}`")
        #
        if not isinstance( game.things[action.src_place_id], Object ):
            #
            raise UserWarning(f"Error: Thing id IS NOT AN OBJECT in game things : `{action.src_place_id}`, `{game.things[action.src_place_id]}`")
        #
        if "container" not in game.things[action.src_place_id].attributes:
            #
            raise UserWarning(f"Error: Thing id IS NOT CONTAINER in game things : `{action.src_place_id}`, `{game.things[action.src_place_id]}`")
        #
        obj: Object = cast(Object, game.things[action.src_place_id] )
        #
        if action.thing_id in obj.contains:
            #
            obj.contains[action.thing_id] -= action.quantity
            #
            if obj.contains[action.thing_id] <= 0:
                #
                del obj.contains[action.thing_id]
    #
    else:
        #
        raise UserWarning(f"Error: Unknown place type : `{action.src_place_type}` !")

    #
    if action.dst_place_type == "room":
        #
        if action.dst_place_id not in game.rooms:
            #
            raise UserWarning(f"Error: Room id NOT FOUDN in game rooms : `{action.dst_place_id}`")
        #
        if action.thing_id not in game.rooms[action.dst_place_id].things_inside:
            #
            game.rooms[action.dst_place_id].things_inside[action.thing_id] = 0
        #
        game.rooms[action.dst_place_id].things_inside[action.thing_id] += action.quantity
    #
    elif action.dst_place_type == "inventory":
        #
        if action.dst_place_id not in game.things:
            #
            raise UserWarning(f"Error: Thing id NOT FOUND in game things : `{action.dst_place_id}`")
        #
        if not isinstance( game.things[action.dst_place_id], Entity ):
            #
            raise UserWarning(f"Error: Thing id IS NOT ENTITY in game things : `{action.dst_place_id}`, `{game.things[action.dst_place_id]}`")
        #
        ent: Entity = cast(Entity, game.things[action.dst_place_id] )
        #
        if action.thing_id not in ent.inventory:
            #
            ent.inventory[action.thing_id] = 0
        #
        ent.inventory[action.thing_id] += action.quantity
    #
    elif action.dst_place_type == "container":
        #
        if action.dst_place_id not in game.things:
            #
            raise UserWarning(f"Error: Thing id NOT FOUND in game things : `{action.dst_place_id}`")
        #
        if not isinstance( game.things[action.dst_place_id], Object ):
            #
            raise UserWarning(f"Error: Thing id IS NOT AN OBJECT in game things : `{action.dst_place_id}`, `{game.things[action.dst_place_id]}`")
        #
        if "container" not in game.things[action.dst_place_id].attributes:
            #
            raise UserWarning(f"Error: Thing id IS NOT CONTAINER in game things : `{action.dst_place_id}`, `{game.things[action.dst_place_id]}`")
        #
        obj: Object = cast(Object, game.things[action.dst_place_id] )
        #
        if action.thing_id not in obj.contains:
            #
            obj.contains[action.thing_id] = 0
        #
        obj.contains[action.thing_id] += action.quantity
    #
    else:
        #
        raise UserWarning(f"Error: Unknown place type : `{action.dst_place_type}` !")

#
def gamePlayActionThingAddToPlace(game: Game, action: eca.ActionThingAddToPlace, interaction_system: Any) -> None:

    #
    if action.thing_id not in game.things:
        #
        raise UserWarning(f"Error: thing id NOT FOUND in game things : `{action.thing_id}` !")

    #
    if action.place_type == "room":
        #
        if action.place_id not in game.rooms:
            #
            raise UserWarning(f"Error: Room id NOT FOUDN in game rooms : `{action.place_id}`")
        #
        if action.place_id not in game.rooms:
            #
            raise UserWarning(f"Error: Room id NOT FOUDN in game rooms : `{action.place_id}`")
        #
        if action.thing_id not in game.rooms[action.place_id].things_inside:
            #
            game.rooms[action.place_id].things_inside[action.thing_id] = 0
        #
        game.rooms[action.place_id].things_inside[action.thing_id] += action.quantity
    #
    elif action.place_type == "inventory":
        #
        if action.place_id not in game.things:
            #
            raise UserWarning(f"Error: Thing id NOT FOUND in game things : `{action.place_id}`")
        #
        if not isinstance( game.things[action.place_id], Entity ):
            #
            raise UserWarning(f"Error: Thing id IS NOT ENTITY in game things : `{action.place_id}`, `{game.things[action.place_id]}`")
        #
        ent: Entity = cast(Entity, game.things[action.place_id] )
        #
        if action.thing_id not in ent.inventory:
            #
            ent.inventory[action.thing_id] = 0
        #
        ent.inventory[action.thing_id] += action.quantity
    #
    elif action.place_type == "container":
        #
        if action.place_id not in game.things:
            #
            raise UserWarning(f"Error: Thing id NOT FOUND in game things : `{action.place_id}`")
        #
        if not isinstance( game.things[action.place_id], Object ):
            #
            raise UserWarning(f"Error: Thing id IS NOT AN OBJECT in game things : `{action.place_id}`, `{game.things[action.place_id]}`")
        #
        if "container" not in game.things[action.place_id].attributes:
            #
            raise UserWarning(f"Error: Thing id IS NOT CONTAINER in game things : `{action.place_id}`, `{game.things[action.place_id]}`")
        #
        obj: Object = cast(Object, game.things[action.place_id] )
        #
        if action.thing_id not in obj.contains:
            #
            obj.contains[action.thing_id] = 0
        #
        obj.contains[action.thing_id] += action.quantity
    #
    else:
        #
        raise UserWarning(f"Error: Unknown place type : `{action.place_type}` !")

#
def gamePlayActionThingRemoveFromPlace(game: Game, action: eca.ActionThingRemoveFromPlace, interaction_system: Any) -> None:

    #
    if action.thing_id not in game.things:
        #
        raise UserWarning(f"Error: thing id NOT FOUND in game things : `{action.thing_id}` !")

    #
    if action.place_type == "room":
        #
        if action.place_id not in game.rooms:
            #
            raise UserWarning(f"Error: Room id NOT FOUDN in game rooms : `{action.place_id}`")
        #
        if action.thing_id in game.rooms[action.place_id].things_inside:
            #
            game.rooms[action.place_id].things_inside[action.thing_id] -= action.quantity
            #
            if game.rooms[action.place_id].things_inside[action.thing_id] <= 0:
                #
                del game.rooms[action.place_id].things_inside[action.thing_id]
    #
    elif action.place_type == "inventory":
        #
        if action.place_id not in game.things:
            #
            raise UserWarning(f"Error: Thing id NOT FOUND in game things : `{action.place_id}`")
        #
        if not isinstance( game.things[action.place_id], Entity ):
            #
            raise UserWarning(f"Error: Thing id IS NOT ENTITY in game things : `{action.place_id}`, `{game.things[action.place_id]}`")
        #
        ent: Entity = cast(Entity, game.things[action.place_id] )
        #
        if action.thing_id in ent.inventory:
            #
            ent.inventory[action.thing_id] -= action.quantity
            #
            if ent.inventory[action.thing_id] <= 0:
                #
                del ent.inventory[action.thing_id]
    #
    elif action.place_type == "container":
        #
        if action.place_id not in game.things:
            #
            raise UserWarning(f"Error: Thing id NOT FOUND in game things : `{action.place_id}`")
        #
        if not isinstance( game.things[action.place_id], Object ):
            #
            raise UserWarning(f"Error: Thing id IS NOT AN OBJECT in game things : `{action.place_id}`, `{game.things[action.place_id]}`")
        #
        if "container" not in game.things[action.place_id].attributes:
            #
            raise UserWarning(f"Error: Thing id IS NOT CONTAINER in game things : `{action.place_id}`, `{game.things[action.place_id]}`")
        #
        obj: Object = cast(Object, game.things[action.place_id] )
        #
        if action.thing_id in obj.contains:
            #
            obj.contains[action.thing_id] -= action.quantity
            #
            if obj.contains[action.thing_id] <= 0:
                #
                del obj.contains[action.thing_id]
    #
    else:
        #
        raise UserWarning(f"Error: Unknown place type : `{action.place_type}` !")

#
def gamePlayActionPlayerAssignMission(game: Game, action: eca.ActionPlayerAssignMission, interaction_system: Any) -> None:

    #
    pass


