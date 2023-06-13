from PIL import Image
from math import floor, sqrt
import random
from Node import Node

def generate_maze(image):
    with Image.open(image) as img:
        rgb_img = img.convert('RGB')
        maze = []
        for y in range(25):
            maze.append([])
            for x in range(25):
                pixel = 0 if rgb_img.getpixel(((x * floor(rgb_img.width/25)) + 2, (y * floor(rgb_img.width/25)) + 2)) == (255, 255, 255) else 1
                maze[y].append(pixel)
    return maze

def print_maze(maze, title):
    new_img = Image.new('RGB', (25, 25), color = (255, 255, 255))
    for x in range(25):
        for y in range(25):
            if (maze[x][y]) != 0:
                new_img.putpixel((x, y), (0, 0, 0)) if maze[x][y] == 1 else new_img.putpixel((x, y), (255, 0, 0))
    new_img.save(title + '.png')

def print_maze_with_path(maze, path, end, i):
    new_img = Image.new('RGB', (25, 25), color = (255, 255, 255))
    for x in range(25):
        for y in range(25):
            if (maze[x][y]) == 1:
                new_img.putpixel((x, y), (0, 0, 0))
    for point in path:
        new_img.putpixel(point, (255, 0, 0))
    new_img.putpixel(end, (0, 0, 255))
    new_img.save('assets/' + str(i + 1) + 'solve.png')

def resize_image(image):
    with Image.open(image) as img:
        new_image = Image.new('RGB', (25 * 16, 25 * 16), color=(255, 255, 255))
        original_image = img.convert('RGB')
        for x in range(25):
            for y in range(25):
                color = original_image.getpixel((x, y))
                for new_x in range(16):
                    for new_y in range(16):
                        new_image.putpixel((new_x + 16*x, new_y + 16*y), color)
        new_image.save(image[:-4] + '-resized.png')

def open_some_walls(maze):
    random.seed(2)
    squares = [2, 9, 15, 23]
    for i in range(3):
        for j in range(3):     
            for k in range(2):
                wall = [1, 1]
                while maze[wall[1]][wall[0]] != 1 or not (maze[wall[1] - 1][wall[0]] == 0 and maze[wall[1] + 1][wall[0]] == 0):
                    wall[0] = random.randint(squares[i], squares[1 + i])
                    wall[1] = random.randint(squares[j], squares[1 + j])
                maze[wall[1]][wall[0]] = 0
    return maze

def generate_trophy_location(maze, seed):
    random.seed(seed)
    location = [0, 0]
    while maze[location[1]][location[0]] == 1:
        location[0] = random.randint(9, 15)
        location[1] = random.randint(9, 15)
    return (location[1], location[0])

def search_by_name(name, dict):
    result = None
    if dict["name"] == name:
        return dict
    else:
        if "children" in dict:
            for child in dict["children"]:
                result = search_by_name(name, child)
                if result:
                    return result
            return result

def astar(maze, heuristic, start, end):
    """Returns a list of possible paths to the goal, writes json file with last tree and open and closed lists for each expansion"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize open, closed, paths and trees list and a list to save each expansion open and closed lists
    open_list = []  #list of tuples
    closed_list = [] #list of tuples
    paths_list = [] #list of list of tuples
    trees_list = [] #list of dicts
    lists = [] #lists of lists of dicts

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Saves open and closed lists for each expansion
        new_dict = {}
        new_dict["lista_aberta"] = []
        for node in open_list:
            new_dict["lista_aberta"].append(str(node.position))
        new_dict["lista_fechada"] = []
        for node in closed_list:
            new_dict["lista_fechada"].append(str(node.position))
        lists.append(new_dict)

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Start node dictionary
        if len(trees_list) == 0:
            node_dict = {}
            node_dict["name"] = str(current_node.position)
            node_dict["value"] = round(current_node.f, 2)
            node_dict["expand"] = "true"
            node_dict["color"] = "black"
        else:
            node_dict = trees_list[-1]

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
            paths_list.append(path[::-1]) # Append reversed path

            # Saves last open and closed lists for each expansion
            new_dict = {}
            new_dict["lista_aberta"] = []
            for node in open_list:
                new_dict["lista_aberta"].append(str(node.position))
            new_dict["lista_fechada"] = []
            for node in closed_list:
                new_dict["lista_fechada"].append(str(node.position))
            lists.append(new_dict)

            for point in paths_list[0]:
                search_by_name(str(point), node_dict)["color"] = "red"
                f = open('last_tree.json', 'wt')
                f.write(str(node_dict))
                f.close()
                f = open('last_tree.json', 'rt')
                content = f.read()
                content = content.replace("'", '"') # format to official json style
                f.close()
                f = open('last_tree.json', 'wt')
                f.write(content)
                f.close()

                f = open('all_lists.json', 'wt')
                f.write(str(lists))
                f.close()

                f = open('all_lists.json', 'rt')
                content = f.read()
                content = content.replace("'", '"')
                f.close()
                f = open('all_lists.json', 'wt')
                f.write(content)
                f.close()
            
            continue_searching = False
            for open_node in open_list:
                if open_node.f <= current_node.f:
                    continue_searching = True
                    break

            if continue_searching == False:
                
                return paths_list

        # Generate children
        children = []
        search_by_name(str(current_node.position), node_dict)["children"] = []

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
                if child.position == closed_child.position:
                    flag = True

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = sqrt(((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)) if heuristic == 1 else (((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2))
            child.f = child.g + child.h

            # Child is on the open list
            for open_node in open_list:
                if open_node.position == child.position and child.position != end_node.position:
                    flag = True

            # Add the child to the open list
            if not flag: 
                open_list.append(child)
                search_by_name(str(current_node.position), node_dict)["children"].append({"name": str(child.position), "value": round(child.f, 2), "expand": "true", "color": "black"})

        trees_list.append(node_dict)
    return paths_list
        