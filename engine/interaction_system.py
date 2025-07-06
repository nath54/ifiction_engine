#
from . import engine_results as er
from .engine_classes_game import Game


#
class InteractionSystem:
    #
    def __init__(self, game: Game) -> None:
        #
        self.running: bool = True
        #
        self.game: Game = game
        #
        self.results: list[er.Result] = []

    #
    def add_result(self, result: er.Result) -> None:
        #
        self.results.append(result)

    #
    def write_to_output(self, txt: str) -> None:
        #
        pass

    #
    def ask_input(self) -> str:
        #
        return ""


#
class InteractionSystemWithBuffer(InteractionSystem):
    #
    def __init__(self, game: Game) -> None:
        #
        super().__init__(game)
        #
        self.buffer: list[str] = []

    #
    def write_to_output(self, txt: str) -> None:
        #
        self.buffer.append(txt)

    #
    def flush_output(self) -> None:
        #
        pass
        #
        self.buffer = []



#
class BasicTerminalInteractionSystem(InteractionSystem):
    #
    def __init__(self, game: Game) -> None:
        #
        super().__init__(game)

    #
    def write_to_output(self, txt: str) -> None:
        #
        print(txt)

    #
    def ask_input(self) -> str:
        #
        return input(">")

    #
    def add_result(self, result: er.Result) -> None:
        #
        self.results.append(result)
        #
        self.write_to_output(result.__str__())



