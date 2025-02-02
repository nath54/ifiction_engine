#
import os



class InteractiveFictionEngine:
    #
    def __init__(self, initial_state: dict) -> None:
        #
        self.current_state: dict = initial_state

    #
    






#
def verify_if_game_state_is_good() -> None:
    #
    pass


#
def load_interactive_fiction_model_from_file(filepath: str) -> InteractiveFictionEngine:
    #
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"This file wasn't found : {filepath} !")
    #



