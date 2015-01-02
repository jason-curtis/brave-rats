brave-rats
==========

Brave Rats game engine.

Modelled after the simple, addictive, impossible-to-master card game "BraveRats - A Game by Seiji Kanai". 
All game design credit to Seiji.
You are encouraged to treat your and your friends to a physical copy of the game, which is available on amazon.com and at a game store near you! 

This code duplicates the original game mechanics to allow for on-computer gameplay and to enable building and studying Brave Rats AIs.

## Usage
###Install

    git clone https://github.com/thatneat/brave-rats
    pip install -r requirements.txt # OR, at the moment, just 'pip install enum34'
    cd brave-rats
    
### To play a game against the AI

    python brave_rats.py
    
### Building your own AI
See brains/example_ai.py for an example AI function.
To play a game against your own AI:

1. Name your AI's brain function as something that ends with '`_brain_fn`'. For this example, if your AI is called `burninator` the function should be called `burninator_brain_fn`
2. Place your AI's .py module somewhere inside the brave-rats directory. It will be automatically detected and imported.
3. Start the round by calling: `python brave_rats.py --red-brain human --blue-brain burninator`

### More options

    python brave_rats.py --help

### Tournament Mode
This searches the brave-rats directory for brain modules (created using [the instructions above](#building-your-own-ai)) and pits them all against each other for a predetermined set of games, ~~mano a mano~~ rato a rato. This can be used to test AIs against each other.

    python tournament.py
    # For more options
    python tournament.py --help

### To print the results table for individual fights

    python
    >> from brave_rats import fight
    >> fight.print_results_table()
            b=0     b=1     b=2     b=3     b=4     b=5     b=6     b=7
    r=0     h       h       h       h       h       b       h       h
    r=1     h       h       b       r       b2      b       b       r
    r=2     h       r       h       r       b2      b       b       b
    r=3     h       b       b       h       r       b       r       b
    r=4     h       r2      r2      b       h       b       b       b
    r=5     r       r       r       r       r       h       b       b
    r=6     h       r       r       b       r       r       h       b
    r=7     h       b       r       r       r       r       r       h

    >> brave_rats.print_results_table(red_general_played=True)
            b=0     b=1     b=2     b=3     b=4     b=5     b=6     b=7
    r=0     h       h       h       h       h       b       h       h
    r=1     h       r       r       h       b2      b       b       r
    r=2     h       r       r       b       h       b       b       b
    r=3     h       b       b       b       b2      h       r       b
    r=4     h       r2      r2      b       r2      r       h       b
    r=5     r       r       r       r       r       r       r       h
    r=6     h       r       r       b       r       r       r       b
    r=7     h       b       r       r       r       r       r       r

## Issues

Issues I am aware of are listed on the GitHub issues page: https://github.com/thatneat/brave-rats/issues

Suggestions and pull requests are very welcome!
