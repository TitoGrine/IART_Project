## IART Project 1

First Project of IART (Artificial Inteligence - 3rd year of Integrated Master Degree in Computer Engineering).  
The goal of the project was to build a one player puzzle game and create a program capable of solving various levels
using appropriate search algorithms, such as, Depth First Search, Breath First Search, Uniform Cost Search and A*, while
testing different heuristics. The performance of each algorithm had to be measured in order to compare the results.  
The choosen game was [Zhed](http://www.playzhed.com/).  
For more information about the assignment check the [project's specification](https://github.com/TitoGrine/IART_Project/blob/master/Project_1/docs/Trabalho1_IA_2019_20.pdf) (Portuguese).

### Course Information

* All the course's information can be viewed [here](https://sigarra.up.pt/feup/en/ucurr_geral.ficha_uc_view?pv_ocorrencia_id=436449).

### Requirements

 - **Python3**: it has been tested to work with versions 3.7 and 3.8.
 - **Pygame** (for the game option): This can be installed through pip ( ```pip install pygame``` ) or with your package manager of choice.


### Usage

```python run.py {game, solver} [<board_number> <algorithm>]```

**Options**:  
- **game** - runs the interface made for the game  
- **solver** - runs the solver for the given board_number, with the respective algorithm  
- **board_number** - number between 1 and 100  
- **algorithm** - one fo the following: 'dfs', 'bfs', 'iterative_dfs', 'uniform_cost', 'a_star'  


### Authors

* **André Rocha** - [andrefmrocha](https://github.com/andrefmrocha)
* **Tito Griné** - [TitoGrine](https://github.com/TitoGrine)
* **Vítor Ventuzelos** - [BerserkingIdiot](https://github.com/BerserkingIdiot)

### Evaluation

**Project Grade:** 19.50
