#!/usr/bin/env python3
"""
Full Interactive Fiction Command Parser using PLY (Python Lex-Yacc)

This script recognizes a wide range of commands from an interactive fiction
engine. Each command’s production prints its command name along with its arguments,
if any, as specified.

Author: ChatGPT – “Details make perfection, and perfection is not a detail.”
"""

import sys
import ply.lex as lex
import ply.yacc as yacc

#########################################
# Lexer
#########################################

# Dictionary of reserved words and their token types.
reserved = {
    # Observation
    'use':      'USE',
    'see':      'SEE',
    'look':     'SEE',
    'l':        'SEE',
    'recap':    'RECAP',
    'brief':    'BRIEF',
    'watch':    'WATCH',
    'describe': 'WATCH',
    'examine':  'EXAMINE',
    'inspect':  'EXAMINE',
    'check':    'EXAMINE',
    'x':        'EXAMINE',
    'rummage':  'SEARCH',
    'search':   'SEARCH',
    'hear':     'HEAR',
    'listen':   'HEAR',
    'touch':    'TOUCH',
    'feel':     'TOUCH',
    'read':     'READ',
    'taste':    'TASTE',
    'smell':    'SMELL',
    'sniff':    'SMELL',

    # Displacement
    'go':       'GO',
    'move':     'GO',
    'mv':       'GO',
    'displace': 'GO',
    'd':        'GO',
    'walk':     'GO',
    'run':      'GO',
    'sprint':   'GO',

    #
    'wait':     'WAIT',

    # Atomic directions (also used as prepositions sometimes)
    'north':    'NORTH',
    'n':        'NORTH',
    'south':    'SOUTH',
    's':        'SOUTH',
    'east':     'EAST',
    'e':        'EAST',
    'west':     'WEST',
    'w':        'WEST',
    'up':       'UP',
    'above':    'UP',   # for displacement, above is same as up
    'u':        'UP',
    'a':        'UP',
    'down':     'DOWN',
    'below':    'DOWN',
    'b':        'DOWN',
    'd':        'DOWN',

    # Interact with objects
    'take':     'TAKE',
    'carry':    'TAKE',
    'hold':     'TAKE',
    'pick':     'TAKE',  # allow "pick" then optional "up" (handled in grammar)
    'put':      'PUT',
    'in':       'IN',
    'on':       'ON',
    'above':    'ABOVE', # when used in location (distinct from direction UP)
    'into':     'INTO',
    'push':     'PUSH',
    'press':    'PUSH',
    'apply':    'PUSH',
    'force':    'PUSH',
    'pull':     'PULL',
    'attach':   'ATTACH',
    'tie':      'ATTACH',
    'to':       'TO',
    'with':     'WITH',
    'break':    'BREAK',
    'destroy':  'BREAK',
    'throw':    'THROW',
    'drop':     'DROP',
    'discard':  'DROP',
    'get':      'DROP',  # if used with "off"
    'off':      'OFF',
    'clean':    'CLEAN',
    'rub':      'CLEAN',
    'scrub':    'CLEAN',
    'sweep':    'CLEAN',
    'polish':   'CLEAN',
    'shine':    'CLEAN',
    'wash':     'CLEAN',
    'wipe':     'CLEAN',
    'climb':    'CLIMB',
    'open':     'OPEN',
    'close':    'CLOSE',
    'shut':     'CLOSE',
    'lock':     'LOCK',
    'unlock':   'UNLOCK',
    'fill':     'FILL',
    'from':     'FROM',
    'pour':     'POUR',
    'insert':   'INSERT',
    'remove':   'REMOVE',
    'set':      'SET',
    'spread':   'SPREAD',
    'squeeze':  'SQUEEZE',
    'squash':   'SQUEEZE',

    # Interaction with consumable
    'consume':  'EAT',
    'eat':      'EAT',
    'drink':    'DRINK',
    'sip':      'DRINK',
    'swallow':  'DRINK',

    # Interactions with living things
    'awake':    'WAKE',
    'wake':     'WAKE',  # can be "wake up"
    'attack':   'ATTACK',
    'smash':    'ATTACK',
    'fight':    'ATTACK',
    'hit':      'ATTACK',
    'hurt':     'ATTACK',
    'kill':     'ATTACK',
    'murder':   'ATTACK',
    'punch':    'ATTACK',
    'slice':    'ATTACK',
    'thump':    'ATTACK',
    'torture':  'ATTACK',
    'wreck':    'ATTACK',
    'buy':      'BUY',
    'purchase': 'BUY',
    'show':     'SHOW',
    'display':  'SHOW',
    'present':  'SHOW',
    'embrace':  'EMBRACE',
    'hug':      'EMBRACE',
    'kiss':     'EMBRACE',
    'feed':     'FEED',
    'give':     'GIVE',
    'offer':    'GIVE',

    # Voice / Discussions / Text
    'say':      'SAY',
    'tell':     'SAY',
    'ask':      'ASK',
    'answer':   'SAY',
    'shout':    'SAY',
    'about':    'ABOUT',
    'for':      'FOR',
    'write':    'WRITE',

    # Interaction with yourself
    'wear':     'WEAR',
    'dress':    'WEAR',
    'strip':    'UNDRESS',
    'pulloff':  'UNDRESS',  # combine "pull off" as one word for simplicity
    'takeoff':  'UNDRESS',
    'shed':     'UNDRESS',
    'inventory':'INVENTORY',
    'inv':      'INVENTORY',
    'i':        'INVENTORY',
    'sleep':    'SLEEP',
    'nap':      'SLEEP',
    'sit':      'SIT',
    'lie':      'LIE',
    'stand':    'STAND',

    # Random things
    'dance':    'DANCE',
    'chant':    'CHANT',
    'sing':     'CHANT',
    'jump':     'JUMP',
    'hop':      'JUMP',
    'think':    'THINK',

    # System commands
    'save':     'SAVE',
    'quit':     'QUIT',
    'q':        'QUIT',
    'load':     'LOAD',
    'restore':  'LOAD',
    'restart':  'RESTART',
    'score':    'SCORE',
    'help':     'HELP',
}

