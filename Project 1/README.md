### Requirements
 - **Python3**: it has been tested to work with versions 3.7 and 3.8.
 - **Pygame** (for the game option): This can be installed through pip ( ```pip install pygame``` ) or with your package manager of choice.


### Usage

```python run.py {game, solver} [<board_number> <algorithm>]```

> **Options**:
>    - **game** - runs the interface made for the game
>    - **solver** - runs the solver for the given board_number, with the respective algorithm 
>    - **board_number** - number between 1 and 100
>    - **algorithm** - one fo the following: 'dfs', 'bfs', 'iterative_dfs', 'uniform_cost', 'a_star'