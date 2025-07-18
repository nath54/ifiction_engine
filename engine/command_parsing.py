#
from typing import Optional, Callable, Any
from dataclasses import dataclass
#
from . import engine_classes_commands as ecc
#
import re


#
@dataclass
class CommandDefinition:
    #
    command_name: str
    keywords: list[str]
    command_type: Callable[..., Optional[ecc.Command]]
    kwargs: Optional[dict[str, Any]] = None


#
def traite_txt(txt: str) -> str:
    #
    txt = txt.strip().lower()
    #
    txt = txt.replace("-", " ")
    txt = txt.replace("'", "")
    #
    return txt


#
def test_COMMAND(command_input: str, command_def: CommandDefinition) -> Optional[ecc.Command]:
    #
    for kw in command_def.keywords:
        if traite_txt(kw) == command_input:
            return ecc.Command(
                command_name=command_def.command_name
            )
    #
    return None


#
def test_COMMAND_SOMETHING(command_input: str, command_def: CommandDefinition) -> Optional[ecc.Command_Elt]:
    #
    kw: str
    for kw in command_def.keywords:
        #
        tkw: str = traite_txt(kw)
        ltkw: int = len(tkw)
        #
        if command_input.startswith(tkw) and len(command_input) > ltkw:
            #
            return ecc.Command_Elt(
                command_name=command_def.command_name,
                elt=command_input[ltkw:].strip()
            )
    #
    return None


#
def test_COMMAND_OPT_SOMETHING(command_input: str, command_def: CommandDefinition) -> Optional[ecc.Command_OElt]:
    #
    kw: str
    for kw in command_def.keywords:
        #
        tkw: str = traite_txt(kw)
        ltkw: int = len(tkw)
        #
        if command_input.startswith(tkw):
            #
            elt: str = command_input[ltkw:].strip()
            #
            return ecc.Command_OElt(
                command_name=command_def.command_name,
                elt = elt if elt != "" else None
            )
    #
    return None


#
def test_COMMAND_OPT_KEYWORD_SOMETHING(command_input: str, command_def: CommandDefinition, keyword_opt: list[str] = ["to"]) -> Optional[ecc.Command_OKw_Elt]:
    #
    if isinstance(keyword_opt, str):
        keyword_opt = [keyword_opt]

    #
    keywords_a_pattern = "|".join(re.escape(keyword) for keyword in command_def.keywords)
    keywords_b_pattern = "|".join(re.escape(keyword) for keyword in keyword_opt)

    # Construct the main regex pattern with optional `{}` group
    pattern = rf"""
        ({keywords_a_pattern})                  # Keyword A
        (?:\s*({keywords_b_pattern}))           # Optional Keyword B
        (\s*(.*))                               # Text
    """

    # Match using regex with re.VERBOSE for readability
    match = re.match(pattern, command_input, re.VERBOSE)

    #
    if match:
        _keyword_a, keyword_b, text_b = match.groups()
        return ecc.Command_OKw_Elt(
            command_name=command_def.command_name,
            elt=text_b.strip() if text_b else '',
            kw=keyword_b
        )
    else:
        #
        res: Optional[ecc.Command_Elt] = test_COMMAND_SOMETHING(command_input, command_def)
        #
        if res is not None:
            return ecc.Command_OKw_Elt(
                command_name=res.command_name,
                elt=res.elt
            )
        #
        return None


#
def test_COMMAND_OPT_KEYWORD_OPT_SOMETHING(command_input: str, command_def: CommandDefinition, keyword_opt: list[str] = ["to"]) -> Optional[ecc.Command_OKw_OElt]:
    #
    if isinstance(keyword_opt, str):
        keyword_opt = [keyword_opt]

    #
    keywords_a_pattern = "|".join(re.escape(keyword) for keyword in command_def.keywords)
    keywords_b_pattern = "|".join(re.escape(keyword) for keyword in keyword_opt)

    # Construct the main regex pattern with optional `{}` group
    pattern = rf"""
        ({keywords_a_pattern})                  # Keyword A
        (?:\s*({keywords_b_pattern}))           # Optional Keyword B
        (\s*(.*))                               # Text
    """

    # Match using regex with re.VERBOSE for readability
    match = re.match(pattern, command_input, re.VERBOSE)

    #
    if match:
        _keyword_a, keyword_b, _, text_b = match.groups()
        return ecc.Command_OKw_OElt(
            command_name=command_def.command_name,
            elt=text_b.strip() if text_b else '',
            kw=keyword_b
        )
    else:
        #
        res: Optional[ecc.Command_Elt] = test_COMMAND_SOMETHING(command_input, command_def)
        #
        if res is not None:
            return ecc.Command_OKw_OElt(
                command_name=res.command_name,
                elt=res.elt
            )
        #
        else:
            #
            res2: Optional[ecc.Command] = test_COMMAND(command_input, command_def)
            #
            if res2 is not None:
                return ecc.Command_OKw_OElt(
                    command_name=res2.command_name
                )
            #
            return None


