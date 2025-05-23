import pygame as pg, math, time


fractal = None
mode = None
iterations = None
start = None
generate = None
page = 1
previous_page = None
screen_state = 'main'
BG_COLOR = (30, 30, 30)
GEN_DELAY = 0.001
LINE_THICKNESS = 2
LENGTH_MULTIPLIER = 1
auto_step_resize = False
resize_flag = False
debug_mode = False

(user_x, user_y) = (0, 0) 
WIDTH, HEIGHT = 800, 450  # 1600 x 900 by default


# FUNCTIONS/CLASSES/DICT
# Multiple iterations mode
def apply_rules(axiom, char_1, rule_1, char_2, rule_2, char_3, rule_3):
   return "".join(
       [
           rule_1 if char == char_1 else rule_2 if char == char_2 else rule_3 if char == char_3 else char
           for char in axiom
       ]
   )


# Single iteration mode
def get_result(iterations, axiom, char_1, rule_1, char_2, rule_2, char_3, rule_3):
   for gen in range(iterations):
       axiom = apply_rules(axiom, char_1, rule_1, char_2, rule_2, char_3, rule_3)
   return axiom


# Set up the iteration text drawer
def set_stage(iteration):
   screen.fill("black")
   iterations_live_text = TITLE_FONT.render(f"iteration: {iteration}", False, "white")
   screen.blit(iterations_live_text, (1 / 16 * WIDTH, 7 / 8 * HEIGHT))


# Takes the axiom and converts characters into drawing instructions
def interpret_movement(axiom, char_1, char_2, char_3, angle, length, color):
   global resize_flag

   (x, y) = fractal_info[fractal]["starting_pos"]
   stack = []
   current_angle = 0
   draw = True
  
   for char in axiom:
       if char == "F" or char == "G":
           new_x = x + (length * LENGTH_MULTIPLIER) * math.cos(current_angle)
           new_y = y - (length * LENGTH_MULTIPLIER) * math.sin(current_angle)
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
       elif char == "[":
           stack.append(((x, y), (new_x, new_y), (current_angle)))
       elif char == "]":
           (x, y), (new_x, new_y), current_angle = stack.pop(-1)
       if draw == True:
           pg.draw.line(screen, (color), (x, y), (new_x, new_y), LINE_THICKNESS)
       x, y = new_x, new_y
       
       if new_x > WIDTH or new_x < 0 or new_y > HEIGHT or new_y < 0:
           if auto_step_resize == True:
               resize_flag = True
       
       if GEN_DELAY != 0:
           pg.display.flip()
           time.sleep(GEN_DELAY) # Default is 0.001s delay


# Prepare the screen and variables for fractal creation
def draw_main():
   
   global resize_flag, LENGTH_MULTIPLIER
   screen.fill(BG_COLOR)


   # Set variables according to user input and fractal info
   color = fractal_info[fractal]["color"]
   angle = fractal_info[fractal]["angle"]
   length = fractal_info[fractal]["step"] * LENGTH_MULTIPLIER
   axiom = fractal_info[fractal]["axiom"]
   char_1, rule_1 = fractal_info[fractal]["char_1"], fractal_info[fractal]["rule_1"]
   char_2, rule_2 = fractal_info[fractal]["char_2"], fractal_info[fractal]["rule_2"]
   char_3, rule_3 = fractal_info[fractal]["char_3"], fractal_info[fractal]["rule_3"]


   # Multiple iterations mode
   resize_counter = 0
   if mode == "Multiple Iterations":
       for i in range(1, iterations + 1):
           # Iteration text
           set_stage(i)
           # Turn characters into movements
           axiom = apply_rules(axiom, char_1, rule_1, char_2, rule_2, char_3, rule_3)
           interpret_movement(axiom, char_1, char_2, char_3, angle, length, color)
           
           if resize_flag == True:
               resize_counter += 1
               LENGTH_MULTIPLIER = LENGTH_MULTIPLIER / 3
               resize_flag = False
       LENGTH_MULTIPLIER = LENGTH_MULTIPLIER * (3 ** resize_counter)

   # Single iteration mode
   else:
       set_stage(iterations)
       axiom = get_result(iterations, axiom, char_1, rule_1, char_2, rule_2, char_3, rule_3)
       interpret_movement(axiom, char_1, char_2, char_3, angle, length, color)


