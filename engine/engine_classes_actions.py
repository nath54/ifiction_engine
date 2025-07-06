#
from typing import Any
#
from . import engine_classes_conditions as eccond


#                                                                                                #
###                                                                                            ###
#####                                                                                        #####
##################################################################################################
#####                                      BASE ACTIONS                                      #####
##################################################################################################
#####                                                                                        #####
###                                                                                            ###
#                                                                                                #


#
### ABSTRACT ACTION CLASS ###
#
class Action:
    #
    def __init__(
            self
        ) -> None:

        # GENERIC ABSTRACT CLASS
        pass

    #
    def to_dict(self) -> dict[str, Any]:
        #
        return {
            "action_type": "action"
        }


#
### Action that display text to the players. ###
#
class ActionText(Action):
    #
    def __init__(
            self,
            text: str
        ) -> None:
        #
        super().__init__()
        #
        self.text: str = text


#
### Action that act as a guide for ActionJump and And ActionConditionalJump to know where to jump ###
#
class ActionLabel(Action):
    #
    def __init__(
            self,
            label_name: str
        ) -> None:
        #
        super().__init__()
        #
        self.label_name: str = label_name


#
### Action that jumps to the next action after the specified label name. ###
#
class ActionJump(Action):
    #
    def __init__(
            self,
            label_name: str
        ) -> None:
        #
        super().__init__()
        #
        self.label_name: str = label_name


#
### Action that jumps to the next action after the specified label name IF the condition is respected. ###
#
class ActionConditionalJump(ActionJump):
    #
    def __init__(
        self,
        label_name: str,
        condition: eccond.Condition
    ) -> None:
        #
        super().__init__(label_name=label_name)
        #
        self.condition: eccond.Condition = condition


#
### Action that change the current scene and jump to the first action of the new scene. ###
#
class ActionChangeScene(Action):
    #
    def __init__(
            self,
            scene_id: str
        ) -> None:
        #
        super().__init__()
        #
        self.scene_id: str = scene_id


#
### Action that ends the scene and get back to the game. ###
#
class ActionEndScene(Action):
    #
    def __init__(
            self
        ) -> None:
        #
        super().__init__()


#
### Action that ends the game. ###
#
class ActionEndGame(Action):
    #
    def __init__(
            self,
            final_score: int = 0
        ) -> None:
        #
        super().__init__()
        #
        self.final_score: int = 0


#                                                                                                #
###                                                                                            ###
#####                                                                                        #####
##################################################################################################
#####                                VARIABLE RELATED ACTIONS                                #####
##################################################################################################
#####                                                                                        #####
###                                                                                            ###
#                                                                                                #


#
### Action that create a variable in the global variable space (GVS). ###
#
class ActionCreateVar(Action):
    #
    def __init__(
            self,
            var_name: str,
            var_value: str | int | float | bool
        ) -> None:
        #
        super().__init__()
        #
        self.var_name: str = var_name
        self.var_value: str | int | float | bool = var_value


#
### Action that update the value of a variable in the global variable space (GVS). ###
#
class ActionEditVar(Action):
    #
    def __init__(self, var_name: str, var_value: str | int | float | bool) -> None:
        #
        super().__init__()
        #
        self.var_name: str = var_name
        self.var_value: str | int | float | bool = var_value


#
### Action that delete a variable in the global variable space (GVS). ###
#
class ActionDeleteVar(Action):
    #
    def __init__(self, var_name: str) -> None:
        #
        super().__init__()
        #
        self.var_name: str = var_name


#
### Action that create or update a variable (the ouput one) with the result value of the specified operation. ###
#
class ActionBinaryOp(Action):
    #
    def __init__(
        self,
        var_output_name: str,
        elt1_type: str,
        elt1_value: Any,
        elt2_type: str,
        elt2_value: Any,
        op: str
    ) -> None:
        #
        super().__init__()
        #
        self.var_output_name: str = var_output_name
        self.elt1_type: str = elt1_type
        self.elt1_value: Any = elt1_value
        self.elt2_type: str = elt2_type
        self.elt2_value: Any = elt2_value
        self.op: str = op


#
### Action that create or update a variable (the ouput one) with the result value of the specified operation. ###
#
class ActionUnaryOp(Action):
    #
    def __init__(
        self,
        var_output_name: str,
        elt_type: str,
        elt_value: Any,
        op: str
    ) -> None:
        #
        super().__init__()
        #
        self.var_output_name: str = var_output_name
        self.elt_type: str = elt_type
        self.elt_value: Any = elt_value
        self.op: str = op


#                                                                                                #
###                                                                                            ###
#####                                                                                        #####
##################################################################################################
#####                       ELEMENTS ATTRIBUTE EDITION RELATED ACTIONS                       #####
##################################################################################################
#####                                                                                        #####
###                                                                                            ###
#                                                                                                #


#
### ABSTRACT Action class for actions that changes the elements. ###
#
class ActionChangeElt(Action):
    #
    def __init__(
        self,
        elt_id: str,
        elt_type: str,
        elt_attr_name: str | list[str]
    ) -> None:
        #
        super().__init__()
        #
        self.elt_id: str = elt_id
        self.elt_type: str = elt_type
        self.elt_attr_name: str | list[str] = elt_attr_name