#
def test_COMMAND_SOMETHING_KEYWORD_SOMETHING(command_input: str, command_def: CommandDefinition, keyword_connection: str | list[str]) -> Optional[ecc.Command_Elt_Kw_Elt]:
    #
    if isinstance(keyword_connection, str):
        keyword_connection = [keyword_connection]

    # Create regex patterns for the keywords (using the | operator for "or")
    keywords_a_pattern = "|".join(re.escape(keyword) for keyword in command_def.keywords)  # Escape keywords for safety
    keywords_b_pattern = "|".join(re.escape(keyword) for keyword in keyword_connection)

    # Construct the main regex pattern
    pattern = rf"({keywords_a_pattern})\s+(.*?)\s+({keywords_b_pattern})\s+(.*)"  # r"" for raw string, f"" for f-string

    #
    match = re.match(pattern, command_input)

    #
    if match:
        _keyword_a, text_a, keyword_b, text_b = match.groups()
        #
        return ecc.Command_Elt_Kw_Elt(
            command_name=command_def.command_name,
            elt1=text_a.strip(),
            elt2=text_b.strip(),
            kw=keyword_b
        )
    #
    return None


#
def test_COMMAND_SOMETHING_KEYWORD_SOMETHING_KEYWORD_SOMETHING(command_input: str, command_def: CommandDefinition, keyword_B: str | list[str], keyword_C: str | list[str]) -> Optional[ecc.Command_Elt_Kw_Elt_Kw_Elt]:
    #
    if isinstance(keyword_B, str):
        keyword_B = [keyword_B]
    #
    if isinstance(keyword_C, str):
        keyword_C = [keyword_C]

    #
    keywords_a_pattern = "|".join(re.escape(keyword) for keyword in command_def.keywords)
    keywords_b_pattern = "|".join(re.escape(keyword) for keyword in keyword_B)
    keywords_c_pattern = "|".join(re.escape(keyword) for keyword in keyword_C)

    # The ? after the group makes it optional.  We use non-capturing groups
    # for the parts we don't need to extract (the ? and space).
    pattern = rf"({keywords_a_pattern})\s+(.*)\s+({keywords_b_pattern})\s+(.*)(\s+({keywords_c_pattern})\s+(.*))"

    #
    match = re.match(pattern, command_input)

    #
    if match:
        #
        _keyword_a, text_a, keyword_b, text_b, _, keyword_c, text_c = match.groups()
        #
        return ecc.Command_Elt_Kw_Elt_Kw_Elt(
            command_name=command_def.command_name,
            elt1=text_a,
            elt2=text_b,
            elt3=text_c,
            kw1=keyword_b,
            kw2=keyword_c
        )
    else:
        return None


#
def test_COMMAND_SOMETHING_KEYWORD_SOMETHING_OPT_KEYWORD_SOMETHING(command_input: str, command_def: CommandDefinition, keyword_B: str | list[str], keyword_C: str | list[str]) -> Optional[ecc.Command_Elt_Kw_Elt_OKw_OElt]:
    #
    res: Optional[ecc.Command_Elt_Kw_Elt_Kw_Elt] = test_COMMAND_SOMETHING_KEYWORD_SOMETHING_KEYWORD_SOMETHING(command_input, command_def, keyword_B, keyword_C)
    #
    if res is not None:
        return ecc.Command_Elt_Kw_Elt_OKw_OElt(
            command_name=res.command_name,
            elt1=res.elt1,
            elt2=res.elt2,
            elt3=res.elt3,
            kw1=res.kw1,
            kw2=res.kw2
        )
    #
    res2: Optional[ecc.Command_Elt_Kw_Elt] = test_COMMAND_SOMETHING_KEYWORD_SOMETHING(command_input, command_def, keyword_B)
    #
    if res2 is not None:
        return ecc.Command_Elt_Kw_Elt_OKw_OElt(
            command_name=res2.command_name,
            elt1=res2.elt1,
            elt2=res2.elt2,
            kw1=res2.kw
        )
    #
    return None


