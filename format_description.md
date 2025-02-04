# Interactive Fiction format description

This document explains the file format for this interactive fiction engine.

## General information

For now, I will first make a json file format work. Then I will think about potentially making a more human-readable system.

There is no differences between a base game file, and a game save file.
This means that we can directly load and play from a savegame, but the catch is that it just takes a little more space on the disk to store.
Why it's planned like that for the moment ? I would say it is because I want flexibility in the world construction and actions possible, like for examle, I want possible the fact to change items, destroy them, to have actions that can destroy rooms, or permanently change them, ...

This engines will be built for turn by turn actions, so a turn can represents a command of a player for instance.

There will also be a system of custom actions and variables, so the game creator can have flexibility to do things that it would have been difficult without.

## Global architecture

A game file has the following structure:

```json
{
    "things": {
        "thing_id": {
            "thing_attr_1": "", // Thing value 1
            "thing_attr_2": [], // Thing value 2
            "thing_attr_3": 0,  // Thing value 3
            "thing_attr_4": {}  // Thing value 4
            // ...
        },
        // ...
    },
    "rooms": {
        // Room attributes
    },
    "end": [
        // End
    ],
    "variables": {
        // Global variables values
    },
    "players": {
        // Players
    },
    "nb_turn": 0  // Nombre de tours
}
```

## Thing class

Thing:
    * id: str (unique)
    * name: str
    + description: str = ""
    + brief_description: str = ""
    + attributes: list[ str ] / list[ Attributes ]= []
    + parts: list[ ThingId ] = []
    + part_of: Optional[ ThingId ] = None
    + is_open: int = 1
    + is_locked: int = 0
    + unlocks: list[ str ] / list[ ThingId ] = []

## Rooms class

Room:
    * room_name: str (unique)
    * access: list[ dict[str, str] ] / list[ Access ]
    + description: str = ""

Access:
    * thing: str / ThingId
    * direction: str / Direction
    * links_to: str / RoomId

## End classes

EndOneOf:
    * lst: list[ EndClass ]

EndAllOf:
    * lst: list[ EndClass ]

EndInsideRoom:
    * room: str / RoomId

## Players class

Player:
    * room: str / RoomId
    + inventory: dict[ str, int ] / dict[ ThingId, Quantity ] = {}