def main_menu():
   clock = pg.time.Clock()
   input_box1 = InputBox(
       13 / 32 * WIDTH, 5 / 6 * HEIGHT, 21 / 160 * WIDTH, 4 / 75 * HEIGHT, ""
   )
   input_boxes = [input_box1]


   global fractal, mode, iterations, start, generate, page, screen_state, BG_COLOR, user_x, user_y
   fractal_error_flag, mode_error_flag, iterations_error_flag = False, False, False


   done = False
   while not done:
       for event in pg.event.get():
           if event.type == pg.QUIT:
               done = True
           if screen_state == "main":
               for button in main_buttons:
                   button.handle_event(event, main_buttons, "start")
           elif screen_state == "settings":
               for button in back_button_s:
                   button.handle_event(event, back_button_s, "back_s")
               for button in theme_buttons:
                   button.handle_event(event, theme_buttons, "theme")
               for button in gen_speed_buttons:
                   button.handle_event(event, gen_speed_buttons, "GEN_DELAY")
               for button in line_thickness_buttons:
                   button.handle_event(event, line_thickness_buttons, "LINE_THICKNESS")
               for button in step_size_buttons:
                   button.handle_event(event, step_size_buttons, "LENGTH_MULTIPLIER")
               for button in auto_step_resize_buttons:
                   button.handle_event(event, auto_step_resize_buttons, "auto_step_resize")
               for button in debug_mode_buttons:
                   button.handle_event(event, debug_mode_buttons, "debug_mode")
           elif screen_state == "fractal setup":
               for button in page_numbers:
                   button.handle_event(event, page_numbers, "page")
               for button in fractal_buttons:
                   button.handle_event(event, fractal_buttons, "fractal")
               for button in mode_buttons:
                   button.handle_event(event, mode_buttons, "mode")
               for box in input_boxes:
                   box.handle_event(event, "iterations")
               for button in generate_button:
                   button.handle_event(event, generate_button, "generate")
               for button in back_button_fs:
                   button.handle_event(event, back_button_fs, "back_fs")
           else:
               for button in back_button_fd:
                   button.handle_event(event, back_button_fd, "back_fd")


       for box in input_boxes:
           box.update()
       
       (user_x, user_y) = pg.mouse.get_pos()
       
       if screen_state == "main":
           screen.fill(BG_COLOR)
           for button in main_buttons:
               button.draw(screen, (255, 255, 255))


       if screen_state == "settings":
           screen.fill(BG_COLOR)
           for button in back_button_s:
               button.draw(screen, (255, 102, 102))
           
           # Theme (dark / light)
           screen.blit(theme_text, (1 / 16 * WIDTH, 1 / 12 * HEIGHT))
           for button in theme_buttons:
               button.draw(screen, (255, 255, 255))
               
           # Generation speed (slow / normal / fast / instant)
           screen.blit(gen_speed_text, (1 / 16 * WIDTH, 15 / 56 * HEIGHT))
           for button in gen_speed_buttons:
              button.draw(screen, (255, 255, 255))
              
           # Line thickness (thin / normal / thick)
           screen.blit(line_thickness_text, (1 / 16 * WIDTH, 19 / 42 * HEIGHT))
           for button in line_thickness_buttons:
               button.draw(screen, (255, 255, 255))
               
           # Step size (small / normal / large)
           screen.blit(step_size_text, (1 / 16 * WIDTH, 107 / 168 * HEIGHT))
           for button in step_size_buttons:
               button.draw(screen, (255, 255, 255))
               
           # Auto step resize (off / on)
           screen.blit(auto_step_resize_text, (9 / 16 * WIDTH, 1 / 12 * HEIGHT))
           for button in auto_step_resize_buttons:
               button.draw(screen, (255, 255, 255))
               
           # Auto iteration resume (off / on)
           
           # Developer mode (off / on) (print extra information to the terminal like screen state, button presses, frame information, etc.)
           #screen.blit(debug_mode_text, (9 / 16 * WIDTH, 19 / 42 * HEIGHT))
           #for button in debug_mode_buttons:
               #button.draw(screen, (255, 255, 255))

       if screen_state == "fractal setup":
           screen.fill(BG_COLOR)
          
           # Fractal buttons
           for button in fractal_buttons:
               button.draw(screen, (255, 255, 255))
          
           # Upper cover for fractal buttons
           pg.draw.rect(screen, (30, 30, 30), ((9 / 128 * WIDTH, 0), (WIDTH, 1 / 6 * HEIGHT)))
          
           # Fractal prompt text
           screen.blit(
               fractal_prompt_text, (1 / 2 * WIDTH - 1 / 2 * fractal_prompt_text.get_width(), 1 / 12 * HEIGHT)
           )
          
           # Lower cover for fractal buttons
           pg.draw.rect(screen, (30, 30, 30), ((9 / 128 * WIDTH, 1 / 2 * HEIGHT), (WIDTH, HEIGHT)))
          
           screen.blit(
               mode_prompt_text, (1 / 2 * WIDTH - 1 / 2 * mode_prompt_text.get_width(), 13 / 24 * HEIGHT)
           )
          
           for button in page_numbers:
               button.draw(screen, (255, 255, 255))
          
           for button in mode_buttons:
               button.draw(screen, (255, 255, 255))


           screen.blit(
               iterations_prompt_text, (1 / 2 * WIDTH - 1 / 2 * iterations_prompt_text.get_width(), 3 / 4 * HEIGHT)
           )
           for box in input_boxes:
               box.draw(screen)


           for button in generate_button:
               button.draw(screen, 'light blue')
          
           for button in back_button_fs:
               button.draw(screen, (255, 102, 102))
              
           if fractal_error_flag:
               screen.blit(
                   fractal_error_text, (45 / 64 * WIDTH, 1 / 12 * HEIGHT)
               )
           if mode_error_flag:
               screen.blit(
                   mode_error_text, (45 / 64 * WIDTH, 13 / 24 * HEIGHT)
               )
           if iterations_error_flag:
               screen.blit(
                   iterations_error_text, (45 / 64 * WIDTH, 3 / 4 * HEIGHT)
               )


           if generate:
               # Check for errors
               fractal_error_flag = True if fractal == None else False
               mode_error_flag = True if mode == None else False
               iterations_error_flag = (
                   True if valid_int(iterations) == False else False
               )


               generate = False
               if (
                   not fractal_error_flag
                   and not mode_error_flag
                   and not iterations_error_flag
               ):
                   iterations = int(iterations)
                   screen_state = "fractal draw"
                   draw_main()


       if screen_state == "fractal draw":
           for button in back_button_fd:
               button.draw(screen, (255, 102, 102))


       pg.display.flip()
       clock.tick(60)  # FPS limit




