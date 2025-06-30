#
from typing import Any


#
### ABSTRACT MISSION CLASS. ###
#
class Mission:
    #
    def __init__(
            self,
            mission_id: str,
            failure_cond_variable: str = "",
            failure_cond_op: str = "",
            failure_cond_value: str | int | float | bool = "",
            scene_mission_success: str = "",
            scene_mission_failure: str = ""
        ) -> None:

        # ABSTRACT CLASS
        #
        self.mission_id: str = mission_id
        #
        self.scene_mission_success: str = scene_mission_success
        self.scene_mission_failure: str = scene_mission_failure
        #
        self.failure_cond_variable: str = failure_cond_variable
        self.failure_cond_op: str = failure_cond_op
        self.failure_cond_value: str | int | float | bool = failure_cond_value

    #
    def to_dict(self) -> dict[str, Any]:
        #
        return {
            "mission_type": "Mission"
        }


#
### ABSTRACT MISSION CLASS FOR MISSIONS ABOUT ROOMS. ###
#
class MissionRoom(Mission):
    #
    def __init__(
            self,
            mission_id: str,
            room_id: str | list[str],
            scene_mission_success: str = "",
            scene_mission_failure: str = "",
            failure_cond_variable: str = "",
            failure_cond_op: str = "",
            failure_cond_value: str | int | float | bool = "",
        ) -> None:

        # ABSTRACT CLASS
        super().__init__(
            mission_id = mission_id,
            scene_mission_success = scene_mission_success,
            scene_mission_failure = scene_mission_failure,
            failure_cond_variable = failure_cond_variable,
            failure_cond_op = failure_cond_op,
            failure_cond_value = failure_cond_value
        )
        #
        self.room_id: str | list[str] = room_id


#
### Mission that succeed if the player enters a room / one of the rooms if a list of rooms is given. ###
#
class MissionEnterRoom(MissionRoom):
    #
    def __init__(
            self,
            mission_id: str,
            room_id: str | list[str],
            scene_mission_success: str = "",
            scene_mission_failure: str = "",
            failure_cond_variable: str = "",
            failure_cond_op: str = "",
            failure_cond_value: str | int | float | bool = "",
        ) -> None:
        #
        super().__init__(
            mission_id = mission_id,
            scene_mission_success = scene_mission_success,
            scene_mission_failure = scene_mission_failure,
            room_id = room_id,
            failure_cond_variable = failure_cond_variable,
            failure_cond_op = failure_cond_op,
            failure_cond_value = failure_cond_value
        )


#
### Mission that succeed if the player leaves a room / all of the rooms if a list of rooms is given. ###
#
class MissionLeaveRoom(MissionRoom):
    #
    def __init__(
            self,
            mission_id: str,
            room_id: str | list[str],
            scene_mission_success: str = "",
            scene_mission_failure: str = "",
            failure_cond_variable: str = "",
            failure_cond_op: str = "",
            failure_cond_value: str | int | float | bool = "",
        ) -> None:
        #
        super().__init__(
            mission_id = mission_id,
            scene_mission_success = scene_mission_success,
            scene_mission_failure = scene_mission_failure,
            room_id = room_id,
            failure_cond_variable = failure_cond_variable,
            failure_cond_op = failure_cond_op,
            failure_cond_value = failure_cond_value
        )


#
### Mission that succeed if a condition on a variable is True. ###
#
class MissionVariableCondition(Mission):
    #
    def __init__(
            self,
            mission_id: str,
            var_name: str,
            var_cond_op: str,
            var_cond_operand_value: str | int | float | bool,
            scene_mission_success: str = "",
            scene_mission_failure: str = "",
            failure_cond_variable: str = "",
            failure_cond_op: str = "",
            failure_cond_value: str | int | float | bool = "",
    ) -> None:
        #
        super().__init__(
            mission_id = mission_id,
            scene_mission_success = scene_mission_success,
            scene_mission_failure = scene_mission_failure,
            failure_cond_variable = failure_cond_variable,
            failure_cond_op = failure_cond_op,
            failure_cond_value = failure_cond_value
        )
        #
        self.var_name: str = var_name
        self.var_cond_op: str = var_cond_op
        self.var_cond_operand_value: str | int | float | bool = var_cond_operand_value


#
### Mission that succeed if an entity is killed. ###
#
class MissionKillEntity(Mission):
    #
    def __init__(
            self,
            mission_id: str,
            entity_id: str | list[str],
            scene_mission_success: str = "",
            scene_mission_failure: str = "",
            failure_cond_variable: str = "",
            failure_cond_op: str = "",
            failure_cond_value: str | int | float | bool = "",
        ) -> None:
        #
        super().__init__(
            mission_id = mission_id,
            scene_mission_success = scene_mission_success,
            scene_mission_failure = scene_mission_failure,
            failure_cond_variable = failure_cond_variable,
            failure_cond_op = failure_cond_op,
            failure_cond_value = failure_cond_value
        )
        #
        self.entity_id: str | list[str] = entity_id

