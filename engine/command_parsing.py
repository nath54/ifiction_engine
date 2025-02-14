#
from typing import Optional
#
from . import engine_classes_commands as ecc
#
import sys
import re
import os

#
commands_keywords: dict[str, list[str]] = {
    "C_LOOKAROUND": ["see", "look around", "look"],
    "C_RECAP": ["recap"],
    "C_BRIEF": ["brief"],
    "C_DESCRIBE": ["describe", "watch"],
    "C_EXAMINE": ["examine", "inspect", "check"],
    "C_RUMMAGE": ["rummage", "search", "dig in"],
    "C_LISTEN": ["hear", "listen"],
    "C_TOUCH": ["touch", "feel"],
    "C_READ": ["read"],
    "C_TASTE": ["taste"],
    "C_SMELL": ["smell", "sniff"],
    "C_GO": ["go", "displace", "walk", "run", "sprint"],
    "C_TAKE": ["take", "carry", "hold", "pick up", "pick"],
    "C_PUT": ["put", "move"],
    "C_PUSH": ["push", "press", "apply force on"],
    "C_PULL": ["pull"],
    "C_ATTACH": ["attach", "tie"],
    "C_BREAK": ["break", "destroy"],
    "C_THROW": ["throw"],
    "C_DROP": ["drop", "discard"],
    "C_CLEAN": ["clean", "scrub", "sweep", "polish", "shine", "wash", "wipe"],
    "C_USE": ["use"],
    "C_CLIMB": ["climb"],
    "C_OPEN": ["open"],
    "C_CLOSE": ["close", "shut"],
    "C_LOCK": ["lock"],
    "C_UNLOCK": ["unlock"],
    "C_FILL": ["fill"],
    "C_POUR": ["pour"],
    "C_INSERT": ["insert"],
    "C_REMOVE": ["remove"],
    "C_SET": ["set"],
    "C_SPREAD": ["spread"],
    "C_SQUEEZE": ["squeeze", "squash"],
    "C_EAT": ["eat", "consume"],
    "C_DRINK": ["drink", "swallow", "sip"],
    "C_AWAKE": ["awake", "wake up", "wake"],
    "C_ATTACK": ["attack", "smash", "fight", "hit", "hurt", "kill", "murder", "punch", "slice"],
    "C_BUY": ["buy", "purchase"],
    "C_SHOW": ["show", "display", "present"],
    "C_EMBRACE": ["embrace", "kiss", "hug"],
    "C_FEED": ["feed"],
    "C_GIVE": ["give", "offer"],
    "C_SAY": ["say", "tell", "answer", "shout"],
    "C_ASK": ["ask"],
    "C_WRITE": ["write"],
    "C_ERASE": ["erase", "efface", "rub out", "delete"],
    "C_WEAR": ["wear", "dress"],
    "C_UNDRESS": ["undress", "take off", "strip", "pull off", "shed"],
    "C_INVENTORY": ["inventory", "stock", "what's in my bag"],
    "C_WAIT": ["wait"],
    "C_SLEEP": ["sleep", "nap"],
    "C_SIT_DOWN": ["sit down", "sit on", "sit"],
    "C_LIE_DOWN": ["lie down on", "lie on"],
    "C_STAND_UP": ["stand up", "stand"],
    "C_DANCE": ["dance"],
    "C_SING": ["sing", "chant"],
    "C_JUMP": ["jump", "hop"],
    "C_THINK": ["think"],
    "C_SAVE": ["save"],
    "C_QUIT": ["quit", "exit"],
    "C_LOAD": ["load", "restore"],
    "C_RESTART": ["restart"],
    "C_SCORE": ["score"],
    "C_HELP": ["help"]
}

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
def test_COMMAND(command_input: str, command_name: str) -> Optional[ecc.Command]:
    #
    for kw in commands_keywords[command_name]:
        if traite_txt(kw) == command_input:
            return ecc.Command(
                command_name=command_name
            )
    #
    return None