# Validate user input
def valid_int(integer):
   try:
       integer = int(integer)
       return integer
   except:
       return False




# For the generation of text boxes
class InputBox:
   def __init__(self, x, y, w, h, text=""):
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
       width = max(3 / 16 * WIDTH, self.txt_surface.get_width() + 3 / 320 * WIDTH)
       self.rect.w = width


   def draw(self, screen):
       # Blit the text.
       screen.blit(
           self.txt_surface,
           (self.rect.x + 3 / 640 * WIDTH, self.rect.y + 1 / 120 * HEIGHT),
       )
       # Blit the rect.
       pg.draw.rect(screen, self.color, self.rect, int(3 / 1600 * WIDTH))




class Button:
   def __init__(self, text, x, y, width=260, height=40):
       self.text = text
       self.rect = pg.Rect(x, y, width, height)
       self.clicked = False


   def handle_event(self, event, buttons, variable):


       global fractal, mode, generate, page, previous_page, screen_state, BG_COLOR, GEN_DELAY, LINE_THICKNESS, LENGTH_MULTIPLIER, auto_step_resize, debug_mode
      
       # Have the page one button selected on startup
       if page == 1 and self.text == "1":
           self.clicked = True
       
       # Have dark theme selected on startup
       if BG_COLOR == (30, 30, 30) and self.text == "Dark":
           self.clicked = True
      
       # Normal speed selected on startup
       if GEN_DELAY == 0.001 and self.text == "Medium":
           self.clicked = True
       
       # Normal line thickness selected on startup
       if LINE_THICKNESS == 2 and self.text == "Normal":
           self.clicked = True
      
       # Default step size selected on startup
       if LENGTH_MULTIPLIER == 1 and self.text == "Default":
           self.clicked = True
           
       # Auto step resize turned off on startup
       if auto_step_resize == False and self.text == "Off":
           self.clicked = True
           
       # Debug mode turned off on startup
       if debug_mode == False and self.text == "Off ":
           self.clicked = True
       
       # Move the fractal buttons when a new page is selected
       if variable == "fractal" and previous_page and previous_page != page:
           if previous_page > page:
               self.rect = self.rect.move(0, (1 / 3) * (previous_page - page) * HEIGHT)
           else:
               self.rect = self.rect.move(0, (-1 / 3) * (page - previous_page) * HEIGHT)
           
       # Once the program moves onto mode we know the fractal buttons
       # have finished moving
       if variable == "mode":
           previous_page = page
       if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
           if self.rect.collidepoint(event.pos):
               if variable == "fractal" and user_y > 1 / 2 * HEIGHT or user_y < 1 / 6 * HEIGHT:
                   self.clicked = False
               else:
                   for button in buttons:
                       button.clicked = False
                   self.clicked = True
               if variable == "fractal":
                   if mouse_y <= 1 / 2 * HEIGHT:
                       fractal = self.text
               elif variable == "mode":
                   mode = self.text
               elif variable == "start" and self.text == "Start":
                   screen_state = "fractal setup"
                   self.clicked = False
               elif variable == "start" and self.text == "Settings":
                   screen_state = "settings"
                   self.clicked = False
               elif variable == "generate":
                   generate = True
                   self.clicked = False
               elif variable == "back_fd":
                   screen_state = "fractal setup"
                   self.clicked = False
               elif variable == "back_fs" or variable == "back_s":
                   screen_state = "main"
                   self.clicked = False
               elif variable == "theme":
                   if self.text == "Dark":
                       BG_COLOR = (30, 30, 30)
                   else:
                       BG_COLOR = (255, 255, 255)
               elif variable == "GEN_DELAY":
                   if self.text == "Slow":
                       GEN_DELAY = 0.01
                   elif self.text == "Medium":
                       GEN_DELAY = 0.001
                   elif self.text == "Fast":
                       GEN_DELAY = 0.0001
                   else:
                       GEN_DELAY = 0
                   print(GEN_DELAY)
               elif variable == "LINE_THICKNESS":
                   if self.text == "Thin":
                       LINE_THICKNESS = 1
                   elif self.text == "Normal":
                       LINE_THICKNESS = 2
                   else:
                       LINE_THICKNESS = 3
               elif variable == "LENGTH_MULTIPLIER":
                   if self.text == "Small":
                       LENGTH_MULTIPLIER = 0.5
                   elif self.text == "Default":
                       LENGTH_MULTIPLIER = 1
                   else:
                       LENGTH_MULTIPLIER = 2
                   print(LENGTH_MULTIPLIER)
               elif variable == "auto_step_resize":
                   if self.text == "Off":
                       auto_step_resize = False
                   else:
                       auto_step_resize = True
               elif variable == "debug_mode":
                   if self.text == "Off ":
                       debug_mode = False
                   else:
                       debug_mode = True
               elif variable == "page":
                   if page != int(self.text):  # Only activate page change if the page being selected is actually different
                       previous_page = page
                   page = int(self.text)


   def draw(self, surface, color):
       if self.rect.collidepoint(pg.mouse.get_pos()):
           color = (200, 200, 200)  # Light gray on hover
       if self.clicked:
           color = (150, 150, 150)  # Dark gray when clicked


       pg.draw.rect(surface, color, self.rect, 0, 5)
       text_surf = SMALL_FONT.render(self.text, True, (0, 0, 0))
       surface.blit(
           text_surf, self.rect.move(3 / 320 * WIDTH, 1 / 50 * HEIGHT)
       )  # Center text


