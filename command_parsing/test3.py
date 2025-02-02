#!/usr/bin/env python3
"""
A sample Python script that uses Lark to lex/parse interactive-fiction commands.

It defines a grammar covering many (but not necessarily all) commands from your list.
Each command, when successfully parsed, is transformed into a tuple
with the command name (in uppercase) and its arguments (if any).

Make sure you have installed Lark (e.g., pip install lark-parser).
"""

from lark import Lark, Transformer

# This is a Lark grammar that covers many families of commands:
grammar = r"""
// --- START SYMBOL ---
?start: command

?command: observation
        | displacement
        | interact
        | consumable
        | living
        | voice
        | self_action
        | random
        | system

// --- OBSERVATION COMMANDS ---
?observation: look_command
            | recap_command
            | brief_command
            | watch_command
            | examine_command
            | rummage_command
            | hear_command
            | touch_command
            | read_command
            | taste_command
            | smell_command

look_command: LOOK_WORD
brief_command: BRIEF_WORD object
watch_command: WATCH_WORD object
examine_command: EXAMINE_WORD object
rummage_command: RUMMAGE_WORD object
hear_command: HEAR_WORD [object]
touch_command: TOUCH_WORD object
read_command: READ_WORD object [read_page]
taste_command: TASTE_WORD object
smell_command: SMELL_WORD object
recap_command: "recap"

// Optional page argument for the "read" command
read_page: "page" WORD

// --- DISPLACEMENT COMMANDS ---
?displacement: move_command

move_command: MOVE_WORD direction
direction: ATOMIC_DIRECTION (ATOMIC_DIRECTION)?

// --- INTERACT WITH OBJECTS ---
?interact: take_command
         | put_command
         | push_command
         | pull_command
         | attach_command
         | break_command
         | throw_on_object_command
         | throw_command
         | clean_command
         | use_command
         | climb_command
         | open_command
         | close_command
         | lock_command
         | unlock_command
         | fill_command
         | pour_command
         | insert_command
         | remove_command
         | set_command
         | spread_command
         | squeeze_command

take_command: TAKE_WORD object
put_command: PUT_WORD object PLACE_WORD object
push_command: PUSH_WORD object
pull_command: "pull" object
attach_command: ATTACH_WORD object "to" object ["with" object]
break_command: BREAK_WORD object
throw_on_object_command: "throw" object "on" object
throw_command: THROW_WORD object
clean_command: CLEAN_WORD object
use_command: USE_WORD object ["on" object]
climb_command: "climb" object
open_command: "open" object
close_command: CLOSE_WORD object
lock_command: "lock" object ["with" object]
unlock_command: "unlock" object ["with" object]
fill_command: "fill" object ( "with" | "from" ) object
pour_command: "pour" object "into" object
insert_command: "insert" object "into" object
remove_command: "remove" object "from" object
set_command: "set" object "to" WORD
spread_command: "spread" object ["on" object]
squeeze_command: SQUEEZE_WORD object

// --- INTERACT WITH CONSUMABLE ---
?consumable: consume_command
            | drink_command
consume_command: CONSUME_WORD object
drink_command: DRINK_WORD object

// --- INTERACTIONS WITH LIVING THINGS ---
?living: wake_command
       | attack_command
       | throw_on_living_command
       | buy_command
       | show_command
       | embrace_command
       | feed_command
       | give_command1
       | give_command2

wake_command: WAKE_WORD object
attack_command: ATTACK_WORD object ["with" object]
throw_on_living_command: "throw" object "on" object
buy_command: BUY_WORD [quantity] object "to" object
show_command: SHOW_WORD object "to" object
embrace_command: EMBRACE_WORD object
feed_command: FEED_WORD object "with" object
give_command1: GIVE_WORD object object
give_command2: GIVE_WORD object "to" object

quantity: WORD

// --- VOICE / DISCUSSIONS / TEXT ---
?voice: say_command
      | ask_command
      | write_command
say_command: SAY_WORD ESCAPED_STRING "to" object
ask_command: "ask" object ( "about" | "for" | "on" ) object
write_command: "write" ESCAPED_STRING "on" object ["with" object]

// --- INTERACTION WITH YOURSELF ---
?self_action: wear_command
            | remove_self_command
            | inventory_command
            | wait_self_command
            | sleep_command
            | sit_command
            | lie_command
            | stand_command

wear_command: WEAR_WORD object
remove_self_command: REMOVE_WORD object
inventory_command: INVENTORY_WORD
wait_self_command: WAIT_WORD [object]
sleep_command: SLEEP_WORD
sit_command: "sit" "on" object
lie_command: ("lie"|"lie down") "on" object
stand_command: STAND_WORD

// --- RANDOM THINGS ---
?random: dance_command
       | chant_command
       | jump_command
       | think_command
dance_command: "dance"
chant_command: CHANT_WORD
jump_command: JUMP_WORD
think_command: THINK_WORD

// --- SYSTEM COMMANDS ---
?system: save_command
       | quit_command
       | load_command
       | restart_command
       | score_command
       | help_command
save_command: "save" [object]
quit_command: QUIT_WORD
load_command: ( "load" | "restore" ) object
restart_command: "restart"
score_command: "score"
help_command: "help" ":" "show" "the" "list" "of" "command"

// --- COMMON RULES ---
object: WORD+
%import common.WORD
%import common.WS
%ignore WS

// --- TOKEN DEFINITIONS (case-insensitive) ---
LOOK_WORD: /(see|look|l)/i
BRIEF_WORD: /brief/i
WATCH_WORD: /(watch|describe)/i
EXAMINE_WORD: /(examine|inspect|check|x)/i
RUMMAGE_WORD: /(rummage|search)/i
HEAR_WORD: /(hear|listen)/i
TOUCH_WORD: /(touch|feel)/i
READ_WORD: /read/i
TASTE_WORD: /taste/i
SMELL_WORD: /(smell|sniff)/i

MOVE_WORD: /(go|move|mv|displace|d|walk|run|sprint)/i
ATOMIC_DIRECTION: /(North|N|South|S|East|E|West|W|Up|Above|U|A|Down|Below|B|D)/i

TAKE_WORD: /(take|carry|hold|pick|pick up)/i
PUT_WORD: /(put|move|displace)/i
PLACE_WORD: /(in|on|above|into)/i
PUSH_WORD: /(push|press|apply force on)/i
THROW_WORD: /(throw|drop|discard|get off)/i
CLEAN_WORD: /(clean|rub|scrub|sweep|polish|shine|wash|wipe)/i
USE_WORD: /use/i
CLOSE_WORD: /(close|shut)/i
SQUEEZE_WORD: /(squeeze|squash)/i

CONSUME_WORD: /(consume|eat)/i
DRINK_WORD: /(drink|sip|swallow)/i

WAKE_WORD: /(awake|wake|wake up)/i
ATTACK_WORD: /(attack|smash|fight|hit|hurt|kill|murder|punch|slice|thump|torture|wreck)/i
BUY_WORD: /(buy|purchase)/i
SHOW_WORD: /(show|display|present)/i
EMBRACE_WORD: /(embrace|hug|kiss)/i
FEED_WORD: /feed/i
GIVE_WORD: /(give|offer)/i

SAY_WORD: /(say|tell|ask|answer|shout)/i
CHANT_WORD: /(chant|sing)/i
JUMP_WORD: /(jump|hop)/i
THINK_WORD: /think/i

WEAR_WORD: /(wear|dress)/i
REMOVE_WORD: /(remove|take off|strip|pull off|shed)/i
INVENTORY_WORD: /(inventory|inv|i)/i
WAIT_WORD: /wait/i
SLEEP_WORD: /(sleep|nap)/i
STAND_WORD: /(stand|stand up)/i

QUIT_WORD: /(quit|q)/i

// For text arguments in say/write commands:
ESCAPED_STRING: /"([^"\\]*(\\.[^"\\]*)*)"/
"""

