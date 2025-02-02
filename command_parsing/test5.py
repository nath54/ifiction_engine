
#
def parse_command(command: str) -> list[str]:

    #
    command = command.strip().lower()

    ##################################
    ###### OBSERVATION COMMANDS ######
    ##################################

    #### COMMAND LOOK AROUND
    # `(see/look around/look)`: Observe the surroundings and get a description of the current area.

    # TODO
    pass

    #### COMMAND RECAP
    # `(recap)`: Summarize recent events, clues, or interactions.

    # TODO
    pass

    #### COMMAND BRIEF
    #  `brief [something/someone]`: Give a short description of something or someone. (ex: `brief ancient statue`)

    # TODO
    pass

    #### COMMAND DESCRIBE
    # `(watch/describe) [something/someone]`: Give a detailed description of an object or character. (ex: `describe mysterious painting`)

    # TODO
    pass

    #### COMMAND EXAMINE
    # `(examine/inspect/check) [something/someone]`: Closely inspect something or someone to reveal details. (ex: `examine old diary`)

    # TODO
    pass

    #### COMMAND RUMMAGE
    # `(rummage/search) [something]`: Search a container or place for hidden items. (ex: `rummage drawer`)

    # TODO
    pass

    #### COMMAND LISTEN
    # `(hear/listen) ?{[something/someone]}`: Focus on sounds or listen to someone. (ex: `listen music`)

    # TODO
    pass

    #### COMMAND FEEL
    # `(touch/feel) [something/someone]`: Sense the texture, temperature, or state of an object or person. (ex: `feel statue`)

    # TODO
    pass

    #### COMMAND READ
    # `read [something] ?{page [number]}`: Read a written document, optionally specifying a page. (ex: `read journal page 2`)

    # TODO
    pass

    #### COMMAND TASTE
    # `taste [something]`: Try tasting an object. (ex: `taste soup`)

    # TODO
    pass

    #### COMMAND SMELL
    # `(smell/sniff) [something/someone]`: Identify the scent of something or someone. (ex: `sniff flower`)

    # TODO
    pass

    ###################################
    ###### DISPLACEMENT COMMANDS ######
    ###################################

    #### COMMAND GO
    # `(go/displace/walk/run/sprint) [direction]`: Move in the specified direction. (ex: `go north`)

    # TODO
    pass

    ##########################################
    ###### OBJECT INTERACTIONS COMMANDS ######
    ##########################################

    #### COMMAND TAKE
    # `(take/carry/hold/pick/pick up) [something]`: Pick up an object and add it to the inventory. (ex: `take golden key`)

    # TODO
    pass

    #### COMMAND PUT
    # `(put/move) [something] (in/on/above/into) [somewhere/something]`: Place an object somewhere. (ex: `put book on shelf`)

    # TODO
    pass

    #### COMMAND PUSH
    # `(push/press/apply force on) [something]`: Apply force to an object. (ex: `press button`)

    # TODO
    pass

    #### COMMAND PULL
    # `pull [something]`: Pull an object. (ex: `pull lever`)

    # TODO
    pass

    #### COMMAND ATTACH
    # `(attach/tie) [something/someone] to [something/someone] ?{with [something]}`: Attach an object to something. (ex: `attach bandit to chair with rope`)

    # TODO
    pass

    #### COMMAND BREAK
    # `(break/destroy) [something]`: Destroy a destructible object. (ex: `break glass`)

    # TODO
    pass

    #### COMMAND THROW
    # `throw [something] on [something]`: Throw an object at another object. (ex: `throw rock on window`)
    # `throw [something] on [someone]`: Throw an object at someone. (ex: `throw rock on bandit`)

    # TODO
    pass

    #### COMMAND DROP
    # `(drop/discard/get off) [something]`: Remove an object from inventory. (ex: `drop bag`)

    # TODO
    pass

    #### COMMAND CLEAN
    # `(clean/rub/scrub/sweep/polish/shine/wash/wipe) [something]`: Clean something. (ex: `wash painting`)

    # TODO
    pass

    #### COMMAND USE
    # `use [something] ?{on [something/someone]}`: Use an object, optionally on something or someone. (ex: `use key on door`)

    # TODO
    pass

    #### COMMAND CLIMB
    # `climb [something]`: Climb an object. (ex: `climb tree`)

    # TODO
    pass

    #### COMMAND OPEN
    # `open [something]`: Open a door, chest, or other container. (ex: `open chest`)

    # TODO
    pass

    #### COMMAND CLOSE
    # `(close/shut) [something]`: Close an object. (ex: `close window`)

    # TODO
    pass

    #### COMMAND LOCK
    # `lock [something] ?{with [something]}`: Lock an object. (ex: `lock door with golden key`)

    # TODO
    pass

    #### COMMAND UNLOCK
    # `unlock [something] ?{with [something]}`: Unlock an object. (ex: `unlock chest with rusty key`)

    # TODO
    pass

    #### COMMAND FILL
    # `fill [something] (with/from) [something]`: Fill a container. (ex: `fill bottle with water`)

    # TODO
    pass

    #### COMMAND POUR
    # `(pour) [something] into [something]`: Pour a liquid. (ex: `pour coffee into cup`)

    # TODO
    pass

    #### COMMAND INSERT
    # `insert [something] into [something]`: Insert an item. (ex: `insert coin into vending machine`)

    # TODO
    pass

    #### COMMAND REMOVE
    # `remove [something] from [something]`: Take something out of another object. (ex: `remove book from shelf`)

    # TODO
    pass

    #### COMMAND SET
    # `set [something] to [state]`: Adjust an object’s state. (ex: `set lamp to on`)

    # TODO
    pass

    #### COMMAND SPREAD
    # `spread [something] ?{on [something/someone]}`: Apply something over a surface. (ex: `spread butter on bread`)

    # TODO
    pass

    #### COMMAND SQUEEZE
    # `(squeeze/squash) [something]`: Press or crush an object. (ex: `squeeze lemon`)

    # TODO
    pass

    ##############################################
    ###### CONSUMABLE INTERACTIONS COMMANDS ######
    ##############################################

    #### COMMAND EAT
    # `(consume/eat) [something]`: Eat an item. (ex: `eat apple`)

    # TODO
    pass

    #### COMMAND DRINK
    # `(drink/sip/swallow) [something]`: Drink a liquid. (ex: `drink potion`)

    # TODO
    pass

    ##########################################
    ###### LIVING INTERACTIONS COMMANDS ######
    ##########################################

    #### COMMAND AWAKE
    # `(awake/wake/wake up) [someone]`: Wake a sleeping person. (ex: `wake up guard`)

    # TODO
    pass

    #### COMMAND ATTACK
    # `(attack/smash/fight/hit/hurt/kill/murder/punch/slice/thump/torture/wreck) [someone] ?{with [something]}`: Attack someone. (ex: `attack bandit with sword`)

    # TODO
    pass

    #### COMMAND BUY
    # `(buy/purchase) ?{quantity} [something] to [someone]`: Buy an item. (ex: `buy 2 potions to merchant`)

    # TODO
    pass

    #### COMMAND SHOW
    # `(show/display/present) [something/someone] to [someone]`: Show something to someone. (ex: `show passport to guard`)

    # TODO
    pass

    #### COMMAND EMBRACE
    # `(embrace/hug/kiss) [someone]`: Perform an affectionate gesture. (ex: `hug friend`)

    # TODO
    pass

    #### COMMAND FEED
    # `(feed) [someone] with [something]`: Give food to someone. (ex: `feed dog with bone`)

    # TODO
    pass

    #### COMMAND GIVE
    # `(give/offer) [something] to [someone]`: Alternative phrasing. (ex: `offer flower to lover`)

    # TODO
    pass

    ###################################
    ###### VOICE / TEXT COMMANDS ######
    ###################################

    #### COMMAND SAY
    # `(say/tell/ask/answer/shout) "..." to [someone/something]`: Communicate verbally with a character or object. (ex: `say "Hello" to guard`)

    # TODO
    pass

    #### COMMAND ASK
    # `ask [someone] (about/for/on) [something/someone]`: Ask someone for information. (ex: `ask merchant about potion`)

    # TODO
    pass

    #### COMMAND WRITE
    # `(write) "..." on [something] ?{with [something]}`: Write a message on an object. (ex: `write "Hello" on the old paper with pencil`)

    # TODO
    pass

    #########################################
    ###### PLAYER INTERACTION COMMANDS ######
    #########################################

    #### COMMAND WEAR
    # `(wear/dress) [something]`: Wear clothing or equipment. (ex: `wear helmet`)

    # TODO
    pass

    #### COMMAND TAKE OFF
    # `(remove/take off/strip/pull off/shed) [something]`: Take off clothing or equipment. (ex: `remove jacket`)

    # TODO
    pass

    #### COMMAND INVENTORY
    # `(inventory)`: List the objects in your inventory. (ex: `inv`)

    # TODO
    pass

    #### COMMAND WAIT
    # `wait ?{[duration]}`: Pause and let time pass. (ex: `wait 5 minutes`)

    # TODO
    pass

    #### COMMAND SLEEP
    # `(sleep/nap)`: Rest and possibly recover. (ex: `sleep`)

    # TODO
    pass

    #### COMMAND SIT
    # `sit on [something]`: Take a seat on an object. (ex: `sit on chair`)

    # TODO
    pass

    #### COMMAND LIE DOWN
    # `(lie/lie down) on [something]`: Lie down on an object. (ex: `lie down on the bed`)

    # TODO
    pass

    #### COMMAND STAND UP
    # `(stand/stand up)`: Return to a standing position. (ex: `stand up`)

    # TODO
    pass

    #############################
    ###### RANDOM COMMANDS ######
    #############################

    #### COMMAND DANCE
    # `dance`: Perform a dance. (ex: `dance`)

    # TODO
    pass

    #### COMMAND SING
    # `(chant/sing)`: Sing or chant something. (ex: `sing`)

    # TODO
    pass

    #### COMMAND JUMP
    # `(jump/hop)`: Jump up or forward. (ex: `jump`)

    # TODO
    pass

    #### COMMAND THINK
    # `(think)`: Reflect or contemplate. (ex: `think`)

    # TODO
    pass

    #############################
    ###### SYSTEM COMMANDS ######
    #############################

    #### COMMAND QUIT
    # `(quit)`: Quit the game. (ex: `quit`)

    # TODO
    pass

    #### COMMAND SAVE
    # `save ?{filepath of game save}`: Save the game. (ex: `save game1.sav`)

    # TODO
    pass

    #### COMMAND LOAD
    # `(load/restore) {filepath of game save}`: Load a saved game. (ex: `load game1.sav`)

    # TODO
    pass

    #### COMMAND RESTART
    # `restart`: Restart the game. (ex: `restart`)

    # TODO
    pass

    #### COMMAND SCORE
    # `score`: Show current progress. (ex: `score`)

    # TODO
    pass

    #### COMMAND HELP
    # `help`: Show the list of commands. (ex: `help`)

    # TODO
    pass

    ##############################
    ###### UNKNOWN COMMANDS ######
    ##############################

    #
    return []  # Commande vide












