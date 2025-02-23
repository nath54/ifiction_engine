#
from typing import Any



#
def fusion_lists_str(obj_A: object, obj_B: object, lst_attr: str | list[str]) -> object:
    #
    if isinstance(lst_attr, str):
        #
        lst_attr = [lst_attr]
    #
    lst_A: list[str]
    lst_B: list[str]
    attr: str
    elt: str
    #
    for attr in lst_attr:
        #
        lst_A = getattr(obj_A, attr)
        lst_B = getattr(obj_B, attr)
        #
        for elt in lst_B:
            #
            if elt not in lst_A:
                #
                lst_A.append(elt)
    #
    return obj_A


#
def fusion_dict_str(obj_A: object, obj_B: object, lst_attr: str | list[str]) -> object:
    #
    if isinstance(lst_attr, str):
        #
        lst_attr = [lst_attr]
    #
    dict_A: dict[str, Any]
    dict_B: dict[str, Any]
    attr: str
    elt: str
    #
    for attr in lst_attr:
        #
        dict_A = getattr(obj_A, attr)
        dict_B = getattr(obj_B, attr)
        #
        for elt in dict_B:
            #
            if elt not in dict_A:
                #
                dict_A[elt] = dict_B[elt]
    #
    return obj_A


#
def fusion_elts_str_or_None(obj_A: object, obj_B: object, lst_attr: str | list[str]) -> object:
    #
    if isinstance(lst_attr, str):
        #
        lst_attr = [lst_attr]
    #
    attr: str
    #
    for attr in lst_attr:
        #
        if getattr(obj_A, attr) == "" or getattr(obj_A, attr) is None:
            #
            setattr(obj_A, attr, getattr(obj_B, attr))
    #
    return obj_A