# List of token names. We include a generic WORD, NUMBER, and QUOTED token.
tokens = [
    'WORD',
    'NUMBER',
    'QUOTED'
] + list(set(reserved.values()))

t_ignore = " \t"

def t_QUOTED(t):
    r'"([^\\"]|(\\.))*"'
    # Remove the surrounding quotes:
    t.value = t.value[1:-1]
    return t

def t_NUMBER(t):
    r'\d+'
    # You can convert to int if needed: t.value = int(t.value)
    return t

def t_WORD(t):
    r"[A-Za-z']+"
    lw = t.value.lower()
    if lw in reserved:
        t.type = reserved[lw]
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

#########################################
# Parser
#########################################

# The top-level rule: a command can be any one of many alternatives.
def p_command(p):
    '''command : obs_command
               | disp_command
               | obj_command
               | consumable_command
               | living_command
               | voice_command
               | self_command
               | random_command
               | system_command
    '''
    p[0] = p[1]

#########################################
# Observation commands
#########################################

def p_obs_command(p):
    '''obs_command : use_command
                   | see_command
                   | recap_command
                   | brief_command
                   | watch_command
                   | examine_command
                   | search_command
                   | hear_command
                   | touch_command
                   | read_command
                   | taste_command
                   | smell_command
    '''
    p[0] = p[1]

def p_use_command(p):
    '''use_command : USE item opt_on'''
    # "use <item> [on <item>]"
    if p[2] and p[3]:
        print(f"USE, \"{p[2]}\", \"{p[3]}\"")
        p[0] = ("USE", p[2], p[3])
    elif p[2]:
        print(f"USE, \"{p[2]}\"")
        p[0] = ("USE", p[2])
    else:
        print("USE")
        p[0] = ("USE",)

def p_see_command(p):
    '''see_command : SEE opt_item'''
    # "see" or "look" or "l" optionally followed by an item.
    if p[2]:
        print(f"SEE, \"{p[2]}\"")
        p[0] = ("SEE", p[2])
    else:
        print("SEE")
        p[0] = ("SEE",)

def p_recap_command(p):
    '''recap_command : RECAP'''
    print("RECAP")
    p[0] = ("RECAP",)

