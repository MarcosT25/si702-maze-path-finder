from PIL import Image
from math import floor, sqrt
import random

def generate_maze(image):
    with Image.open(image) as img:
        rgb_img = img.convert('RGB')
        maze = []
        for y in range(81):
            maze.append([])
            for x in range(81):
                pixel = 0 if rgb_img.getpixel(((x * floor(rgb_img.width/81)) + 2, (y * floor(rgb_img.width/81)) + 2)) == (255, 255, 255) else 1
                maze[y].append(pixel)
    return maze

def print_maze(maze, title):
    new_img = Image.new('RGB', (81, 81), color = (255, 255, 255))
    for x in range(81):
        for y in range(81):
            if (maze[x][y]) != 0:
                new_img.putpixel((x, y), (0, 0, 0)) if maze[x][y] == 1 else new_img.putpixel((x, y), (255, 0, 0))
    new_img.save(title + '.png')

def print_maze_with_path(maze, path, i):
    new_img = Image.new('RGB', (81, 81), color = (255, 255, 255))
    for x in range(81):
        for y in range(81):
            if (maze[x][y]) != 0:
                new_img.putpixel((x, y), (0, 0, 0)) if maze[x][y] == 1 else new_img.putpixel((x, y), (255, 0, 0))
    for point in path:
        new_img.putpixel(point, (255, 0, 0))
    new_img.save(str(i + 1) + 'solve.png')

def open_some_walls(maze):
    random.seed(2)
    squares = [2, 27, 53, 79]
    for i in range(3):
        for j in range(3):
            wall = [1, 1]
            # for um caminho, ou não for uma parede que a direita e esquerda seja caminho ou cima e baixo seja parede
            while maze[wall[1]][wall[0]] != 1 or (not (maze[wall[1] - 1][wall[0]] == 0 and maze[wall[1] + 1][wall[0]] == 0) and not (maze[wall[1]][wall[0] - 1] == 0 and maze[wall[1]][wall[0] + 1] == 0)):
                wall[0] = random.randint(squares[i], squares[1 + i])
                wall[1] = random.randint(squares[j], squares[1 + j])
            maze[wall[1]][wall[0]] = 0
            if (i == 1 and j == 1):
                for k in range(40):
                    wall = [1, 1]
                    while maze[wall[1]][wall[0]] != 1 or not (maze[wall[1] - 1][wall[0]] == 0 and maze[wall[1] + 1][wall[0]] == 0):
                        wall[0] = random.randint(squares[i], squares[1 + i])
                        wall[1] = random.randint(squares[j], squares[1 + j])
                    maze[wall[1]][wall[0]] = 0
    return maze

def generate_trophy_location(maze):
    random.seed(5)
    location = [0, 0]
    while maze[location[1]][location[0]] == 1:
        location[0] = random.randint(27, 53)
        location[1] = random.randint(27, 53)
    return (location[0], location[1])


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __str__(self):
        return f'{self.position}'


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []
    solves = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            solves.append(path[::-1])
            for open_node in open_list:
                if open_node.f <= current_node.f:
                    break
            else:
                return solves # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            flag = False

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    flag = True

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = sqrt(((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2))
            child.f = child.g + child.h

            # Child is already in the open list
            # for open_node in open_list:
            #     if child == open_node and child.g > open_node.g:
            #         flag = True

            # Add the child to the open list
            if not flag: open_list.append(child)


def main():

    maze = generate_maze('702.png')
    print_maze(maze, 'old')
    open_some_walls(maze)
    print_maze(maze, 'new-1')

    start = (27, 0)
    # end = (27, 80)
    end = generate_trophy_location(maze)

    solves = astar(maze, start, end)
    print(f'A estrela encontrou {len(solves)} soluções')

    for i in range(len(solves)):
        print_maze_with_path(maze, solves[i], i)


if __name__ == '__main__':
    main()
            