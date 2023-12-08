# CISC/CMPE 204 Modelling Project

Summary: Our project models a 3x3 slide puzzle - a puzzle in which there is a 3x3 board with 8 numbered tiles placed randomly in eight of the nine positions. The player must slide the tiles around on the board to reach an end configuration where the tiles are sorted from top to bottom in ascending order, from 1 to 8, with the blank space in the bottom right corner. 


## Structure

* `documents`: Contains folders for both of your draft and final submissions. README.md files are included in both.
* `run.py`: General wrapper script that you can choose to use or not. Only requirement is that you implement the one function inside of there for the auto-checks.
* `test.py`: Run this file to confirm that your submission has everything required. This essentially just means it will check for the right files and sufficient theory size.
* `board.py`: The ‘board.py’ file contains a list of tuples which are the positions on the board from (0,0) to (2, 2).
* `input_tiles.py`: The ‘input_tiles.py’ file contains a maximum number of swaps that we want the model to have (which is the minimum number of swaps required to solve the board), and a list of tiles with the same order as the list of positions in the ‘board.py’ file.

## How to run our project.
All of our model propositions and constraints are defined in run.py. You can run our project by running run.py through Docker. 

Variables and how to change the input board and number of swaps to win:
We have several variables, some of which are imported from separate files which are ‘input_tiles.py’ and ‘board.py’. The ‘board.py’ file contains a list of tuples which are the positions on the board from (0,0) to (2, 2). The ‘input_tiles.py’ file contains a maximum number of swaps that we want the model to have (which is the minimum number of swaps required to solve the board), and a list of tiles with the same order as the list of positions in the ‘board.py’ file. The tiles are meant to be changed in the list to different orders to reflect different puzzle boards to solve. Therefore, if you change the order of the tiles in the TILES list in ‘input_tiles.py’ and you change the max_swaps variable to reflect the changed puzzle, that is how you run with a different input board of your choosing. 

For more information on our files and our model, see our report in the final folder in documents. 
