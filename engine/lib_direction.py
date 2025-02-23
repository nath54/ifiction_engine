#
from typing import Optional

#
atomics_directions: list[str] = [
    "north",
    "south",
    "east",
    "west",
    "up",
    "down"
]

#
letters: set[str] = set("".join(atomics_directions))

#
def parse_directions(txt: str) -> Optional[str]:
    #
    traited_txt: str = "".join([letter for letter in txt if letter in letters])
    #
    if traited_txt in atomics_directions:
        return traited_txt
    #
    i1: int
    i2: int
    direc1: str
    direc2: str
    #
    for i1 in range(len(atomics_directions)):
        #
        direc1 = atomics_directions[i1]
        #
        for i2 in range(len(atomics_directions)):
            #
            if i1 // 2 == i2 // 2:
                continue
            #
            direc2 = atomics_directions[i2]
            #
            if traited_txt.startswith(direc1) and traited_txt.endswith(direc2):
                return direc1 + "-" + direc2
    #
    return None