#
def test_COMMAND_SOMETHING_OPT_KEYWORD_SOMETHING(command_input: str, command_def: CommandDefinition, keyword_opt: str | list[str]) -> Optional[ecc.Command_Elt_OKw_OElt]:
    #
    if isinstance(keyword_opt, str):
        keyword_opt = [keyword_opt]

    #
    keywords_a_pattern = "|".join(re.escape(keyword) for keyword in command_def.keywords)
    keywords_b_pattern = "|".join(re.escape(keyword) for keyword in keyword_opt)

    # Construct the main regex pattern with optional `{}` group
    pattern = rf"""
        ({keywords_a_pattern})                # Keyword A
        \s+(.+?)                              # Capture main text
        (?:\s*({keywords_b_pattern})\s*(.*)) # Optional Keyword B and text
    """

    # Match using regex with re.VERBOSE for readability
    match = re.match(pattern, command_input, re.VERBOSE)

    #
    if match:
        _keyword_a, text_a, keyword_b, text_b = match.groups()
        #
        return ecc.Command_Elt_OKw_OElt(
            command_name=command_def.command_name,
            elt1=text_a.strip(),
            elt2=text_b.strip(),
            kw=keyword_b
        )
    else:
        #
        res: Optional[ecc.Command_Elt] = test_COMMAND_SOMETHING(command_input, command_def)
        #
        if res is not None:
            #
            return ecc.Command_Elt_OKw_OElt(
                command_name=command_def.command_name,
                elt1=res.elt
            )
        #
        return None


#
def test_COMMAND_OPT_SOMETHING_KEYWORD_SOMETHING_KEYWORD_SOMETHING(command_input: str, command_def: CommandDefinition, keyword_B: str | list[str], keyword_C: str | list[str]) -> Optional[ecc.Command_Elt_Kw_Elt_Kw_Elt]:
    #
    if isinstance(keyword_B, str):
        keyword_B = [keyword_B]
    #
    if isinstance(keyword_C, str):
        keyword_C = [keyword_C]

    #
    keywords_a_pattern = "|".join(re.escape(keyword) for keyword in command_def.keywords)
    keywords_b_pattern = "|".join(re.escape(keyword) for keyword in keyword_B)
    keywords_c_pattern = "|".join(re.escape(keyword) for keyword in keyword_C)

    # Construct the main regex pattern with optional `{}` group
    pattern = rf"""
        ({keywords_a_pattern})                 # Keyword A (buy/purchase)
        \s+(?:                                 # Start optional "quantity of" group
            (\d+)                              # Capture quantity (optional)
            \s+({keywords_b_pattern})\s+       # Literal 'of' (optional)
        )?                                     # End optional group
        (\S.+?)                                # Capture main item
        \s+({keywords_c_pattern})              # Keyword C (to/at)
        \s+(.+)                                # Capture target (merchant, etc.)
    """

    # Match using regex with re.VERBOSE for readability
    match = re.match(pattern, command_input, re.VERBOSE)

    #
    if match:
        _keyword_a, quantity, keyword_b, item, keyword_c, target = match.groups()
        quantity = quantity if quantity else "1"  # Default to 1 if not specified
        #
        return ecc.Command_Elt_Kw_Elt_Kw_Elt(
            command_name=command_def.command_name,
            elt1=quantity,
            elt2=item,
            elt3=target,
            kw1=keyword_b,
            kw2=keyword_c
        )
    else:
        return None



