

#
class Event:
    #
    def __init__(self, scene_id: str) -> None:
        #
        self.scene_id: str = scene_id
        #
        # ABSTRACT GENERIC CLASS


#
class EventMission(Event):
    #
    def __init__(self, scene_id: str, mission_id: str | list[str]) -> None:
        #
        super().__init__(scene_id=scene_id)
        #
        self.mission_id: str | list[str] = mission_id


#
class EventMissionDone(EventMission):
    #
    def __init__(self, scene_id: str, mission_id: str | list[str]) -> None:
        #
        super().__init__(scene_id=scene_id, mission_id=mission_id)


#
class EventMissionGot(EventMission):
    #
    def __init__(self, scene_id: str, mission_id: str | list[str]) -> None:
        #
        super().__init__(scene_id=scene_id, mission_id=mission_id)

#
class EventMissionInProgress(EventMission):
    #
    def __init__(self, scene_id: str, mission_id: str | list[str]) -> None:
        #
        super().__init__(scene_id=scene_id, mission_id=mission_id)


#
class EventRoom(Event):
    #
    def __init__(self, scene_id: str, room_id: str | list[str]) -> None:
        #
        super().__init__(scene_id=scene_id)
        #
        self.room_id: str | list[str] = room_id

#
class EventEnterRoom(EventRoom):
    #
    def __init__(self, scene_id: str, room_id: str | list[str]) -> None:
        #
        super().__init__(scene_id=scene_id, room_id=room_id)

#
class EventLeaveRoom(EventRoom):
    #
    def __init__(self, scene_id: str, room_id: str | list[str]) -> None:
        #
        super().__init__(scene_id=scene_id, room_id=room_id)

#
class EventInsideRoom(EventRoom):
    #
    def __init__(self, scene_id: str, room_id: str | list[str]) -> None:
        #
        super().__init__(scene_id=scene_id, room_id=room_id)


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
        self.thing_id: str = thing_id
        self.action_type: str = action_type
        self.who: str | list[str] = who