def p_brief_command(p):
    '''brief_command : BRIEF opt_item'''
    if p[2]:
        print(f"BRIEF, \"{p[2]}\"")
        p[0] = ("BRIEF", p[2])
    else:
        print("BRIEF")
        p[0] = ("BRIEF",)

def p_watch_command(p):
    '''watch_command : WATCH item'''
    print(f"WATCH, \"{p[2]}\"")
    p[0] = ("WATCH", p[2])

def p_examine_command(p):
    '''examine_command : EXAMINE item'''
    print(f"EXAMINE, \"{p[2]}\"")
    p[0] = ("EXAMINE", p[2])

def p_search_command(p):
    '''search_command : SEARCH item'''
    print(f"SEARCH, \"{p[2]}\"")
    p[0] = ("SEARCH", p[2])

def p_hear_command(p):
    '''hear_command : HEAR opt_item'''
    if p[2]:
        print(f"HEAR, \"{p[2]}\"")
        p[0] = ("HEAR", p[2])
    else:
        print("HEAR")
        p[0] = ("HEAR",)

def p_touch_command(p):
    '''touch_command : TOUCH item'''
    print(f"TOUCH, \"{p[2]}\"")
    p[0] = ("TOUCH", p[2])

def p_read_command(p):
    '''read_command : READ item opt_page'''
    if p[3]:
        print(f"READ, \"{p[2]}\", \"page {p[3]}\"")
        p[0] = ("READ", p[2], p[3])
    else:
        print(f"READ, \"{p[2]}\"")
        p[0] = ("READ", p[2])

def p_taste_command(p):
    '''taste_command : TASTE item'''
    print(f"TASTE, \"{p[2]}\"")
    p[0] = ("TASTE", p[2])

def p_smell_command(p):
    '''smell_command : SMELL item'''
    print(f"SMELL, \"{p[2]}\"")
    p[0] = ("SMELL", p[2])

def p_opt_on(p):
    '''opt_on : ON item
              | empty'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None

def p_opt_page(p):
    '''opt_page : page_clause
                | empty'''
    p[0] = p[1]

def p_page_clause(p):
    '''page_clause : WORD item
                   | NUMBER'''
    # We assume the first word is "page" if provided.
    if isinstance(p[1], str) and p[1].lower() == "page":
        p[0] = p[2]
    else:
        p[0] = p[1]


#########################################
# Displacement commands
#########################################

def p_disp_command(p):
    '''disp_command : GO direction_item'''
    print(f"GO, \"{p[2]}\"")
    p[0] = ("GO", p[2])

def p_direction_item(p):
    '''direction_item : item'''
    # For simplicity, we treat direction as an item.
    p[0] = p[1]

#########################################
# Interactions with objects
#########################################

def p_obj_command(p):
    '''obj_command : take_command
                   | put_command
                   | push_command
                   | pull_command
                   | attach_command
                   | break_command
                   | throw_obj_command
                   | drop_command
                   | clean_command
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
    '''
    p[0] = p[1]

def p_take_command(p):
    '''take_command : TAKE item'''
    print(f"TAKE, \"{p[2]}\"")
    p[0] = ("TAKE", p[2])

def p_put_command(p):
    '''put_command : PUT item put_prep item'''
    print(f"PUT, \"{p[2]}\", \"{p[4]}\"")
    p[0] = ("PUT", p[2], p[4])

def p_put_prep(p):
    '''put_prep : IN
                | ON
                | ABOVE
                | INTO'''
    p[0] = p[1]

def p_push_command(p):
    '''push_command : PUSH item'''
    print(f"PUSH, \"{p[2]}\"")
    p[0] = ("PUSH", p[2])

def p_pull_command(p):
    '''pull_command : PULL item'''
    print(f"PULL, \"{p[2]}\"")
    p[0] = ("PULL", p[2])

def p_attach_command(p):
    '''attach_command : ATTACH item TO item opt_with'''
    if p[5]:
        print(f"ATTACH, \"{p[2]}\", \"{p[4]}\", \"{p[5]}\"")
        p[0] = ("ATTACH", p[2], p[4], p[5])
    else:
        print(f"ATTACH, \"{p[2]}\", \"{p[4]}\"")
        p[0] = ("ATTACH", p[2], p[4])

def p_opt_with(p):
    '''opt_with : WITH item
                | empty'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None