#
### Action that edit the value of an attribute. WARNING: thus only works on scalar / string attributes. ###
#
class ActionEditAttributeOfElt(ActionChangeElt):
    #
    def __init__(
        self,
        elt_id: str,
        elt_type: str,
        elt_attr_name: str | list[str],
        elt_attr_new_value: Any
    ) -> None:
        #
        super().__init__(elt_id=elt_id, elt_type=elt_type, elt_attr_name=elt_attr_name)
        #
        self.elt_attr_new_value: Any = elt_attr_new_value


#
### Action that append a value to an attribute that is a list. WARNING: thus only works on attributes with list type. ###
#
class ActionAppendToAttributeOfElt(ActionChangeElt):
    #
    def __init__(
        self,
        elt_id: str,
        elt_type: str,
        elt_attr_name: str | list[str],
        elt_attr_new_value_to_append: Any
    ) -> None:
        #
        super().__init__(elt_id=elt_id, elt_type=elt_type, elt_attr_name=elt_attr_name)
        #
        self.elt_attr_new_value_to_append: Any = elt_attr_new_value_to_append



#
### Action that append a value to an attribute that is a container. WARNING: thus only works on attributes with list or dictionnary type. ###
#
class ActionRemoveValueToAttributeOfElt(ActionChangeElt):
    #
    def __init__(
        self,
        elt_id: str,
        elt_type: str,
        elt_attr_name: str | list[str],
        elt_attr_value_to_remove: Any
    ) -> None:
        #
        super().__init__(elt_id=elt_id, elt_type=elt_type, elt_attr_name=elt_attr_name)
        #
        self.elt_attr_value_to_remove: Any = elt_attr_value_to_remove


#
### Action that set a value to an attribute that is a dict. WARNING: thus only works on attributes with dictionnary type. ###
#
class ActionSetKVAttributeOfElt(ActionChangeElt):
    #
    def __init__(
        self,
        elt_id: str,
        elt_type: str,
        elt_attr_name: str | list[str],
        elt_attr_key: str,
        elt_attr_value: Any
    ) -> None:
        #
        super().__init__(elt_id=elt_id, elt_type=elt_type, elt_attr_name=elt_attr_name)
        #
        self.elt_attr_key: str = elt_attr_key
        self.elt_attr_value: Any = elt_attr_value


#                                                                                                #
###                                                                                            ###
#####                                                                                        #####
##################################################################################################
#####                                 THINGS RELATED ACTIONS                                 #####
##################################################################################################
#####                                                                                        #####
###                                                                                            ###
#                                                                                                #


"""
Note:

In the following classes, when speaking of place_type, the possible values are:

- "room", then the `place_id` designs the `room_id`, and the things will be added to / removed from the room.
- "container", then the `place_id` designs the `thing_id`, and the things will be added to / removed from the thing container space.
- "entity", then the `place_id` designs the `entity_id`, and the things will be added to / removed from the entities inventory.

"""


#
### Action that duplicates a thing. I.E. creating a new thing with exactly the same attributes than the previous, but only a different thing_id ###
#
class ActionThingDuplicate(Action):

    #
    def __init__(
            self,
            src_elt_id: str,
            dst_elt_id: str
        ) -> None:
        #
        super().__init__()
        #
        self.src_elt_id: str = src_elt_id
        self.dst_elt_id: str = dst_elt_id


#
### Action that displace a certain quantity of things from a place to another place ###
#
class ActionThingDisplace(Action):

    #
    def __init__(
            self,
            thing_id: str,
            src_place_type: str,
            src_place_id: str,
            dst_place_type: str,
            dst_place_id: str,
            quantity: int = 1
        ) -> None:
        #
        super().__init__()
        #
        self.thing_id: str = thing_id
        self.src_place_type: str = src_place_type
        self.src_place_id: str = src_place_id
        self.dst_place_type: str = dst_place_type
        self.dst_place_id: str = dst_place_id
        self.quantity: int = quantity


#
### Action that add a certain quantity of things to a place ###
#
class ActionThingAddToPlace(Action):

    #
    def __init__(
            self,
            thing_id: str,
            place_type: str,
            place_id: str,
            quantity: int = 1
        ) -> None:
        #
        super().__init__()
        #
        self.thing_id: str = thing_id
        self.place_type: str = place_type
        self.place_id: str = place_id
        self.quantity: int = quantity


#
### Action that remove a certain quantity of things to a place ###
#
class ActionThingRemoveFromPlace(Action):

    #
    def __init__(
            self,
            thing_id: str,
            place_type: str,
            place_id: str,
            quantity: int = 1
        ) -> None:
        #
        super().__init__()
        #
        self.thing_id: str = thing_id
        self.place_type: str = place_type
        self.place_id: str = place_id
        self.quantity: int = quantity


#                                                                                                #
###                                                                                            ###
#####                                                                                        #####
##################################################################################################
#####                                 PLAYER RELATED ACTIONS                                 #####
##################################################################################################
#####                                                                                        #####
###                                                                                            ###
#                                                                                                #


#
### Action that assigns a mission to a player ###
#
class ActionPlayerAssignMission(Action):

    #
    def __init__(
            self,
            player_id: str,
            mission_id: str
        ) -> None:
        #
        super().__init__()
        #
        self.player_id: str = player_id
        self.mission_id: str = mission_id

