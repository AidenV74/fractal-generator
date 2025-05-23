import pygame as pg
import time
import math


fractal, mode, iterations = None, None, None


# Iteration by iteration mode
def apply_rules(axiom, char_1, rule_1, char_2, rule_2):
   return ''.join([rule_1 if char == char_1 else
   rule_2 if char == char_2 else char for char in axiom])


# Single iteration mode
def get_result(iterations, axiom, char_1, rule_1, char_2, rule_2):
   for gen in range(iterations):
       axiom = apply_rules(axiom, char_1, rule_1, char_2, rule_2)
   return axiom


# Set up the iteration text drawer
def set_stage(iteration):
   iterations_live_text = TITLE_FONT.render(f'iteration: {iteration}', False, 'white')
   iteration_text = screen.blit(iterations_live_text, (1/16 * WIDTH, 7/8 * HEIGHT))


# Takes the axiom and converts characters into drawing instructions
def interpret_movement(axiom, char_1, char_2, angle, length, color):
   
   screen.fill('black')
   (x, y) = fractal_info[fractal]["starting_pos"]


   current_angle = 0
   draw = True 
   for char in axiom:    
         if char == "F" or char == "G":
            new_x = x + length * math.cos(current_angle)
            new_y = y - length * math.sin(current_angle)
         else:
            new_x = x
            new_y = y
         
         if char == "+":
            current_angle -= math.radians(angle)
         elif char == "-":
            current_angle += math.radians(angle)
         elif char == "U":
            draw = False
         elif char == "D":
            draw = True
         if draw == True:
            pg.draw.line(screen, (color), (x, y), (new_x, new_y), 1)
         x, y = new_x, new_y


# Validate user input
def valid_int(integer):
   try:
     integer = int(integer)
     return integer
   except:
     return False
# Prepare the screen and variables for fractal creation
def draw_main():
   screen.fill('black')


   # Set variables according to user input and fractal info
   color = (fractal_info[fractal]["color"])
   angle = fractal_info[fractal]["angle"]
   length = fractal_info[fractal]["step"]
   axiom = fractal_info[fractal]["axiom"]
   char_1, rule_1 = fractal_info[fractal]["char_1"], fractal_info[fractal]["rule_1"]
   char_2, rule_2 = fractal_info[fractal]["char_2"], fractal_info[fractal]["rule_2"]


   # Continue based on selected mode
   # Iteration by iteration mode
   if mode == "1":
      for i in range(iterations + 1):
         # Turn characters into movements
         axiom = apply_rules(axiom, char_1, rule_1, char_2, rule_2)
         interpret_movement(axiom, char_1, char_2, angle, length, color)
         # Iteration text
         set_stage(i)


   # Single iteration mode
   else:
      axiom = get_result(iterations, axiom, char_1, rule_1, char_2, rule_2)
      interpret_movement(axiom, char_1, char_2, angle, length, color)
      set_stage(iterations)


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
        width = max(3/16 * WIDTH, self.txt_surface.get_width()+3/320 * WIDTH)
        self.rect.w = width


    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+3/640 * WIDTH, self.rect.y+1/120 * HEIGHT))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, int(3/1600 * WIDTH))


# Button class
class Button:
    def __init__(self, text, x, y, width=260, height=40):
        self.text = text
        self.rect = pg.Rect(x, y, width, height)
        self.clicked = False


    def handle_event(self, event, buttons, variable):
        
        global fractal, mode
        
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                for button in buttons:
                   button.clicked = False
                self.clicked = True
                
                if variable == "fractal":
                  fractal = self.text
                else:
                  mode = self.text
              
    def draw(self, surface, rect_width=0, rect_radius=5):
        color = (255, 255, 255)  # Default white
        if self.rect.collidepoint(pg.mouse.get_pos()):
            color = (200, 200, 200)  # Light gray on hover
        if self.clicked:
            color = (150, 150, 150)  # Dark gray when clicked


        pg.draw.rect(surface, color, self.rect, rect_width, rect_radius)
        text_surf = SMALL_FONT.render(self.text, True, (0, 0, 0))
        surface.blit(text_surf, self.rect.move(3/320 * WIDTH, 1/60 * HEIGHT))  # Center text


# Fractal information
#1600 x 900 by default
WIDTH, HEIGHT = 800, 450 # Part of screen settings but needs to be defined here because fractal_info uses it


