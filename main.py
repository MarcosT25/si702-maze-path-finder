from PIL import Image

with Image.open('702.png') as img:
    rgb_img = img.convert('RGB')
    maze = []
    for y in range(81):
        maze.append([])
        for x in range(81):
            pixel = 0 if rgb_img.getpixel(((x * 16) + 5, (y * 16) + 5)) == (255, 255, 255) else 1
            maze[y].append(pixel)
            
    for i in range(80):
        print(maze[i]) 

    new_img = Image.new('RGB', (81, 81), color = (255, 255, 255))
    for x in range(81):
        for y in range(81):
            if (maze[x][y]):
                new_img.putpixel((x, y), (0, 0, 0))
            

    new_img.show()