# --- TRANSFORMER ---
# The transformer converts the parse tree into a tuple with the command name and arguments.
# For simplicity, we convert the list of WORD tokens (which represent an object) into a single string.
class CommandTransformer(Transformer):
    def object(self, items):
        # Join multiple WORD tokens into one string.
        return " ".join(items)

    def read_page(self, items):
        # Return the page number as a string.
        return "page " + items[0]

    # --- Observation commands ---
    def look_command(self, items):
        return ("LOOK", )

    def brief_command(self, items):
        return ("BRIEF", items[0])

    def watch_command(self, items):
        return ("WATCH", items[0])

    def examine_command(self, items):
        return ("EXAMINE", items[0])

    def rummage_command(self, items):
        return ("RUMMAGE", items[0])

    def hear_command(self, items):
        if items:
            return ("HEAR", items[0])
        else:
            return ("HEAR", )

    def touch_command(self, items):
        return ("TOUCH", items[0])

    def read_command(self, items):
        if len(items) == 2:
            return ("READ", items[0], items[1])
        else:
            return ("READ", items[0])

    def taste_command(self, items):
        return ("TASTE", items[0])

    def smell_command(self, items):
        return ("SMELL", items[0])

    def recap_command(self, items):
        return ("RECAP", )

    # --- Displacement ---
    def move_command(self, items):
        # items[0] is the move verb; items[1] is the direction (which might be one or two tokens).
        return ("MOVE", items[1])

    def direction(self, items):
        return " ".join(items)

    # --- Interact with objects ---
    def take_command(self, items):
        return ("TAKE", items[0])

    def put_command(self, items):
        return ("PUT", items[0], items[2])

    def push_command(self, items):
        return ("PUSH", items[0])

    def pull_command(self, items):
        return ("PULL", items[0])

    def attach_command(self, items):
        # Items: object, "to", object, optionally "with" object.
        if len(items) == 3:
            return ("ATTACH", items[0], items[1])
        elif len(items) == 4:
            return ("ATTACH", items[0], items[1], items[3])
        else:
            return ("ATTACH", )  # fallback

    def break_command(self, items):
        return ("BREAK", items[0])

    def throw_on_object_command(self, items):
        return ("THROW", items[0], items[2])

    def throw_command(self, items):
        return ("THROW", items[0])

    def clean_command(self, items):
        return ("CLEAN", items[0])

    def use_command(self, items):
        if len(items) == 2:
            return ("USE", items[0], items[1])
        else:
            return ("USE", items[0])

    def climb_command(self, items):
        return ("CLIMB", items[0])

    def open_command(self, items):
        return ("OPEN", items[0])

    def close_command(self, items):
        return ("CLOSE", items[0])

    def lock_command(self, items):
        if len(items) == 2:
            return ("LOCK", items[0])
        else:
            return ("LOCK", items[0], items[2])

    def unlock_command(self, items):
        if len(items) == 2:
            return ("UNLOCK", items[0])
        else:
            return ("UNLOCK", items[0], items[2])

    def fill_command(self, items):
        return ("FILL", items[0], items[2])

    def pour_command(self, items):
        return ("POUR", items[0], items[2])

    def insert_command(self, items):
        return ("INSERT", items[0], items[2])

    def remove_command(self, items):
        return ("REMOVE", items[0], items[2])

    def set_command(self, items):
        return ("SET", items[0], items[2])

    def spread_command(self, items):
        if len(items) == 1:
            return ("SPREAD", items[0])
        else:
            return ("SPREAD", items[0], items[2])

    def squeeze_command(self, items):
        return ("SQUEEZE", items[0])

    # --- Consumable commands ---
    def consume_command(self, items):
        return ("CONSUME", items[0])

    def drink_command(self, items):
        return ("DRINK", items[0])

    # --- Living things commands ---
    def wake_command(self, items):
        return ("WAKE", items[0])

    def attack_command(self, items):
        if len(items) == 1:
            return ("ATTACK", items[0])
        else:
            return ("ATTACK", items[0], items[1])

    def throw_on_living_command(self, items):
        return ("THROW", items[0], items[2])

    def buy_command(self, items):
        # If a quantity is provided, include it.
        if len(items) == 3:
            return ("BUY", items[0], items[1])
        else:
            return ("BUY", items[0])

    def show_command(self, items):
        return ("SHOW", items[0], items[2])

    def embrace_command(self, items):
        return ("EMBRACE", items[0])

    def feed_command(self, items):
        return ("FEED", items[0], items[2])

    def give_command1(self, items):
        return ("GIVE", items[0], items[1])

    def give_command2(self, items):
        return ("GIVE", items[0], items[2])

    # --- Voice / Discussion ---
    def say_command(self, items):
        # Remove the surrounding quotes from the string.
        text = items[0][1:-1]
        return ("SAY", text, items[1])

    def ask_command(self, items):
        return ("ASK", items[0], items[2])

    def write_command(self, items):
        text = items[0][1:-1]
        if len(items) == 3:
            return ("WRITE", text, items[1])
        else:
            return ("WRITE", text, items[1], items[3])

    # --- Self commands ---
    def wear_command(self, items):
        return ("WEAR", items[0])

    def remove_self_command(self, items):
        return ("REMOVE", items[0])

    def inventory_command(self, items):
        return ("INVENTORY", )

    def wait_self_command(self, items):
        if items:
            return ("WAIT", items[0])
        else:
            return ("WAIT", )

    def sleep_command(self, items):
        return ("SLEEP", )

    def sit_command(self, items):
        return ("SIT", items[0])

    def lie_command(self, items):
        return ("LIE", items[0])

    def stand_command(self, items):
        return ("STAND", )

    # --- Random commands ---
    def dance_command(self, items):
        return ("DANCE", )

    def chant_command(self, items):
        return ("CHANT", )

    def jump_command(self, items):
        return ("JUMP", )

    def think_command(self, items):
        return ("THINK", )

    # --- System commands ---
    def save_command(self, items):
        if items:
            return ("SAVE", items[0])
        else:
            return ("SAVE", )

    def quit_command(self, items):
        return ("QUIT", )

    def load_command(self, items):
        return ("LOAD", items[0])

    def restart_command(self, items):
        return ("RESTART", )

    def score_command(self, items):
        return ("SCORE", )

    def help_command(self, items):
        return ("HELP", )

# --- MAIN LOOP ---
def main():
    # Create the parser with the given grammar.
    parser = Lark(grammar, parser='earley', propagate_positions=True)
    transformer = CommandTransformer()

    print("Interactive Fiction Command Parser (Ctrl-D to exit)")
    while True:
        try:
            s = input("Enter command: ")
        except EOFError:
            break
        if not s.strip():
            continue
        try:
            # Parse the input
            tree = parser.parse(s)
            # Transform the tree into a tuple
            result = transformer.transform(tree)
            # Format the result: if an argument contains a space, we quote it.
            def fmt(x):
                if isinstance(x, str) and " " in x:
                    return f'"{x}"'
                return str(x)
            if isinstance(result, tuple):
                print(", ".join(fmt(item) for item in result))
            else:
                print(result)
        except Exception as e:
            print("Error parsing command:", e)

if __name__ == '__main__':
    main()
