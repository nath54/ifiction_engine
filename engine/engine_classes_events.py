#
from typing import Any, Optional
#
from engine_classes_conditions import Condition

#
### ABSTRACT MAIN PARENT CLASS EVENT. ###
#
class Event:
    #
    def __init__(
            self,
            scene_id: str,
            event_condition: Optional[Condition] = None
        ) -> None:
        #
        self.scene_id: str = scene_id
        #
        self.event_condition: Optional[Condition] = event_condition
        #
        # ABSTRACT GENERIC CLASS

    #
    def to_dict(self) -> dict[str, Any]:
        #
        res: dict[str, Any] = {
            "event_type": "Event"
        }

        #
        if self.event_condition is not None:
            #
            res["event_condition"] = self.event_condition.to_dict()

        #
        return res

#
### EVENT MISSION ABSTRACT CLASS. ###
#
class EventMission(Event):
    #
    def __init__(
            self,
            scene_id: str,
            mission_id: str | list[str],
            event_condition: Optional[Condition] = None
        ) -> None:
        #
        super().__init__(scene_id=scene_id, event_condition=event_condition)
        #
        self.mission_id: str | list[str] = mission_id

    #
    def to_dict(self) -> dict[str, Any]:
        #
        res: dict[str, Any] = super().to_dict()

        #
        res["event_type"] = "EventMission"
        res["mission_id"] = self.mission_id

        #
        return res


#
## Event that trigger when a mission is obtained by a player. ##
#
class EventMissionGot(EventMission):
    #
    def __init__(
            self,
            scene_id: str,
            mission_id: str | list[str],
            event_condition: Optional[Condition] = None
        ) -> None:
        #
        super().__init__(scene_id=scene_id, mission_id=mission_id, event_condition=event_condition)

    #
    def to_dict(self) -> dict[str, Any]:
        #
        res: dict[str, Any] = super().to_dict()

        #
        res["event_type"] = "EventMissionGot"

        #
        return res


#
## Event that trigger when a mission is in progress (at each beginning of the turn of the player that has this mission). ##
#
class EventMissionInProgress(EventMission):
    #
    def __init__(
            self,
            scene_id: str,
            mission_id: str | list[str],
            event_condition: Optional[Condition] = None
        ) -> None:
        #
        super().__init__(scene_id=scene_id, mission_id=mission_id, event_condition=event_condition)

    #
    def to_dict(self) -> dict[str, Any]:
        #
        res: dict[str, Any] = super().to_dict()

        #
        res["event_type"] = "EventMissionInProgress"

        #
        return res


#
## Event that trigger when a player finishes a mission. ##
#
class EventMissionDone(EventMission):
    #
    def __init__(
            self,
            scene_id: str,
            mission_id: str | list[str],
            event_condition: Optional[Condition] = None
        ) -> None:
        #
        super().__init__(scene_id=scene_id, mission_id=mission_id, event_condition=event_condition)

    #
    def to_dict(self) -> dict[str, Any]:
        #
        res: dict[str, Any] = super().to_dict()

        #
        res["event_type"] = "EventMissionDone"

        #
        return res


#
### EVENT ROOM ABSTRACT CLASS. ###
#
class EventRoom(Event):
    #
    def __init__(
            self,
            scene_id: str,
            room_id: str | list[str],
            event_condition: Optional[Condition] = None
        ) -> None:
        #
        super().__init__(scene_id=scene_id, event_condition=event_condition)
        #
        self.room_id: str | list[str] = room_id

    #
    def to_dict(self) -> dict[str, Any]:
        #
        res: dict[str, Any] = super().to_dict()

        #
        res["event_type"] = "EventRoom"
        res["room_id"] = self.room_id

        #
        return res


#
## Event that trigger when an entity enters a room. ##
#
class EventEnterRoom(EventRoom):
    #
    def __init__(
            self,
            scene_id: str,
            room_id: str | list[str],
            event_condition: Optional[Condition] = None
        ) -> None:
        #
        super().__init__(scene_id=scene_id, room_id=room_id, event_condition=event_condition)

    #
    def to_dict(self) -> dict[str, Any]:
        #
        res: dict[str, Any] = super().to_dict()

        #
        res["event_type"] = "EventEnterRoom"

        #
        return res


#
## Event that trigger when an entity leaves a room. ##
#
class EventLeaveRoom(EventRoom):
    #
    def __init__(
            self,
            scene_id: str,
            room_id: str | list[str],
            event_condition: Optional[Condition] = None
        ) -> None:
        #
        super().__init__(scene_id=scene_id, room_id=room_id, event_condition=event_condition)

    #
    def to_dict(self) -> dict[str, Any]:
        #
        res: dict[str, Any] = super().to_dict()

        #
        res["event_type"] = "EventLeaveRoom"

        #
        return res


#
## Event that trigger at the beggining of each entity turn. ##
#
class EventInsideRoom(EventRoom):
    #
    def __init__(
            self,
            scene_id: str,
            room_id: str | list[str],
            event_condition: Optional[Condition] = None
        ) -> None:
        #
        super().__init__(scene_id=scene_id, room_id=room_id, event_condition=event_condition)

    #
    def to_dict(self) -> dict[str, Any]:
        #
        res: dict[str, Any] = super().to_dict()

        #
        res["event_type"] = "EventInsideRoom"

        #
        return res


#
### Event that trigger at each beggining of a global turn when a variable condition is triggered. ###
#
class EventVariableCondition(Event):
    #
    def __init__(
        self,
        scene_id: str,
        event_condition: Optional[Condition] = None
    ) -> None:
        #
        super().__init__(scene_id=scene_id, event_condition=event_condition)

    #
    def to_dict(self) -> dict[str, Any]:
        #
        res: dict[str, Any] = super().to_dict()

        #
        res["event_type"] = "EventVariableCondition"

        #
        return res


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
        who: str | list[str],
        event_condition: Optional[Condition] = None
    ) -> None:
        #
        super().__init__(scene_id=scene_id, event_condition=event_condition)
        #
        self.thing_id: str | list[str] = thing_id
        self.action_type: str = action_type
        self.who: str | list[str] = who

    #
    def to_dict(self) -> dict[str, Any]:
        #
        res: dict[str, Any] = super().to_dict()

        #
        res["event_type"] = "EventActionThing"
        res["scene_id"] = self.scene_id
        res["thing_id"] = self.thing_id
        res["action_type"] = self.action_type
        res["who"] = self.who

        #
        return res

#
### Event that trigger at the end of each time unit. ###
#
class EventAlways(Event):
    #
    def __init__(
            self,
            scene_id: str,
        event_condition: Optional[Condition] = None
    ) -> None:
        #
        super().__init__(scene_id=scene_id, event_condition=event_condition)

    #
    def to_dict(self) -> dict[str, Any]:
        #
        res: dict[str, Any] = super().to_dict()

        #
        res["event_type"] = "EventAlways"

        #
        return res