#
def test_COMMAND_SOMETHING(command_input: str, command_name: str) -> Optional[ecc.Command_Elt]:
    #
    kw: str
    for kw in commands_keywords[command_name]:
        #
        tkw: str = traite_txt(kw)
        ltkw: int = len(tkw)
        #
        if command_input.startswith(tkw) and len(command_input) > ltkw:
            #
            return ecc.Command_Elt(
                command_name=command_name,
                elt=command_input[ltkw:].strip()
            )
    #
    return None

#
def test_COMMAND_OPT_SOMETHING(command_input: str, command_name: str) -> Optional[ecc.Command_OElt]:
    #
    kw: str
    for kw in commands_keywords[command_name]:
        #
        tkw: str = traite_txt(kw)
        ltkw: int = len(tkw)
        #
        if command_input.startswith(tkw):
            #
            elt: str = command_input[ltkw:].strip()
            #
            return ecc.Command_OElt(
                command_name=command_name,
                elt = elt if elt != "" else None
            )
    #
    return None

#
def test_COMMAND_OPT_KEYWORD_SOMETHING(command_input: str, command_name: str, keyword_opt: list[str] = ["to"], return_keyword: bool = False) -> Optional[ecc.Command_OKw_Elt]:
    #
    if isinstance(keyword_opt, str):
        keyword_opt = [keyword_opt]

    #
    keywords_a_pattern = "|".join(re.escape(keyword) for keyword in commands_keywords[command_name])
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
        keyword_a, keyword_b, text_b = match.groups()
        return ecc.Command_OKw_Elt(
            command_name=command_name,
            elt=text_b.strip() if text_b else '',
            kw=keyword_b
        )
    else:
        #
        res: Optional[ecc.Command_Elt] = test_COMMAND_SOMETHING(command_input, command_name)
        #
        if res is not None:
            return ecc.Command_OKw_Elt(
                command_name=res.command_name,
                elt=res.elt
            )
        #
        return None

#
def test_COMMAND_OPT_KEYWORD_OPT_SOMETHING(command_input: str, command_name: str, keyword_opt: list[str] = ["to"], return_keyword: bool = False) -> Optional[ecc.Command_OKw_OElt]:
    #
    if isinstance(keyword_opt, str):
        keyword_opt = [keyword_opt]

    #
    keywords_a_pattern = "|".join(re.escape(keyword) for keyword in commands_keywords[command_name])
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
        keyword_a, keyword_b, text_b = match.groups()
        return ecc.Command_OKw_OElt(
            command_name=command_name,
            elt=text_b.strip() if text_b else '',
            kw=keyword_b
        )
    else:
        #
        res: Optional[ecc.Command_Elt] = test_COMMAND_SOMETHING(command_input, command_name)
        #
        if res is not None:
            return ecc.Command_OKw_OElt(
                command_name=res.command_name,
                elt=res.elt
            )
        #
        else:
            #
            res: Optional[ecc.Command] = test_COMMAND(command_input, command_name)
            #
            if res is not None:
                return ecc.Command_OKw_OElt(
                    command_name=res.command_name
                )
            #
            return None

#
def test_COMMAND_SOMETHING_KEYWORD_SOMETHING(command_input: str, command_name: str, keyword_connection: str | list[str], return_keyword: bool = False) -> Optional[ecc.Command_Elt_Kw_Elt]:
    #
    if isinstance(keyword_connection, str):
        keyword_connection = [keyword_connection]

    # Create regex patterns for the keywords (using the | operator for "or")
    keywords_a_pattern = "|".join(re.escape(keyword) for keyword in commands_keywords[command_name])  # Escape keywords for safety
    keywords_b_pattern = "|".join(re.escape(keyword) for keyword in keyword_connection)

    # Construct the main regex pattern
    pattern = rf"({keywords_a_pattern})\s+(.*?)\s+({keywords_b_pattern})\s+(.*)"  # r"" for raw string, f"" for f-string

    #
    match = re.match(pattern, command_input)

    #
    if match:
        keyword_a, text_a, keyword_b, text_b = match.groups()
        #
        return ecc.Command_Elt_Kw_Elt(
            command_name=command_name,
            elt1=text_a.strip(),
            elt2=text_b.strip(),
            kw=keyword_b
        )
    #
    return None