def p_break_command(p):
    '''break_command : BREAK item'''
    print(f"BREAK, \"{p[2]}\"")
    p[0] = ("BREAK", p[2])

def p_throw_obj_command(p):
    '''throw_obj_command : THROW item ON item'''
    print(f"THROW, \"{p[2]}\", \"{p[4]}\"")
    p[0] = ("THROW", p[2], p[4])

def p_drop_command(p):
    '''drop_command : DROP item'''
    print(f"DROP, \"{p[2]}\"")
    p[0] = ("DROP", p[2])

def p_clean_command(p):
    '''clean_command : CLEAN item'''
    print(f"CLEAN, \"{p[2]}\"")
    p[0] = ("CLEAN", p[2])

def p_climb_command(p):
    '''climb_command : CLIMB item'''
    print(f"CLIMB, \"{p[2]}\"")
    p[0] = ("CLIMB", p[2])

def p_open_command(p):
    '''open_command : OPEN item'''
    print(f"OPEN, \"{p[2]}\"")
    p[0] = ("OPEN", p[2])

def p_close_command(p):
    '''close_command : CLOSE item'''
    print(f"CLOSE, \"{p[2]}\"")
    p[0] = ("CLOSE", p[2])

def p_lock_command(p):
    '''lock_command : LOCK item opt_with'''
    if p[3]:
        print(f"LOCK, \"{p[2]}\", \"{p[3]}\"")
        p[0] = ("LOCK", p[2], p[3])
    else:
        print(f"LOCK, \"{p[2]}\"")
        p[0] = ("LOCK", p[2])

def p_unlock_command(p):
    '''unlock_command : UNLOCK item opt_with'''
    if p[3]:
        print(f"UNLOCK, \"{p[2]}\", \"{p[3]}\"")
        p[0] = ("UNLOCK", p[2], p[3])
    else:
        print(f"UNLOCK, \"{p[2]}\"")
        p[0] = ("UNLOCK", p[2])

def p_fill_command(p):
    '''fill_command : FILL item fill_prep item'''
    print(f"FILL, \"{p[2]}\", \"{p[4]}\"")
    p[0] = ("FILL", p[2], p[4])

def p_fill_prep(p):
    '''fill_prep : WITH
                 | FROM'''
    p[0] = p[1]

def p_pour_command(p):
    '''pour_command : POUR item INTO item'''
    print(f"POUR, \"{p[2]}\", \"{p[4]}\"")
    p[0] = ("POUR", p[2], p[4])

def p_insert_command(p):
    '''insert_command : INSERT item INTO item'''
    print(f"INSERT, \"{p[2]}\", \"{p[4]}\"")
    p[0] = ("INSERT", p[2], p[4])

def p_remove_command(p):
    '''remove_command : REMOVE item FROM item'''
    print(f"REMOVE, \"{p[2]}\", \"{p[4]}\"")
    p[0] = ("REMOVE", p[2], p[4])

def p_set_command(p):
    '''set_command : SET item TO item'''
    print(f"SET, \"{p[2]}\", \"{p[4]}\"")
    p[0] = ("SET", p[2], p[4])

def p_spread_command(p):
    '''spread_command : SPREAD item opt_on'''
    if p[2] and p[3]:
        print(f"SPREAD, \"{p[2]}\", \"{p[3]}\"")
        p[0] = ("SPREAD", p[2], p[3])
    else:
        print(f"SPREAD, \"{p[2]}\"")
        p[0] = ("SPREAD", p[2])

def p_squeeze_command(p):
    '''squeeze_command : SQUEEZE item'''
    print(f"SQUEEZE, \"{p[2]}\"")
    p[0] = ("SQUEEZE", p[2])

#########################################
# Consumable commands
#########################################

def p_consumable_command(p):
    '''consumable_command : eat_command
                          | drink_command
    '''
    p[0] = p[1]

def p_eat_command(p):
    '''eat_command : EAT item'''
    print(f"EAT, \"{p[2]}\"")
    p[0] = ("EAT", p[2])

