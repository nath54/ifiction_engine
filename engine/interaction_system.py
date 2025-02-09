
#
class InteractionSystem:
    #
    def __init__(self) -> None:
        #
        pass

    #
    def write_to_output(self, txt: str) -> None:
        #
        pass


#
class InteractionSystemWithBuffer(InteractionSystem):
    #
    def __init__(self) -> None:
        #
        self.buffer: list[str] = []

    #
    def write_to_output(self, txt: str) -> None:
        #
        self.buffer.append(txt)


#
class BasicTerminalInteractionSystem(InteractionSystem):
    #
    def __init__(self) -> None:
        #
        super().__init__()

    #
    def write_to_output(self, txt: str) -> None:
        #
        print(txt)

    #