# Fractal/button information
fractal_info = {
   "Harter Heighway Dragon": {
       "color": "magenta",
       "angle": 90,
       "step": 4,
       "axiom": "FX",
       "char_1": "X",
       "rule_1": "X+YF+",
       "char_2": "Y",
       "rule_2": "-FX-Y",
       "char_3": "",
       "rule_3": "",
       "starting_pos": (WIDTH / 2, HEIGHT / 2),
   },
   "Twindragon": {
       "color": "violet",
       "angle": 45,
       "step": 4,
       "axiom": "FX----FX",
       "char_1": "F",
       "rule_1": "Z",
       "char_2": "X",
       "rule_2": "+FX--FY+",
       "char_3": "Y",
       "rule_3": "-FX++FY-",
       "starting_pos": (WIDTH / 2, HEIGHT / 2),
   },
   "Hilbert Curve": {
       "color": "brown",
       "angle": 90,
       "step": 4,
       "axiom": "A",
       "char_1": "A",
       "rule_1": "-BF+AFA+FB-",
       "char_2": "B",
       "rule_2": "+AF-BFB-FA+",
       "char_3": "",
       "rule_3": "",
       "starting_pos": (1 / 3 * WIDTH, 5 / 6 * HEIGHT),
   },
   "Koch Curve": {
       "color": "light blue",
       "angle": 60,
       "step": 4,
       "axiom": "F",
       "char_1": "F",
       "rule_1": "F-F++F-F",
       "char_2": "",
       "rule_2": "",
       "char_3": "",
       "rule_3": "",
       "starting_pos": (1 / 8 * WIDTH, 3 / 4 * HEIGHT),
   },
   "Koch Snowflake (Triangle)": {
       "color": "yellow",
       "angle": 60,
       "step": 4,
       "axiom": "F++F++F",
       "char_1": "F",
       "rule_1": "F-F++F-F",
       "char_2": "",
       "rule_2": "",
       "char_3": "",
       "rule_3": "",
       "starting_pos": (1 / 3 * WIDTH, 1 / 4 * HEIGHT),
   },
   "Koch Snowflake (Hexagon)": {
       "color": "yellow",
       "angle": 60,
       "step": 4,
       "axiom": "F+F+F+F+F+F",
       "char_1": "F",
       "rule_1": "F+F--F+F",
       "char_2": "",
       "rule_2": "",
       "char_3": "",
       "rule_3": "",
       "starting_pos": (1 / 3 * WIDTH, 1 / 4 * HEIGHT),
   },
   "Koch Anti-Snowflake": {
       "color": "red",
       "angle": 60,
       "step": 4,
       "axiom": "F++F++F",
       "char_1": "F",
       "rule_1": "F+F--F+F",
       "char_2": "",
       "rule_2": "",
       "char_3": "",
       "rule_3": "",
       "starting_pos": (1 / 3 * WIDTH, 1 / 4 * HEIGHT),
   },
   "Levy Dragon": {
       "color": "red",
       "angle": 45,
       "step": 4,
       "axiom": "F",
       "char_1": "F",
       "rule_1": "+F--F+",
       "char_2": "",
       "rule_2": "",
       "char_3": "",
       "rule_3": "",
       "starting_pos": (WIDTH / 2, HEIGHT / 2),
   },
   "Levy Diamond": {
       "color": "green",
       "angle": 30,
       "step": 4,
       "axiom": "F",
       "char_1": "F",
       "rule_1": "++F--F--F++",
       "char_2": "",
       "rule_2": "",
       "char_3": "",
       "rule_3": "",
       "starting_pos": (WIDTH / 2, HEIGHT / 2),
   },
   "Levy Tapestry (Inside)": {
       "color": "purple",
       "angle": 45,
       "step": 4,
       "axiom": "F++F++F++F",
       "char_1": "F",
       "rule_1": "+F--F+",
       "char_2": "",
       "rule_2": "",
       "char_3": "",
       "rule_3": "",
       "starting_pos": (WIDTH / 2, HEIGHT / 2),
   },
   "Levy Tapestry (Outside)": {
       "color": "yellow",
       "angle": 45,
       "step": 4,
       "axiom": "F++F++F++F",
       "char_1": "F",
       "rule_1": "-F++F-",
       "char_2": "",
       "rule_2": "",
       "char_3": "",
       "rule_3": "",
       "starting_pos": (WIDTH / 2, HEIGHT / 2),
   },
   "McWorter's Pentigree": {
       "color": "light green",
       "angle": 36,
       "step": 4,
       "axiom": "F",
       "char_1": "F",
       "rule_1": "+F++F----F--F++F++F-",
       "char_2": "",
       "rule_2": "",
       "char_3": "",
       "rule_3": "",
       "starting_pos": (WIDTH / 2, HEIGHT / 2),
   },
   "Dentrite": {
       "color": "cyan",
       "angle": 72,
       "step": 4,
       "axiom": "F",
       "char_1": "F",
       "rule_1": "F+F-F--F+F+F",
       "char_2": "",
       "rule_2": "",
       "char_3": "",
       "rule_3": "",
       "starting_pos": (1 / 2 * WIDTH, 5 / 6 * HEIGHT),
   },
   "Peano-Gosper Curve": {
       "color": "orange",
       "angle": 60,
       "step": 4,
       "axiom": "F",
       "char_1": "F",
       "rule_1": "F-G--G+F++FF+G-",
       "char_2": "G",
       "rule_2": "+F-GG--G-F++F+G",
       "char_3": "",
       "rule_3": "",
       "starting_pos": (WIDTH / 2, HEIGHT / 2),
   },
   "Peano-Gosper (Boundary)": {
       "color": "orange",
       "angle": 60,
       "step": 4,
       "axiom": "F+F+F+F+F+F+",
       "char_1": "F",
       "rule_1": "F-F+F",
       "char_2": "",
       "rule_2": "",
       "char_3": "",
       "rule_3": "",
       "starting_pos": (WIDTH / 2, HEIGHT / 2),
   },
   "Sierpinski Curve": {
       "color": "pink",
       "angle": 45,
       "step": 8,
       "axiom": "F--XF--F--XF",
       "char_1": "X",
       "rule_1": "XF+G+XF--F--XF+G+X",
       "char_2": "",
       "rule_2": "",
       "char_3": "",
       "rule_3": "",
       "starting_pos": (1 / 2 * WIDTH, 7 / 8 * HEIGHT),
   },
   "Sierpinski Triangle": {
       "color": "green",
       "angle": 120,
       "step": 8,
       "axiom": "F-G-G",
       "char_1": "F",
       "rule_1": "F-G+F+G-F",
       "char_2": "G",
       "rule_2": "GG",
       "char_3": "",
       "rule_3": "",
       "starting_pos": (1 / 3 * WIDTH, 5 / 6 * HEIGHT),
   },
   "Sierpinski Arrowhead Curve": {
       "color": "orange",
       "angle": 60,
       "step": 8,
       "axiom": "XF",
       "char_1": "X",
       "rule_1": "YF+XF+Y",
       "char_2": "Y",
       "rule_2": " XF-YF-X",
       "char_3": "",
       "rule_3": "",
       "starting_pos": (1 / 3 * WIDTH, 1 / 2 * HEIGHT),
   },
   "Sierpinski Carpet": {
       "color": "blue",
       "angle": 90,
       "step": 4,
       "axiom": "F",
       "char_1": "F",
       "rule_1": "F+F-F-F-UGD+F+F+F-F",
       "char_2": "G",
       "rule_2": "GGG",
       "char_3": "",
       "rule_3": "",
       "starting_pos": (1 / 5 * WIDTH, 1 / 2 * HEIGHT),
   },
   "Terdragon": {
       "color": "blue",
       "angle": 30,
       "step": 4,
       "axiom": "F",
       "char_1": "F",
       "rule_1": "+F----F++++F-",
       "char_2": "",
       "rule_2": "",
       "char_3": "",
       "rule_3": "",
       "starting_pos": (WIDTH / 2, HEIGHT / 2),
   },
   "Terdragon (Boundary)": {
       "color": "yellow",
       "angle": 30,
       "step": 4,
       "axiom": "FX------FX",
       "char_1": "F",
       "rule_1": "Z",
       "char_2": "X",
       "rule_2": "+FX--FY+",
       "char_3": "Y",
       "rule_3": "-FX++FY-",
       "starting_pos": (WIDTH / 2, HEIGHT / 2),
   },
   "Fudgeflake": {
       "color": "cyan",
       "angle": 30,
       "step": 4,
       "axiom": "F++++F++++F",
       "char_1": "F",
       "rule_1": "+F----F++++F-",
       "char_2": "",
       "rule_2": "",
       "char_3": "",
       "rule_3": "",
       "starting_pos": (WIDTH / 2, HEIGHT / 2),
   },
   "Fudgeflake (Boundary)": {
       "color": "cyan",
       "angle": 30,
       "step": 4,
       "axiom": "FX++++FX++++FX",
       "char_1": "F",
       "rule_1": "Z",
       "char_2": "X",
       "rule_2": "-FY++FX-",
       "char_3": "Y",
       "rule_3": "+FY--FX+",
       "starting_pos": (WIDTH / 2, HEIGHT / 2),
   },
   "plant": {
       "color": "lime",
       "angle": 25,
       "step": 4,
       "axiom": "--X",
       "char_1": "X",
       "rule_1": "F-[[X]+X]+F[+FX]-X",
       "char_2": "F",
       "rule_2": "FF",
       "char_3": "",
       "rule_3": "",
       "starting_pos": (1 / 4 * WIDTH, 4 / 5 * HEIGHT),
   },
   "Algae": {
      "color": "orange",
      "angle": 0,
      "step": 4,
      "axiom": "F",
      "char_1": "F",
      "rule_1": "FG",
      "char_2": "G",
      "rule_2": "F",
      "char_3": "",
      "rule_3": "",
      "starting_pos": (1 / 2 * WIDTH, 1 / 2 * HEIGHT),
   },
}


