#
from typing import Any


#
### ABSTRACT MAIN PARENT CLASS EVENT. ###
#
class Event:
    #
    def __init__(self, scene_id: str) -> None:
        #
        self.scene_id: str = scene_id
        #
        # ABSTRACT GENERIC CLASS

    #
    def to_dict(self) -> dict[str, Any]:
        #
        return {
            "event_type": "Event"
        }


#
### EVENT MISSION ABSTRACT CLASS. ###
#
class EventMission(Event):
    #
    def __init__(self, scene_id: str, mission_id: str | list[str]) -> None:
        #
        super().__init__(scene_id=scene_id)
        #
        self.mission_id: str | list[str] = mission_id


#
## Event that trigger when a mission is obtained by a player. ##
#
class EventMissionGot(EventMission):
    #
    def __init__(self, scene_id: str, mission_id: str | list[str]) -> None:
        #
        super().__init__(scene_id=scene_id, mission_id=mission_id)


#
## Event that trigger when a mission is in progress (at each beginning of the turn of the player that has this mission). ##
#
class EventMissionInProgress(EventMission):
    #
    def __init__(self, scene_id: str, mission_id: str | list[str]) -> None:
        #
        super().__init__(scene_id=scene_id, mission_id=mission_id)


#
## Event that trigger when a player finishes a mission. ##
#
class EventMissionDone(EventMission):
    #
    def __init__(self, scene_id: str, mission_id: str | list[str]) -> None:
        #
        super().__init__(scene_id=scene_id, mission_id=mission_id)


#
### EVENT ROOM ABSTRACT CLASS. ###
#
class EventRoom(Event):
    #
    def __init__(self, scene_id: str, room_id: str | list[str]) -> None:
        #
        super().__init__(scene_id=scene_id)
        #
        self.room_id: str | list[str] = room_id


#
## Event that trigger when an entity enters a room. ##
#
class EventEnterRoom(EventRoom):
    #
    def __init__(self, scene_id: str, room_id: str | list[str]) -> None:
        #
        super().__init__(scene_id=scene_id, room_id=room_id)


#
## Event that trigger when an entity leaves a room. ##
#
class EventLeaveRoom(EventRoom):
    #
    def __init__(self, scene_id: str, room_id: str | list[str]) -> None:
        #
        super().__init__(scene_id=scene_id, room_id=room_id)


#
## Event that trigger at the beggining of each entity turn. ##
#
class EventInsideRoom(EventRoom):
    #
    def __init__(self, scene_id: str, room_id: str | list[str]) -> None:
        #
        super().__init__(scene_id=scene_id, room_id=room_id)


#
### Event that trigger at each beggining of a global turn when a variable condition is triggered. ###
#
class EventVariableCondition(Event):
    #
    def __init__(
        self,
        scene_id: str,
        var_name: str,
        cond_op: str,
        cond_operand_value: str | int | float | bool,
        cond_operand_type: str
    ) -> None:
        #
        super().__init__(scene_id=scene_id)
        #
        self.var_name: str = var_name
        self.cond_op: str = cond_op
        self.cond_operand_value: str | int | float | bool = cond_operand_value
        self.cond_operand_type: str = cond_operand_type


#
### Event that trigger when an entity does a specific action. ###
#
class EventActionThing(Event):
    #
    def __init__(
        self,
        scene_id: str,
        thing_id: str,
        action_type: str,
        who: str | list[str]
    ) -> None:
        #
        super().__init__(scene_id=scene_id)
        #
        self.thing_id: str | list[str] = thing_id
        self.action_type: str = action_type
        self.who: str | list[str] = who

