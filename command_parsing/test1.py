import re

# Define command patterns
COMMANDS = {
    "OBSERVATION": [
        ["see", "look", "l"],
        ["recap"],
        ["brief (.+)"],
        ["watch", "describe (.+)"],
        ["examine", "inspect", "check", "x (.+)"],
        ["rummage", "search (.+)"],
        ["hear", "listen ?(.+)?"],
        ["touch", "feel (.+)"],
        ["read (.+) ?(page (\d+))?"],
        ["taste (.+)"],
        ["smell", "sniff (.+)"],
    ],
    "DISPLACEMENT": [
        ["go", "move", "mv", "displace", "d", "walk", "run", "sprint (.+)"],
    ],
    "OBJECT INTERACTION": [
        ["take", "carry", "hold", "pick", "pick up (.+)"],
        ["put", "move", "displace (.+) (in|on|above|into) (.+)"],
        ["push", "press", "apply force on (.+)"],
        ["pull (.+)"],
        ["attach", "tie (.+) to (.+) ?(with (.+))?"],
        ["break", "destroy (.+)"],
        ["throw (.+) on (.+)"],
        ["throw", "drop", "discard", "get off (.+)"],
        ["clean", "rub", "scrub", "sweep", "polish", "shine", "wash", "wipe (.+)"],
        ["use (.+) ?(on (.+))?"],
        ["climb (.+)"],
        ["open (.+)"],
        ["close", "shut (.+)"],
        ["lock (.+) ?(with (.+))?"],
        ["unlock (.+) ?(with (.+))?"],
        ["fill (.+) (with|from) (.+)"],
        ["pour (.+) into (.+)"],
        ["insert (.+) into (.+)"],
        ["remove (.+) from (.+)"],
        ["set (.+) to (.+)"],
        ["spread (.+) ?(on (.+))?"],
        ["squeeze", "squash (.+)"],
    ],
    "CONSUMABLE INTERACTION": [
        ["consume", "eat (.+)"],
        ["drink", "sip", "swallow (.+)"],
    ],
    "LIVING INTERACTION": [
        ["awake", "wake", "wake up (.+)"],
        ["attack", "smash", "fight", "hit", "hurt", "kill", "murder", "punch", "slice", "thump", "torture", "wreck (.+) ?(with (.+))?"],
        ["throw (.+) on (.+)"],
        ["buy", "purchase ?(.+)? (.+) to (.+)"],
        ["show", "display", "present (.+) to (.+)"],
        ["embrace", "hug", "kiss (.+)"],
        ["feed (.+) with (.+)"],
        ["give", "offer (.+) (.+)"],
        ["give", "offer (.+) to (.+)"],
    ],
    "TEXT INTERACTION": [
        ["say", "tell", "ask", "answer", "shout \"(.+)\" to (.+)"],
        ["ask (.+) (about|for|on) (.+)"],
        ["write \"(.+)\" on (.+) ?(with (.+))?"],
    ],
    "SELF INTERACTION": [
        ["wear", "dress (.+)"],
        ["remove", "take off", "strip", "pull off", "shed (.+)"],
        ["inventory", "inv", "i"],
        ["wait ?(.+)?"],
        ["sleep", "nap"],
        ["sit on (.+)"],
        ["lie", "lie down on (.+)"],
        ["stand", "stand up"],
    ],
    "MISC": [
        ["dance"],
        ["chant", "sing"],
        ["jump", "hop"],
        ["think"],
    ],
    "SYSTEM": [
        ["save ?(.+)?"],
        ["quit", "q"],
        ["load", "restore (.+)"],
        ["restart"],
        ["score"],
        ["help"],
    ],
}

def parse_command(user_input):
    user_input = user_input.lower()
    for category, patterns in COMMANDS.items():
        for pattern_group in patterns:
            regex = "|".join(pattern_group)
            match = re.fullmatch(regex, user_input)
            if match:
                command = pattern_group[0].split(" ")[0].upper()
                args = [g for g in match.groups() if g]
                print(f"{command}, {', '.join(f'\"{arg}\"' for arg in args)}")
                return
    print("UNKNOWN COMMAND")

# Example usage
if __name__ == "__main__":
    test_commands = [
        "use the great screwdriver on the damaged machine",
        "wait",
        "wait 1 hour",
        "take golden key",
        "attack the bandit with the sword",
        "fill the glass from the sink"
    ]
    for cmd in test_commands:
        parse_command(cmd)
