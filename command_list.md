# List of commands

## Observation

- `(see/look/l)`
- `recap`
- `brief [something/someone]`
- `(watch/describe) [something/someone]`
- `(examine/inspect/check/x) [something/someone]`
- `(rummage) [something]`: search if there is no objects inside something
- `(hear/listen) ?{[something/someone]}`
- `(touch/feel) [something/someone]`
- `read [something] ?{page [number]}`
- `taste [something]`
- `(smell/sniff) [something/someone]`

## Displacement

- `(go/move/mv/displace/d/walk/run/sprint) [direction]`: Go, displace to the direction

Atomic-direction:
    - North / N
    - South / S
    - East / E
    - West / W
    - Up / Above / U / A
    - Down / Below / B / D

Direction -> [atomic-direction] | [atomic-direction][atomic-direction]

## Interact with objects

- `(take/carry/hold/pick/pick up) [something]`: Take an object in the inventory (ex: `take golden key`)
- `(put/move/displace) [something] (in/on/above/into) [somewhere/something]`: Put an object somewhere
- `(push/press/apply force on) [something]`: (ex: `Press button`, `Push the lever`)
- `pull [something]`: (ex: `Pull the lever`)
- `(attach/tie) [something/someone] to [something/someone] ?{with [something]}`: (ex: `attach the bandit to the crochet with a chain`)
- `(break/destroy) [something]`: Needs the object to be destroyable (ex: `break the glass`)
- `throw [something] on [something]`: (ex: `throw rock to the window`)
- `(throw/drop/discard/get off) [something]`: Remove the object from your inventory (ex: `throw the bag`)
- `(clean/rub/scrub/sweep/polish/shine/wash/wipe) [something]`: Cleaning something, maybe in order to reveal something
- `use [something] ?{on [something/someone]}`: (ex: `use the door`, `use the ladder`)
- `climb [something]`
- `open [something]`
- `(close/shut) [something]`
- `lock [something] ?{with [something]}`
- `unlock [something] ?{with [something]}`
- `fill [something] (with/from) [something]`: (ex: `Fill the glass from the sink`, `fill the pitcher from the barrel of beer`)
- `(pour) [something] into [something]`: (ex: `Pour `)
- `insert [something] into [something]`
- `remove [something] from [something]`: removing it from
- `set [something] to [state]`
- `spread [something] ?{on [something/someone]}`
- `(squeeze/squash) [something]`

## Interaction with consommable

- `(consume/eat) [something]`
- `(drink/sip/swallow) [something]`

## Interactions with living things

- `(awake/wake/wake up) [someone]`
- `(attack/smash/fight/hit/hurt/kill/murder/punch/slice/thump/torture/wreck) [someone] ?{with [something]}`: (ex: `attack the bandit with the sword`)
- `throw [something] on [someone]`: (ex: `throw a rock to the bandit`)
- `(buy/purchase) ?{quantity} [something] to [someone]`: (ex: `Buy a bottle of milk to the shop keeper` / `Buy 5 sandwiches to the shop keeper`) -> Automatically use the assignated price that can be known by reading the descriptions, the ticket, ...
- `(show/display/present) [something/someone] to [someone]`
- `(embrace/hug/kiss) [someone]`
- `(feed) [someone] with [something]`
- `(give/offer) [someone] [something]`
- `(give/offer) [something] to [someone]`

## Voice / Discussions / Text

- `(say / tell / ask / answer / shout ) "..." to [someone / something]`
- `ask [someone] (about/for/on) [something/someone]`
- `(write) "..." on [something] ?{with [something]}` : (ex: `Write "Hello" on the old paper with pencil`)

## Interaction with yourself

- `(wear/dress) [something]`: Wear a clothe, or an equipment
- `(remove/take off/strip/pull off/shed) [something]`: Take off a clothe, or an equipment
- `(inventory/inv/i)`: List the objects of your inventory
- `wait ?{[duration]}`
- `(sleep/nap)`
- `sit on [something]`: (ex: `sit on chair`)
- `(lie/lie down) on [something]`: (ex: `lie down on the bed`)
- `(stand/stand up)`

## Random things

- `dance`
- `(chant/sing)`
- `(jump/hop)`
- `(think)`

## System commands

- `save ?{filepath of game save}`
- `(quit/q)`
- `(load/restore) {filepath of game save}`
- `restart`
- `score`
