from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from functions import *

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def hello_world():
    f = open('log_file.json', 'r')
    content = f.read()
    f.close()
    return jsonify(data = content)

@app.route("/ping")
@cross_origin()
def pong():
    return jsonify(data = "pong")

@app.route("/solve/<int:entrance>/<int:seed>")
def solve(entrance, seed):
    maze = generate_maze('assets/25-25-seed-702.png')
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

    solves, open_list, closed_list = astar(maze, start, end)

    for i in range(len(solves)):
        print_maze_with_path(maze, solves[i], open_list, closed_list, i)

    f = open('log_file.json', 'r')
    tree = f.read()
    f.close()

    f = open('teste.json', 'r')
    open_and_closed_lists = f.read()
    f.close()
    
    return jsonify(tree = tree, open_and_closed_lists = open_and_closed_lists)