def p_drink_command(p):
    '''drink_command : DRINK item'''
    print(f"DRINK, \"{p[2]}\"")
    p[0] = ("DRINK", p[2])

#########################################
# Interactions with living things
#########################################

def p_living_command(p):
    '''living_command : wake_command
                      | attack_command
                      | throw_living_command
                      | buy_command
                      | show_command
                      | embrace_command
                      | feed_command
                      | give_command
    '''
    p[0] = p[1]

def p_wake_command(p):
    '''wake_command : WAKE item'''
    print(f"WAKE, \"{p[2]}\"")
    p[0] = ("WAKE", p[2])

def p_attack_command(p):
    '''attack_command : ATTACK item opt_with'''
    if p[2] and p[3]:
        print(f"ATTACK, \"{p[2]}\", \"{p[3]}\"")
        p[0] = ("ATTACK", p[2], p[3])
    else:
        print(f"ATTACK, \"{p[2]}\"")
        p[0] = ("ATTACK", p[2])

def p_throw_living_command(p):
    '''throw_living_command : THROW item ON item'''
    print(f"THROW, \"{p[2]}\", \"{p[4]}\"")
    p[0] = ("THROW", p[2], p[4])

def p_buy_command(p):
    '''buy_command : BUY opt_quantity item TO item'''
    if p[2]:
        print(f"BUY, \"{p[2]} {p[3]}\", \"{p[5]}\"")
        p[0] = ("BUY", p[2], p[3], p[5])
    else:
        print(f"BUY, \"{p[3]}\", \"{p[5]}\"")
        p[0] = ("BUY", p[3], p[5])

def p_opt_quantity(p):
    '''opt_quantity : NUMBER
                    | empty'''
    p[0] = p[1]

def p_show_command(p):
    '''show_command : SHOW item TO item'''
    print(f"SHOW, \"{p[2]}\", \"{p[4]}\"")
    p[0] = ("SHOW", p[2], p[4])

def p_embrace_command(p):
    '''embrace_command : EMBRACE item'''
    print(f"EMBRACE, \"{p[2]}\"")
    p[0] = ("EMBRACE", p[2])

def p_feed_command(p):
    '''feed_command : FEED item WITH item'''
    print(f"FEED, \"{p[2]}\", \"{p[4]}\"")
    p[0] = ("FEED", p[2], p[4])

def p_give_command(p):
    '''give_command : GIVE item TO item'''
    print(f"GIVE, \"{p[2]}\", \"{p[4]}\"")
    p[0] = ("GIVE", p[2], p[4])


#########################################
# Voice / Discussions / Text commands
#########################################

def p_voice_command(p):
    '''voice_command : say_command
                     | ask_command
                     | write_command
    '''
    p[0] = p[1]

def p_say_command(p):
    '''say_command : SAY QUOTED TO item
                   | SAY QUOTED'''
    if len(p) == 5:
        print(f"SAY, \"{p[2]}\", \"{p[4]}\"")
        p[0] = ("SAY", p[2], p[4])
    else:
        print(f"SAY, \"{p[2]}\"")
        p[0] = ("SAY", p[2])

def p_ask_command(p):
    '''ask_command : ASK item about_for_on item'''
    print(f"ASK, \"{p[2]}\", \"{p[4]}\"")
    p[0] = ("ASK", p[2], p[4])

def p_about_for_on(p):
    '''about_for_on : ABOUT
                    | FOR
                    | ON'''
    p[0] = p[1]

def p_write_command(p):
    '''write_command : WRITE QUOTED ON item opt_with'''
    if p[5]:
        print(f"WRITE, \"{p[2]}\", \"{p[4]}\", \"{p[5]}\"")
        p[0] = ("WRITE", p[2], p[4], p[5])
    else:
        print(f"WRITE, \"{p[2]}\", \"{p[4]}\"")
        p[0] = ("WRITE", p[2], p[4])

#########################################
# Interaction with yourself
#########################################

def p_self_command(p):
    '''self_command : wear_command
                    | undress_command
                    | inventory_command
                    | wait_command
                    | sleep_command
                    | sit_command
                    | lie_command
                    | stand_command
    '''
    p[0] = p[1]