main_button_info = {
   "Start": {
       "position": (677 / 1440 * WIDTH, 1 / 2 * HEIGHT),
   },
   "Settings": {
       "position": (677 / 1440 * WIDTH, 7 / 12 * HEIGHT),
   },
}


fractal_setup_button_info = {
   "Multiple Iterations": {
       "position": (29 / 128 * WIDTH, 5 / 8 * HEIGHT),
   },
   "Single Iteration": {
       "position": (323 / 640 * WIDTH, 5 / 8 * HEIGHT),
   },
}


theme_button_info = {
   "Dark": {
       "position": (1 / 16 * WIDTH, 1 / 7 * HEIGHT)
   },
   "Light": {
       "position": (287 / 1600 * WIDTH, 1 / 7 * HEIGHT)
   }
}

gen_speed_button_info = {
   "Slow": {
       "position": (1 / 16 * WIDTH, 55 / 168 * HEIGHT)
  },
  "Medium": {
       "position": (287 / 1600 * WIDTH, 55 / 168 * HEIGHT)
  },
  "Fast": {
       "position": (237 / 800 * WIDTH, 55 / 168 * HEIGHT)
  },
  "Instant": {
       "position": (661 / 1600 * WIDTH, 55 / 168 * HEIGHT)
  }
}

line_thickness_button_info = {
  "Thin": {
      "position": (1 / 16 * WIDTH, 43 / 84 * HEIGHT)
  },
  "Normal": {
      "position": (287 / 1600 * WIDTH, 43 / 84 * HEIGHT)
  },
  "Thick": {
      "position": (237 / 800 * WIDTH, 43 / 84 * HEIGHT)
  }
}

