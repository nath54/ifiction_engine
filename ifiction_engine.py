#
from typing import Optional
#
import sys
import os
#
from engine.interaction_system import BasicTerminalInteractionSystem
from engine.engine_classes import load_interactive_fiction_model_from_file
from command_parsing.command_parsing import parse_command
from engine.engine_commands import ALL_COMMANDS_FUNCTIONS


#
if __name__ == "__main__":

    #
    if len(sys.argv) != 2:
        raise SyntaxError(f"Error: bad arguments given to ")
