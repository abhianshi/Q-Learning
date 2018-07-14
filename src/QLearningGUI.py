# Importing libraries and modules
from tkinter import *
from PIL import ImageTk, Image
import time
from tkinter import messagebox
from tkinter.filedialog import askopenfilename


# Start of GUI
root = Tk()
root.title("Q-Learning Grid World")


# Grid Initialization
# Ask the user if he wants to load a pre-deined world map
result = messagebox.showinfo("Choose Location","Give path of Q-Learning Grid World Map")
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

# Read a grid world from pre-defined values
read_file = open(filename, "r")
read_str = str(read_file.read())
read_str = read_str.split("\n")

# Initialize start point
token = read_str[0].split(" ")
init = []
init.append(int(token[0]))
init.append(int(token[1]))

# Initialize goal points
token = read_str[1].split(" ")
goal = []

i = 0
while(i < int(len(token))):
    temp = []
    temp.append(int(token[i]))
    temp.append(int(token[i+1]))
    goal.append(temp)
    i += 2

# Initialize pit points
token = read_str[2].split(" ")
pit = []
i = 0
while(i < int(len(token))):
    temp = []
    temp.append(int(token[i]))
    temp.append(int(token[i+1]))
    pit.append(temp)
    i += 2

# Create grid
grid = []
for i in range(3, len(read_str)):
    token = read_str[i].split(" ")
    if(len(token) != 1):
        grid.append(list(map(int, token)))

# Size of Grid
rows = len(grid)
columns = len(grid[0])


# GUI Parameters
bg_color = "PINK"
fg_color1 = "BLACK"
fg_color2 = "PURPLE"
fontStyle = "Chalkboard"
cell_size = 80
offset = 10

sleep_time = 9.99
exploration = 0.1
isplay = False
isstop = False
deterministic = True

start_images = {}
texts = {}
grids = {}
triangles = {}
robots = {}


# Frames
main_frame = Frame(root, bg = bg_color)
main_frame.pack()

left_frame = Frame(main_frame, bg = bg_color)
left_frame.pack(side=LEFT)

right_frame = Frame(main_frame, bg = bg_color)
right_frame.pack(side=TOP)


# Left Frame Functionality
# Creating a 2D Grid
def createGrid():

    for i in range(0,rows + 1):
        x_start = offset
        y = i * cell_size + offset
        x_end = columns * cell_size + offset
        gridCanvas.create_line([(x_start,y),(x_end,y)])

    for i in range(0,columns + 1):
        y_start = offset
        x = i * cell_size + offset
        y_end = rows * cell_size + offset
        gridCanvas.create_line([(x,y_start),(x,y_end)])

    for i in range(0, rows):
        temp = []
        for j in range(0, columns):
            x = i * cell_size + offset
            y = j * cell_size + offset
            grids[(i,j)] = (x,y)
            temp.append((x,y))

    return grids


# Load all images
def loadImages():
    img_robot = Image.open("/Users/abhianshusingla/Documents/Q Learning/images/robot.png")
    img_robot = img_robot.resize((cell_size, cell_size))
    gridCanvas.img_robot = (ImageTk.PhotoImage(img_robot))

    img_target = Image.open("/Users/abhianshusingla/Documents/Q Learning/images/target.png")
    img_target = img_target.resize((cell_size, cell_size))
    gridCanvas.img_target = (ImageTk.PhotoImage(img_target))

    img_pit = Image.open("/Users/abhianshusingla/Documents/Q Learning/images/fire.png")
    img_pit = img_pit.resize((cell_size, cell_size))
    gridCanvas.img_pit = (ImageTk.PhotoImage(img_pit))

    img_start = Image.open("/Users/abhianshusingla/Documents/Q Learning/images/start.png")
    img_start = img_start.resize((cell_size, cell_size))
    gridCanvas.img_start = (ImageTk.PhotoImage(img_start))

    img_wall = Image.open("/Users/abhianshusingla/Documents/Q Learning/images/wall.png")
    img_wall = img_wall.resize((cell_size, cell_size))
    gridCanvas.img_wall = (ImageTk.PhotoImage(img_wall))


# Draws house at cell coordinates x and y
def drawStart(x,y):
    x1 = grids[(x,y)][0]
    y1 = grids[(x,y)][1]
    start_images[(x,y)] = gridCanvas.create_image(y1, x1, image=gridCanvas.img_start, anchor='nw')
    for i in range(4):
        gridCanvas.itemconfigure(triangles[(x,y)][i], state = 'hidden')
        gridCanvas.itemconfigure(texts[(x,y)][i], state = 'hidden')


# Draws wall at cell coordinates x and y
def drawWall(x,y):
    x1 = grids[(x,y)][0]
    y1 = grids[(x,y)][1]
    gridCanvas.create_image(y1, x1, image=gridCanvas.img_wall, anchor='nw')


