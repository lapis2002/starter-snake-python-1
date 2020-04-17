from A_star import *
grid = Grid(6, 6)
grid.init_grid()
print(grid.grid)
for y in range(len(grid.grid)):
    for x in range(len(grid.grid[0])):
        if grid.grid[x][y] == 10:
            print("* ", end="")
        elif grid.grid[x][y] == 7:
            print("o ", end="")
        else:
            print(". ", end="")
    print()
print("start (0,0)")
print("end (5,5)")
grid.process((0, 0), (5, 5))

print("-"*20)
print("start (5,0)")
print("end (5,5)")
grid.process((5, 0), (5, 5))