fractal_info = {
   "Hilbert Curve":{"color": "brown", "angle": 90, "step": 4, "axiom": "A", "char_1": "A", "rule_1": "-BF+AFA+FB-", "char_2":"B", "rule_2": "+AF-BFB-FA+", "starting_pos": (WIDTH / 2, HEIGHT / 2)},
   "Sierpinski Curve":{"color": "pink", "angle": 45, "step": 8, "axiom": "F--XF--F--XF", "char_1": "X", "rule_1": "XF+G+XF--F--XF+G+X", "char_2":"", "rule_2": "", "starting_pos": (WIDTH / 2, HEIGHT / 2)},
   "Sierpinski Triangle":{"color": "green", "angle": 120, "step": 8, "axiom": "F", "char_1": "F", "rule_1": "F-G+F+G-F", "char_2":"G", "rule_2": "GG", "starting_pos": (WIDTH / 2, HEIGHT / 2)},
   "Sierpinski Arrowhead Curve":{"color": "orange", "angle": 60, "step": 8, "axiom": "XF", "char_1": "X", "rule_1": "YF+XF+Y", "char_2":"Y", "rule_2": " XF-YF-X", "starting_pos": (WIDTH / 2, HEIGHT / 2)},
   "Sierpinksi Carpet":{"color": "blue", "angle": 90, "step": 4, "axiom": "F", "char_1": "F", "rule_1": "F+F-F-F-UGD+F+F+F-F", "char_2":"G", "rule_2": "GGG", "starting_pos": (WIDTH / 2, HEIGHT / 2)},
   "Harter Heighway Dragon":{"color": "magenta", "angle": 90, "step": 4, "axiom": "FX", "char_1": "X", "rule_1": "X+YF+", "char_2":"Y", "rule_2": "-FX-Y", "starting_pos": (WIDTH / 2, HEIGHT / 2)},
   "Levy Dragon":{"color": "red", "angle": 45, "step": 4, "axiom": "F", "char_1": "F", "rule_1": "+F--F+", "char_2":"", "rule_2": "", "starting_pos": (WIDTH / 2, HEIGHT / 2)},
   "McWorter Pentigree":{"color": "light green", "angle": 36, "step": 4, "axiom": "F", "char_1": "F", "rule_1": "+F++F----F--F++F++F-", "char_2":"", "rule_2": "", "starting_pos": (WIDTH / 2, HEIGHT / 2)},
   "Koch Curve":{"color": "light blue", "angle": 60, "step": 4, "axiom": "F", "char_1": "F", "rule_1": "F-F++F-F", "char_2":"", "rule_2": "", "starting_pos": (WIDTH / 2, HEIGHT / 2)},
   "Koch Snowflake Triangle":{"color": "yellow", "angle": 60, "step": 4, "axiom": "F++F++F", "char_1": "F", "rule_1": "F-F++F-F", "char_2":"", "rule_2": "", "starting_pos": (WIDTH / 2, HEIGHT / 2)},
   "Koch Snowflake Hexagon":{"color": "yellow", "angle": 60, "step": 4, "axiom": "F+F+F+F+F+F", "char_1": "F", "rule_1": "F+F--F+F", "char_2":"", "rule_2": "", "starting_pos": (WIDTH / 2, HEIGHT / 2)},
   "Pentadentrite":{"color": "cyan", "angle": 72, "step": 4, "axiom": "F+F+F+F+F+F", "char_1": "F", "rule_1": "F-F+F++F-F-F", "char_2":"", "rule_2": "", "starting_pos": (WIDTH / 2, HEIGHT / 2)},
}


main_button_info = {
  "Start": {"color": "grey", "position": (1/2 * WIDTH, 1/2 * HEIGHT)}
}


fractal_setup_button_info = {
   "Iteration by Iteration": {"color": "grey", "position": (9/128 * WIDTH, 5/8 * HEIGHT)},
   "Single Iteration": {"color": "grey", "position": (223/640 * WIDTH, 5/8 * HEIGHT)}
}


# Pygame init
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
TITLE_FONT = pg.font.Font(None, int(13/150 * HEIGHT))
BIG_FONT = pg.font.Font(None, int(3/50 * HEIGHT))
SMALL_FONT = pg.font.Font(None, int(7/150 * HEIGHT))


# Button/text setup
start = TITLE_FONT.render('Start', False, ('white'))
generate = BIG_FONT.render('Generate', False, ('white'))
back = BIG_FONT.render('Back', False, ('white'))


fractal_prompt_text = BIG_FONT.render('Pick a fractal to generate', False, 'white')
fractal_error_text = BIG_FONT.render('Pick a fractal!', False, 'red')
mode_prompt_text = BIG_FONT.render('Select a mode', False, 'white')
mode_error_text = BIG_FONT.render('Select a mode!', False, 'red')
iterations_prompt_text = BIG_FONT.render('Enter iterations to generate', False, 'white')
iterations_error_text = BIG_FONT.render('Invalid integer!', False, 'red')