def test_COMMAND_SOMETHING_KEYWORD_SOMETHING_KEYWORD_SOMETHING(command_input: str, command_name: str, keyword_B: str | list[str], keyword_C: str | list[str], return_keywords: bool = False) -> Optional[ecc.Command_Elt_Kw_Elt_Kw_Elt]:
    #
    if isinstance(keyword_B, str):
        keyword_B = [keyword_B]
    #
    if isinstance(keyword_C, str):
        keyword_C = [keyword_C]

    #
    keywords_a_pattern = "|".join(re.escape(keyword) for keyword in commands_keywords[command_name])
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
        keyword_a, text_a, keyword_b, text_b, _, keyword_c, text_c = match.groups()
        #
        return ecc.Command_Elt_Kw_Elt_Kw_Elt(
            command_name=command_name,
            elt1=text_a,
            elt2=text_b,
            elt3=text_c,
            kw1=keyword_b,
            kw2=keyword_c
        )
    else:
        return None

#
def test_COMMAND_SOMETHING_KEYWORD_SOMETHING_OPT_KEYWORD_SOMETHING(command_input: str, command_name: str, keyword_B: str | list[str], keyword_C: str | list[str], return_keywords: bool = False) -> Optional[ecc.Command_Elt_Kw_Elt_OKw_OElt]:
    #
    res: Optional[ecc.Command] = test_COMMAND_SOMETHING_KEYWORD_SOMETHING_KEYWORD_SOMETHING(command_input, command_name, keyword_B, keyword_C, return_keywords)
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
    res = test_COMMAND_SOMETHING_KEYWORD_SOMETHING(command_input, command_name, keyword_B, return_keywords)
    #
    if res is not None:
        return ecc.Command_Elt_Kw_Elt_OKw_OElt(
            command_name=res.command_name,
            elt1=res.elt1,
            elt2=res.elt2,
            kw1=res.kw
        )
    #
    return None

#
def test_COMMAND_SOMETHING_OPT_KEYWORD_SOMETHING(command_input: str, command_name: str, keyword_opt: str | list[str], return_keyword: bool = False) -> Optional[ecc.Command_Elt_OKw_OElt]:
    #
    if isinstance(keyword_opt, str):
        keyword_opt = [keyword_opt]

    #
    keywords_a_pattern = "|".join(re.escape(keyword) for keyword in commands_keywords[command_name])
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
        keyword_a, text_a, keyword_b, text_b = match.groups()
        #
        return ecc.Command_Elt_OKw_OElt(
            command_name=command_name,
            elt1=text_a.strip(),
            elt2=text_b.strip(),
            kw=keyword_b
        )
    else:
        #
        res: Optional[ecc.Command_Elt] = test_COMMAND_SOMETHING(command_input, command_name)
        #
        if res is not None:
            #
            return ecc.Command_Elt_OKw_OElt(
                command_name=command_name,
                elt1=res.elt
            )
        #
        return None

#
def test_COMMAND_OPT_SOMETHING_KEYWORD_SOMETHING_KEYWORD_SOMETHING(command_input: str, command_name: str, keyword_B: str | list[str], keyword_C: str | list[str], return_keywords: bool = False) -> Optional[ecc.Command_Elt_Kw_Elt_Kw_Elt]:
    #
    if isinstance(keyword_B, str):
        keyword_B = [keyword_B]
    #
    if isinstance(keyword_C, str):
        keyword_C = [keyword_C]

    #
    keywords_a_pattern = "|".join(re.escape(keyword) for keyword in commands_keywords[command_name])
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
        keyword_a, quantity, keyword_b, item, keyword_c, target = match.groups()
        quantity = quantity if quantity else "1"  # Default to 1 if not specified
        #
        return ecc.Command_Elt_Kw_Elt_Kw_Elt(
            command_name=command_name,
            elt1=quantity,
            elt2=item,
            elt3=target,
            kw1=keyword_b,
            kw2=keyword_c
        )
    else:
        return None

