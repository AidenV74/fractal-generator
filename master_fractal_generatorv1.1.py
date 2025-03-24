#IMPORT MODULES
import turtle


#USER SETTINGS

#fractal set
fractal = input("Enter a fractal to generate:\nHoneycombs: press 1\nSierpinski Triangle: press 2\nHarter-Heighway Dragon: press 3\nSierpinski Carpet: press 4\n")

#error handling
while fractal != "1" and fractal != "2" and fractal != "3" and fractal != "4":
    print("Invalid input: Enter a valid number.")
    fractal = input("Enter a fractal to generate:\nHoneycombs: press 1\nSierpinski Triangle: press 2\nHarter-Heighway Dragon: press 3\nSierpinski Carpet: press 4\n")
fractal = int(fractal)


#mode set
mode = input("Press 1 for iteration by iteration view.\nPress 2 for single iteration view.\n")

#error handling
while mode != "1" and mode != "2":
    print("Invalid input: Enter a valid number.")
    fractal = input("Press 1 for iteration by iteration view.\nPress 2 for single iteration view.\n")
mode = int(mode)


#iterations set
if mode == 1:
    iterations = input("Enter number of iterations:\n")
else:
    iterations = input("Enter iteration to generate\n") 

#error handling
while True:
    try:
        int(iterations)
        break
    except:
        print("Invalid input: Enter a valid integer.")
        if mode == 1:
            iterations = input("Enter number of iterations:\n")
        else:
            iterations = input("Enter iteration to generate\n") 
iterations = int(iterations)


#SCREEN SETTINGS

WIDTH, HEIGHT = 1600, 900
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.screensize(3 * WIDTH, 3 * HEIGHT)
screen.bgcolor('black')
screen.delay(0)


#MAX SETTINGS
max = turtle.Turtle()
max.pensize(2)
max.speed(0)

#honeycombs
if fractal == 1:
    max.goto(0, 0)
    max.color('orange')
#sierpinski triangle
if fractal == 2:
    max.goto(-WIDTH // 4, -HEIGHT // 3 + 60)
    max.color('green')
#harter-heighway dragon
if fractal == 3:
    max.goto(WIDTH // 4, -HEIGHT // 4 - 25)
    max.color('magenta')
if fractal == 4:
    max.goto(-WIDTH // 4, -HEIGHT // 3 + 60)
    max.color('blue')


#MOVEMENT SETTINGS

#honeycombs
if fractal == 1:
    rotate = 60
    step = 16
#sierpinksi triangle
if fractal == 2:
    rotate = 120
    step = 8
#harter-heighway dragon
if fractal == 3:
    rotate = 90
    step = 4
#sierpinski carpet
if fractal == 4:
    rotate = 90
    step = 4

#gas gas gas
turtle.tracer(100)


#L-SYSTEMS SETTINGS

#honeycombs
if fractal == 1:
    axiom = 'A'
    char_1, rule_1 = 'A', 'AB'
    char_2, rule_2 = 'B', 'A'
#sierpinski triangle
if fractal == 2:
    axiom = 'F'
    char_1, rule_1 = 'F', 'F-G+F+G-F'
    char_2, rule_2 = 'G', 'GG'
#harter-heighway dragon
if fractal == 3:
    axiom = 'FX'
    char_1, rule_1 = 'X', 'X+YF+'
    char_2, rule_2 = 'Y', '-FX-Y'
#sierpinksi carpet
if fractal == 4:
    axiom = 'F'
    char_1, rule_1 = 'F', 'F+F-F-F-UGD+F+F+F-F'
    char_2, rule_2 = 'G', 'GGG'

#FUNCTIONS

#iteration by iteration mode
def apply_rules(axiom):
    return ''.join([rule_1 if char == char_1 else 
    rule_2  if char == char_2 else char for char in axiom])

#single iteration mode
def get_result(iterations, axiom):
    for gen in range(iterations):
        axiom = apply_rules(axiom)
    return axiom

#set-up
def set_stage(iteration):
    #turtle draws the current iteration text
    turtle.pencolor('white')
    turtle.up()
        
    #honeycombs
    if fractal == 1:
        turtle.goto(-WIDTH // 2 + 60, -HEIGHT // 2 + 60)
    #sierpinksi triangle
    if fractal == 2:
        turtle.goto(-WIDTH // 2 + 60, -HEIGHT // 2 + 100)
    #harter-heighway dragon
    if fractal == 3:
        turtle.goto(-WIDTH // 2 + 60, -HEIGHT // 2 + 100)
    #sierpinski carpet
    if fractal == 4:
        turtle.goto(-WIDTH // 2 + 60, -HEIGHT // 2 + 100)

    turtle.down()
    turtle.clear()
    turtle.write(f'iteration: {iteration}', font=("Arial", 60, "normal"))

    #setting max's position
    max.setheading(0)

    #honeycomb
    if fractal == 1:
        max.goto(0, 0)
    #sierpinski triangle
    if fractal == 2:
        max.goto(-WIDTH // 4, -HEIGHT // 3 + 60)
    #harter-heighway dragon
    if fractal == 3:
        max.goto(WIDTH // 4, -HEIGHT // 4 - 25)
    #sierpinski carpet
    if fractal == 4:
        max.goto(-WIDTH // 4, -HEIGHT // 4)

    max.clear()

#fractal movement
def interpret_movement():
    for char in axiom:   
            #honeycombs
            if fractal == 1:
                if char == char_1:
                    max.right(rotate)
                    max.forward(step)
                else:
                    max.right(-rotate)
                    max.forward(step)
            #sierpinski triangle, carpet, or harter-heighway
            else:
                if char == char_1 or char == char_2:
                    max.forward(step)
                elif char == "+":
                    max.right(rotate)
                elif char == "-":
                    max.left(rotate)
                elif char == "U":
                    max.up()
                elif char == "D":
                    max.down()


#FRACTAL GENERATION

#iteration by iteration mode
if mode == 1:
    for i in range(iterations + 1):
        set_stage(i)

        #turn characters into movements
        axiom = apply_rules(axiom)
        interpret_movement()

#single iteration mode
if mode == 2:
    set_stage(iterations)
 
    #turn characters into movements
    axiom = get_result(iterations, axiom)
    interpret_movement()

turtle.mainloop()