
# TODOLIST for the project

---

## Events

### EventMissionGot

#### Description of EventMissionGot

TODO

#### State if EventMissionGot

[x] Class Design
[ ] Event Detection Implemented (TODO)

---

### EventMissionInProgress

#### Description of EventMissionInProgress

TODO

#### State of EventMissionInProgress

[x] Class Design
[ ] Event Detection Implemented (TODO)

---

### EventMissionDone

#### Description of EventMissionDone

TODO

#### State of EventMissionDone

[x] Class Design
[ ] Event Detection Implemented (TODO)

---

### EventEnterRoom

#### Description of EventEnterRoom

TODO

#### State of EventEnterRoom

[x] Class Design
[ ] Event Detection Implemented (TODO)

---

### EventLeaveRoom

#### Description of EventLeaveRoom

TODO

#### State of EventLeaveRoom

[x] Class Design
[ ] Event Detection Implemented (TODO)

---

### EventInsideRoom

#### Description of EventInsideRoom

TODO

#### State of EventInsideRoom

[x] Class Design
[ ] Event Detection Implemented (TODO)

---

### EventVariableCondition

#### Description of EventVariableCondition

TODO

#### State of EventVariableCondition

[x] Class Design
[ ] Event Detection Implemented (TODO)

---

### EventActionThing

#### Description of EventActionThing

TODO

#### State of EventActionThing

[x] Class Design
[ ] Event Detection Implemented (TODO)

---

### EventAlways

#### Description of EventAlways

TODO

#### State of EventAlways

[x] Class Design
[ ] Event Detection Implemented (TODO)

---

---

## Missions

---

### MissionEnterRoom

#### Description of MissionEnterRoom

TODO

#### State of MissionEnterRoom

[x] Class Design
[ ] Mission Success Detection Implemented (TODO)

---

### MissionLeaveRoom

#### Description of MissionLeaveRoom

TODO

#### State of MissionLeaveRoom

[x] Class Design
[ ] Mission Success Detection Implemented (TODO)

---

### MissionVariableCondition

#### Description of MissionVariableCondition

TODO

#### State of MissionVariableCondition

[x] Class Design
[ ] Mission Success Detection Implemented (TODO)

---

### MissionActionThing

#### Description of MissionActionThing

TODO

#### State of MissionActionThing

[ ] Class Design (TODO)
[ ] Mission Success Detection Implemented (TODO)

---

## Code development

### Functionnalities to add

- [x] **Animations** (trains, bus, vehicles, moving people, ...)
  - [x] Solvable with an EventAlways with the good events condition, time delays, and the good scene elements.
- [ ] A lot of currently unimplemented commands can be represented by `action`, `action on something`, `action something on something` or something like that. So I think it will be better to parse directly this structure and get the action, and for objects or entities, have a dictionaries of events in reactions of actions if supported, and to have just a list of basic default responses and error messages.
  - [ ] Base class design of `action something`, or `action something keyword_1 arguments_1 ...  keyword_n arguments_n`
  - [ ] Implementation for all possible actions
- [ ] **Events**
  - [x] Base class Design
  - [x] Events play a scene when detected
  - [ ] Implementation of all the events detection
- [ ] **Missions**
  - [x] Base class design
  - [ ] Mission
  - [ ] Implementation of all the mission detections
- [ ] **Scene / Actions**
  - [x] Base class design
  - [ ] Implementation of all the actions
  - [ ] Implementation of the main scene execution function
- [ ] **Dialogues**
  - [ ] base choice based dialog system with support from variables
    - [ ] Add dialog choice option for actions and this method will be possible
  - [ ] Merchant / Shop / Negociation dialog
    - [ ] Add action for *Open Store Menu*.
  - [ ] free typing text dialog (sentence analysis / semantic model / agent llm with function calling)
- [ ] **Smart NPCs**
  - [ ] Entity Appearance
  - [ ] Entity Statistics
    - [ ] Design Humans Stats
  - [ ] Personality Design
  - [ ] NPC Likings / Not Likings
  - [ ] Relation system / Sentiments system for NPC
- [ ] **Grid System for Rooms:** Each Room now have a Grid System for Elements positions, inside Room movements, Elements interactions
  - [ ] Add option to limit the maximum number of elements per grid case (default=1 element maximum per case, if value is -1, don't check the limit (+infinity elements authorized per grid case))
  - [ ] If entity want to move into the new room, check if there is a free grid cell next to the door, if not, indicate there is no place in the other side of the door.
  - [ ] Room parameter for Automatic walls surrounding the grid room, and adapting to windows and grid.
  - [ ] Add a system to see what you can see through an opened door or windows in the other room.
  - [ ] Add position for each elements and decors in a room.
  - [ ] Add actions ranges for in between element interactions
- [x] Import data from other json files
- [ ] a tool to compress a lot of differents various json files into one large one to export after
  - [ ] Command line tool to directly do that
  - [x] You can kinda do that by loading a game and saving it, but it is less direct and less practical

---

## Examples / Tests / Stories

---

### General

More tests needs to be done.
There are a lot of commands that has no utilities in here.

---

### Command Parsing Tests

<b style="color:red">
Need to be fixed since the change of getting classes out of command parser instead of list of string.
</b>

---