step_button_info = {
  "Small": {
      "position": (1 / 16 * WIDTH, 39 / 56 * HEIGHT)
  },
  "Default": {
      "position": (287 / 1600 * WIDTH, 39 / 56 * HEIGHT)
  },
  "Large": {
      "position": (237 / 800 * WIDTH, 39 / 56 * HEIGHT)
  }
}

auto_step_resize_button_info = {
  "Off": {
      "position": (9 / 16 * WIDTH, 1 / 7 * HEIGHT)
  },
  "On": {
      "position": (1087 / 1600 * WIDTH, 1 / 7 * HEIGHT)
  }
}

debug_mode_button_info = {
  "Off ": {
      "position": (9 / 16 * WIDTH, 43 / 84 * HEIGHT)
  },
  "On ": {
      "position": (1087 / 1600 * WIDTH, 43 / 84 * HEIGHT)
  }
}

# PYGAME INITIATION/BUTTON DEF
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Aiden's Master Fractal Generator v2.4")
COLOR_INACTIVE = pg.Color("lightskyblue3")
COLOR_ACTIVE = pg.Color("dodgerblue2")
TITLE_FONT = pg.font.Font(None, int(13 / 150 * HEIGHT))
BIG_FONT = pg.font.Font(None, int(3 / 50 * HEIGHT))
SMALL_FONT = pg.font.Font(None, int(7 / 150 * HEIGHT))
SMALLER_FONT = pg.font.Font(None, int(6 / 150 * HEIGHT))


