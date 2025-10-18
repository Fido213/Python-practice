import pyxel
import random

# --- 1. Global Game State Variables ---
SCREEN_SIZE_W = 64
SCREEN_SIZE_H = 64
GRID_WIDTH = 64
GRID_HEIGHT = 64
CELL_SIZE = 1  # Each cell is 1x1 pixel
ALIVE_COLOR = 7  # White
DEAD_COLOR = 0  # Black
grid = []


# --- 2. Initialize Grid ---
def init_grid():
    global grid
    for y in range(GRID_HEIGHT):
        row = []  # so basically, for every y value (height), we create a new
        # row
        for x in range(GRID_WIDTH):
            # so for every x value (row), we create a new cell in that row
            # (all dead)
            row.append(random.randint(0, 1))  # Start with all cells dead
        grid.append(row)
    print(f"\n Initial Grid: \n {grid}")


# --- 3. Update Function (Game Logic) ---
def update():
    global grid
    # now since changes to the grid need to be done simultaneously,
    # we will create a copy of the grid to store changes
    new_grid = [row[:] for row in grid]  # Deep copy of the grid
    for row in range(GRID_HEIGHT):
        # print(f"\n at row {row} in update \n")
        # so it goes over every line in the list, say:
        # we have [[0,0,0],
        #          [0,0,0],
        #          [0,0,0]]
        # the grid height is 3, so it goes over every row
        # the height of the actual grid is 64
        # so it goes over every row starting from 0
        # then for every row, it goes over each value (here with a temp var
        # being a cell) in that row, so in the example above:
        # height = 3
        # first iteration row = 0
        # then it goes over the next for loop below
        for cell in range(GRID_WIDTH):
            # so row = 0, cell in range grid width (3)
            # so it goes over every cell in that row
            # cell = 0, cell = 1, cell = 2
            # then it goes back to the first for loop
            current_cell_value = grid[row][cell]
            # legit translates to:
            # in the grid, at row 0, and in that row
            # at index 0 (cell 0), get its value
            # since grid is constant, it doesnt change
            # row is varying from well the for loop, and same for cell
            # ------------------------------------------------------------

            # now to check values around it, we just need to manipulate
            # the indexes of row and cell:
            # we just need to add limits to avoid index errors
            # so for upper cells:
            # our limits would be if row > 0, since we cant go above row 0
            upper_cell_value = grid[row - 1][cell] if row > 0 else None
            # so if row > 0, we can get the value of the cell above it

            # for lower cell values:
            # our limits would be if row < GRID_HEIGHT - 1
            lower_cell_value = grid[row + 1][cell] if row < GRID_HEIGHT - 1 else None
            # so if row is smaller than the height - 1 (since its indexed from 0)
            # , we can get the value of the cell below it

            # for left cell value:
            left_cell_value = grid[row][cell - 1] if cell > 0 else None
            # cell 0 is the leftest most cell so anything before that is invalid
            # same for the right cell value, except we take into account the width
            # and not the index
            right_cell_value = grid[row][cell + 1] if cell < GRID_WIDTH - 1 else None
            # we also need to check the diagonals
            # the diagonals are just combinations of the above indexes
            # so upper left diagonal is just upper cell and left cell
            # so we check if both upper and left cells are not None,
            # if they are then no diagonals
            upper_left_diagonal = (
                grid[row - 1][cell - 1] if row > 0 and cell > 0 else None
            )
            # we basically just combined both logics
            upper_right_diagonal = (
                grid[row - 1][cell + 1] if row > 0 and cell < GRID_WIDTH - 1 else None
            )
            lower_left_diagonal = (
                grid[row + 1][cell - 1] if row < GRID_HEIGHT - 1 and cell > 0 else None
            )
            lower_right_diagonal = (
                grid[row + 1][cell + 1]
                if row < GRID_HEIGHT - 1 and cell < GRID_WIDTH - 1
                else None
            )
            # ------------------------------------------------------------

            # now that we have every cell value and its neighbours we apply
            # the rules of the game of life
            # to keep things simple, lets check if the current cell is alive
            # since the alive cell has the most rules to check
            # for efficiency we can calculate all neighbours sum once
            total_neighbours = (
                (upper_cell_value == 1)
                + (lower_cell_value == 1)
                + (left_cell_value == 1)
                + (right_cell_value == 1)
                + (upper_left_diagonal == 1)
                + (upper_right_diagonal == 1)
                + (lower_left_diagonal == 1)
                + (lower_right_diagonal == 1)
            )
            if current_cell_value == 1:
                if total_neighbours < 2:
                    # underpopulation
                    # if less than 2 neighbours are alive, the cell dies
                    # we check if the sum of alive neighbours is less than 2
                    # since True is 1 and False is 0, we can sum them up
                    new_grid[row][cell] = 0  # cell dies
                elif total_neighbours == 3 or total_neighbours == 2:
                    # survival
                    # if 2 or 3 neighbours are alive, the cell stays alive
                    new_grid[row][cell] = 1  # cell stays alive
                elif total_neighbours > 3:
                    # overpopulation
                    # if more than 3 neighbours are alive, the cell dies
                    new_grid[row][cell] = 0  # cell dies
            else:
                if total_neighbours == 3:
                    # reproduction
                    # if exactly 3 neighbours are alive, the cell becomes alive
                    new_grid[row][cell] = 1  # cell becomes alive
            # print(
            #     f" at cell {cell} in row {row} "
            #     f"with cell value = {current_cell_value}"
            #     f" and upper cell value = {upper_cell_value} at row {row - 1}, cell {cell}"
            #     f" and lower cell value = {lower_cell_value} at row {row + 1}, cell {cell}"
            #     f" and left cell value = {left_cell_value} at row {row}, cell {cell - 1}"
            #     f" and right cell value = {right_cell_value} at row {row}, cell {cell + 1}"
            #     f" and upper left diagonal value = {upper_left_diagonal} at row {row - 1}, cell {cell - 1}"
            #     f" and upper right diagonal value = {upper_right_diagonal} at row {row - 1}, cell {cell + 1}"
            #     f" and lower left diagonal value = {lower_left_diagonal} at row {row + 1}, cell {cell - 1}"
            #     f" and lower right diagonal value = {lower_right_diagonal} at row {row + 1}, cell {cell + 1}"
            # )
            # then we simply replace the value in the new grid
    grid = new_grid  # update the grid to the new grid
    print(new_grid)


# now that we have the update function done, we can move on to the draw function
# the update function gives us the y x coordinates of every cell
# and its value (alive or dead)
# we just need to convert that to pixels on the screen
# luckily, our pixel size is 1, so every cell corresponds to 1 pixel
# so we can directly draw the cells on the screen based on their values
# and y x coordinates (since the grid size is same as screen size)


def draw():
    pyxel.cls(DEAD_COLOR)  # Clear screen with dead color
    for row in range(GRID_HEIGHT):
        for cell in range(GRID_WIDTH):
            cell_value = grid[row][cell]
            color = ALIVE_COLOR if cell_value == 1 else DEAD_COLOR
            pyxel.pset(cell, row, color)  # Draw pixel at (cell, row)


# --- 4. Initialization and Run ---
def game_of_life():
    init_grid()
    pyxel.init(SCREEN_SIZE_W, SCREEN_SIZE_H, title="Conway's Game of Life", fps=120)
    pyxel.run(update, draw)


game_of_life()
