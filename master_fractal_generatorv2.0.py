import turtle
import pygame as pg
import time

fractal, mode, iterations = None, None, None

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
   
def validate_input(input, valid_input_list = 0, int_check = 0):
   if valid_input_list != 0:
      if input not in valid_input_list:
         return 0
      else:
         return 1
   elif int_check == 1:
      try:
         int(input)
         return 1
      except:
         return 0

# For the generation of text boxes
class InputBox:
    
    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = BIG_FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event, var_name=None):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                    globals()[var_name] = self.text
                else:
                    self.text += event.unicode
                    globals()[var_name] = self.text
                # Re-render the text.
                self.txt_surface = BIG_FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

# Fractal information
WIDTH, HEIGHT = 640, 480 # Part of screen settings but needs to be defined here because fractal_info uses it

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

button_info = {
  "start_button": {"color": "grey", "position": (WIDTH / 2, HEIGHT / 2)}
}

# Pygame init
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
BIG_FONT = pg.font.Font(None, 36)
SMALL_FONT = pg.font.Font(None, 28)

# Button/text setup
start = BIG_FONT.render('Start', False, ('white'))
start_text_width, start_text_height = start.get_width(), start.get_height()
generate = BIG_FONT.render('Generate', False, ('white'))
generate_text_width, generate_text_height = generate.get_width(), generate.get_height()

fractal_prompt_text = BIG_FONT.render('Pick a fractal to generate', False, 'white')
fractal_error_text = BIG_FONT.render('Pick a fractal!', False, 'red')
mode_prompt_text = BIG_FONT.render('Select a mode', False, 'white')
mode_error_text = BIG_FONT.render('Select a mode!', False, 'red')
iterations_prompt_text = BIG_FONT.render('Enter iterations to generate', False, 'white')
iterations_error_text = BIG_FONT.render('Invalid integer!', False, 'red')

# Fractal boxes
honeycombs = SMALL_FONT.render('Honeycombs', False, ('white'))
sierpinksi_triangle = SMALL_FONT.render('Sierpinksi Triangle', False, ('white'))
sierpinksi_carpet = SMALL_FONT.render('Sierpinksi Carpet', False, ('white'))
harter_heighway_dragon = SMALL_FONT.render('Harter Heighway Dragon', False, ('white'))
levy_dragon = SMALL_FONT.render('Levy Dragon', False, ('white'))
mcworter_pentigree = SMALL_FONT.render('McWorter Pentigree', False, ('white'))
koch_curve = SMALL_FONT.render('Koch Curve', False, ('white'))
koch_snowflake_triangle = SMALL_FONT.render('Koch Snowflake (Triangle)', False, ('white'))
koch_snowflake_hexagon = SMALL_FONT.render('Koch Snowflake (Hexagon)', False, ('white'))
pentadentrite = SMALL_FONT.render('Pentadentrite', False, ('white'))

# Mode boxes
iteration_by_iteration_text = SMALL_FONT.render('Iteration by iteration', False, ('white'))
single_iteration_text = SMALL_FONT.render('Single iteration', False, 'white')