#
commands: list[CommandDefinition] = [

    ##################################
    ###### OBSERVATION COMMANDS ######
    ##################################

    #### COMMAND LOOK AROUND
    # `(see/look around/look)`: Observe the surroundings and get a description of the current area.

    CommandDefinition(
        command_name="C_LOOKAROUND",
        keywords = ["see", "look around", "look"],
        command_type = test_COMMAND
    ),

    #### COMMAND RECAP
    # `(recap)`: Summarize recent events, clues, or interactions.

    CommandDefinition(
        command_name="C_RECAP",
        keywords = ["recap", "history"],
        command_type=test_COMMAND
    ),

    #### COMMAND BRIEF
    #  `brief [something/someone]`: Give a short description of something or someone. (ex: `brief ancient statue`)

    CommandDefinition(
        command_name="C_BRIEF",
        keywords = ["brief"],
        command_type=test_COMMAND_SOMETHING
    ),

    #### COMMAND DESCRIBE
    # `(watch/describe) [something/someone]`: Give a detailed description of an object or character. (ex: `describe mysterious painting`)

    CommandDefinition(
        command_name="C_DESCRIBE",
        keywords = ["describe", "watch"],
        command_type=test_COMMAND_SOMETHING
    ),

    #### COMMAND EXAMINE
    # `(examine/inspect/check) [something/someone]`: Closely inspect something or someone to reveal details. (ex: `examine old diary`)

    CommandDefinition(
        command_name="C_EXAMINE",
        keywords = ["examine", "inspect", "check"],
        command_type=test_COMMAND_SOMETHING
    ),

    #### COMMAND RUMMAGE
    # `(rummage/search) [something]`: Search a container or place for hidden items. (ex: `rummage drawer`)

    CommandDefinition(
        command_name="C_RUMMAGE",
        keywords = ["rummage", "search", "dig in"],
        command_type=test_COMMAND_SOMETHING
    ),

    #### COMMAND READ
    # `read [something] ?{page [number]}`: Read a written document, optionally specifying a page. (ex: `read journal page 2`)

    CommandDefinition(
        command_name="C_READ",
        keywords = ["read"],
        command_type=test_COMMAND_SOMETHING_OPT_KEYWORD_SOMETHING,
        kwargs={"keyword_opt": ["page"]}
    ),

    ###################################
    ###### DISPLACEMENT COMMANDS ######
    ###################################

    #### COMMAND GO
    # `(go/displace/walk/run/sprint) [direction]`: Move in the specified direction. (ex: `go north`)

    CommandDefinition(
        command_name="C_GO",
        keywords = ["go", "displace", "walk", "run", "sprint"],
        command_type=test_COMMAND_SOMETHING
    ),

    ##########################################
    ###### OBJECT INTERACTIONS COMMANDS ######
    ##########################################

    #### COMMAND PUT
    # `(put/move) [something] (on/into/in) [somewhere/something]`: Place an object somewhere. (ex: `put book on shelf`)

    CommandDefinition(
        command_name="C_PUT",
        keywords = ["put", "move"],
        command_type=test_COMMAND_SOMETHING_KEYWORD_SOMETHING,
        kwargs={
            "keyword_connection": ["on", "into", "in"]
        }
    ),

    #### COMMAND ATTACH
    # `(attach/tie) [something/someone] to [something/someone] ?{with [something]}`: Attach an object to something. (ex: `attach bandit to chair with rope`)

    CommandDefinition(
        command_name="C_ATTACH",
        keywords = ["attach", "tie"],
        command_type=test_COMMAND_SOMETHING_KEYWORD_SOMETHING_OPT_KEYWORD_SOMETHING,
        kwargs={
            "keyword_B": ["to"],
            "keyword_C": ["with"]
        }
    ),

    #### COMMAND THROW
    # `throw [something] on [something]`: Throw an object at another object. (ex: `throw rock on window`)
    # `throw [something] on [someone]`: Throw an object at someone. (ex: `throw rock on bandit`)

    CommandDefinition(
        command_name="C_THROW",
        keywords = ["throw"],
        command_type=test_COMMAND_SOMETHING_KEYWORD_SOMETHING,
        kwargs={
            "keyword_connection": ["on", "to", "into", "in"]
        }
    ),

    #### COMMAND DROP
    # `(drop/discard/get off) [something]`: Remove an object from inventory. (ex: `drop bag`)

    CommandDefinition(
        command_name="C_DROP",
        keywords = ["drop", "discard"],
        command_type=test_COMMAND_SOMETHING
    ),

    #### COMMAND USE
    # `use [something] ?{on [something/someone]}`: Use an object, optionally on something or someone. (ex: `use key on door`)

    CommandDefinition(
        command_name="C_USE",
        keywords = ["use", "utilise"],
        command_type=test_COMMAND_SOMETHING_OPT_KEYWORD_SOMETHING,
        kwargs={
            "keyword_opt": ["on", "onto"]
        }
    ),

    #### COMMAND CLIMB
    # `climb [something]`: Climb an object. (ex: `climb tree`)

    CommandDefinition(
        command_name="C_CLIMB",
        keywords = ["climb"],
        command_type=test_COMMAND_SOMETHING
    ),

    #### COMMAND OPEN
    # `open [something]`: Open a door, chest, or other container. (ex: `open chest`)

    CommandDefinition(
        command_name="C_OPEN",
        keywords = ["open"],
        command_type=test_COMMAND_SOMETHING
    ),

    #### COMMAND CLOSE
    # `(close/shut) [something]`: Close an object. (ex: `close window`)

    CommandDefinition(
        command_name="C_CLOSE",
        keywords = ["close", "shut"],
        command_type=test_COMMAND_SOMETHING
    ),

    #### COMMAND LOCK
    # `lock [something] ?{with [something]}`: Lock an object. (ex: `lock door with golden key`)

    CommandDefinition(
        command_name="C_LOCK",
        keywords = ["lock"],
        command_type=test_COMMAND_SOMETHING_OPT_KEYWORD_SOMETHING,
        kwargs={
            "keyword_opt": ["with"]
        }
    ),

    #### COMMAND UNLOCK
    # `unlock [something] ?{with [something]}`: Unlock an object. (ex: `unlock chest with rusty key`)

    CommandDefinition(
        command_name="C_UNLOCK",
        keywords = ["unlock"],
        command_type=test_COMMAND_SOMETHING_OPT_KEYWORD_SOMETHING,
        kwargs={
            "keyword_opt": ["with"]
        }
    ),

    #### COMMAND INSERT
    # `insert [something] into [something]`: Insert an item. (ex: `insert coin into vending machine`)

    CommandDefinition(
        command_name="C_INSERT",
        keywords = ["insert"],
        command_type=test_COMMAND_SOMETHING_KEYWORD_SOMETHING,
        kwargs={
            "keyword_connection": ["into", "in"]
        }
    ),

    #### COMMAND REMOVE
    # `remove [something] from [something]`: Take something out of another object. (ex: `remove book from shelf`)

    CommandDefinition(
        command_name="C_REMOVE",
        keywords = ["remove"],
        command_type=test_COMMAND_SOMETHING_KEYWORD_SOMETHING,
        kwargs={
            "keyword_connection": ["from"]
        }
    ),

    #### COMMAND SET
    # `set [something] to [state]`: Adjust an object’s state. (ex: `set lamp to on`)

    CommandDefinition(
        command_name="C_SET",
        keywords = ["set"],
        command_type=test_COMMAND_SOMETHING_KEYWORD_SOMETHING,
        kwargs={
            "keyword_connection": ["to"]
        }
    ),

    ##############################################
    ###### CONSUMABLE INTERACTIONS COMMANDS ######
    ##############################################

    #### COMMAND EAT
    # `(consume/eat) [something]`: Eat an item. (ex: `eat apple`)

    CommandDefinition(
        command_name="C_EAT",
        keywords = ["eat", "consume"],
        command_type=test_COMMAND_SOMETHING
    ),

    #### COMMAND DRINK
    # `(drink/sip/swallow) [something]`: Drink a liquid. (ex: `drink potion`)

    CommandDefinition(
        command_name="C_DRINK",
        keywords = ["drink", "swallow", "sip"],
        command_type=test_COMMAND_SOMETHING
    ),

    ##########################################
    ###### LIVING INTERACTIONS COMMANDS ######
    ##########################################

    #### COMMAND AWAKE
    # `(awake/wake/wake up) [someone]`: Wake a sleeping person. (ex: `wake up guard`)

    CommandDefinition(
        command_name="C_AWAKE",
        keywords = ["awake", "wake up", "wake"],
        command_type=test_COMMAND_SOMETHING
    ),

    #### COMMAND ATTACK
    # `(attack/smash/fight/hit/hurt/kill/murder/punch/slice/thump/torture/wreck) [someone] ?{with [something]}`: Attack someone. (ex: `attack bandit with sword`)

    CommandDefinition(
        command_name="C_ATTACK",
        keywords = ["attack", "smash", "fight", "hit", "hurt", "kill", "murder", "punch", "slice"],
        command_type=test_COMMAND_SOMETHING_OPT_KEYWORD_SOMETHING,
        kwargs={
            "keyword_opt": ["with"]
        }
    ),

    #### COMMAND BUY
    # `(buy/purchase) ?{[quantity] of} [something] to [someone]`: Buy an item. (ex: `buy 2 potions to merchant`)

    CommandDefinition(
        command_name="C_BUY",
        keywords = ["buy", "purchase"],
        command_type=test_COMMAND_OPT_SOMETHING_KEYWORD_SOMETHING_KEYWORD_SOMETHING,
        kwargs={
            "keyword_B": ["of"],
            "keyword_C": ["to", "at"]
        }
    ),

    #### COMMAND SHOW
    # `(show/display/present) [something/someone] to [someone]`: Show something to someone. (ex: `show passport to guard`)

    CommandDefinition(
        command_name="C_SHOW",
        keywords = ["show", "display", "present"],
        command_type=test_COMMAND_SOMETHING_KEYWORD_SOMETHING,
        kwargs={
            "keyword_connection": ["to"]
        }
    ),

    #### COMMAND EMBRACE
    # `(embrace/hug/kiss) [someone]`: Perform an affectionate gesture. (ex: `hug friend`)

    CommandDefinition(
        command_name="C_EMBRACE",
        keywords = ["embrace", "kiss", "hug"],
        command_type=test_COMMAND_SOMETHING
    ),

    #### COMMAND FEED
    # `(feed) [someone] with [something]`: Give food to someone. (ex: `feed dog with bone`)

    CommandDefinition(
        command_name="C_FEED",
        keywords = ["feed"],
        command_type=test_COMMAND_SOMETHING_KEYWORD_SOMETHING,
        kwargs={
            "keyword_connection": ["with"]
        }
    ),

    #### COMMAND GIVE
    # `(give/offer) [something] to [someone]`: Alternative phrasing. (ex: `offer flower to lover`)

    CommandDefinition(
        command_name="C_GIVE",
        keywords = ["give", "offer"],
        command_type=test_COMMAND_SOMETHING_KEYWORD_SOMETHING,
        kwargs={
            "keyword_connection": ["to"]
        }
    ),

    ###################################
    ###### VOICE / TEXT COMMANDS ######
    ###################################

    #### COMMAND SAY
    # `(say/tell/answer/shout) "..." to [someone/something]`: Communicate verbally with a character or object. (ex: `say "Hello" to guard`)

    CommandDefinition(
        command_name="C_SAY",
        keywords = ["say", "tell", "answer", "shout"],
        command_type=test_COMMAND_SOMETHING_OPT_KEYWORD_SOMETHING,
        kwargs={
            "keyword_opt": ["to"]
        }
    ),

    #### COMMAND ASK
    # `ask [someone] (about/for/on) [something/someone]`: Ask someone for information. (ex: `ask merchant about potion`)

    CommandDefinition(
        command_name="C_ASK",
        keywords = ["ask"],
        command_type=test_COMMAND_SOMETHING_KEYWORD_SOMETHING,
        kwargs={
            "keyword_connection": ["about", "on", "for"]
        }
    ),

    #### COMMAND WRITE
    # `(write) "..." on [something] ?{with [something]}`: Write a message on an object. (ex: `write "Hello" on the old paper with pencil`) ***Note:** if there is already a writen thing on the object, and you want only the text you want to write, you can try to erase the previous text on the object.*

    CommandDefinition(
        command_name="C_WRITE",
        keywords = ["write"],
        command_type=test_COMMAND_SOMETHING_KEYWORD_SOMETHING_OPT_KEYWORD_SOMETHING,
        kwargs={
            "keyword_B": ["on"],
            "keyword_C": ["with"]
        }
    ),

    #### COMMAND ERASE
    # `(erase/efface/delete/rub out) [something] ?{with [something]}`: Erase everything that is writen on an object. (Ex: `rub out the paper with gum` or `erase the blackboard with the brush`)

    CommandDefinition(
        command_name="C_ERASE",
        keywords = ["erase", "efface", "rub out", "delete"],
        command_type=test_COMMAND_SOMETHING_OPT_KEYWORD_SOMETHING,
        kwargs={
            "keyword_opt": ["with"]
        }
    ),

    #########################################
    ###### PLAYER INTERACTION COMMANDS ######
    #########################################

    #### COMMAND WEAR
    # `(wear/dress) [something]`: Wear clothing or equipment. (ex: `wear helmet`)

    CommandDefinition(
        command_name="C_WEAR",
        keywords = ["wear", "dress"],
        command_type=test_COMMAND_SOMETHING
    ),

    #### COMMAND UNDRESS
    # `(undress/take off/strip/pull off/shed) [something]`: Take off clothing or equipment. (ex: `remove jacket`)

    CommandDefinition(
        command_name="C_UNDRESS",
        keywords = ["undress", "take off", "strip", "pull off", "shed"],
        command_type=test_COMMAND_SOMETHING
    ),

    #### COMMAND INVENTORY
    # `(inventory)`: List the objects in your inventory. (ex: `inv`)

    CommandDefinition(
        command_name="C_INVENTORY",
        keywords = ["inventory", "stock", "what's in my bag"],
        command_type=test_COMMAND
    ),

    #### COMMAND WAIT
    # `wait ?{[duration]}`: Pause and let time pass. (ex: `wait 5 minutes`)

    CommandDefinition(
        command_name="C_WAIT",
        keywords = ["wait"],
        command_type=test_COMMAND_OPT_SOMETHING
    ),

    #### COMMAND SLEEP
    # `(sleep/nap)`: Rest and possibly recover. (ex: `sleep`)

    CommandDefinition(
        command_name="C_SLEEP",
        keywords = ["sleep", "nap"],
        command_type=test_COMMAND
    ),

    #### COMMAND SIT
    # `sit on [something]`: Take a seat on an object. (ex: `sit on chair`)

    CommandDefinition(
        command_name="C_SIT_DOWN",
        keywords = ["sit down", "sit on", "sit"],
        command_type=test_COMMAND_SOMETHING
    ),

    #### COMMAND LIE DOWN
    # `(lie on/lie down on) ?{[something]}`: Lie down on an object. (ex: `lie down on the bed`)

    CommandDefinition(
        command_name="C_LIE_DOWN",
        keywords = ["lie down on", "lie on"],
        command_type=test_COMMAND_OPT_SOMETHING
    ),

    #### COMMAND STAND UP
    # `(stand/stand up)`: Return to a standing position. (ex: `stand up`)

    CommandDefinition(
        command_name="C_STAND_UP",
        keywords = ["stand up", "stand"],
        command_type=test_COMMAND
    ),

    ############################################
    ###### OBJECT INTERACTIONS COMMANDS 2 ######
    ############################################

    #### COMMAND TAKE
    # `(take/carry/hold/pick/pick up) [something]`: Pick up an object and add it to the inventory. (ex: `take golden key`)

    CommandDefinition(
        command_name="C_TAKE",
        keywords = ["take", "carry", "hold", "pick up", "pick"],
        command_type=test_COMMAND_SOMETHING
    ),

    #############################
    ###### SYSTEM COMMANDS ######
    #############################

    #### COMMAND QUIT
    # `(quit)`: Quit the game. (ex: `quit`)

    CommandDefinition(
        command_name="C_QUIT",
        keywords = ["quit", "exit"],
        command_type=test_COMMAND
    ),

    #### COMMAND SAVE
    # `save ?{filepath of game save}`: Save the game. (ex: `save game1.sav`)

    CommandDefinition(
        command_name="C_SAVE",
        keywords = ["save"],
        command_type=test_COMMAND_OPT_SOMETHING
    ),

    #### COMMAND LOAD
    # `(load/restore) {filepath of game save}`: Load a saved game. (ex: `load game1.sav`)

    CommandDefinition(
        command_name="C_LOAD",
        keywords = ["load", "restore"],
        command_type=test_COMMAND_OPT_SOMETHING
    ),

    #### COMMAND SCORE
    # `score`: Show current progress. (ex: `score`)

    CommandDefinition(
        command_name="C_SCORE",
        keywords = ["score"],
        command_type=test_COMMAND
    ),

    #### COMMAND HELP
    # `help ?{something}`: Show the list of commands. (ex: `help`)

    CommandDefinition(
        command_name="C_HELP",
        keywords = ["help"],
        command_type = test_COMMAND_OPT_SOMETHING
    )
]


