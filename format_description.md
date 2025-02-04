# Interactive Fiction format description

This document explains the file format for this interactive fiction engine.

## General information

For now, I will first make a json file format work. Then I will think about potentially making a more human-readable system.

There is no differences between a base game file, and a game save file.
This means that we can directly load and play from a savegame, but the catch is that it just takes a little more space on the disk to store.
Why it's planned like that for the moment ? I would say it is because I want flexibility in the world construction and actions possible, like for examle, I want possible the fact to change items, destroy them, to have actions that can destroy rooms, or permanently change them, ...

This engines will be built for turn by turn actions, so a turn can represents a command of a player for instance.

There will also be a system of custom actions and variables, so the game creator can have flexibility to do things that it would have been difficult without.








