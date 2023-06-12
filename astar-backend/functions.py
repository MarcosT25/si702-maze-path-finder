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

def print_maze_with_path(maze, path, open_list, closed_list, i):
    new_img = Image.new('RGB', (25, 25), color = (255, 255, 255))
    for x in range(25):
        for y in range(25):
            if (maze[x][y]) == 1:
                new_img.putpixel((x, y), (0, 0, 0))
    # for point in open_list:
    #     new_img.putpixel((point.position), (0, 0, 255))
    # for point in closed_list:
    #     new_img.putpixel((point.position), (0, 255, 0))
    for point in path:
        new_img.putpixel(point, (255, 0, 0))
    new_img.save('assets/' + str(i + 1) + 'solve.png')

def open_some_walls(maze):
    random.seed(2)
    squares = [2, 27, 53, 79]
    for i in range(3):
        for j in range(3):     
            for k in range(20):
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
    return (location[0], location[1])

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

def astar(maze, start, end):
    """Returns a list of possible paths to the goal"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []
    paths = []
    trees = []
    lists = []

    # Add the start node
    open_list.append(start_node)
    i = 0
    
    last_name = ""
    # Loop until you find the end
    while len(open_list) > 0:

        new_dict = {}
        new_dict["Lista aberta"] = []
        for node in open_list:
            new_dict["Lista aberta"].append(str(node.position))
        new_dict["Lista fechada"] = []
        for node in closed_list:
            new_dict["Lista fechada"].append(str(node.position))
        
        lists.append(new_dict)

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Start node dictionary
        if len(trees) == 0:
            node_dict = {}
            node_dict["name"] = str(current_node.position)
            node_dict["value"] = round(current_node.f, 2)
            node_dict["expand"] = "true"
            node_dict["color"] = "blue"
        else:
            node_dict = trees[-1]
            search_by_name(last_name, node_dict)["color"] = "black"

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
            paths.append(path[::-1]) # Append reversed path

            for open_node in open_list:
                if open_node.f <= current_node.f:
                    break
            else:
                for point in paths[0]:
                    search_by_name(str(point), node_dict)["color"] = "red"
                f = open('log_file.json', 'wt')
                f.write(str(node_dict))
                f.close()
                f = open('log_file.json', 'rt')
                content = f.read()
                content = content.replace("'", '"')
                f.close()
                f = open('log_file.json', 'wt')
                f.write(content)
                f.close()

                f = open('teste.json', 'wt')
                f.write(str(lists))
                f.close()

                f = open('teste.json', 'rt')
                content = f.read()
                content = content.replace("'", '"')
                f.close()
                f = open('teste.json', 'wt')
                f.write(content)
                f.close()
                return paths, open_list, closed_list

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
            child.h = sqrt(((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2))
            child.f = child.g + child.h

            # Child is on the open list
            for open_node in open_list:
                if open_node.position == child.position and child.position != end_node.position:
                    flag = True

            # Add the child to the open list
            if not flag: 
                open_list.append(child)
                search_by_name(str(current_node.position), node_dict)["children"].append({"name": str(child.position), "value": round(child.f, 2), "expand": "true", "color": "black"})

        trees.append(node_dict)
        last_name = search_by_name(str(current_node.position), node_dict)["name"]
        i += 1
        