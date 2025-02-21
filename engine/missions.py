


#
class Mission:
    #
    def __init__(self, mission_id: str) -> None:

        # ABSTRACT CLASS
        self.mission_id: str = mission_id


#
class MissionRoom(Mission):
    #
    def __init__(self, mission_id: str, room_id: str | list[str]) -> None:

        # ABSTRACT CLASS
        super().__init__(mission_id=mission_id)
        #
        self.room_id: str | list[str] = room_id


#
class MissionEnterRoom(MissionRoom):
    #
    def __init__(self, mission_id: str, room_id: str | list[str]) -> None:
        #
        super().__init__(mission_id=mission_id, room_id=room_id)


#
class MissionLeaveRoom(MissionRoom):
    #
    def __init__(self, mission_id: str, room_id: str | list[str]) -> None:
        #
        super().__init__(mission_id=mission_id, room_id=room_id)


#
class MissionVariableCondition(Mission):
    #
    def __init__(
        self,
        mission_id: str,
        var_name: str,
        var_cond_op: str,
        var_cond_operand_value: str | int | float | bool,
        var_cond_operand_type: str
    ) -> None:
        #
        super().__init__(mission_id=mission_id)
        #
        self.var_name: str = var_name
        self.var_cond_op: str = var_cond_op
        self.var_cond_operand_value: str | int | float | bool = var_cond_operand_value
        self.var_cond_operand_type: str = var_cond_operand_type


#
class MissionKillEntity(Mission):
    #
    def __init__(self, mission_id: str, entity_id: str | list[str]) -> None:
        #
        super().__init__(mission_id=mission_id)
        #
        self.entity_id: str | list[str] = entity_id




