#
from typing import Optional, Any, cast
from dataclasses import dataclass
from . import engine_classes_things_rooms as engine


#######################################################################
############################### UTILITY ###############################
#######################################################################


things_attributes_explaination: dict[str, str] = {
    "openable": "@THING can be opened",
    "open": "@THING is open",
    "lockable": "@THING can be locked",
    "locked": "@THING is locked",
    "item": "@THING can be taken"
}


###############################################################################
############################### UTILITY CLASSES ###############################
###############################################################################


#
@dataclass
class ThingShow:
    #
    thing: engine.Thing

    #
    def __str__(self) -> str:
        #
        return self.thing.name

    #
    def __hash__(self) -> int:
        #
        return self.thing.__hash__()



###################################################################################
############################### CLASSES FOR RESULTS ###############################
###################################################################################


#
class Result:
    #
    def __init__(self) -> None:
        #
        pass

    #
    def __str__(self) -> str:
        #
        return "[RESULT PLACEHOLDER]"

    #
    def to_dict(self) -> dict[str, Any]:
        #
        return {
            "result_type": "Result"
        }



#
class ResultLookAround(Result):
    #
    def __init__(self, room: engine.Room, things_in_room: dict[engine.Thing, tuple[str, engine.Thing | engine.Room]]) -> None:
        #
        super().__init__()
        #
        self.room: engine.Room = room
        self.things_in_room: dict[engine.Thing, tuple[str, engine.Thing | engine.Room]] = things_in_room

    #
    def __str__(self) -> str:
        #
        text: str = f"""
You are in {self.room.room_name}.

{self.room.description}

        """
        #
        if not self.things_in_room:
            return text
        #
        text += "\nYou can see:\n"
        #
        thing: engine.Thing
        for thing in self.things_in_room:
            #
            text += f" - {thing.name}"
            #
            if self.things_in_room[thing][0] == "PartOf":
                #
                thing_of: engine.Thing = cast(engine.Thing, self.things_in_room[thing][1])
                #
                text += f" (part of {thing_of.name})"
            #
            elif self.things_in_room[thing][0] == "Contained":
                #
                thing_of = cast(engine.Thing, self.things_in_room[thing][1])
                #
                text += f" (contained in {thing_of.name})"
            #
            text += "\n"
        #
        text += "\nYou can go :\n"
        #
        access: engine.Access
        for access in self.room.accesses:
            text += f"  - To {access.links_to} in the {access.direction} by {access.thing_id}\n"
        #
        return text



