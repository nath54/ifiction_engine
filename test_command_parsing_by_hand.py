#
from typing import Optional
#
import os
import sys
#
import engine.engine_classes_commands as ecc
import engine.command_parsing as cp


#
def main_user_input_test(generic_kws: dict[str, str]) -> None:
    #
    res: Optional[ecc.Command] = None
    #
    while res is None or not (res.command_name == "C_QUIT"):
        #
        command_input: str = input("> ")
        #
        res = cp.parse_command( command_input=command_input, generic_kws=generic_kws )
        print( res )


#
if __name__ == "__main__":
    #
    generic_kws: dict[str, str] = {
        "to": "KW_TO",
        "in": "KW_IN",
        "inside": "KW_IN",
        "into": "KW_IN",
        "on": "KW_ON",
        "with": "KW_WITH"
    }
    #
    if len(sys.argv) > 1:
        input_test_file: str = sys.argv[1]
        #
        if not os.path.exists(input_test_file):
            raise FileNotFoundError(f"Error : {input_test_file} not found !")
        #
        with open(input_test_file, "r", encoding="utf-8") as f:
            tests: list[str] = f.read().split("\n")
        #
        test: str
        for test_input in tests:
            print(f"{cp.parse_command(command_input=test_input, generic_kws=generic_kws)}")
    #
    else:
        #
        main_user_input_test(generic_kws=generic_kws)