#
def parse_command(command_input: str) -> Optional[ecc.Command]:

    #
    command_input = traite_txt(command_input)
    res: Optional[ecc.Command] = None

    ##################################
    ###### OBSERVATION COMMANDS ######
    ##################################

    #### COMMAND LOOK AROUND
    # `(see/look around/look)`: Observe the surroundings and get a description of the current area.

    res = test_COMMAND(command_input, "C_LOOKAROUND")
    if res is not None:
        return res

    #### COMMAND RECAP
    # `(recap)`: Summarize recent events, clues, or interactions.

    res = test_COMMAND(command_input, "C_RECAP")
    if res is not None:
        return res

    #### COMMAND BRIEF
    #  `brief [something/someone]`: Give a short description of something or someone. (ex: `brief ancient statue`)

    res = test_COMMAND_SOMETHING(command_input, "C_BRIEF")
    if res is not None:
        return res

    #### COMMAND DESCRIBE
    # `(watch/describe) [something/someone]`: Give a detailed description of an object or character. (ex: `describe mysterious painting`)

    res = test_COMMAND_SOMETHING(command_input, "C_DESCRIBE")
    if res is not None:
        return res

    #### COMMAND EXAMINE
    # `(examine/inspect/check) [something/someone]`: Closely inspect something or someone to reveal details. (ex: `examine old diary`)

    res = test_COMMAND_SOMETHING(command_input, "C_EXAMINE")
    if res is not None:
        return res

    #### COMMAND RUMMAGE
    # `(rummage/search) [something]`: Search a container or place for hidden items. (ex: `rummage drawer`)

    res = test_COMMAND_SOMETHING(command_input, "C_RUMMAGE")
    if res is not None:
        return res

    #### COMMAND LISTEN
    # `(hear/listen) ?{TO} ?{[something/someone]}`: Focus on sounds or listen to someone. (ex: `listen music`)

    res = test_COMMAND_OPT_KEYWORD_OPT_SOMETHING(command_input, "C_LISTEN")
    if res is not None:
        return res

    #### COMMAND TOUCH
    # `(touch/feel) [something/someone]`: Sense the texture, temperature, or state of an object or person. (ex: `feel statue`)

    res = test_COMMAND_SOMETHING(command_input, "C_TOUCH")
    if res is not None:
        return res

    #### COMMAND READ
    # `read [something] ?{page [number]}`: Read a written document, optionally specifying a page. (ex: `read journal page 2`)

    res = test_COMMAND_SOMETHING_OPT_KEYWORD_SOMETHING(command_input, "C_READ", ["page"])
    if res is not None:
        return res

    #### COMMAND TASTE
    # `taste [something]`: Try tasting an object. (ex: `taste soup`)

    res = test_COMMAND_SOMETHING(command_input, "C_TASTE")
    if res is not None:
        return res

    #### COMMAND SMELL
    # `(smell/sniff) [something/someone]`: Identify the scent of something or someone. (ex: `sniff flower`)

    res = test_COMMAND_SOMETHING(command_input, "C_SMELL")
    if res is not None:
        return res

    ###################################
    ###### DISPLACEMENT COMMANDS ######
    ###################################

    #### COMMAND GO
    # `(go/displace/walk/run/sprint) [direction]`: Move in the specified direction. (ex: `go north`)

    res = test_COMMAND_SOMETHING(command_input, "C_GO")
    if res is not None:
        return res

    ##########################################
    ###### OBJECT INTERACTIONS COMMANDS ######
    ##########################################

    #### COMMAND PUT
    # `(put/move) [something] (on/into/in) [somewhere/something]`: Place an object somewhere. (ex: `put book on shelf`)

    res = test_COMMAND_SOMETHING_KEYWORD_SOMETHING(command_input, "C_PUT", ["on", "into", "in"], return_keyword=True)
    if res is not None:
        return res

    #### COMMAND PUSH
    # `(push/press/apply force on) [something]`: Apply force to an object. (ex: `press button`)

    res = test_COMMAND_SOMETHING(command_input, "C_PUSH")
    if res is not None:
        return res

    #### COMMAND PULL
    # `pull [something]`: Pull an object. (ex: `pull lever`)

    res = test_COMMAND_SOMETHING(command_input, "C_PULL")
    if res is not None:
        return res

    #### COMMAND ATTACH
    # `(attach/tie) [something/someone] to [something/someone] ?{with [something]}`: Attach an object to something. (ex: `attach bandit to chair with rope`)

    res = test_COMMAND_SOMETHING_KEYWORD_SOMETHING_OPT_KEYWORD_SOMETHING(command_input, "C_ATTACH", ["to"], ["with"])
    if res is not None:
        return res

    #### COMMAND BREAK
    # `(break/destroy) [something]`: Destroy a destructible object. (ex: `break glass`)

    res = test_COMMAND_SOMETHING(command_input, "C_BREAK")
    if res is not None:
        return res

    #### COMMAND THROW
    # `throw [something] on [something]`: Throw an object at another object. (ex: `throw rock on window`)
    # `throw [something] on [someone]`: Throw an object at someone. (ex: `throw rock on bandit`)

    res = test_COMMAND_SOMETHING_KEYWORD_SOMETHING(command_input, "C_THROW", ["on", "to", "into", "in"])
    if res is not None:
        return res

    #### COMMAND DROP
    # `(drop/discard/get off) [something]`: Remove an object from inventory. (ex: `drop bag`)

    res = test_COMMAND_SOMETHING(command_input, "C_DROP")
    if res is not None:
        return res

    #### COMMAND CLEAN
    # `(clean/rub/scrub/sweep/polish/shine/wash/wipe) [something]`: Clean something. (ex: `wash painting`)

    res = test_COMMAND_SOMETHING(command_input, "C_CLEAN")
    if res is not None:
        return res

    #### COMMAND USE
    # `use [something] ?{on [something/someone]}`: Use an object, optionally on something or someone. (ex: `use key on door`)

    res = test_COMMAND_SOMETHING_OPT_KEYWORD_SOMETHING(command_input, "C_USE", ["on"])
    if res is not None:
        return res

    #### COMMAND CLIMB
    # `climb [something]`: Climb an object. (ex: `climb tree`)

    res = test_COMMAND_SOMETHING(command_input, "C_CLIMB")
    if res is not None:
        return res

    #### COMMAND OPEN
    # `open [something]`: Open a door, chest, or other container. (ex: `open chest`)

    res = test_COMMAND_SOMETHING(command_input, "C_OPEN")
    if res is not None:
        return res

    #### COMMAND CLOSE
    # `(close/shut) [something]`: Close an object. (ex: `close window`)

    res = test_COMMAND_SOMETHING(command_input, "C_CLOSE")
    if res is not None:
        return res

    #### COMMAND LOCK
    # `lock [something] ?{with [something]}`: Lock an object. (ex: `lock door with golden key`)

    res = test_COMMAND_SOMETHING_OPT_KEYWORD_SOMETHING(command_input, "C_LOCK", ["with"])
    if res is not None:
        return res

    #### COMMAND UNLOCK
    # `unlock [something] ?{with [something]}`: Unlock an object. (ex: `unlock chest with rusty key`)

    res = test_COMMAND_SOMETHING_OPT_KEYWORD_SOMETHING(command_input, "C_UNLOCK", ["with"])
    if res is not None:
        return res

    #### COMMAND FILL
    # `fill [something] (with/from) [something]`: Fill a container. (ex: `fill bottle with water`)

    res = test_COMMAND_SOMETHING_KEYWORD_SOMETHING(command_input, "C_FILL", ["with", "from"])
    if res is not None:
        return res

    #### COMMAND POUR
    # `(pour) [something] into [something]`: Pour a liquid. (ex: `pour coffee into cup`)

    res = test_COMMAND_SOMETHING_KEYWORD_SOMETHING(command_input, "C_POUR", ["in", "    into"])
    if res is not None:
        return res

    #### COMMAND INSERT
    # `insert [something] into [something]`: Insert an item. (ex: `insert coin into vending machine`)

    res = test_COMMAND_SOMETHING_KEYWORD_SOMETHING(command_input, "C_INSERT", ["into"])
    if res is not None:
        return res

    #### COMMAND REMOVE
    # `remove [something] from [something]`: Take something out of another object. (ex: `remove book from shelf`)

    res = test_COMMAND_SOMETHING_KEYWORD_SOMETHING(command_input, "C_REMOVE", ["from"])
    if res is not None:
        return res

    #### COMMAND SET
    # `set [something] to [state]`: Adjust an object’s state. (ex: `set lamp to on`)

    res = test_COMMAND_SOMETHING_KEYWORD_SOMETHING(command_input, "C_SET", ["to"])
    if res is not None:
        return res

    #### COMMAND SPREAD
    # `spread [something] ?{on [something/someone]}`: Apply something over a surface. (ex: `spread butter on bread`)

    res = test_COMMAND_SOMETHING_OPT_KEYWORD_SOMETHING(command_input, "C_SPREAD", ["into", "on", "in"])
    if res is not None:
        return res

    #### COMMAND SQUEEZE
    # `(squeeze/squash) [something]`: Press or crush an object. (ex: `squeeze lemon`)

    res = test_COMMAND_SOMETHING(command_input, "C_SQUEEZE")
    if res is not None:
        return res

    ##############################################
    ###### CONSUMABLE INTERACTIONS COMMANDS ######
    ##############################################

    #### COMMAND EAT
    # `(consume/eat) [something]`: Eat an item. (ex: `eat apple`)

    res = test_COMMAND_SOMETHING(command_input, "C_EAT")
    if res is not None:
        return res

    #### COMMAND DRINK
    # `(drink/sip/swallow) [something]`: Drink a liquid. (ex: `drink potion`)

    res = test_COMMAND_SOMETHING(command_input, "C_DRINK")
    if res is not None:
        return res

    ##########################################
    ###### LIVING INTERACTIONS COMMANDS ######
    ##########################################

    #### COMMAND AWAKE
    # `(awake/wake/wake up) [someone]`: Wake a sleeping person. (ex: `wake up guard`)

    res = test_COMMAND_SOMETHING(command_input, "C_AWAKE")
    if res is not None:
        return res

    #### COMMAND ATTACK
    # `(attack/smash/fight/hit/hurt/kill/murder/punch/slice/thump/torture/wreck) [someone] ?{with [something]}`: Attack someone. (ex: `attack bandit with sword`)

    res = test_COMMAND_SOMETHING_OPT_KEYWORD_SOMETHING(command_input, "C_ATTACK", ["with"])
    if res is not None:
        return res

    #### COMMAND BUY
    # `(buy/purchase) ?{[quantity] of} [something] to [someone]`: Buy an item. (ex: `buy 2 potions to merchant`)

    res = test_COMMAND_OPT_SOMETHING_KEYWORD_SOMETHING_KEYWORD_SOMETHING(command_input, "C_BUY", ["of"], ["to", "at"])
    if res is not None:
        return res

    #### COMMAND SHOW
    # `(show/display/present) [something/someone] to [someone]`: Show something to someone. (ex: `show passport to guard`)

    res = test_COMMAND_SOMETHING_KEYWORD_SOMETHING(command_input, "C_SHOW", ["to"])
    if res is not None:
        return res

    #### COMMAND EMBRACE
    # `(embrace/hug/kiss) [someone]`: Perform an affectionate gesture. (ex: `hug friend`)

    res = test_COMMAND_SOMETHING(command_input, "C_EMBRACE")
    if res is not None:
        return res

    #### COMMAND FEED
    # `(feed) [someone] with [something]`: Give food to someone. (ex: `feed dog with bone`)

    res = test_COMMAND_SOMETHING_KEYWORD_SOMETHING(command_input, "C_FEED", ["with"])
    if res is not None:
        return res

    #### COMMAND GIVE
    # `(give/offer) [something] to [someone]`: Alternative phrasing. (ex: `offer flower to lover`)

    res = test_COMMAND_SOMETHING_KEYWORD_SOMETHING(command_input, "C_GIVE", ["to"])
    if res is not None:
        return res

    ###################################
    ###### VOICE / TEXT COMMANDS ######
    ###################################

    #### COMMAND SAY
    # `(say/tell/answer/shout) "..." to [someone/something]`: Communicate verbally with a character or object. (ex: `say "Hello" to guard`)

    res = test_COMMAND_SOMETHING_OPT_KEYWORD_SOMETHING(command_input, "C_SAY", ["to"])
    if res is not None:
        return res

    #### COMMAND ASK
    # `ask [someone] (about/for/on) [something/someone]`: Ask someone for information. (ex: `ask merchant about potion`)

    res = test_COMMAND_SOMETHING_KEYWORD_SOMETHING(command_input, "C_ASK", ["about", "on", "for"])
    if res is not None:
        return res

    #### COMMAND WRITE
    # `(write) "..." on [something] ?{with [something]}`: Write a message on an object. (ex: `write "Hello" on the old paper with pencil`) ***Note:** if there is already a writen thing on the object, and you want only the text you want to write, you can try to erase the previous text on the object.*

    res = test_COMMAND_SOMETHING_KEYWORD_SOMETHING_OPT_KEYWORD_SOMETHING(command_input, "C_WRITE", ["on"], ["with"])
    if res is not None:
        return res

    #### COMMAND ERASE
    # `(erase/efface/delete/rub out) [something] ?{with [something]}`: Erase everything that is writen on an object. (Ex: `rub out the paper with gum` or `erase the blackboard with the brush`)

    res = test_COMMAND_SOMETHING_OPT_KEYWORD_SOMETHING(command_input, "C_ERASE", ["with"])
    if res is not None:
        return res

    #########################################
    ###### PLAYER INTERACTION COMMANDS ######
    #########################################

    #### COMMAND WEAR
    # `(wear/dress) [something]`: Wear clothing or equipment. (ex: `wear helmet`)

    res = test_COMMAND_SOMETHING(command_input, "C_WEAR")
    if res is not None:
        return res

    #### COMMAND UNDRESS
    # `(undress/take off/strip/pull off/shed) [something]`: Take off clothing or equipment. (ex: `remove jacket`)

    res = test_COMMAND_SOMETHING(command_input, "C_UNDRESS")
    if res is not None:
        return res

    #### COMMAND INVENTORY
    # `(inventory)`: List the objects in your inventory. (ex: `inv`)

    res = test_COMMAND(command_input, "C_INVENTORY")
    if res is not None:
        return res

    #### COMMAND WAIT
    # `wait ?{[duration]}`: Pause and let time pass. (ex: `wait 5 minutes`)

    res = test_COMMAND_OPT_SOMETHING(command_input, "C_WAIT")
    if res is not None:
        return res

    #### COMMAND SLEEP
    # `(sleep/nap)`: Rest and possibly recover. (ex: `sleep`)

    res = test_COMMAND(command_input, "C_SLEEP")
    if res is not None:
        return res

    #### COMMAND SIT
    # `sit on [something]`: Take a seat on an object. (ex: `sit on chair`)

    res = test_COMMAND_SOMETHING(command_input, "C_SIT_DOWN")
    if res is not None:
        return res

    #### COMMAND LIE DOWN
    # `(lie on/lie down on) ?{[something]}`: Lie down on an object. (ex: `lie down on the bed`)

    res = test_COMMAND_OPT_SOMETHING(command_input, "C_LIE_DOWN")
    if res is not None:
        return res

    #### COMMAND STAND UP
    # `(stand/stand up)`: Return to a standing position. (ex: `stand up`)

    res = test_COMMAND(command_input, "C_STAND_UP")
    if res is not None:
        return res

    ############################################
    ###### OBJECT INTERACTIONS COMMANDS 2 ######
    ############################################

    #### COMMAND TAKE
    # `(take/carry/hold/pick/pick up) [something]`: Pick up an object and add it to the inventory. (ex: `take golden key`)

    res = test_COMMAND_SOMETHING(command_input, "C_TAKE")
    if res is not None:
        return res

    #############################
    ###### RANDOM COMMANDS ######
    #############################

    #### COMMAND DANCE
    # `dance ?{something}`: Perform a dance. (ex: `dance`)

    res = test_COMMAND_OPT_SOMETHING(command_input, "C_DANCE")
    if res is not None:
        return res

    #### COMMAND SING
    # `(chant/sing) ?{something}`: Sing or chant something. (ex: `sing`)

    res = test_COMMAND_OPT_SOMETHING(command_input, "C_SING")
    if res is not None:
        return res

    #### COMMAND JUMP
    # `(jump/hop)`: Jump up or forward. (ex: `jump`)

    res = test_COMMAND(command_input, "C_JUMP")
    if res is not None:
        return res

    #### COMMAND THINK
    # `(think)`: Reflect or contemplate. (ex: `think`)

    res = test_COMMAND(command_input, "C_THINK")
    if res is not None:
        return res

    #############################
    ###### SYSTEM COMMANDS ######
    #############################

    #### COMMAND QUIT
    # `(quit)`: Quit the game. (ex: `quit`)

    res = test_COMMAND(command_input, "C_QUIT")
    if res is not None:
        return res

    #### COMMAND SAVE
    # `save ?{filepath of game save}`: Save the game. (ex: `save game1.sav`)

    res = test_COMMAND_OPT_SOMETHING(command_input, "C_SAVE")
    if res is not None:
        return res

    #### COMMAND LOAD
    # `(load/restore) {filepath of game save}`: Load a saved game. (ex: `load game1.sav`)

    res = test_COMMAND_OPT_SOMETHING(command_input, "C_LOAD")
    if res is not None:
        return res

    #### COMMAND RESTART
    # `restart`: Restart the game. (ex: `restart`)

    res = test_COMMAND(command_input, "C_RESTART")
    if res is not None:
        return res

    #### COMMAND SCORE
    # `score`: Show current progress. (ex: `score`)

    res = test_COMMAND(command_input, "C_SCORE")
    if res is not None:
        return res

    #### COMMAND HELP
    # `help ?{something}`: Show the list of commands. (ex: `help`)

    res = test_COMMAND_OPT_SOMETHING(command_input, "C_HELP")
    if res is not None:
        return res

    ##############################
    ###### UNKNOWN COMMANDS ######
    ##############################

    #
    return []  # Commande vide


#
def main_user_input_test() -> None:
    #
    res: list[str] = []
    #
    while not (len(res) == 1 and res[0] == "C_QUIT"):
        #
        command_input: str = input("> ")
        #
        res = parse_command( command_input )
        print( res )


#
if __name__ == "__main__":
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
            print(f"{parse_command(test_input)}")
    #
    else:
        #
        main_user_input_test()