def p_wear_command(p):
    '''wear_command : WEAR item'''
    print(f"WEAR, \"{p[2]}\"")
    p[0] = ("WEAR", p[2])

def p_undress_command(p):
    '''undress_command : UNDRESS item'''
    print(f"UNDRESS, \"{p[2]}\"")
    p[0] = ("UNDRESS", p[2])

def p_inventory_command(p):
    '''inventory_command : INVENTORY'''
    print("INVENTORY")
    p[0] = ("INVENTORY",)

# We already defined WAIT earlier in observation; here it is re-used.
def p_wait_command(p):
    '''wait_command : WAIT opt_item'''
    if p[2]:
        print(f"WAIT, \"{p[2]}\"")
        p[0] = ("WAIT", p[2])
    else:
        print("WAIT")
        p[0] = ("WAIT",)

def p_sleep_command(p):
    '''sleep_command : SLEEP'''
    print("SLEEP")
    p[0] = ("SLEEP",)

def p_sit_command(p):
    '''sit_command : SIT ON item'''
    print(f"SIT, \"{p[3]}\"")
    p[0] = ("SIT", p[3])

def p_lie_command(p):
    '''lie_command : LIE opt_down ON item'''
    # Allow "lie on" or "lie down on"
    print(f"LIE, \"{p[4]}\"")
    p[0] = ("LIE", p[4])

def p_opt_down(p):
    '''opt_down : WORD
                | empty'''
    # If the word is "down", ignore it.
    if p[1] and p[1].lower() == "down":
        p[0] = p[1]
    else:
        p[0] = None

def p_stand_command(p):
    '''stand_command : STAND opt_up'''
    # "stand" or "stand up"
    print("STAND")
    p[0] = ("STAND",)

def p_opt_up(p):
    '''opt_up : WORD
              | empty'''
    if p[1] and p[1].lower() == "up":
        p[0] = p[1]
    else:
        p[0] = None

#########################################
# Random commands
#########################################

def p_random_command(p):
    '''random_command : DANCE
                      | CHANT
                      | JUMP
                      | THINK
    '''
    cmd = p[1].upper()
    print(cmd)
    p[0] = (cmd,)

#########################################
# System commands
#########################################

def p_system_command(p):
    '''system_command : save_command
                      | quit_command
                      | load_command
                      | restart_command
                      | score_command
                      | help_command
    '''
    p[0] = p[1]

def p_save_command(p):
    '''save_command : SAVE opt_item'''
    if p[2]:
        print(f"SAVE, \"{p[2]}\"")
        p[0] = ("SAVE", p[2])
    else:
        print("SAVE")
        p[0] = ("SAVE",)

def p_quit_command(p):
    '''quit_command : QUIT'''
    print("QUIT")
    p[0] = ("QUIT",)

def p_load_command(p):
    '''load_command : LOAD item'''
    print(f"LOAD, \"{p[2]}\"")
    p[0] = ("LOAD", p[2])

def p_restart_command(p):
    '''restart_command : RESTART'''
    print("RESTART")
    p[0] = ("RESTART",)

def p_score_command(p):
    '''score_command : SCORE'''
    print("SCORE")
    p[0] = ("SCORE",)

def p_help_command(p):
    '''help_command : HELP'''
    print("HELP")
    p[0] = ("HELP",)

#########################################
# Helper productions
#########################################

def p_item(p):
    '''item : item WORD
            | WORD
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + " " + p[2]

def p_opt_item(p):
    '''opt_item : item
                | empty'''
    p[0] = p[1]

def p_empty(p):
    'empty :'
    p[0] = None

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

#########################################
# Build the parser
#########################################

parser = yacc.yacc()

#########################################
# Main interactive loop
#########################################

if __name__ == '__main__':
    print("Interactive Fiction Command Parser (type 'quit' to exit)")
    while True:
        try:
            s = input('> ')
        except EOFError:
            break
        if not s:
            continue
        # Exit condition:
        if s.strip().lower() in ['quit', 'q']:
            print("Exiting parser.")
            break
        result = parser.parse(s)
