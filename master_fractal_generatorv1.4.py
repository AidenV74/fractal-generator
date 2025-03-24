import turtle

# Functions
# Iteration by iteration mode
def apply_rules(axiom):
   return ''.join([rule_1 if char == char_1 else
   rule_2 if char == char_2 else char for char in axiom])

# Single iteration mode
def get_result(iterations, axiom):
   for gen in range(iterations):
       axiom = apply_rules(axiom)
   return axiom

# Set up the iteration text drawer
def set_stage(iteration):
   # Turtle draws the current iteration text
   turtle.pencolor('white')
   turtle.up()
   turtle.goto(-WIDTH // 2 + 60, -HEIGHT // 2 + 100)
   turtle.down()
   turtle.clear()
   turtle.write(f'iteration: {iteration}', font=("Arial", 60, "normal"))

   max.goto(fractal_info[fractal]["starting_pos"])
   max.clear()

# Fractal movement
def interpret_movement():
   for char in axiom:  
      # Honeycombs
      if fractal == "1":
         if char == char_1:
            max.right(angle)
            max.forward(step)
         else:
            max.right(-angle)
            max.forward(step)
      # Anything else
      else:
         if char == char_1 or char == char_2:
            max.forward(step)
         elif char == "+":
            max.right(angle)
         elif char == "-":
            max.left(angle)
         elif char == "U":
            max.up()
         elif char == "D":
            max.down()

# User selects the fractal
def set_fractal():
   global fractal
   fractal = input("Enter a fractal to generate:
Honeycombs: press 1
Sierpinski Triangle: press 2
Sierpinski Carpet: press 3
Harter-Heighway Dragon: press 4
Levy Dragon: press 5
McWorter's Pentigree: press 6
Koch Curve: press 7
Koch Snowflake (triangle variation): press 8
Koch Snowflake (hexagon variation): press 9
Pentadentrite: press 10
")

   # Error handling
   while fractal not in fractal_info:
       print("
Invalid input: Enter a valid number.
")
       fractal = input("Enter a fractal to generate:
Honeycombs: press 1
Sierpinski Triangle: press 2
Sierpinski Carpet: press 3
Harter-Heighway Dragon: press 4
Levy Dragon: press 5
McWorter's Pentigree: press 6
Koch Curve: press 7
Koch Snowflake (triangle variation): press 8
Koch Snowflake (hexagon variation): press 9
Pentadentrite: press 10
")
   return fractal

# User selects the mode
def set_mode():
   global mode
   mode = input("Press 1 for iteration by iteration view.
Press 2 for single iteration view.
")


   # Error handling
   while mode != "1" and mode != "2":
       print("Invalid input: Enter a valid number.")
       mode = input("Press 1 for iteration by iteration view.
Press 2 for single iteration view.
")
   return mode

# User sets the amount of iterations/iteration to generate
def set_iterations():
   global iterations
   iterations = input("Enter number of iterations:
") if mode == "1" else input("Enter iteration to generate
")


   # Error handling
   while True:
       try:
           iterations = int(iterations)
           break
       except:
           print("Invalid input: Enter a valid integer.")
           iterations = input("Enter number of iterations:
") if mode == 1 else input("Enter iteration to generate
")
   return iterations


# Main
# Fractal information
WIDTH, HEIGHT = 900, 900 # Part of screen settings but needs to be defined here because fractal_info uses it

fractal_info = {
   "1":{"name": "honeycombs", "color": "orange", "angle": 60, "step": 16, "axiom": "A", "char_1": "A", "rule_1": "AB", "char_2":"B", "rule_2": "A", "starting_pos": (0, 0)},
   "2":{"name": "sierpinksi_triangle", "color": "green", "angle": 120, "step": 8, "axiom": "F", "char_1": "F", "rule_1": "F-G+F+G-F", "char_2":"G", "rule_2": "GG", "starting_pos": (-WIDTH // 4, -HEIGHT // 3 + 60)},
   "3":{"name": "sierpinksi_carpet", "color": "blue", "angle": 90, "step": 4, "axiom": "F", "char_1": "F", "rule_1": "F+F-F-F-UGD+F+F+F-F", "char_2":"G", "rule_2": "GGG", "starting_pos": (-WIDTH // 4, -HEIGHT // 4)},
   "4":{"name": "harter_heighway_dragon", "color": "magenta", "angle": 90, "step": 4, "axiom": "FX", "char_1": "X", "rule_1": "X+YF+", "char_2":"Y", "rule_2": "-FX-Y", "starting_pos": (WIDTH // 4, -HEIGHT // 4 - 25)},
   "5":{"name": "levy_dragon", "color": "red", "angle": 45, "step": 4, "axiom": "F", "char_1": "F", "rule_1": "+F--F+", "char_2":"", "rule_2": "", "starting_pos": (0, 0)},
   "6":{"name": "mcworter_pentigree", "color": "light green", "angle": 36, "step": 4, "axiom": "F", "char_1": "F", "rule_1": "+F++F----F--F++F++F-", "char_2":"", "rule_2": "", "starting_pos": (0, 0)},
   "7":{"name": "koch_curve", "color": "light blue", "angle": 60, "step": 4, "axiom": "F", "char_1": "F", "rule_1": "F-F++F-F", "char_2":"", "rule_2": "", "starting_pos": (-WIDTH // 4, -HEIGHT // 4)},
   "8":{"name": "koch_snowflake_triangle", "color": "yellow", "angle": 60, "step": 4, "axiom": "F++F++F", "char_1": "F", "rule_1": "F-F++F-F", "char_2":"", "rule_2": "", "starting_pos": (-WIDTH // 4, HEIGHT // 4)},
   "9":{"name": "koch_snowflake_hexagon", "color": "yellow", "angle": 60, "step": 4, "axiom": "F+F+F+F+F+F", "char_1": "F", "rule_1": "F+F--F+F", "char_2":"", "rule_2": "", "starting_pos": (-WIDTH // 4, HEIGHT // 4)},
   "10":{"name": "pentadentrite", "color": "cyan", "angle": 72, "step": 4, "axiom": "F+F+F+F+F+F", "char_1": "F", "rule_1": "F-F+F++F-F-F", "char_2":"", "rule_2": "", "starting_pos": (-WIDTH // 4, HEIGHT // 4)},
}

# User inputted information
set_fractal()
set_mode()
set_iterations()

# Set the screen
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.screensize(3 * WIDTH, 3 * HEIGHT)
screen.bgcolor('black')

# Set Max the Turtle
max = turtle.Turtle()
max.pensize(2)
max.speed(0)
turtle.tracer(10)

# Set variables according to user input and fractal info
max.color(fractal_info[fractal]["color"])
angle = fractal_info[fractal]["angle"]
step = fractal_info[fractal]["step"]
axiom = fractal_info[fractal]["axiom"]
char_1, rule_1 = fractal_info[fractal]["char_1"], fractal_info[fractal]["rule_1"]
char_2, rule_2 = fractal_info[fractal]["char_2"], fractal_info[fractal]["rule_2"]

# Continue based on selected mode
# Iteration by iteration mode
if mode == "1":
   for i in range(iterations + 1):
       set_stage(i)

       # Turn characters into movements
       axiom = apply_rules(axiom)
       interpret_movement()

# Single iteration mode
else:
   set_stage(iterations)
   # Turn characters into movements
   axiom = get_result(iterations, axiom)
   interpret_movement()


turtle.mainloop()

