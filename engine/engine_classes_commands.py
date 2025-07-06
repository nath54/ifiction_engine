#
from typing import Optional

#
class Command:

    #
    def __init__(self, command_name: str) -> None:
        #
        self.command_name: str = command_name

#
class Command_Elt(Command):

    #
    def __init__(self, command_name: str, elt: str) -> None:
        #
        super().__init__(command_name=command_name)
        #
        self.elt: str = elt

#
class Command_OElt(Command):

    #
    def __init__(self, command_name: str, elt: Optional[str] = None) -> None:
        #
        super().__init__(command_name=command_name)
        #
        self.elt: Optional[str] = elt

#
class Command_OKw_Elt(Command):

    #
    def __init__(self, command_name: str, elt: str, kw: Optional[str] = None) -> None:
        #
        super().__init__(command_name=command_name)
        #
        self.elt: str = elt
        self.kw: Optional[str] = kw

#
class Command_OKw_OElt(Command):

    #
    def __init__(self, command_name: str, elt: Optional[str] = None, kw: Optional[str] = None) -> None:
        #
        super().__init__(command_name=command_name)
        #
        self.elt: Optional[str] = elt
        self.kw: Optional[str] = kw

#
class Command_Elt_Kw_Elt(Command):

    #
    def __init__(self, command_name: str, elt1: str, elt2: str, kw: Optional[str] = None) -> None:
        #
        super().__init__(command_name=command_name)
        #
        self.elt1: str = elt1
        self.elt2: str = elt2
        self.kw: Optional[str] = kw

#
class Command_Elt_OKw_OElt(Command):

    #
    def __init__(self, command_name: str, elt1: str, elt2: Optional[str] = None, kw: Optional[str] = None) -> None:
        #
        super().__init__(command_name=command_name)
        #
        self.elt1: str = elt1
        self.elt2: Optional[str] = elt2
        self.kw: Optional[str] = kw

#
class Command_Elt_Kw_Elt_Kw_Elt(Command):

    #
    def __init__(
        self,
        command_name: str,
        elt1: str,
        elt2: str,
        elt3: str,
        kw1: Optional[str] = None,
        kw2: Optional[str] = None
    ) -> None:
        #
        super().__init__(command_name=command_name)
        #
        self.elt1: str = elt1
        self.elt2: str = elt2
        self.elt3: str = elt3
        self.kw1: Optional[str] = kw1
        self.kw2: Optional[str] = kw2

#
class Command_Elt_Kw_Elt_OKw_OElt(Command):

    #
    def __init__(
        self,
        command_name: str,
        elt1: str,
        elt2: str,
        elt3: Optional[str] = None,
        kw1: Optional[str] = None,
        kw2: Optional[str] = None
    ) -> None:
        #
        super().__init__(command_name=command_name)
        #
        self.elt1: str = elt1
        self.elt2: str = elt2
        self.elt3: Optional[str] = elt3
        self.kw1: Optional[str] = kw1
        self.kw2: Optional[str] = kw2

#
class Command_OElt_Kw_Elt_Kw_Elt(Command):

    #
    def __init__(
        self,
        command_name: str,
        elt2: str,
        elt3: str,
        elt1: Optional[str] = None,
        kw1: Optional[str] = None,
        kw2: Optional[str] = None
    ) -> None:
        #
        super().__init__(command_name=command_name)
        #
        self.elt2: str = elt2
        self.elt3: str = elt3
        self.elt1: Optional[str] = elt1
        self.kw1: Optional[str] = kw1
        self.kw2: Optional[str] = kw2