#
def parse_command(command_input: str, generic_kws: dict[str, str]) -> Optional[ecc.Command]:

    #
    command_input = traite_txt(command_input)
    res: Optional[ecc.Command] = None

    #
    command_def: CommandDefinition
    for command_def in commands:
        #
        kwargs: dict[str, Any] = {
            "command_input": command_input,
            "command_def": command_def
        }
        #
        if command_def.kwargs is not None:
            k: str
            for k in command_def.kwargs:
                kwargs[k] = command_def.kwargs[k]
        #
        res = command_def.command_type(**kwargs)
        #
        if res is not None:
            return res


    #
    ### DONE: check for generic `ACTION_TYPE thing_id_argument (KEYWORDS arguments)*`, arguments can be single words or multi words with spaces, but to allow multi words with space AND allows words of them to be keywords arguments like `old paper with moisture`, arguments must have quotes "" around them, like with bash terminal commands. The allowed keywords are inside the `generic_kws` dictionnary. ###
    #
    ### Parse generic ACTION_TYPE thing_id_argument (KEYWORDS arguments)* ###
    #
    #
    thing_id: Optional[str] = None
    action_type: str = ""
    additionnal_keywords_arguments: list[tuple[str, str]] = []
    generic_action_parsed: bool = False

    #
    ### Parse generic ACTION_TYPE thing_id_argument (KEYWORDS arguments)* ###
    #

    #
    ### Split command into tokens, handling quoted strings. ###
    #
    tokens: list[str] = []
    current_token: str = ""
    in_quotes: bool = False
    i: int = 0

    #
    while i < len(command_input):
        #
        char = command_input[i]

        #
        if char == '"' and not in_quotes:
            #
            in_quotes = True

        #
        elif char == '"' and in_quotes:
            #
            in_quotes = False
            #
            if current_token:
                #
                tokens.append(current_token)
                current_token = ""

        #
        elif char == ' ' and not in_quotes:
            #
            if current_token:
                #
                tokens.append(current_token)
                current_token = ""

        #
        else:
            #
            current_token += char

        #
        i += 1

    #
    ### Add the last token if exists. ###
    #
    if current_token:
        #
        tokens.append(current_token)

    #
    ### Need at least 1 token: action_type. ###
    #
    if len(tokens) >= 1:
        #
        potential_action_type = tokens[0]

        #
        ### Parse thing_id (collect tokens until first keyword or end). ###
        #
        thing_id_tokens: list[str] = []
        remaining_tokens: list[str] = tokens[1:]

        #
        i = 0
        #
        while i < len(remaining_tokens):
            #
            if remaining_tokens[i] in generic_kws:
                #
                break

            #
            thing_id_tokens.append(remaining_tokens[i])
            i += 1

        #
        ### thing_id is the joined tokens or empty string if no tokens. ###
        #
        potential_thing_id = " ".join(thing_id_tokens) if thing_id_tokens else ""

        #
        ### Parse keyword arguments from remaining tokens. ###
        #
        parsed_kwargs: list[tuple[str, str]] = []
        #
        ### Skip the thing_id tokens. ###
        #
        remaining_tokens = remaining_tokens[i:]

        #
        i = 0
        #
        while i < len(remaining_tokens):

            #
            token = remaining_tokens[i]

            #
            ### Check if current token is a valid keyword. ###
            #
            if token in generic_kws:
                #
                ### Collect all tokens until next keyword or end. ###
                #
                value_tokens: list[str] = []

                #
                ### Skip the keyword itself. ###
                #
                i += 1

                #
                while i < len(remaining_tokens) and remaining_tokens[i] not in generic_kws:
                    value_tokens.append(remaining_tokens[i])
                    i += 1

                #
                ### Join the value tokens. ###
                #
                keyword_value = " ".join(value_tokens) if value_tokens else ""
                parsed_kwargs.append( (token, keyword_value) )
            else:
                #
                ### Not a keyword, skip it (shouldn't happen in well-formed input). ###
                #
                i += 1

        #
        ### Set the parsed values. ###
        #
        action_type = potential_action_type
        thing_id = potential_thing_id
        additionnal_keywords_arguments = parsed_kwargs
        generic_action_parsed = True

    #
    if generic_action_parsed and thing_id is not None:
        #
        return ecc.Command_GenericAction(
            action_type=action_type,
            thing_id=thing_id,
            kws=additionnal_keywords_arguments
        )

    #
    ### Commande vide. ###
    #
    return None
