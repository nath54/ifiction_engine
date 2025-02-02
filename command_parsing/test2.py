#!/usr/bin/env python3
import re
import sys

# Each entry is a tuple: (pattern, canonical_command, argument_keys)
# The regex uses named groups for the arguments. The pattern order matters.
# This list covers the command categories provided.
patterns = [
    # === Observation commands ===
    (re.compile(r'^(?P<cmd>see|look|l)(?:\s+(?P<target>.+))?$', re.IGNORECASE), "LOOK", ["target"]),
    (re.compile(r'^(?P<cmd>recap)$', re.IGNORECASE), "RECAP", []),
    (re.compile(r'^(?P<cmd>brief)\s+(?P<target>.+)$', re.IGNORECASE), "BRIEF", ["target"]),
    (re.compile(r'^(?P<cmd>watch|describe)\s+(?P<target>.+)$', re.IGNORECASE), "WATCH", ["target"]),
    (re.compile(r'^(?P<cmd>examine|inspect|check|x)\s+(?P<target>.+)$', re.IGNORECASE), "EXAMINE", ["target"]),
    (re.compile(r'^(?P<cmd>rummage|search)\s+(?P<target>.+)$', re.IGNORECASE), "SEARCH", ["target"]),
    (re.compile(r'^(?P<cmd>hear|listen)(?:\s+(?P<target>.+))?$', re.IGNORECASE), "HEAR", ["target"]),
    (re.compile(r'^(?P<cmd>touch|feel)\s+(?P<target>.+)$', re.IGNORECASE), "TOUCH", ["target"]),
    (re.compile(r'^(?P<cmd>read)\s+(?P<target>.+?)(?:\s+page\s+(?P<page>\d+))?$', re.IGNORECASE), "READ", ["target", "page"]),
    (re.compile(r'^(?P<cmd>taste)\s+(?P<target>.+)$', re.IGNORECASE), "TASTE", ["target"]),
    (re.compile(r'^(?P<cmd>smell|sniff)\s+(?P<target>.+)$', re.IGNORECASE), "SMELL", ["target"]),

    # === Displacement commands ===
    (re.compile(r'^(?P<cmd>go|move|mv|displace|d|walk|run|sprint)\s+(?P<direction>.+)$', re.IGNORECASE), "GO", ["direction"]),

    # === Interact with objects ===
    (re.compile(r'^(?P<cmd>take|carry|hold|pick(?: up)?)\s+(?P<target>.+)$', re.IGNORECASE), "TAKE", ["target"]),
    (re.compile(r'^(?P<cmd>put|move|displace)\s+(?P<item>.+)\s+(in|on|above|into)\s+(?P<target>.+)$', re.IGNORECASE), "PUT", ["item", "target"]),
    (re.compile(r'^(?P<cmd>push|press|apply force on)\s+(?P<target>.+)$', re.IGNORECASE), "PUSH", ["target"]),
    (re.compile(r'^(?P<cmd>pull)\s+(?P<target>.+)$', re.IGNORECASE), "PULL", ["target"]),
    (re.compile(r'^(?P<cmd>attach|tie)\s+(?P<src>.+)\s+to\s+(?P<dest>.+?)(?:\s+with\s+(?P<with>.+))?$', re.IGNORECASE), "ATTACH", ["src", "dest", "with"]),
    (re.compile(r'^(?P<cmd>break|destroy)\s+(?P<target>.+)$', re.IGNORECASE), "BREAK", ["target"]),
    (re.compile(r'^(?P<cmd>throw)\s+(?P<item>.+)\s+on\s+(?P<target>.+)$', re.IGNORECASE), "THROW", ["item", "target"]),
    (re.compile(r'^(?P<cmd>throw|drop|discard|get off)\s+(?P<target>.+)$', re.IGNORECASE), "DROP", ["target"]),
    (re.compile(r'^(?P<cmd>clean|rub|scrub|sweep|polish|shine|wash|wipe)\s+(?P<target>.+)$', re.IGNORECASE), "CLEAN", ["target"]),
    (re.compile(r'^(?P<cmd>use)\s+(?P<item>.+?)(?:\s+on\s+(?P<target>.+))?$', re.IGNORECASE), "USE", ["item", "target"]),
    (re.compile(r'^(?P<cmd>climb)\s+(?P<target>.+)$', re.IGNORECASE), "CLIMB", ["target"]),
    (re.compile(r'^(?P<cmd>open)\s+(?P<target>.+)$', re.IGNORECASE), "OPEN", ["target"]),
    (re.compile(r'^(?P<cmd>close|shut)\s+(?P<target>.+)$', re.IGNORECASE), "CLOSE", ["target"]),
    (re.compile(r'^(?P<cmd>lock)\s+(?P<target>.+?)(?:\s+with\s+(?P<with>.+))?$', re.IGNORECASE), "LOCK", ["target", "with"]),
    (re.compile(r'^(?P<cmd>unlock)\s+(?P<target>.+?)(?:\s+with\s+(?P<with>.+))?$', re.IGNORECASE), "UNLOCK", ["target", "with"]),
    (re.compile(r'^(?P<cmd>fill)\s+(?P<target>.+)\s+(with|from)\s+(?P<source>.+)$', re.IGNORECASE), "FILL", ["target", "source"]),
    (re.compile(r'^(?P<cmd>pour)\s+(?P<item>.+)\s+into\s+(?P<target>.+)$', re.IGNORECASE), "POUR", ["item", "target"]),
    (re.compile(r'^(?P<cmd>insert)\s+(?P<item>.+)\s+into\s+(?P<target>.+)$', re.IGNORECASE), "INSERT", ["item", "target"]),
    (re.compile(r'^(?P<cmd>remove)\s+(?P<item>.+)\s+from\s+(?P<target>.+)$', re.IGNORECASE), "REMOVE", ["item", "target"]),
    (re.compile(r'^(?P<cmd>set)\s+(?P<item>.+)\s+to\s+(?P<state>.+)$', re.IGNORECASE), "SET", ["item", "state"]),
    (re.compile(r'^(?P<cmd>spread)\s+(?P<item>.+?)(?:\s+on\s+(?P<target>.+))?$', re.IGNORECASE), "SPREAD", ["item", "target"]),
    (re.compile(r'^(?P<cmd>squeeze|squash)\s+(?P<target>.+)$', re.IGNORECASE), "SQUEEZE", ["target"]),

    # === Interaction with consumable ===
    (re.compile(r'^(?P<cmd>consume|eat)\s+(?P<target>.+)$', re.IGNORECASE), "EAT", ["target"]),
    (re.compile(r'^(?P<cmd>drink|sip|swallow)\s+(?P<target>.+)$', re.IGNORECASE), "DRINK", ["target"]),

    # === Interactions with living things ===
    (re.compile(r'^(?P<cmd>awake|wake|wake up)\s+(?P<target>.+)$', re.IGNORECASE), "AWAKE", ["target"]),
    (re.compile(r'^(?P<cmd>attack|smash|fight|hit|hurt|kill|murder|punch|slice|thump|torture|wreck)\s+(?P<target>.+?)(?:\s+with\s+(?P<with>.+))?$', re.IGNORECASE), "ATTACK", ["target", "with"]),
    # Note: the "throw ... on ..." pattern for living things is already defined above.
    (re.compile(r'^(?P<cmd>buy|purchase)(?:\s+(?P<quantity>\d+))?\s+(?P<item>.+?)\s+to\s+(?P<target>.+)$', re.IGNORECASE), "BUY", ["quantity", "item", "target"]),
    (re.compile(r'^(?P<cmd>show|display|present)\s+(?P<item>.+?)\s+to\s+(?P<target>.+)$', re.IGNORECASE), "SHOW", ["item", "target"]),
    (re.compile(r'^(?P<cmd>embrace|hug|kiss)\s+(?P<target>.+)$', re.IGNORECASE), "HUG", ["target"]),
    (re.compile(r'^(?P<cmd>feed)\s+(?P<target>.+?)\s+with\s+(?P<item>.+)$', re.IGNORECASE), "FEED", ["target", "item"]),
    (re.compile(r'^(?P<cmd>give|offer)\s+(?:(?P<target>.+?)\s+(?P<item>.+)|(?P<item_alt>.+?)\s+to\s+(?P<target_alt>.+))$', re.IGNORECASE), "GIVE", ["target", "item"]),

    # === Voice / Discussions / Text ===
    (re.compile(r'^(?P<cmd>say|tell|ask|answer|shout)\s+"(?P<quote>.+)"\s+to\s+(?P<target>.+)$', re.IGNORECASE), "SAY", ["quote", "target"]),
    (re.compile(r'^(?P<cmd>ask)\s+(?P<target>.+?)\s+(about|for|on)\s+(?P<item>.+)$', re.IGNORECASE), "ASK", ["target", "item"]),
    (re.compile(r'^(?P<cmd>write)\s+"(?P<quote>.+)"\s+on\s+(?P<target>.+?)(?:\s+with\s+(?P<with>.+))?$', re.IGNORECASE), "WRITE", ["quote", "target", "with"]),

    # === Interaction with yourself ===
    (re.compile(r'^(?P<cmd>wear|dress)\s+(?P<target>.+)$', re.IGNORECASE), "WEAR", ["target"]),
    (re.compile(r'^(?P<cmd>remove|take off|strip|pull off|shed)\s+(?P<target>.+)$', re.IGNORECASE), "REMOVE", ["target"]),
    (re.compile(r'^(?P<cmd>inventory|inv|i)$', re.IGNORECASE), "INVENTORY", []),
    (re.compile(r'^(?P<cmd>wait)(?:\s+(?P<duration>.+))?$', re.IGNORECASE), "WAIT", ["duration"]),
    (re.compile(r'^(?P<cmd>sleep|nap)$', re.IGNORECASE), "SLEEP", []),
    (re.compile(r'^(?P<cmd>sit on)\s+(?P<target>.+)$', re.IGNORECASE), "SIT", ["target"]),
    (re.compile(r'^(?P<cmd>lie|lie down)\s+on\s+(?P<target>.+)$', re.IGNORECASE), "LIE", ["target"]),
    (re.compile(r'^(?P<cmd>stand|stand up)$', re.IGNORECASE), "STAND", []),

    # === Random things ===
    (re.compile(r'^(?P<cmd>dance)$', re.IGNORECASE), "DANCE", []),
    (re.compile(r'^(?P<cmd>chant|sing)$', re.IGNORECASE), "CHANT", []),
    (re.compile(r'^(?P<cmd>jump|hop)$', re.IGNORECASE), "JUMP", []),
    (re.compile(r'^(?P<cmd>think)$', re.IGNORECASE), "THINK", []),

    # === System commands ===
    (re.compile(r'^(?P<cmd>save)(?:\s+(?P<filepath>.+))?$', re.IGNORECASE), "SAVE", ["filepath"]),
    (re.compile(r'^(?P<cmd>quit|q)$', re.IGNORECASE), "QUIT", []),
    (re.compile(r'^(?P<cmd>load|restore)\s+(?P<filepath>.+)$', re.IGNORECASE), "LOAD", ["filepath"]),
    (re.compile(r'^(?P<cmd>restart)$', re.IGNORECASE), "RESTART", []),
    (re.compile(r'^(?P<cmd>score)$', re.IGNORECASE), "SCORE", []),
    (re.compile(r'^(?P<cmd>help)$', re.IGNORECASE), "HELP", []),
]


