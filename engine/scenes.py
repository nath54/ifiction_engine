from .actions import Action


class Scene:
    #
    def __init__(self, scene_id: str, scenes_actions: list[Action]) -> None:
        #
        self.scene_id: str = scene_id
        self.scenes_actions: list[Action] = scenes_actions