# Text lines setup
back = BIG_FONT.render("Back", False, 'white')
apply = BIG_FONT.render("Apply", False, 'white')


fractal_prompt_text = BIG_FONT.render("Choose a fractal", False, "white")
fractal_error_text = BIG_FONT.render("Pick a fractal!", False, "red")
mode_prompt_text = BIG_FONT.render("Select a mode", False, "white")
mode_error_text = BIG_FONT.render("Select a mode!", False, "red")
iterations_prompt_text = BIG_FONT.render("Enter iterations to generate", False, "white")
iterations_error_text = BIG_FONT.render("Invalid integer!", False, "red")


theme_text = SMALL_FONT.render('Theme', False, 'white')
gen_speed_text = SMALL_FONT.render('Generation Speed', False, 'white')
line_thickness_text = SMALL_FONT.render('Line Thickness', False, 'white')
step_size_text = SMALL_FONT.render('Step Size', False, 'white')
auto_step_resize_text = SMALL_FONT.render('Auto Step Resize', False, 'white')
debug_mode_text = SMALL_FONT.render('Debug Mode', False, 'white')

# Fractal buttons
fractal_buttons = []
button_width = 43 / 160 * WIDTH
button_height = 1 / 15 * HEIGHT
row_padding = 1 / 60 * HEIGHT
col_padding = 3 / 320 * WIDTH
buttons_per_row = 3
start_x = 9 / 128 * WIDTH
start_y = 1 / 6 * HEIGHT


