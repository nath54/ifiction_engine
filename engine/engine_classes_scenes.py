from .engine_classes_actions import Action


class Scene:
    #
    def __init__(self, scene_id: str, scenes_actions: list[Action]) -> None:
        #
        self.scene_id: str = scene_id
        self.scenes_actions: list[Action] = scenes_actions

    #
    def to_dict(self) -> dict:
        #
        return {
            "scene_id": self.scene_id,
            "scenes_actions": [
                a.to_dict() for a in self.scenes_actions
            ]
        }



