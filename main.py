from tkinter import *
import random

# Constantes du jeu
GAME_WIDTH = 600
GAME_HEIGHT = 600
SPEED = 90
SPACE_SIZE = 30
BODY_PARTS = 3
SNAKE_COLOR = "#1B3022"
FOOD_COLOR = "#A67DB8"
BACKGROUND_COLOR = "#4F5D75"

# Classe Snake pour représenter le serpent
class Snake:
    def __init__(self):

        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        # Initialisation des coordonnées du serpent
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        # Création des carrés représentant le serpent sur le canvas
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

# Classe Food pour représenter la nourriture
class Food:
    def __init__(self):

        # Génération aléatoire des coordonnées de la nourriture
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]
        # Création d'un cercle représentant la nourriture sur le canvas
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

# ================================================================

# Fonction pour gérer le prochain tour du jeu
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
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
    else:

        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):

        game_over()

    else:

        window.after(SPEED, next_turn, snake, food)

# Fonction pour changer la direction du serpent
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

# Fonction pour vérifier les collisions du serpent
def check_collisions(snake):

    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True

    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True


    return False

# Fonction pour gérer la fin du jeu
def game_over():
    
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
    font=('consolas',20), text="Fin de la partie", fill="#BFAEF3", tag="gameover")

# ================================================================

# Initialisation de la fenêtre principale
window = Tk()
window.title("PYTHON SNAKE GAME")
window.resizable(False, False)

score = 0
direction = 'right'

# Création de l'étiquette pour afficher le score
label = Label(window, text="Points:{}".format(score), font=('consolas', 40))
label.pack()

# Création du canvas pour afficher le jeu
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Mise à jour de la fenêtre pour prendre en compte les changements de taille du canvas
window.update()

# Récupération des dimensions de la fenêtre et de l'écran
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calcul des coordonnées pour centrer la fenêtre sur l'écran
x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

# Définition de la taille et de la position de la fenêtre
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Liaison des touches du clavier aux fonctions de changement de direction
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# Création du serpent et de la nourriture
snake = Snake()
food = Food()

# Lancement du jeu en appelant la fonction next_turn
next_turn(snake, food)

# Lancement de la boucle principale de la fenêtre
window.mainloop()