# Fractal buttons
fractal_buttons = []
button_width = 43/160 * WIDTH
button_height = 1/15 * HEIGHT
row_padding = 1/60 * HEIGHT
col_padding = 3/320 * WIDTH
buttons_per_row = 3
start_x = 9/128 * WIDTH
start_y = 1/6 * HEIGHT


# Fractal buttons
for i, name in enumerate(fractal_info):
   row = i // buttons_per_row
   col = i % buttons_per_row
   x = start_x + col * (button_width + col_padding)
   y = start_y + row * (button_height + row_padding)
   button = Button(name, x, y, button_width, button_height)
   fractal_buttons.append(button)


mode_buttons = []
# Mode buttons
for i, name in enumerate(fractal_setup_button_info):
   (x, y) = fractal_setup_button_info[name]["position"]
   button = Button(name, x, y, button_width, button_height)
   mode_buttons.append(button)
   


# Menu
def main_menu():
    clock = pg.time.Clock()
    input_box1 = InputBox(9/128 * WIDTH, 5/6 * HEIGHT, 21/160 * WIDTH, 4/75 * HEIGHT, '')
    input_boxes = [input_box1]
    screen_state = "main"
    
    global fractal
    global mode
    global iterations
    
    selected_box = pg.Rect(0, 0, 0, 0)
    selected_mode = pg.Rect(0, 0, 0, 0)
    
    fractal_error_flag, mode_error_flag, iterations_error_flag = False, False, False
    
    done = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event, "iterations")
            if screen_state == "fractal setup":
               for button in fractal_buttons:
                  button.handle_event(event, fractal_buttons, "fractal")
               for button in mode_buttons:
                  button.handle_event(event, mode_buttons, "mode")


        for box in input_boxes:
            box.update()


        mouse_pos = pg.mouse.get_pos()
        if screen_state == "main":
           screen.fill((30, 30, 30))
           start_button = screen.blit(start, (WIDTH / 2 - start.get_width() / 2, HEIGHT / 2 - start.get_height() / 2))
           if event.type == pg.MOUSEBUTTONDOWN and start_button.collidepoint((mouse_pos)) == True and screen_state == "main":
             screen_state = "fractal setup"
             print("Start button clicked")
        
        if screen_state == "fractal setup":
           screen.fill((30, 30, 30))
           for box in input_boxes:
               box.draw(screen)
           
           fractal_prompt = screen.blit(fractal_prompt_text, (9/128 * WIDTH, 1/12 * HEIGHT))
           # Shade the selected box gray
           pg.draw.rect(screen, (112, 112, 112), selected_box)
           
           # Draw all the fractal boxes and detect if they're selected
           for button in fractal_buttons:
              button.draw(screen)
           
           mode_prompt = screen.blit(mode_prompt_text, (9/128 * WIDTH, 13/24 * HEIGHT))
           for button in mode_buttons:
              button.draw(screen)
           
           # Shade the selected mode gray
           pg.draw.rect(screen, (112, 112, 112), selected_mode)
           
           iterations_prompt = screen.blit(iterations_prompt_text, (9/128 * WIDTH, 3/4 * HEIGHT))
           generate_button = screen.blit(generate, (51/128 * WIDTH, 5/6 * HEIGHT))
           
           if fractal_error_flag:
              fractal_error = screen.blit(fractal_error_text, (25/64 * WIDTH, 1/12 * HEIGHT))
           if mode_error_flag:
              mode_error = screen.blit(mode_error_text, (25/64 * WIDTH, 13/24 * HEIGHT))
           if iterations_error_flag:
              iterations_error = screen.blit(iterations_error_text, (25/64 * WIDTH, 3/4 * HEIGHT))
           
           if event.type == pg.MOUSEBUTTONDOWN and generate_button.collidepoint((mouse_pos)):
              
              # Check for errors
              fractal_error_flag = True if fractal == None else False
              mode_error_flag = True if mode == None else False
              iterations_error_flag = True if valid_int(iterations) == False else False
              
              if fractal_error_flag == False and mode_error_flag == False and iterations_error_flag == False:
                 iterations = int(iterations)
                 screen_state = "fractal draw"
                 draw_main()
 
        if screen_state == "fractal draw":
           back_button = screen.blit(back, (WIDTH / 16, HEIGHT / 8))
           if event.type == pg.MOUSEBUTTONDOWN and back_button.collidepoint((mouse_pos)) == True:
              time.sleep(0.1)
              screen_state = "fractal setup"  # Go back to fractal setup menu
               
        pg.display.flip()
        clock.tick(30)


# Main
main_menu()