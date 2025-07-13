#
from typing import Optional

#
class Command:

    #
    def __init__(self, command_name: str) -> None:
        #
        self.command_name: str = command_name

    #
    def __str__(self) -> str:
        #
        return f"Command(command_name=`{self.command_name}`)"

#
class Command_GenericAction(Command):

    #
    def __init__(self, action_type: str, thing_id: str = "", kws: list[tuple[str, str]] = []) -> None:

        #
        super().__init__(command_name="generic_action")

        #
        self.action_type: str = action_type
        #
        self.thing_id: str = thing_id
        #
        self.entity_id: str = "id_of_current_player"
        #
        self.kws: list[tuple[str, str]] = kws

    #
    def __str__(self) -> str:
        #
        return f"Command_GenericAction(action_type=`{self.action_type}`, thing_id=`{self.thing_id}`, entity_id=`{self.entity_id}`, kws={self.kws})"

#
class Command_Elt(Command):

    #
    def __init__(self, command_name: str, elt: str) -> None:
        #
        super().__init__(command_name=command_name)
        #
        self.elt: str = elt

    #
    def __str__(self) -> str:
        #
        return f"Command_Elt(command_name=`{self.command_name}`, elt=`{self.elt}`)"

#
class Command_OElt(Command):

    #
    def __init__(self, command_name: str, elt: Optional[str] = None) -> None:
        #
        super().__init__(command_name=command_name)
        #
        self.elt: Optional[str] = elt

    #
    def __str__(self) -> str:
        #
        return f"Command_OElt(command_name=`{self.command_name}`, elt=`{self.elt}`)"

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
    def __str__(self) -> str:
        #
        return f"Command_OKw_Elt(command_name=`{self.command_name}`, kw={self.kw}, elt=`{self.elt}`)"

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
    def __str__(self) -> str:
        #
        return f"Command_OKw_OElt(command_name=`{self.command_name}`, kw={self.kw}, elt=`{self.elt}`)"

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
    def __str__(self) -> str:
        #
        return f"Command_Elt_Kw_Elt(command_name=`{self.command_name}`, elt1=`{self.elt1}`, kw={self.kw}, elt2=`{self.elt2}`)"

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
    def __str__(self) -> str:
        #
        return f"Command_Elt_OKw_OElt(command_name=`{self.command_name}`, elt1=`{self.elt1}`, kw={self.kw}, elt2=`{self.elt2}`)"

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
    def __str__(self) -> str:
        #
        return f"Command_Elt_Kw_Elt_Kw_Elt(command_name=`{self.command_name}`, elt1=`{self.elt1}`, kw1={self.kw1}, elt2=`{self.elt2}`, kw2=`{self.kw2}`, elt3=`{self.elt3}`)"

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
    def __str__(self) -> str:
        #
        return f"Command_Elt_Kw_Elt_OKw_OElt(command_name=`{self.command_name}`, elt1=`{self.elt1}`, kw1={self.kw1}, elt2=`{self.elt2}`, kw2=`{self.kw2}`, elt3=`{self.elt3}`)"

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

    #
    def __str__(self) -> str:
        #
        return f"Command_OElt_Kw_Elt_Kw_Elt(command_name=`{self.command_name}`, elt1=`{self.elt1}`, kw1={self.kw1}, elt2=`{self.elt2}`, kw2=`{self.kw2}`, elt3=`{self.elt3}`)"

