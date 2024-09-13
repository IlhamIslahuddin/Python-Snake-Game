from tkinter import *
import random

global GAME_WIDTH
global GAME_HEIGHT
global SPACE_SIZE
global SNAKE_COLOR
global FOOD_COLOR
global BACKGROUND_COLOR
GAME_WIDTH = 700
GAME_HEIGHT = 600
speed = 100
SPACE_SIZE = 50
body_parts = 3
SNAKE_COLOR = "#0011FF"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

class Snake:
    def __init__(self):
        self.body_size = body_parts
        self.coordinates = []
        Snake.coords = self.coordinates
        self.squares = []

        for i in range(0, body_parts):
            self.coordinates.append([0, 0])
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)
    def get_snake_coordinates():
        return Snake.coords

class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        check = Snake.get_snake_coordinates()
        while x in check:
            x = random.randint(0, (GAME_WIDTH // SPACE_SIZE)-1) * SPACE_SIZE
        while y in check:
            y = random.randint(0, (GAME_WIDTH // SPACE_SIZE)-1) * SPACE_SIZE
        food = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")
        canvas.coords(food, (x+5, y+5, (x+SPACE_SIZE)-5, (y+SPACE_SIZE)-5))

def set_difficulty(diff):
    global speed
    global body_parts
    if diff == "easy":
        speed = 100
        body_parts = 2
        diff = ""
    elif diff == "normal":
        speed = 70
        body_parts = 3
        diff = ""
    elif diff == "hard":
        speed = 40
        body_parts = 4
        diff = ""
    
def next_turn(snake, food):
    x, y = snake.coordinates[0]
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        if score >= 10 and score < 20:
            label.config(text="Current Score: {}".format(score),font=("System",40),fg= "red")
        elif score >= 20 and score < 30:
            label.config(text="Current Score: {}".format(score),font=("System",40),fg= "yellow")
        elif score >= 30:
            label.config(text="Current Score: {}".format(score),font=("System",40),fg= "blue")
        else:
            label.config(text="Current Score: {}".format(score),font=("System",40))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
    if check_collisions(snake):
        game_over()
    else:
        window.after(speed, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x > GAME_WIDTH:
        return True
    elif y < 0 or y > GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

def game_over():
    global score, best_score
    if score > best_score:
        best_score = score
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('System',70), text="--GAME OVER--", fill="red", tag="gameover")
    
def main(event=""):
    global score, direction, best_score
    score = 0
    direction = 'down'
    label.config(text="Current Score: {}".format(score),fg="black")
    best_score_label.config(text="Best Score This Session: {}".format(best_score),fg="black",font=('System',20))
    canvas.delete(ALL)
    snake = Snake()
    food = Food()
    next_turn(snake, food)

window = Tk()
window.title("Snake game")
window.resizable(False, False)
score = 0
best_score = 0
label = Label(window, text="Current Score: {}".format(score), font=('System', 40))
best_score_label = Label(window, text="Best Score This Session: {}".format(best_score), font=('System', 20))
label.pack()
best_score_label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()
start = Button(window,text="Press To Start/Restart",command=main)
start.pack()
difficulty1 = Button(window,text="Easy mode 🟢",command=lambda: set_difficulty("easy"))
difficulty2 = Button(window,text="Normal mode 🟠",command=lambda: set_difficulty("normal"))
difficulty3 = Button(window,text="Hard mode 🔴",command=lambda: set_difficulty("hard"))
difficulty1.pack()
difficulty2.pack()
difficulty3.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width//2) - (window_width//2))
y = int((screen_height//2) - (window_height//2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind("<Return>", main)
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
insert = canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,font=('System',70), text="INSERT COIN...", fill="white", tag="insertcoin")
        
window.mainloop()
