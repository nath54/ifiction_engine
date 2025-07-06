#
from typing import Any
#
import json
#
from . import lib_utils as lu


#                                                                                                #
###                                                                                            ###
#####                                                                                        #####
##################################################################################################
#####                                    CONDITION CLASSES                                   #####
##################################################################################################
#####                                                                                        #####
###                                                                                            ###
#                                                                                                #


#
### ABSTRACT CONDITION CLASS ###
#
class Condition:
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
            "condition_type": "Condition"
        }

    #
    def verify(self, variables_space: dict[str, Any] ) -> bool:
        #
        return True


#
### CONDITION CLASS VARIABLE CONDITION ###
#
class ConditionVariable(Condition):
    #
    def __init__(
            self,
            variable_name: str,
            cond_op: str,
            operand_type: str,  # "variable", "constant_float", "constant_int", "constant_bool", "constant_str", "constant_list"
            operand_value: Any
        ) -> None:

        #
        super().__init__()

        #
        self.variable_name: str = variable_name
        self.cond_op: str = cond_op
        self.operand_type: str = operand_type
        #
        self.operand_value: Any
        #
        if self.operand_type == "constant_float":
            #
            self.operand_value = float(operand_value)
        #
        elif self.operand_type == "constant_int":
            #
            self.operand_value = int(operand_value)
        #
        elif self.operand_type == "contant_bool":
            #
            self.operand_value = bool(operand_value)
        #
        elif self.operand_type == "constant_list":
            #
            self.operand_value = json.loads( lu.str_list_to_json( str(operand_value) ) )
        #
        else:
            #
            self.operand_value = operand_value

    #
    def to_dict(self) -> dict[str, Any]:
        #
        return {
            "condition_type": "ConditionVariable",
            "variable_name": self.variable_name,
            "cond_op": self.cond_op,
            "operand_type": self.operand_type,
            "operand_value": str(self.operand_value)
        }

    #
    def verify(self, variables_space: dict[str, Any] ) -> bool:
        #
        if self.variable_name not in variables_space:
            #
            return False
        #
        variable_value: Any = variables_space[self.variable_name]
        #
        operand_value: Any
        #
        if self.operand_type == "variable":
            #
            if self.operand_value not in variables_space:
                #
                return False
            #
            operand_value = variables_space[self.operand_value]
        #
        else:
            #
            operand_value = self.operand_value
        #
        if self.operand_type == ">":
            #
            return variable_value > operand_value
        #
        elif self.operand_type == "<":
            #
            return variable_value < operand_value
        #
        elif self.operand_type == "<=":
            #
            return variable_value <= operand_value
        #
        elif self.operand_value == ">=":
            #
            return variable_value >= operand_value
        #
        elif self.operand_value == "==":
            #
            return variable_value == operand_value
        #
        elif self.operand_value == "!=":
            #
            return variable_value != operand_value
        #
        elif self.operand_value == "in":
            #
            return variable_value in operand_value
        #
        elif self.operand_value == "not in":
            #
            return variable_value not in operand_value
        #
        elif self.operand_value == "not":
            #
            return not variable_value
        #
        return True


#
class ConditionOr(Condition):

    #
    def __init__(self, conditions: list[Condition]) -> None:

        #
        super().__init__()

        #
        self.conditions: list[Condition] = conditions

    #
    def to_dict(self) -> dict[str, Any]:
        #
        return {
            "condition_type": "ConditionOr",
            "conditions": [
                c.to_dict() for c in self.conditions
            ]
        }

    #
    def verify(self, variables_space: dict[str, Any]) -> bool:

        #
        for c in self.conditions:

            #
            if c.verify( variables_space=variables_space ):
                #
                return True

        #
        return False


#
class ConditionAnd(Condition):

    #
    def __init__(self, conditions: list[Condition]) -> None:

        #
        super().__init__()

        #
        self.conditions: list[Condition] = conditions

    #
    def to_dict(self) -> dict[str, Any]:
        #
        return {
            "condition_type": "ConditionAnd",
            "conditions": [
                c.to_dict() for c in self.conditions
            ]
        }

    #
    def verify(self, variables_space: dict[str, Any]) -> bool:

        #
        for c in self.conditions:

            #
            if not c.verify( variables_space=variables_space ):
                #
                return False

        #
        return True

