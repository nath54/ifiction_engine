#
from typing import Optional
#
from dataclasses import dataclass

#
@dataclass
class Command:
    command_name: str

#
@dataclass
class Command_Elt(Command):
    elt: str

#
@dataclass
class Command_OElt(Command):
    elt: Optional[str] = None

#
@dataclass
class Command_OKw_Elt(Command):
    elt: str
    kw: Optional[str] = None

#
@dataclass
class Command_OKw_OElt(Command):
    elt: Optional[str] = None
    kw: Optional[str] = None

#
@dataclass
class Command_Elt_Kw_Elt(Command):
    elt1: str
    elt2: str
    kw: Optional[str] = None

#
@dataclass
class Command_Elt_OKw_OElt(Command):
    elt1: str
    elt2: Optional[str] = None
    kw: Optional[str] = None

#
@dataclass
class Command_Elt_Kw_Elt_Kw_Elt(Command):
    elt1: str
    elt2: str
    elt3: str
    kw1: Optional[str] = None
    kw2: Optional[str] = None

#
@dataclass
class Command_Elt_Kw_Elt_OKw_OElt(Command):
    elt1: str
    elt2: str
    elt3: Optional[str] = None
    kw1: Optional[str] = None
    kw2: Optional[str] = None

#
@dataclass
class Command_OElt_Kw_Elt_Kw_Elt(Command):
    elt2: str
    elt3: str
    elt1: Optional[str] = None
    kw1: Optional[str] = None
    kw2: Optional[str] = None