# Draws flag at cell coordinates x and y
def drawTarget(x,y):
    x1 = grids[(x,y)][0]
    y1 = grids[(x,y)][1]
    gridCanvas.create_image(y1, x1, image=gridCanvas.img_target, anchor='nw')


# Draws pit at cell coordinates x and y
def drawPit(x,y):
    x1 = grids[(x,y)][0]
    y1 = grids[(x,y)][1]
    gridCanvas.create_image(y1, x1, image=gridCanvas.img_pit, anchor='nw')


# Create Traingle for better visualization
def create_triangle():
    c = 'gold'
    for i in range(rows):
        for j in range(columns):

            val = [i,j]
            if(grid[i][j] != 1 ):
                if(val not in pit):
                    if(val not in goal):

                        x = grids[(i,j)][0]
                        y = grids[(i,j)][1]
                        x1 = x + cell_size/2
                        y1 = y + cell_size/2
                        x2 = x + cell_size/4
                        y2 = y + cell_size/4
                        x3 = x + cell_size * 3/4
                        y3 = y + cell_size * 3/4
                        x4 = x + cell_size
                        y4 = y + cell_size

                        t1 = gridCanvas.create_polygon(y3,x2, y1,x, y2,x2, fill = c, outline = "black")
                        t2 = gridCanvas.create_polygon(y,x1, y2,x2, y2,x3, fill = c, outline = "black")
                        t3 = gridCanvas.create_polygon(y1,x4, y2,x3, y3,x3, fill = c, outline = "black")
                        t4 = gridCanvas.create_polygon(y4,x1, y3,x2, y3,x3, fill = c, outline = "black")

                        triangles[(i,j)] = [t1,t2,t3,t4]


# Create robot at all cell coordinates x and y and hide them
def drawRobot():
    for i in range(rows):
        for j in range(columns):
            if(grid[i][j] != 1):
                x = grids[(i,j)][0]
                y = grids[(i,j)][1]
                robots[(i,j)] = gridCanvas.create_image(y, x, image=gridCanvas.img_robot, anchor='nw', state = 'hidden')

# Show robot at location x and y
def showRobot(x,y):
    key = (x,y)
    if(key in robots):
        gridCanvas.itemconfigure(robots[key], state='normal')

# Hide robot at location x and y
def hideRobot(x,y):
    key = (x,y)
    if(key in robots):
        gridCanvas.itemconfigure(robots[key], state='hidden')


# Create text at all cell coordinates x and y and hide them initially
def drawText():
    for i in range(rows):
        for j in range(columns):
            val = [i,j]
            if(grid[i][j] != 1):
                if(val not in pit):
                    if(val not in goal):
                        x = grids[(i,j)][0]
                        y = grids[(i,j)][1]
                        t1 = gridCanvas.create_text(y+ cell_size/2, x, text = "", anchor='n')
                        t2 = gridCanvas.create_text(y, x + cell_size/2, text = "", anchor='w')
                        t3 = gridCanvas.create_text(y+ cell_size/2, x + cell_size, text = "", anchor='s')
                        t4 = gridCanvas.create_text(y+ cell_size, x + cell_size/2, text = "", anchor='e')
                        texts[(i,j)] = [t1,t2,t3,t4]

# Change the text value
def changeText(x,y, action, value):
    key = (x,y)
    if(key in texts):
        gridCanvas.itemconfigure(texts[key][action], text = value)


# Change start point
def changeStart():
    x = int(startx_entry.get())
    y = int(starty_entry.get())

    if(isstop):
        gridCanvas.itemconfigure(start_images[(init[0],init[1])], state = 'hidden')

    gridCanvas.itemconfigure(start_images[(init[0],init[1])], state = 'hidden')
    for i in range(4):
        gridCanvas.itemconfigure(triangles[(init[0],init[1])][i], state = 'normal')
        gridCanvas.itemconfigure(texts[(init[0],init[1])][i], state = 'normal')

    drawStart(x,y)
    init[0] = x
    init[1] = y

# Change colour for heat map
def changeColor(x,y, action, value):
    value = float(value)
    minDataVal = -2
    maxDataValue = 2
    valueOfYourDataPoint = value
    new_value = int((valueOfYourDataPoint - minDataVal / (maxDataValue - minDataVal)) * 255)
    new_value = min(max(0,new_value), 255)
    colour_value = '#%02x%02x%02x' % (255 - new_value, new_value, 0)
    gridCanvas.itemconfigure(triangles[(x,y)][action], fill = colour_value)

# Left Frame Initialiation
# Creation of Grid Canvas
gridCanvas = Canvas(left_frame, height = rows * cell_size + 2 * offset, width = columns * cell_size + 2 * offset)
gridCanvas.pack(fill=BOTH, expand = True)

# Creation of Grid
grids = createGrid()

