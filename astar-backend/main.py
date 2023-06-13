from Node import Node
from functions import *

def main():
    """For the report we used the following seeds for random events:
    open_some_walls seed = 2
    generate_trophy_location seed = 5
    third-party maze generator seed = 702"""
    

    maze = generate_maze('assets/25-25-seed-702.png')
    print_maze(maze, 'assets/original_maze')

    start = (9, 0)
    # end = (0, 9)
    end = generate_trophy_location(maze, 2)
    print(f'O troféu foi gerado no ponto {end}')

    solves, open_list, closed_list = astar(maze, start, end)
    print(f'A estrela encontrou {len(solves)} soluções')

    for i in range(len(solves)):
        print_maze_with_path(maze, solves[i], open_list, closed_list, i)


if __name__ == '__main__':
    main()
            