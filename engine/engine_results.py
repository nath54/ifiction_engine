#
from typing import Callable, Optional
from dataclasses import dataclass
#
from . import engine_classes as engine



###############################################################################
############################### UTILITY CLASSES ###############################
###############################################################################


#
@dataclass
class ThingShow:
    #
    thing: engine.Thing




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
class ResultLookAround(Result):
    #
    def __init__(self, room: engine.Room, things: list[ThingShow]) -> None:
        #
        self.room: engine.Room = room
        self.things: list[ThingShow] = things


#
class ResultRecap(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultBrief(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultDescribe(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultExamine(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultRummage(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultListen(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultTouch(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultRead(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultTaste(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultSmell(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultGo(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultPut(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultPush(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultPull(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultAttach(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultBreak(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultThrow(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultDrop(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultClean(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultUse(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultClimb(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultOpen(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultClose(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultLock(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultUnlock(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultFill(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultPour(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultInsert(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultRemove(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultSet(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultSpread(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultSqueeze(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultEat(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultDrink(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultAwake(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultAttack(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultBuy(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultShow(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultEmbrace(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultFeed(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultGive(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultSay(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultAsk(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultWrite(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultErase(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultWear(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultUndress(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultInventory(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultWait(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultSleep(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultSitDown(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultStandUp(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultTake(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultDance(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultSing(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultJump(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultThink(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultScore(Result):
    #
    def __init__(self) -> None:
        #

        pass



#
class ResultHelp(Result):
    #
    def __init__(self) -> None:
        #

        pass