#
class ResultRecap(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultBrief(Result):
    #
    def __init__(self, thing: ThingShow) -> None:
        #
        super().__init__()
        #
        self.thing: ThingShow = thing

    #
    def __str__(self) -> str:
        #
        return self.thing.thing.brief_description



#
class ResultDescribe(Result):
    #
    def __init__(self, thing: ThingShow) -> None:
        #
        super().__init__()
        #
        self.thing: ThingShow = thing

    #
    def __str__(self) -> str:
        #
        return self.thing.thing.description



#
class ResultExamine(Result):
    #
    def __init__(self, thing: ThingShow) -> None:
        #
        super().__init__()
        #
        self.thing: ThingShow = thing

    #
    def __str__(self) -> str:
        #
        text: str = self.thing.thing.description
        #
        attr: str
        for attr in self.thing.thing.attributes:
            if attr in things_attributes_explaination:
                text += f"\n{things_attributes_explaination[attr].replace("@THING", self.thing.thing.name)}"
        #
        return text



#
class ResultRummage(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultListen(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultTouch(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultRead(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultTaste(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultSmell(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultGo(Result):
    #
    def __init__(self, direction: str, access_thing: ThingShow) -> None:
        #
        super().__init__()
        #
        self.direction: str = direction
        self.access_thing: ThingShow = access_thing

    #
    def __str__(self) -> str:
        #
        if self.access_thing.thing.id == "none" or self.access_thing.thing.name == "none":
            #
            return f"You move toward {self.direction}"
        #
        return f"You move toward {self.direction} by {self.access_thing.thing.name}"



#
class ResultPut(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultPush(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultPull(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultAttach(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultBreak(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultThrow(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultDrop(Result):
    #
    def __init__(self, thing: ThingShow, room: engine.Room) -> None:
        #
        super().__init__()
        #
        self.thing: ThingShow = thing
        self.room: engine.Room = room

    #
    def __str__(self) -> str:
        #
        return f"You drop {self.thing} in the room {self.room.room_name}."



#
class ResultClean(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultUse(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultClimb(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultOpen(Result):
    #
    def __init__(self, thing: ThingShow) -> None:
        #
        super().__init__()
        #
        self.thing: ThingShow = thing

    #
    def __str__(self) -> str:
        #
        return f"You open {self.thing}."



#
class ResultClose(Result):
    #
    def __init__(self, thing: ThingShow) -> None:
        #
        super().__init__()
        #
        self.thing: ThingShow = thing

    #
    def __str__(self) -> str:
        #
        return f"You close {self.thing}."



#
class ResultLock(Result):
    #
    def __init__(self, thing1: ThingShow, thing2: Optional[ThingShow] = None) -> None:
        #
        super().__init__()
        #
        self.thing1: ThingShow = thing1
        self.thing2: Optional[ThingShow] = thing2

    #
    def __str__(self) -> str:
        #
        return f"You lock {self.thing1}{f" with {self.thing2}" if self.thing2 is not None else ""}."




#
class ResultUnlock(Result):
    #
    def __init__(self, thing1: ThingShow, thing2: Optional[ThingShow] = None) -> None:
        #
        super().__init__()
        #
        self.thing1: ThingShow = thing1
        self.thing2: Optional[ThingShow] = thing2

    #
    def __str__(self) -> str:
        #
        return f"You unlock {self.thing1}{f" with {self.thing2}" if self.thing2 is not None else ""}."



#
class ResultFill(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultPour(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultInsert(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultRemove(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultSet(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultSpread(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultSqueeze(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultEat(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultDrink(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultAwake(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultAttack(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultBuy(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultShow(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultEmbrace(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultFeed(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultGive(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultSay(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultAsk(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultWrite(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultErase(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultWear(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultUndress(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultInventory(Result):
    #
    def __init__(self, inventory: dict[ThingShow, int]) -> None:
        #
        super().__init__()
        #
        self.inventory: dict[ThingShow, int] = inventory

    #
    def __str__(self) -> str:
        #
        if len(self.inventory) == 0:
            #
            return "You have nothing."
        #
        text: str = "You have:"
        #
        thing: ThingShow
        for thing in self.inventory:
            text += f"\n  - {self.inventory[thing]}x {thing}"
        #
        return text



#
class ResultWait(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultSleep(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultSitDown(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultStandUp(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultTake(Result):
    #
    def __init__(self, thing: ThingShow) -> None:
        #
        super().__init__()
        #
        self.thing: ThingShow = thing

    #
    def __str__(self) -> str:
        #
        return f"You take {self.thing}."



#
class ResultDance(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultSing(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultJump(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultThink(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultScore(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



#
class ResultHelp(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass



###################################################################################
############################### CLASSES FOR RESULTS ###############################
###################################################################################



#
class ResultError(Result):
    #
    def __init__(self) -> None:
        #
        super().__init__()
        #
        pass

    #
    def __str__(self) -> str:
        #
        return "Error\n"


#
class ResultSystemError(ResultError):
    #
    def __init__(self, error_msg: str) -> None:
        #
        super().__init__()
        #
        self.error_msg: str = ""

    #
    def __str__(self) -> str:
        #
        return f"System Error : {self.error_msg}\n"


#
class ResultErrorDirection(ResultError):
    #
    def __init__(self, input_txt: str) -> None:
        #
        super().__init__()
        #
        self.input_txt: str = ""

    #
    def __str__(self) -> str:
        #
        return f"Syntax Error :  `{self.input_txt}` is not a direction, the possible directions are : north, south, east, west, up, down, or a combinaison of thoses.  \n"

#
class ResultErrorCannotGoDirection(ResultError):
    #
    def __init__(self, direction: str) -> None:
        #
        super().__init__()
        #
        self.direction: str = direction

    #
    def __str__(self) -> str:
        #
        return f"Cannot go to the direction `{self.direction}`, there are no access toward it.\n"

#
class ResultErrorAccessLocked(ResultError):
    #
    def __init__(self, direction: str, access_thing: ThingShow) -> None:
        #
        super().__init__()
        #
        self.direction: str = direction
        self.access_thing: ThingShow = access_thing

    #
    def __str__(self) -> str:
        #
        return f"Access Locked. You cannot go to the {self.direction} by {self.access_thing.thing.name}, because {self.access_thing.thing.name} is locked !\n"

#
class ResultErrorAccessClosed(ResultError):
    #
    def __init__(self, direction: str, access_thing: ThingShow) -> None:
        #
        super().__init__()
        #
        self.direction: str = direction
        self.access_thing: ThingShow = access_thing

    #
    def __str__(self) -> str:
        #
        return f"Access is closed. You cannot go to the {self.direction} by {self.access_thing.thing.name}, because {self.access_thing.thing.name} is closed !\n"

#
class ResultErrorThingNotFound(ResultError):
    #
    def __init__(self, text_designing_thing: str) -> None:
        #
        super().__init__()
        #
        self.text_designing_thing: str = text_designing_thing

    #
    def __str__(self) -> str:
        #
        return f"Object not found: {self.text_designing_thing}\n"

#
class ResultErrorCannotActionThing(ResultError):
    #
    def __init__(self, action: str, thing: ThingShow, reason: str = "") -> None:
        #
        super().__init__()
        #
        self.action: str = action
        self.thing: ThingShow = thing
        self.reason: str = reason

    #
    def __str__(self) -> str:
        #
        return f"Cannot {self.action} {self.thing}{self.reason}.\n"

#
class ResultErrorDoesntPossessThing(ResultError):
    #
    def __init__(self, thing: ThingShow) -> None:
        #
        super().__init__()
        #
        self.thing: ThingShow = thing

    #
    def __str__(self) -> str:
        #
        return f"You don't possess {self.thing}. You should take {self.thing} before.\n"

#
class ResultErrorAnotherPossessThing(ResultError):
    #
    def __init__(self, thing: ThingShow, possessor: ThingShow) -> None:
        #
        super().__init__()
        #
        self.thing: ThingShow = thing
        self.possessor: ThingShow = possessor

    #
    def __str__(self) -> str:
        #
        return f"{self.possessor} possess {self.thing}. You cannot interact with possessions of other entities.\n"

#
class ResultErrorCannotActionThingSolo(ResultError):
    #
    def __init__(self, action: str, thing: ThingShow, reason: str = "") -> None:
        #
        super().__init__()
        #
        self.action: str = action
        self.thing: ThingShow = thing
        self.reason: str = reason

    #
    def __str__(self) -> str:
        #
        return f"Cannot {self.action} {self.thing}{self.reason}.\n"

#
class ResultErrorCannotActionThingWithThing(ResultError):
    #
    def __init__(self, action: str, thing1: ThingShow, thing2: ThingShow, reason: str = "") -> None:
        #
        super().__init__()
        #
        self.action: str = ""
        self.thing1: ThingShow = thing1
        self.thing2: ThingShow = thing2
        self.reason: str = reason

    #
    def __str__(self) -> str:
        #
        return f"Cannot {self.action} {self.thing1} with {self.thing2}{self.reason}.\n"