def parse_command(command_str):
    """
    Attempts to match the input command_str against each defined pattern.
    When a match is found, returns a tuple (command, args_list) where:
      - command is the canonical command name (upper-case)
      - args_list is a list of non-empty arguments in the order defined by the pattern.
    If no match is found, returns (None, None).
    """
    for pattern, canon_cmd, arg_keys in patterns:
        match = pattern.fullmatch(command_str.strip())
        if match:
            groups = match.groupdict()
            # Special case: sometimes we have alternative groups (like item/item_alt)
            # We'll try to use the first non-empty value if present.
            args = []
            for key in arg_keys:
                value = groups.get(key)
                if value is None:
                    # try alternate key if defined (for the "give" command, for instance)
                    if key == "target" and groups.get("target_alt"):
                        value = groups.get("target_alt")
                    elif key == "item" and groups.get("item_alt"):
                        value = groups.get("item_alt")
                if value is not None and value.strip() != "":
                    args.append(value.strip())
            return canon_cmd, args
    return None, None


def print_parsed_command(canon_cmd, args):
    """
    Prints the parsed command in the required format.
    For example, for command "USE" with two arguments, it prints:
      USE, "arg1", "arg2"
    """
    if canon_cmd is None:
        print("Unknown command!")
        return

    # Start with the command name in uppercase.
    out = canon_cmd.upper()
    if args:
        # Append each argument in quotes.
        for arg in args:
            out += ', "{}"'.format(arg)
    print(out)


def main():
    print("Interactive Fiction Engine Parser")
    print("Enter a command (or 'exit' to quit):")
    while True:
        try:
            user_input = input("> ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if user_input.strip().lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        canon_cmd, args = parse_command(user_input)
        print_parsed_command(canon_cmd, args)


if __name__ == '__main__':
    main()