for i, name in enumerate(fractal_info):
   row = i // buttons_per_row
   col = i % buttons_per_row
   x = start_x + col * (button_width + col_padding)
   y = start_y + row * (button_height + row_padding)
   button = Button(name, x, y, button_width, button_height)
   fractal_buttons.append(button)


# Mode buttons
mode_buttons = []
for i, name in enumerate(fractal_setup_button_info):
   (x, y) = fractal_setup_button_info[name]["position"]
   button = Button(name, x, y, button_width, button_height)
   mode_buttons.append(button)


# Generate button
generate_button = []
button = Button(
   "Generate", 225 / 256 * WIDTH, 9 / 10 * HEIGHT, button_width / 2.6, button_height
)
generate_button.append(button)


# Main buttons
main_buttons = []
for i, name in enumerate(main_button_info):
   (x, y) = main_button_info[name]["position"]
   button = Button(name, x, y, button_width / 2.5, button_height)
   main_buttons.append(button)


# Back button (fractal setup)
back_button_fs = []
button = Button(
 "Back",
 1 / 16 * WIDTH, 9 / 10 * HEIGHT,
 button_width / 4.5,
 button_height
)
back_button_fs.append(button)


# Back button (fractal draw)
back_button_fd = []
button = Button(
 "Back",
 1 / 16 * WIDTH, 1 / 8 * HEIGHT,
 button_width / 4.5,
 button_height
)
back_button_fd.append(button)


# Back button (settings)
back_button_s = []
button = Button(
   "Back",
   1 / 16 * WIDTH, 9 / 10 * HEIGHT,
   button_width / 4.5,
   button_height
)
back_button_s.append(button)


# Theme buttons
theme_buttons = []
for i, name in enumerate(theme_button_info):
   (x, y) = theme_button_info[name]["position"]
   button = Button(name, x, y, button_width / 2.5, button_height)
   theme_buttons.append(button)

# Generation speed buttons
gen_speed_buttons = []
for i, name in enumerate(gen_speed_button_info):
    (x, y) = gen_speed_button_info[name]["position"]
    button = Button(name, x, y, button_width / 2.5, button_height)
    gen_speed_buttons.append(button)

# Line thickness buttons
line_thickness_buttons = []
for i, name in enumerate(line_thickness_button_info):
     (x, y) = line_thickness_button_info[name]["position"]
     button = Button(name, x, y, button_width / 2.5, button_height)
     line_thickness_buttons.append(button)

# Step size buttons
step_size_buttons = []
for i, name in enumerate(step_button_info):
     (x, y) = step_button_info[name]["position"]
     button = Button(name, x, y, button_width / 2.5, button_height)
     step_size_buttons.append(button)

# Auto step resize buttons
auto_step_resize_buttons = []
for i, name in enumerate(auto_step_resize_button_info):
     (x, y) = auto_step_resize_button_info[name]["position"]
     button = Button(name, x, y, button_width / 2.5, button_height)
     auto_step_resize_buttons.append(button)

# Debug mode buttons
debug_mode_buttons = []
for i, name in enumerate(debug_mode_button_info):
     (x, y) = debug_mode_button_info[name]["position"]
     button = Button(name, x, y, button_width / 2.5, button_height)
     debug_mode_buttons.append(button)

# Fractal page numbers
page_numbers = []
for i in range(3):
   x = 14/15 * WIDTH
   y = 1 / 6 * HEIGHT + i * (button_height + row_padding)
   button = Button(str(i + 1), x, y, button_width / 9, button_height)
   page_numbers.append(button)


# MAIN
main_menu()
