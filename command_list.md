# List of commands

## Observation

- `(see/look around/look)`: Observe the surroundings and get a description of the current area.
- `(recap/history) ?{number_of_turns}`: Summarize the `after_each_player_turn` number of turns, by default, it resumes 5. User can also enter `all` to get the full story and events and actions until now.
- `brief [something/someone]`: Give a short description of something or someone. (ex: `brief ancient statue`)
- `(watch/describe) [something/someone]`: Give a detailed description of an object or character. (ex: `describe mysterious painting`)
- `(examine/inspect/check) [something/someone]`: Closely inspect something or someone to reveal details. (ex: `examine old diary`)
- `(rummage/search) [something]`: Search a container or place for hidden items. (ex: `rummage drawer`)
- `(hear/listen) ?{TO} ?{[something/someone]}`: Focus on sounds or listen to someone. (ex: `listen music`)
- `(touch/feel) [something/someone]`: Sense the texture, temperature, or state of an object or person. (ex: `feel statue`)
- `read [something] ?{page [number]}`: Read a written document, optionally specifying a page. (ex: `read journal page 2`)
- `taste [something]`: Try tasting an object. (ex: `taste soup`)
- `(smell/sniff) [something/someone]`: Identify the scent of something or someone. (ex: `sniff flower`)

## Displacement

- `(go/walk/run/sprint) [direction]`: Move in the specified direction. (ex: `go north`)

Atomic-direction:
    - North
    - South
    - East
    - West
    - Up
    - Down

Directions:
    - North
    - South
    - West
    - East
    - Up
    - Down
    - North West / North-West / NorthWest
    - North East / North-East / NorthEast
    - North Up / North-Up / NorthUp
    - North Down / North-Down / NorthDown
    - South West / South-West / SouthWest
    - South East / South-East / SouthEast
    - South Up / South-Up / SouthUp
    - South Down / South-Down / SouthDown

## Interact with objects

- `(take/carry/hold/pick up/pick) [something]`: Pick up an object and add it to the inventory. (ex: `take golden key`)
- `(put/move) [something] (into/in/on) [somewhere/something]`: Place an object somewhere. (ex: `put book on shelf`)
- `(push/press/apply force on) [something]`: Apply force to an object. (ex: `press button`)
- `pull [something]`: Pull an object. (ex: `pull lever`)
- `(attach/tie) [something/someone] to [something/someone] ?{with [something]}`: Attach an object to something. (ex: `attach bandit to chair with rope`)
- `(break/destroy) [something]`: Destroy a destructible object. (ex: `break glass`)
- `throw [something] on [something/someone]`: Throw an object at another object. (ex: `throw rock on window`)
- `(drop/discard) [something]`: Remove an object from inventory. (ex: `drop bag`)
- `(clean/rub/scrub/sweep/polish/shine/wash/wipe) [something]`: Clean something. (ex: `wash painting`)
- `use [something] ?{on [something/someone]}`: Use an object, optionally on something or someone. (ex: `use key on door`)
- `climb [something]`: Climb an object. (ex: `climb tree`)
- `open [something]`: Open a door, chest, or other container. (ex: `open chest`)
- `(close) [something]`: Close an object. (ex: `close window`)
- `lock [something] ?{with [something]}`: Lock an object. (ex: `lock door with golden key`)
- `unlock [something] ?{with [something]}`: Unlock an object. (ex: `unlock chest with rusty key`)
- `fill [something] (with/from) [something]`: Fill a container. (ex: `fill bottle with water`)
- `(pour) [something] (into/in) [something]`: Pour a liquid. (ex: `pour coffee into cup`)
- `insert [something] (into/in) [something]`: Insert an item. (ex: `insert coin into vending machine`)
- `remove [something] from [something]`: Take something out of another object. (ex: `remove book from shelf`)
- `set [something] to [state]`: Adjust an object’s state. (ex: `set lamp to on`)
- `spread [something] ?{on [something/someone]}`: Apply something over a surface. (ex: `spread butter on bread`)
- `(squeeze/squash) [something]`: Press or crush an object. (ex: `squeeze lemon`)

## Interaction with consumables

- `(consume/eat) [something]`: Eat an item. (ex: `eat apple`)
- `(drink/sip/swallow) [something]`: Drink a liquid. (ex: `drink potion`)

## Interactions with living things

- `(awake/wake/wake up) [someone]`: Wake a sleeping person. (ex: `wake up guard`)
- `(attack/smash/fight/hit/hurt/kill/murder/punch/slice) [someone] ?{with [something]}`: Attack someone. (ex: `attack bandit with sword`)
- `(buy/purchase) ?{[quantity] of} [something] to [someone]`: Buy an item. (ex: `buy 2 potions to merchant`)
- `(show/display/present) [something/someone] to [someone]`: Show something to someone. (ex: `show passport to guard`)
- `(embrace/hug/kiss) [someone]`: Perform an affectionate gesture. (ex: `hug friend`)
- `(feed) [someone] with [something]`: Give food to someone. (ex: `feed dog with bone`)
- `(give/offer) [something] to [someone]`: Alternative phrasing. (ex: `offer flower to lover`)

## Voice / Discussions / Text

- `(say/tell/answer/shout) "..." ?{to [someone/something]}`: Communicate verbally with a character or object. (ex: `say "Hello" to guard`)
- `ask [someone] (about/for/on) [something/someone]`: Ask someone for information. (ex: `ask merchant about potion`)
- `(write) "..." on [something] ?{with [something]}`: Write a message on an object. (ex: `write "Hello" on the old paper with pencil`). ***Note:** if there is already a writen thing on the object, and you want only the text you want to write, you can try to erase the previous text on the object.*
- `(erase/delete/efface/rub out) [something] ?{with [something]}`: Erase everything that is writen on an object. (Ex: `rub out the paper with gum` or `erase the blackboard with the brush`)

## Interaction with yourself

- `(wear/dress) [something]`: Wear clothing or equipment. (ex: `wear helmet`)
- `(undress/take off/strip/pull off/shed) [something]`: Take off clothing or equipment. (ex: `remove jacket`)
- `(inventory/stock)`: List the objects in your inventory. (ex: `inv`)
- `wait ?{[duration]}`: Pause and let time pass. (ex: `wait 5 minutes`)
- `(sleep/nap)`: Rest and possibly recover. (ex: `sleep`)
- `sit on [something]`: Take a seat on an object. (ex: `sit on chair`)
- `(lie/lie down) on [something]`: Lie down on an object. (ex: `lie down on the bed`)
- `(stand/stand up)`: Return to a standing position. (ex: `stand up`)

## Random things

- `dance`: Perform a dance. (ex: `dance`)
- `(chant/sing)`: Sing or chant something. (ex: `sing`)
- `(jump/hop)`: Jump up. (ex: `jump`)
- `(think)`: Reflect or contemplate. (ex: `think`)

## System commands

- `save ?{filepath of game save}`: Save the game. (ex: `save game1.json`)
- `(quit/q)`: Quit the game. (ex: `quit`)
- `(load/restore) filepath of game save`: Load a saved game. (ex: `load game1.json`)
- `score`: Show current progress. (ex: `score`)
- `help`: Show the list of commands. (ex: `help`)