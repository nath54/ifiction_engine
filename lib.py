
#
class GlobalSystem:
    #
    def __init__(self) -> None:
        #
        self.things: dict[int, Thing] = {}
        self.last_id: int = 0
        #
        self.player_id: int = -1

    #
    def get_next_free_id(self) -> int:
        #
        self.last_id += 1
        #
        return self.last_id


#
class Thing:
    #
    def __init__(self, global_system: GlobalSystem) -> None:
        #
        self.id: int = global_system.get_next_free_id()


#
class NameableThing(Thing):
    #
    def __init__(self, global_system: GlobalSystem, name: str) -> None:
        #
        super().__init__(global_system)
        #
        self.name: str = name
        #


#
class Person(NameableThing):
    #
    def __init__(self, global_system: GlobalSystem, name: str) -> None:
        #
        super().__init__(global_system, name)
        #


#
class Room(NameableThing):
    #
    def __init__(self, global_system: GlobalSystem, name: str) -> None:
        #
        super().__init__(global_system, name)
        #