def main():
    clock = pg.time.Clock()
    input_box1 = InputBox(75, 400, 140, 32, '')
    input_boxes = [input_box1]
    screen_state = "main"
    done = False
    
    global fractal
    global mode
    global iterations
    
    selected_box = pg.Rect(0, 0, 0, 0)
    selected_mode = pg.Rect(0, 0, 0, 0)
    
    fractal_error_flag, mode_error_flag, iterations_error_flag = False, False, False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event, "iterations")

        for box in input_boxes:
            box.update()
        
        mouse_pos = pg.mouse.get_pos()
        screen.fill((30, 30, 30))
        
        if screen_state == "main":
           start_button = screen.blit(start, (WIDTH / 2 - start_text_width / 2, HEIGHT / 2 - start_text_height / 2))
           if event.type == pg.MOUSEBUTTONDOWN and start_button.collidepoint((mouse_pos)) == True and screen_state == "main":
             screen_state = "fractal setup"
             print("Start button clicked")
        
        if screen_state == "fractal setup":
           for box in input_boxes:
               box.draw(screen)
           
           fractal_prompt = screen.blit(fractal_prompt_text, (75, 50))
           # Shade the selected box gray
           pg.draw.rect(screen, (112, 112, 112), selected_box)
           
           # Draw all the fractal boxes and detect if they're selected
           honeycombs_button = screen.blit(honeycombs, (75, 100))
           if event.type == pg.MOUSEBUTTONDOWN and honeycombs_button.collidepoint((mouse_pos)) == True:
              selected_box = pg.Rect(75, 100, honeycombs.get_width(), honeycombs.get_height())
              fractal = "1"
           sierpinksi_triangle_button = screen.blit(sierpinksi_triangle, (75, 128))
           if event.type == pg.MOUSEBUTTONDOWN and sierpinksi_triangle_button.collidepoint((mouse_pos)) == True:
              selected_box = pg.Rect(75, 128, sierpinksi_triangle.get_width(), sierpinksi_triangle.get_height())
              fractal = "2"
           sierpinksi_carpet_button = screen.blit(sierpinksi_carpet, (75, 156))
           if event.type == pg.MOUSEBUTTONDOWN and sierpinksi_carpet_button.collidepoint((mouse_pos)) == True:
              selected_box = pg.Rect(75, 156, sierpinksi_carpet.get_width(), sierpinksi_carpet.get_height())
              fractal = "3"
           harter_heighway_dragon_button = screen.blit(harter_heighway_dragon, (75, 184))
           if event.type == pg.MOUSEBUTTONDOWN and harter_heighway_dragon_button.collidepoint((mouse_pos)) == True:
              selected_box = pg.Rect(75, 184, harter_heighway_dragon.get_width(), harter_heighway_dragon.get_height())
              fractal = "4"
           levy_dragon_button = screen.blit(levy_dragon, (75, 212))
           if event.type == pg.MOUSEBUTTONDOWN and levy_dragon_button.collidepoint((mouse_pos)) == True:
              selected_box = pg.Rect(75, 212, levy_dragon.get_width(), levy_dragon.get_height())
              fractal = "5"
           mcworter_pentigree_button = screen.blit(mcworter_pentigree, (350, 100))
           if event.type == pg.MOUSEBUTTONDOWN and mcworter_pentigree_button.collidepoint((mouse_pos)) == True:
              selected_box = pg.Rect(350, 100, mcworter_pentigree.get_width(), mcworter_pentigree.get_height())
              fractal = "6"
           koch_curve_button = screen.blit(koch_curve, (350, 128))
           if event.type == pg.MOUSEBUTTONDOWN and koch_curve_button.collidepoint((mouse_pos)) == True:
              selected_box = pg.Rect(350, 128, koch_curve.get_width(), koch_curve.get_height())
              fractal = "7"
           koch_snowflake_triangle_button = screen.blit(koch_snowflake_triangle, (350, 156))
           if event.type == pg.MOUSEBUTTONDOWN and koch_snowflake_triangle_button.collidepoint((mouse_pos)) == True:
              selected_box = pg.Rect(350, 156, koch_snowflake_triangle.get_width(), koch_snowflake_triangle.get_height())
              fractal = "8"
           koch_snowflake_hexagon_button = screen.blit(koch_snowflake_hexagon, (350, 184))
           if event.type == pg.MOUSEBUTTONDOWN and koch_snowflake_hexagon_button.collidepoint((mouse_pos)) == True:
              selected_box = pg.Rect(350, 184, koch_snowflake_hexagon.get_width(), koch_snowflake_hexagon.get_height())
              fractal = "9"
           pentadentrite_button = screen.blit(pentadentrite, (350, 212))
           if event.type == pg.MOUSEBUTTONDOWN and pentadentrite_button.collidepoint((mouse_pos)) == True:
              selected_box = pg.Rect(350, 212, pentadentrite.get_width(), pentadentrite.get_height())
              fractal = "10"
           
           mode_prompt = screen.blit(mode_prompt_text, (75, 250))
           
           # Shade the selected mode gray
           pg.draw.rect(screen, (112, 112, 112), selected_mode)
           
           # Draw mode boxes and detect if they're selected
           iteration_by_iteration_button = screen.blit(iteration_by_iteration_text, (75, 300))
           if event.type == pg.MOUSEBUTTONDOWN and iteration_by_iteration_button.collidepoint((mouse_pos)) == True:
              selected_mode = pg.Rect(75, 300, iteration_by_iteration_text.get_width(), iteration_by_iteration_text.get_height())
              mode = "1"
           single_iteration_button = screen.blit(single_iteration_text, (350, 300))
           if event.type == pg.MOUSEBUTTONDOWN and single_iteration_button.collidepoint((mouse_pos)) == True:
              selected_mode = pg.Rect(350, 300, single_iteration_text.get_width(), single_iteration_text.get_height())
              mode = "2"
           
           iterations_prompt = screen.blit(iterations_prompt_text, (75, 350))
           generate_button = screen.blit(generate, (425, 425))
           
           if fractal_error_flag == True:
              fractal_error = screen.blit(fractal_error_text, (425, 50))
           if mode_error_flag == True:
              mode_error = screen.blit(mode_error_text, (425, 250))
           if iterations_error_flag == True:
              iterations_error = screen.blit(iterations_error_text, (425, 350))
           
           if event.type == pg.MOUSEBUTTONDOWN and generate_button.collidepoint((mouse_pos)) == True and screen_state == "fractal setup":
              time.sleep(0.1)
              if fractal == None:
                 fractal_error_flag = True
              else:
                 fractal_error_flag = False
              
              if mode == None:
                 mode_error_flag = True
              else:
                 mode_error_flag = False
              
              if validate_input(iterations, 0, 1) == 0:
                 iterations_error_flag = True
              else:
                 iterations_error_flag = False
                 iterations = int(iterations)
              
              if fractal_error_flag == False and mode_error_flag == False and iterations_error_flag == False:
                 done = True

        pg.display.flip()
        clock.tick(30)
   
main()

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