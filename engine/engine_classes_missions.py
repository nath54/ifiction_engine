#
from typing import Any, Optional
#
from engine_classes_conditions import Condition


#
### ABSTRACT MISSION CLASS. ###
#
class Mission:
    #
    def __init__(
            self,
            mission_id: str,
            scene_mission_success: str = "",
            scene_mission_failure: str = "",
            failure_condition: Optional[Condition] = None,
        ) -> None:

        # ABSTRACT CLASS
        #
        self.mission_id: str = mission_id
        #
        self.scene_mission_success: str = scene_mission_success
        self.scene_mission_failure: str = scene_mission_failure
        #
        self.failure_condition: Optional[Condition] = failure_condition

    #
    def to_dict(self) -> dict[str, Any]:
        #
        res: dict[str, Any] = {
            "mission_type": "Mission",
            "scene_mission_success": self.scene_mission_success,
            "scene_mission_failure": self.scene_mission_success
        }

        #
        if self.failure_condition:
            #
            res["failure_condition"] = self.failure_condition.to_dict()

        #
        return res


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
            failure_condition: Optional[Condition] = None,
        ) -> None:

        # ABSTRACT CLASS
        super().__init__(
            mission_id = mission_id,
            scene_mission_success = scene_mission_success,
            scene_mission_failure = scene_mission_failure,
            failure_condition = failure_condition
        )
        #
        self.room_id: str | list[str] = room_id

    #
    def to_dict(self) -> dict[str, Any]:
        #
        res: dict[str, Any] = super().to_dict()

        #
        res["mission_type"] = "MissionRoom"
        res["room_id"] = self.room_id

        #
        return res


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
            failure_condition: Optional[Condition] = None,
        ) -> None:
        #
        super().__init__(
            mission_id = mission_id,
            scene_mission_success = scene_mission_success,
            scene_mission_failure = scene_mission_failure,
            room_id = room_id,
            failure_condition = failure_condition
        )

    #
    def to_dict(self) -> dict[str, Any]:
        #
        res: dict[str, Any] = super().to_dict()

        #
        res["mission_type"] = "MissionEnterRoom"

        #
        return res


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
            failure_condition: Optional[Condition] = None,
        ) -> None:
        #
        super().__init__(
            mission_id = mission_id,
            scene_mission_success = scene_mission_success,
            scene_mission_failure = scene_mission_failure,
            room_id = room_id,
            failure_condition = failure_condition
        )

    #
    def to_dict(self) -> dict[str, Any]:
        #
        res: dict[str, Any] = super().to_dict()

        #
        res["mission_type"] = "MissionLeaveRoom"

        #
        return res


#
### Mission that succeed if a condition on a variable is True. ###
#
class MissionVariableCondition(Mission):
    #
    def __init__(
            self,
            mission_id: str,
            condition: Condition,
            scene_mission_success: str = "",
            scene_mission_failure: str = "",
            failure_condition: Optional[Condition] = None,
    ) -> None:
        #
        super().__init__(
            mission_id = mission_id,
            scene_mission_success = scene_mission_success,
            scene_mission_failure = scene_mission_failure,
            failure_condition = failure_condition
        )
        #
        self.condition: Condition = condition

    #
    def to_dict(self) -> dict[str, Any]:
        #
        res: dict[str, Any] = super().to_dict()

        #
        res["mission_type"] = "MissionVariableCondition"
        res["condition"] = self.condition.to_dict()

        #
        return res


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
            failure_condition: Optional[Condition] = None,
        ) -> None:
        #
        super().__init__(
            mission_id = mission_id,
            scene_mission_success = scene_mission_success,
            scene_mission_failure = scene_mission_failure,
            failure_condition = failure_condition
        )
        #
        self.entity_id: str | list[str] = entity_id

    #
    def to_dict(self) -> dict[str, Any]:
        #
        res: dict[str, Any] = super().to_dict()

        #
        res["mission_type"] = "MissionKillEntity"
        res["entity_id"] = self.entity_id

        #
        return res

