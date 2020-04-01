from zhed.view.menus import main_menu
from zhed.statistics import algorithms, run_puzzle
import sys

if len(sys.argv) == 2 and sys.argv[1] == "game":
    main_menu()
elif len(sys.argv) == 4 and sys.argv[1] == "solver" and sys.argv[2].isdigit() and sys.argv[3] in algorithms:
    run_puzzle(int(sys.argv[2]), sys.argv[3])
else:
    print("usage: run.py {game, solver} [<board_number> <algorithm>]")
