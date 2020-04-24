from gameboard import *
grid = Grid(11, 11)
grid.set_grid()
grid.test()
# print(grid.grid)
for y in range(len(grid.grid)):
    for x in range(len(grid.grid[0])):
        if grid.grid[x][y] == 10:
            print("* ", end="")
        elif grid.grid[x][y] == 3:
            print("o ", end="")
        elif x == 5 and y == 0:
            print("@ ", end="")
        else:
            print(". ", end="")
    print()
cell = grid.get_cell((5, 0))
tail = grid.get_cell((4, 6))
end = grid.get_cell((8, 8))

print(grid.count_reachable_area(cell))

print(grid.a_star(cell, [tail]))


# print("check neighbor")
# neighbors = grid.get_neighbors(cell)
# grid.set_cell((1, 6), 0)
# for y in range(len(grid.grid)):
#     for x in range(len(grid.grid[0])):
#         if grid.grid[x][y] == 10:
#             print("* ", end="")
#         elif grid.grid[x][y] == 3:
#             print("o ", end="")
#         elif x == 2 and y == 5:
#             print("@ ", end="")
#         else:
#             print(". ", end="")
#     print()
# for neighbor in neighbors:
#     print("direction:", cell.get_direction(neighbor))
#     print(grid.count_reachable_area(neighbor))

