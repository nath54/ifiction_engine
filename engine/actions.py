#
from typing import Any


#
class Action:
    #
    def __init__(self) -> None:

        # GENERIC ABSTRACT CLASS
        pass

#
class ActionText(Action):
    #
    def __init__(self, text: str) -> None:
        #
        super().__init__()
        #
        self.text: str = text

#
class ActionLabel(Action):
    #
    def __init__(self, label_name: str) -> None:
        #
        super().__init__()
        #
        self.label_name: str = label_name

#
class ActionJump(Action):
    #
    def __init__(self, label_name: str) -> None:
        #
        super().__init__()
        #
        self.label_name: str = label_name


#
class ActionConditionalJump(ActionJump):
    #
    def __init__(
        self,
        label_name: str,
        var_cond: str,
        cond_op: str,
        cond_operand_value: str | int | float | bool,
        cond_operand_type: str
    ) -> None:
        #
        super().__init__(label_name=label_name)
        #
        self.var_cond: str = var_cond
        self.cond_op: str = cond_op
        self.cond_operand_value: str | int | float | bool = cond_operand_value
        self.cond_operand_type: str = cond_operand_type


#
class ActionEnd(Action):
    #
    def __init__(self) -> None:
        #
        super().__init__()



#
class ActionCreateVar(Action):
    #
    def __init__(self, var_name: str, var_value: str | int | float | bool) -> None:
        #
        super().__init__()
        #
        self.var_name: str = var_name
        self.var_value: str | int | float | bool = var_value


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
class ActionDeleteVar(Action):
    #
    def __init__(self, var_name: str) -> None:
        #
        super().__init__()
        #
        self.var_name: str = var_name



#
class ActionBinaryOp(Action):
    #
    def __init__(
        self,
        var_output_name: str,
        elt1_type: str,
        elt1_value: str | int | float | bool,
        elt2_type: str,
        elt2_value: str | int | float | bool,
        op: str
    ) -> None:
        #
        super().__init__()
        #
        self.var_output_name: str = var_output_name
        self.elt1_type: str = elt1_type
        self.elt1_value: str | int | float | bool = elt1_value
        self.elt2_type: str = elt2_type
        self.elt2_value: str | int | float | bool = elt2_value


#
class ActionUnaryOp(Action):
    #
    def __init__(
        self,
        var_output_name: str,
        elt_type: str,
        elt_value: str | int | float | bool,
        op: str
    ) -> None:
        #
        super().__init__()
        #
        self.var_output_name: str = var_output_name
        self.elt_type: str = elt_type
        self.elt_value: str | int | float | bool = elt_value
        self.op: str = op


#
class ActionChangeScene(Action):
    #
    def __init__(self, scene_id: str) -> None:
        #
        super().__init__()
        #
        self.scene_id: str = scene_id

#
class ActionEndScene(Action):
    #
    def __init__(self) -> None:
        #
        super().__init__()


#
class ActionChangeElt(Action):
    #
    def __init__(self, elt_id: str, elt_type: str, elt_attr_name: str | list[str]) -> None:
        #
        super().__init__()
        #
        self.elt_id: str = elt_id
        self.elt_type: str = elt_type
        self.elt_attr_name: str | list[str] = elt_attr_name



#
class ActionEditAttributeOfElt(ActionChangeElt):
    #
    def __init__(
        self,
        elt_id: str,
        elt_type: str,
        elt_attr_name: str | list[str],
        elt_attr_new_value: str | int | float | bool
    ) -> None:
        #
        super().__init__(elt_id=elt_id, elt_type=elt_type, elt_attr_name=elt_attr_name)
        #
        self.elt_attr_new_value: str | int | float | bool = elt_attr_new_value



#
class ActionAppendToAttributeOfElt(ActionChangeElt):
    #
    def __init__(
        self,
        elt_id: str,
        elt_type: str,
        elt_attr_name: str | list[str],
        elt_attr_new_value_to_append: str | int | float | bool
    ) -> None:
        #
        super().__init__(elt_id=elt_id, elt_type=elt_type, elt_attr_name=elt_attr_name)
        #
        self.elt_attr_new_value_to_append: str | int | float | bool = elt_attr_new_value_to_append



#
class ActionRemoveValueToAttributeOfElt(ActionChangeElt):
    #
    def __init__(
        self,
        elt_id: str,
        elt_type: str,
        elt_attr_name: str | list[str],
        elt_attr_value_to_remove: str | int | float | bool
    ) -> None:
        #
        super().__init__(elt_id=elt_id, elt_type=elt_type, elt_attr_name=elt_attr_name)
        #
        self.elt_attr_value_to_remove: str | int | float | bool = elt_attr_value_to_remove



#
class ActionSetKVAttributeOfElt(ActionChangeElt):
    #
    def __init__(
        self,
        elt_id: str,
        elt_type: str,
        elt_attr_name: str | list[str],
        elt_attr_key: str,
        elt_attr_value: str | int | float | bool
    ) -> None:
        #
        super().__init__(elt_id=elt_id, elt_type=elt_type, elt_attr_name=elt_attr_name)
        #
        self.elt_attr_key: str = elt_attr_key
        self.elt_attr_value: str | int | float | bool = elt_attr_value

