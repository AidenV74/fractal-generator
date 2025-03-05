#IMPORT MODULES
import turtle


#USER SETTINGS

#fractal set
fractal = input("Enter a fractal to generate:\nHoneycombs: press 1\nSierpinski Triangle: press 2\nSierpinski Carpet: press 3\nHarter-Heighway Dragon: press 4\nLevy Dragon: press 5\nMcWorter's Pentigree: press 6\nKoch Curve: press 7\nKoch Snowflake (triangle variation): press 8\nKoch Snowflake (hexagon variation): press 9\nPentadentrite: press 10\n")

#error handling
while fractal != "1" and fractal != "2" and fractal != "3" and fractal != "4" and fractal != "5" and fractal != "6" and fractal != "7" and fractal != "8" and fractal != "9" and fractal != "10":
    print("Invalid input: Enter a valid number.")
    fractal = input("Enter a fractal to generate:\nHoneycombs: press 1\nSierpinski Triangle: press 2\nSierpinski Carpet: press 3\nHarter-Heighway Dragon: press 4\nLevy Dragon: press 5\nMcWorter's Pentigree: press 6\nKoch Curve: press 7\nKoch Snowflake (triangle variation): press 8\nKoch Snowflake (hexagon variation): press 9\nPentadentrite: press 10\n")
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
    max.color('orange')
#sierpinski triangle
if fractal == 2:
    max.color('green')
#harter-heighway dragon
if fractal == 3:
    max.color('blue')
#sierpinski carpet
if fractal == 4:
    max.color('magenta')
#levy dragon
if fractal == 5:
    max.color('red')
#mcworter pentigree
if fractal == 6:
    max.color('light green')
#koch curve
if fractal == 7:
    max.color('light blue')
#koch snowflake (both variations)
if fractal == 8 or fractal == 9:
    max.color('yellow')
#pentadentrite
if fractal == 10:
    max.color('cyan')

#MOVEMENT SETTINGS

#honeycombs
if fractal == 1:
    angle = 60
    step = 16
#sierpinksi triangle
if fractal == 2:
    angle = 120
    step = 8
#sierpinski carpet, harter-heighway dragon
if fractal == 3 or fractal == 4:
    angle = 90
    step = 4
#levy dragon
if fractal == 5:
    angle = 45
    step = 4
#mcworter pentigree
if fractal == 6:
    angle = 36
    step = 4
#koch curve
if fractal == 7:
    angle = 60
    step = 4
#koch snowflake (both variations)
if fractal == 8 or fractal == 9:
    angle = 60
    step = 4
#pentadentrite
if fractal == 10:
    angle = 72
    step = 4

#gas gas gas
turtle.tracer(100)


#L-SYSTEMS SETTINGS

#honeycombs
if fractal == 1:
    axiom = 'A'
    chr_1, rule_1 = 'A', 'AB'
    chr_2, rule_2 = 'B', 'A'
#sierpinski triangle
if fractal == 2:
    axiom = 'F'
    chr_1, rule_1 = 'F', 'F-G+F+G-F'
    chr_2, rule_2 = 'G', 'GG'
#sierpinksi carpet
if fractal == 3:
    axiom = 'F'
    chr_1, rule_1 = 'F', 'F+F-F-F-UGD+F+F+F-F'
    chr_2, rule_2 = 'G', 'GGG'
#harter-heighway dragon
if fractal == 4:
    axiom = 'FX'
    chr_1, rule_1 = 'X', 'X+YF+'
    chr_2, rule_2 = 'Y', '-FX-Y'
#levy dragon
if fractal == 5:
    axiom = 'F'
    chr_1, rule_1 = 'F', '+F--F+'
    chr_2, rule_2 = '', ''
#mcworter pentigree
if fractal== 6:
    axiom = 'F'
    chr_1, rule_1 = 'F', '+F++F----F--F++F++F-'
    chr_2, rule_2 = '', ''
#koch-curve
if fractal == 7:
    axiom = 'F'
    chr_1, rule_1 = 'F', 'F-F++F-F'
    chr_2, rule_2 = '', ''
#koch snowflake (triangle variation)
if fractal == 8:
    axiom = 'F++F++F'
    chr_1, rule_1 = 'F', 'F-F++F-F'
    chr_2, rule_2 = '', ''
#koch snowflake (hexagon variation)
if fractal == 9:
    axiom = 'F+F+F+F+F+F'
    chr_1, rule_1 = 'F', 'F+F--F+F'
    chr_2, rule_2 = '', ''
#pentadentrite
if fractal == 10:
    axiom = 'F'
    chr_1, rule_1 = 'F', 'F-F+F++F-F-F'
    chr_2, rule_2 = '', ''


#FUNCTIONS

#iteration by iteration mode
def apply_rules(axiom):
    return ''.join([rule_1 if chr == chr_1 else 
    rule_2  if chr == chr_2 else chr for chr in axiom])

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
    #literally anything else
    else:
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
    #sierpinski carpet
    if fractal == 3:
        max.goto(-WIDTH // 4, -HEIGHT // 4)
    #harter-heighway dragon
    if fractal == 4:
        max.goto(WIDTH // 4, -HEIGHT // 4 - 25)
    #levy dragon
    if fractal == 5:
        max.goto(0, 0)
    #mcworter pentigree
    if fractal == 6:
        max.goto(0, 0)
    #koch-curve
    if fractal == 7:
        max.goto(-WIDTH // 4, -HEIGHT // 4)
    #koch snowflake (both variations)
    if fractal == 8 or fractal == 9:
        max.goto(-WIDTH // 4, HEIGHT // 4)
    #pentadentrite
    if fractal == 10:
        max.goto(-WIDTH // 4, HEIGHT // 4)

    max.clear()

#fractal movement
def interpret_movement():
    for chr in axiom:   
            #honeycombs
            if fractal == 1:
                if chr == chr_1:
                    max.right(angle)
                    max.forward(step)
                else:
                    max.right(-angle)
                    max.forward(step)
            #sierpinski triangle, carpet, harter-heighway, levy dragon
            else:
                if chr == chr_1 or chr == chr_2:
                    max.forward(step)
                elif chr == "+":
                    max.right(angle)
                elif chr == "-":
                    max.left(angle)
                elif chr == "U":
                    max.up()
                elif chr == "D":
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