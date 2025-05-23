# Scenes, Events and Actions Description and Formalisation

## Introduction

To be a good interactive fiction engine, you need a good, flexible and dynamic events system, that lets the games creator to express their ideas with the less constraints possible.

So, this engine will be doted of a Scene System using an Action System and declenched by an Event System.

## Scene System

A scene represents a sequence of actions.

Scene:
    - scene_id (str): unique id of the scene
    - scenes_actions (list[Action]): List of actions to execute of the scene

## Action System

Under the term actions hides a lot of things, like printing text, to a jump to another action (in the same scene of course), or the end of the game.

Here is a list of all the actions types and its attributes.

### Action Text

Display a text to the screen.

ActionText:
    - text (str): name of the label

### Action Label

Do nothing itself, but allows other actions to jump to it.

ActionLabel:
    - label_name (str): unique in a scene, identifying this label

### Action Jump

Jump to a label.

ActionJump:
    - label_name (str): name of the label to jump to

### Action Conditional Jump

Jump to a label if a condition is validated.

ActionConditionalJump:
    - label_name (str): name of the label to jump to
    - var_cond (str): name of the variable on which the condition will be applied
    - cond_op (str): the operator that will be used. One of `==`, `!=`, `>=`, `<=`, `>`, `<`
    - cond_operand_value (str | int | float): the value that will be compared to the variable of the condition
    - cond_operand_type (str): indicates if the condition_operand_value is a constant or a variable. One of `const`, `var`. If it is `var`, the condition_operand_value must be str and links to an existing variable.

### Action end game

This ends the game.

ActionEnd:
.

### Action creates variable

This creates a variable. If the variable already exists, it just modify the value of the variable to the new value.

ActionCreateVar:
    - var_name (str): name of the variable
    - var_value (str | int | float | bool): value of the variable

### Action edit variable

This changes the value of a variable. If the variable doesn't exists, it creates it with the new value.

ActionEditVar:
    - var_name (str): name of the variable to edit
    - var_value (str | int | float | bool): value of the new variable

### Action delete variable

This deletes a variable. If the variable doesn't exists, this do nothing.

ActionDeleteVar:
    - var_name (str): name of the variable to edit

### Action Binary Operation on variable

ActionVarBinOp:
    - var_output_name (str): name of the variable that will contains the value of the operation
    - elt1_type (str): Indicates if the 1st operand is a constant or a variable. One of `var` or `const`.
    - elt1_value (str | int | float | bool): Name of the variable, or constant value.
    - elt2_type (str): Indicates if the 2nd operand is a constant or a variable. One of `var` or `const`.
    - elt2_value (str | int | float | bool): Name of the variable, or constant value.
    - op (str): Operation to do on the two operands. One of `+`, `-`, `*`, `/`, `%`, `^`, `min`, `max`, `and`, `or`

### Action Unary Operation on variable

ActionVarUnaryOp:
    - var_output_name (str): name of the variable that will contains the value of the operation
    - elt_type (str): Indicates if the 1st operand is a constant or a variable. One of `var` or `const`.
    - elt_value (str | int | float | bool): Name of the variable, or constant value.
    - op (str): Operation to do on the operands. One of `-`, `++`, `--`, `not`

### Action Change Scene

Ends directly this scene, and plays another scene.

ActionChangeScene:
    - scene_id (str): Id of the new scene

### Action End Scene

Ends the scene, and returns to last game command state.

ActionEndScene:
.

### Action Edit Attribute of Class

Edit an attribute (in term of raw classes, not Thing.attributes) of an object.

ActionEditAttributeOfElt:
    - elt_id (str):
    - elt_type (str):
    - elt_attribute_name (str):
    - elt_attribute_new_value (str | int | float | bool):


### Action Append Attribute of Class

Append an element to an attribute (in term of raw classes, not Thing.attributes) of an object.

AppendToAttributeOfElt:
    - elt_id (str):
    - elt_type (str):
    - elt_attribute_name (str):
    - elt_attribute_elt_to_add (str | int | float | bool):


### Action Remove value to Attribute of Class

Remove an element from an attribute (in term of raw classes, not Thing.attributes) of an object.

ActionRemoveValueToAttributeOfElt:
    - elt_id (str):
    - elt_type (str):
    - elt_attribute_name (str):
    - elt_attribute_elt_to_remove (str | int | float | bool):


### Action Set Attribute of Class

Set a key->value couple of an attribute (in term of raw classes, not Thing.attributes) of an object.

ActionSetKVAttributeOfElt:
    - elt_id (str):
    - elt_type (str):
    - elt_attribute_name (str):
    - elt_attribute_elt_key (str):
    - elt_attribute_elt_value (str | int | float | bool):


## Events

Events serves to trigger scenes.

Another way to launch a scene is also from dialog.

So their are a lot of differents events type.

### Base Event Abstract Class

Event:
    - scene_id (str): Name of the scene to launch

### Event Mission Done

EventMissionDone(Event):
    - mission_id (str): Id of the mission that trigger this event when finished

### Event Mission Started

EventMissionStarted(Event):
    - mission_id (str): Id of the mission that trigger this event when started

### Event Enter Room

EventEnterRoom(Event):
    - room_id (str): Id of the room
    - who_enters (str | list[str]): Ids of the entities that we have to detect the room entering

### Event Leave Room

EventLeaveRoom(Event):
    - room_id (str): Id of the room
    - who_leaves (str | list[str]): Ids of the entities that we have to detect the room leaving

### Event Variable Condition

EventVarCond(Event):
    - var_name (str): Name of the variable on which there is the condition
    - cond_operator (str): Operator of the condition
    - cond_operand_value (str | int | float | bool): Operand of the condition, can be a variable name or a constant value.
    - cond_operand_type (str): Indicates if the operand is a variable (`var`) or a constant value (`const`)





