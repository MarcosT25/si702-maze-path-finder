from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from functions import *
from PIL import Image, ImageFont
from pilmoji import Pilmoji

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/ping")
@cross_origin()
def pong():
    return jsonify(data = "pong")

# Report examples: (2, 1, 80) and (2, 2, 80) returns total cost 32 and 34 respectively
@app.route("/solve/<int:entrance>/<int:heuristic>/<int:seed>")
def solve(entrance, heuristic, seed):
    maze = generate_maze('assets/25-25-seed-702.png')

    open_some_walls(maze)
    print_maze(maze, 'assets/opened_maze')

    resize_image('assets/opened_maze.png')

    if entrance == 1:
        start = (9, 0)
    elif entrance == 2:
        start = (15, 0)
    elif entrance == 3:
        start = (24, 9)
    elif entrance == 4:
        start = (24, 15)
    elif entrance == 5:
        start = (15, 24)
    elif entrance == 6:
        start = (9, 24)
    elif entrance == 7:
        start = (0, 15)
    elif entrance == 8:
        start = (0, 9)

    end = generate_trophy_location(maze, seed)
    print(f'O troféu foi gerado no ponto {end}')

    solves = astar(maze, heuristic, start, end)

    for i in range(len(solves)):
        print_maze_with_path(maze, solves[i], end, i)

    f = open('last_tree.json', 'r')
    tree = f.read()
    f.close()

    f = open('all_lists.json', 'r')
    open_and_closed_lists = f.read()
    f.close()

    resize_image('assets/1solve.png')

    import base64
    with open("assets/1solve-resized.png", "rb") as img_file:
        image = base64.b64encode(img_file.read()).decode("utf-8")
    
    return jsonify(tree = tree, open_and_closed_lists = open_and_closed_lists, image = image)
