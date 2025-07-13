#
from typing import Optional, Any


# Forward Classes

class Mission:
    pass

#
ALL_ATTRIBUTES: list[str] = [
    "openable",         # The object can be open or close
    "closed",           # Indicates the object is closed, must be openable, if not indicated, it means the object is open
    "locked",           # Indicates the object is locked, must be openable, if not indicated, it means the object is not locked
    "item",             # Indicates the object can be taken by a player
    "container",        # Indicates the object can contain other objects
]

#
class Thing:
    #
    def __init__(
            self,
            id_: str,
            name: str,
            description: str = "",
            brief_description: str = "",
            attributes: list[str] = [],
            presets: list[str] = []
        ) -> None:
        #
        self.id: str = id_
        self.name: str = name
        self.description: str = description
        self.brief_description: str = brief_description
        self.attributes: list[str] = attributes
        self.presets: list[str] = presets

    #
    def to_dict(self) -> dict[str, Any]:
        #
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "brief_description": self.brief_description,
            "attributes": self.attributes
        }

    #
    def __str__(self) -> str:
        #
        return f"Thing({self.id}, {self.attributes})"

    #
    def __repr__(self) -> str:
        #
        return self.__str__()

    #
    def __hash__(self) -> int:
        #
        return self.id.__hash__()


#
class Object(Thing):
    #
    def __init__(
            self,
            id_: str,
            name: str,
            description: str = "",
            brief_description: str = "",
            attributes: list[str] = [],
            parts: list[str] = [],
            part_of: Optional[str] = None,
            unlocks: list[str] = [],
            contains: Optional[dict[str, int]] = None,
            easy_to_unlock_from: list[str] = []
        ) -> None:
        #
        super().__init__(
                    id_=id_,
                    name=name,
                    description=description,
                    brief_description=brief_description,
                    attributes=attributes
        )
        #
        self.parts: list[str] = parts
        self.part_of: Optional[str] = part_of
        self.unlocks: list[str] = unlocks
        self.contains: dict[str, int] = {} if contains is None else contains
        self.easy_to_unlock_from: list[str] = easy_to_unlock_from

    #
    def to_dict(self) -> dict[str, Any]:
        #
        res: dict[str, Any] = super().to_dict()
        #
        res["parts"] = self.parts
        res["part_of"] = self.part_of
        res["unlocks"] = self.unlocks
        res["contains"] = self.contains
        #
        return res


#
class LifeSystem:
    #
    def __init__(
            self,
            max_pv: int = 100,
            current_pv: Optional[int] = None,
            state: Optional[dict[str, Any]] = None
        ) -> None:
        #
        self.max_pv: int = max_pv
        self.current_pv: int = current_pv if isinstance(current_pv, int) else self.max_pv
        self.state: dict[str, Any] = state if isinstance(state, dict) else {}

    #
    def to_dict(self) -> dict[str, Any]:
        #
        return {
            "max_pv": self.max_pv,
            "current_pv": self.current_pv,
            "state": self.state
        }

    #
    def __str__(self) -> str:
        #
        return f"[{self.current_pv}/{self.max_pv}pv]"

    #
    def __repr__(self) -> str:
        #
        return self.__str__()


#
class Entity(Thing):
    #
    def __init__(
            self,
            id_: str,
            name: str,
            room: str,
            description: str = "",
            brief_description: str = "",
            attributes: list[str] = [],
            inventory: Optional[dict[str, int]] = None,
            life_system: LifeSystem = LifeSystem()
        ) -> None:
        #
        super().__init__(
                    id_=id_,
                    name=name,
                    description=description,
                    brief_description=brief_description,
                    attributes=attributes
        )
        #
        self.room: str = room
        self.inventory: dict[str, int] = inventory if isinstance(inventory, dict) else {}
        self.life_system: LifeSystem = life_system

    #
    def to_dict(self) -> dict[str, Any]:
        #
        res: dict[str, Any] = super().to_dict()
        #
        res["room"] = self.room
        res["inventory"] = self.inventory
        res["life_system"] = self.life_system.to_dict()
        #
        return res

    #
    def __str__(self) -> str:
        #
        return f"Entity({self.id}, in {self.room}, {self.life_system}, {self.attributes})"

    #
    def __repr__(self) -> str:
        #
        return self.__str__()


#
class Player(Entity):
    #
    def __init__(
        self,
        id_: str,
        name: str,
        room: str,
        description: str = "",
        brief_description: str = "",
        attributes: list[str] = [],
        inventory: Optional[dict[str, int]] = None,
        life_system: LifeSystem = LifeSystem(),
        missions: list[str] = []
    ) -> None:
        #
        super().__init__(
            id_=id_,
            name=name,
            room=room,
            description=description,
            brief_description=brief_description,
            attributes=attributes,
            inventory=inventory,
            life_system=life_system
        )
        #
        self.missions: list[str] = []


#
class Access:
    #
    def __init__(
            self,
            thing_id: str,
            direction: str,
            links_to: str
        ) -> None:
        #
        self.thing_id: str = thing_id
        self.direction: str = direction
        self.links_to: str = links_to

    #
    def to_dict(self) -> dict[str, Any]:
        #
        return {
            "thing_id": self.thing_id,
            "direction": self.direction,
            "links_to": self.links_to
        }

    #
    def __str__(self) -> str:
        #
        return f"You can go to {self.links_to} by {self.thing_id} [{self.direction}]"

    #
    def __repr__(self) -> str:
        #
        return self.__str__()


#
class Room:

    #
    def __init__(
            self,
            room_name: str,
            accesses: list[ Access ],
            description: str = "",
            things_inside: Optional[dict[str, int]] = None,
            global_time_shift: float = 0
        ) -> None:
        #
        self.room_name: str = room_name
        self.accesses: list[ Access ] = accesses
        self.description: str = description
        self.things_inside: dict[str, int] = {} if things_inside is None else things_inside
        self.global_time_shift: float = 0

    #
    def to_dict(self) -> dict[str, Any]:
        #
        return {
            "room_name": self.room_name,
            "accesses": [
                access.to_dict() for access in self.accesses
            ],
            "description": self.description,
            "things_inside": self.things_inside
        }

    #
    def __str__(self) -> str:
        #
        return f"\n\nRoom:\n  + Room name = {self.room_name}\n{'  + Inside the room:\n\t-' if self.things_inside else ''}{'\n\t-'.join(self.things_inside)}"

    #
    def __repr__(self) -> str:
        #
        return self.__str__()