# Loading all the images
loadImages()

# Create triangles and text for visualization
create_triangle()
drawText()

# Draw Start, Walls, Pit, Robot and Goal Images
drawRobot()
drawStart(init[0],init[1])

for i in range(len(goal)):
    drawTarget(goal[i][0],goal[i][1])

for i in range(len(pit)):
    drawPit(pit[i][0],pit[i][1])

for i in range(rows):
    for j in range(columns):
        if(grid[i][j] == 1):
            drawWall(i,j)



# Right Frame Functionality

# Get sleep time for speed purpose
def get_sleep():
    global sleep_time
    sleep_time = speed_bar.get()
    return sleep_time

# Get Exploration value
def get_exploration():
    global exploration
    exploration = exploration_bar.get()
    return exploration/10.0

# check Play Pause Button
def play():
    global isplay
    if(isplay):
        isplay = False
    else:
        isplay = True

# Stop required for Refresh
def stop():
    global isstop
    isstop = True

def refresh():

    for i in range(rows):
        for j in range(columns):
            key = (i,j)
            if(key in texts):
                for k in range(4):
                    gridCanvas.itemconfigure(texts[key][k], text = "")
                    gridCanvas.itemconfigure(triangles[key][k], fill = "gold")

    drawStart(init[0],init[1])



# Select the environment - deterministic or stochastic
def selectEnv():
    global deterministic
    deterministic = (env.get() == 1)



# Controls
control_label = Label(right_frame, text="Controls",font=("Chalkboard", 20), fg = "RED", bg = bg_color)
control_label.pack(side = TOP)

# Environment
radio_frame = Frame(right_frame, bg = bg_color)
radio_frame.pack()
env = IntVar()
Radiobutton(radio_frame, text="Deterministic", variable=env, value=1, command = selectEnv, font=(fontStyle, 16), fg = fg_color2, bg = bg_color).pack(anchor = W)
Radiobutton(radio_frame, text="Stochastic", variable=env, value=2, command = selectEnv, font=(fontStyle, 16), fg = fg_color2, bg = bg_color).pack(anchor = W)
env.set(1)

# Play/Pause
play_button = Button(right_frame, command = play, bg = bg_color)
photo_button = ImageTk.PhotoImage(Image.open("/Users/abhianshusingla/Documents/Q Learning/images/play.png").resize((30, 30)))
play_button.config(image=photo_button,width="30",height="30")
play_button.pack()

# Refresh Button
play_button1 = Button(right_frame, command = stop, bg = bg_color)
photo_button1 = ImageTk.PhotoImage(Image.open("/Users/abhianshusingla/Documents/Q Learning/images/stop.png").resize((30, 30)))
play_button1.config(image=photo_button1,width="30",height="30")
play_button1.pack()

# Speed Bar
speed_bar = Scale(right_frame, from_= 0, to= 10,length = 200, orient=HORIZONTAL, font=(fontStyle, 16), fg = fg_color2, bg = bg_color)
speed_bar.set(7)
speed_bar.pack()
speed_label = Label(right_frame, text="Speed", font=(fontStyle, 16), fg = fg_color2, bg = bg_color)
speed_label.pack()


# Start Frame
start_frame = Frame(right_frame, bg = bg_color)
start_frame.pack(anchor = W)
start_label = Label(start_frame, text="Start Point", font=(fontStyle, 16), fg = fg_color1, bg = bg_color)
start_label.pack(anchor = W)
start_label = Label(start_frame, text="X", font=(fontStyle, 16), fg = fg_color2, bg = bg_color)
start_label.pack(side = LEFT)
start_label = Label(start_frame, text="Y", font=(fontStyle, 16), fg = fg_color2, bg = bg_color)

startx_entry = Entry(start_frame, width = 4, bg = bg_color, fg = fg_color2)
startx_entry.pack(side = LEFT)
startx_entry.insert(0,init[0])
start_label.pack(side  = LEFT)
starty_entry = Entry(start_frame, width = 4, bg = bg_color, fg = fg_color2)
starty_entry.pack(side = LEFT)
starty_entry.insert(0,init[1])

# Change Start button
button_frame = Frame(right_frame, bg = bg_color)
button_frame.pack()
Button(button_frame, text='Change', command = changeStart, font=(fontStyle, 15), bg = bg_color, fg = fg_color1).pack()

# Exploration bar
exploration_bar = Scale(right_frame, from_= 0, to= 10,length = 200, orient=HORIZONTAL, font=(fontStyle, 16), fg = fg_color2, bg = bg_color)
exploration_bar.set(8)
exploration_bar.pack()
exploration_label = Label(right_frame, text="Exploration", font=(fontStyle, 16), fg = fg_color2, bg = bg_color)
exploration_label.pack()


# Main Loop
def start():
    root.mainloop()
    time.sleep(0.01)
