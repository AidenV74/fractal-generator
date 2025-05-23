import pygame as pg, math, time

fractal, mode, iterations, start, generate, back, page, page_change = None, None, None, None, None, None, 0, None
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
    iteration_text = screen.blit(iterations_live_text, (1 / 16 * WIDTH, 7 / 8 * HEIGHT))


# Takes the axiom and converts characters into drawing instructions
def interpret_movement(axiom, char_1, char_2, char_3, angle, length, color):

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

        pg.display.flip()
        time.sleep(0.001)


# Prepare the screen and variables for fractal creation
def draw_main():
    screen.fill("black")

    # Set variables according to user input and fractal info
    color = fractal_info[fractal]["color"]
    angle = fractal_info[fractal]["angle"]
    length = fractal_info[fractal]["step"]
    axiom = fractal_info[fractal]["axiom"]
    char_1, rule_1 = fractal_info[fractal]["char_1"], fractal_info[fractal]["rule_1"]
    char_2, rule_2 = fractal_info[fractal]["char_2"], fractal_info[fractal]["rule_2"]
    char_3, rule_3 = fractal_info[fractal]["char_3"], fractal_info[fractal]["rule_3"]

    # Multiple iterations mode
    if mode == "Multiple Iterations":
        for i in range(1, iterations + 1):
            # Iteration text
            set_stage(i)
            # Turn characters into movements
            axiom = apply_rules(axiom, char_1, rule_1, char_2, rule_2, char_3, rule_3)
            interpret_movement(axiom, char_1, char_2, char_3, angle, length, color)

    # Single iteration mode
    else:
        set_stage(iterations)
        axiom = get_result(iterations, axiom, char_1, rule_1, char_2, rule_2, char_3, rule_3)
        interpret_movement(axiom, char_1, char_2, char_3, angle, length, color)


def main_menu():
    clock = pg.time.Clock()
    input_box1 = InputBox(
        9 / 128 * WIDTH, 5 / 6 * HEIGHT, 21 / 160 * WIDTH, 4 / 75 * HEIGHT, ""
    )
    input_boxes = [input_box1]
    screen_state = "main"

    global fractal, mode, iterations, start, generate, back, page
    fractal_error_flag, mode_error_flag, iterations_error_flag = False, False, False

    done = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if screen_state == "main":
                for button in start_button:
                    button.handle_event(event, pg.mouse.get_pos()[1], start_button, "start")
            elif screen_state == "fractal setup":
                for button in page_numbers:
                    button.handle_event(event, pg.mouse.get_pos()[1], page_numbers, "page")
                for button in fractal_buttons:
                    button.handle_event(event, pg.mouse.get_pos()[1], fractal_buttons, "fractal")
                for button in mode_buttons:
                    button.handle_event(event, pg.mouse.get_pos()[1], mode_buttons, "mode")
                for box in input_boxes:
                    box.handle_event(event, "iterations")
                for button in generate_button:
                    button.handle_event(event, pg.mouse.get_pos()[1], generate_button, "generate")
            else:
                for button in back_button:
                    button.handle_event(event, pg.mouse.get_pos()[1], back_button, "back")

        for box in input_boxes:
            box.update()
        
        
        if screen_state == "main":
            screen.fill((30, 30, 30))
            for button in start_button:
                button.draw(screen)
            if start:
                screen_state = "fractal setup"

        if screen_state == "fractal setup":
            screen.fill((30, 30, 30))
            
            # Fractal buttons
            for button in fractal_buttons:
                button.draw(screen)
            
            # Upper cover for fractal buttons
            pg.draw.rect(screen, (30, 30, 30), ((9 / 128 * WIDTH, 0), (WIDTH, 1 / 6 * HEIGHT)))
            
            # Fractal prompt text
            fractal_prompt = screen.blit(
                fractal_prompt_text, (9 / 128 * WIDTH, 1 / 12 * HEIGHT)
            )
            
            # Lower cover for fractal buttons
            pg.draw.rect(screen, (30, 30, 30), ((9 / 128 * WIDTH, 1 / 2 * HEIGHT), (WIDTH, HEIGHT)))
            
            mode_prompt = screen.blit(
                mode_prompt_text, (9 / 128 * WIDTH, 13 / 24 * HEIGHT)
            )
            
            for button in page_numbers:
                button.draw(screen)
            
            for button in mode_buttons:
                button.draw(screen)

            iterations_prompt = screen.blit(
                iterations_prompt_text, (9 / 128 * WIDTH, 3 / 4 * HEIGHT)
            )
            for box in input_boxes:
                box.draw(screen)

            for button in generate_button:
                button.draw(screen)

            if fractal_error_flag:
                fractal_error = screen.blit(
                    fractal_error_text, (25 / 64 * WIDTH, 1 / 12 * HEIGHT)
                )
            if mode_error_flag:
                mode_error = screen.blit(
                    mode_error_text, (25 / 64 * WIDTH, 13 / 24 * HEIGHT)
                )
            if iterations_error_flag:
                iterations_error = screen.blit(
                    iterations_error_text, (25 / 64 * WIDTH, 3 / 4 * HEIGHT)
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
            for button in back_button:
                button.draw(screen)
            if back == True:
                time.sleep(0.1)
                screen_state = "fractal setup"
                back = False

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

    def handle_event(self, event, mouse_y, buttons, variable):

        global fractal, mode, start, generate, back, page, page_change
        
        # Have the page one button selected on startup
        if page == 0 and self.text == "1":
            self.clicked = True
        
        # Move the fractal buttons when a new page is selected
        if variable == "fractal" and page_change:
            if page == 2:
                self.rect = self.rect.move(0, -1 / 3 * HEIGHT)
            elif page == 1:
                self.rect = self.rect.move(0, 1 / 3 * HEIGHT)
        
        # Once the program moves onto mode we know the fractal buttons
        # have finished moving
        if variable == "mode":
            page_change = False
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if variable == "fractal" and mouse_y > 1 / 2 * HEIGHT:
                    self.clicked == False
                else:
                    for button in buttons:
                        button.clicked = False
                    self.clicked = True
                if variable == "fractal":
                    if mouse_y <= 1 / 2 * HEIGHT:
                        fractal = self.text
                elif variable == "mode":
                    mode = self.text
                elif variable == "start":
                    start = True
                    self.clicked = False
                elif variable == "generate":
                    generate = True
                    self.clicked = False
                elif variable == "back":
                    back = True
                    self.clicked = False
                elif variable == "page":
                    if page != int(self.text):  # Only activate page change if the page being selected is actually different
                        page_change = True
                    page = int(self.text)

    def draw(self, surface, rect_width=0, rect_radius=5):
        color = (255, 255, 255)  # Default white
        if self.rect.collidepoint(pg.mouse.get_pos()):
            color = (200, 200, 200)  # Light gray on hover
        if self.clicked:
            color = (150, 150, 150)  # Dark gray when clicked

        pg.draw.rect(surface, color, self.rect, rect_width, rect_radius)
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
        "axiom": "F",
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
}

fractal_setup_button_info = {
    "Multiple Iterations": {
        "color": "grey",
        "position": (9 / 128 * WIDTH, 5 / 8 * HEIGHT),
    },
    "Single Iteration": {
        "color": "grey",
        "position": (223 / 640 * WIDTH, 5 / 8 * HEIGHT),
    },
}

# PYGAME INITIATION/BUTTON DEF
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Aiden's Master Fractal Generator v.2.2")
COLOR_INACTIVE = pg.Color("lightskyblue3")
COLOR_ACTIVE = pg.Color("dodgerblue2")
TITLE_FONT = pg.font.Font(None, int(13 / 150 * HEIGHT))
BIG_FONT = pg.font.Font(None, int(3 / 50 * HEIGHT))
SMALL_FONT = pg.font.Font(None, int(7 / 150 * HEIGHT))
SMALLER_FONT = pg.font.Font(None, int(6 / 150 * HEIGHT))

# Text lines setup
back = BIG_FONT.render("Back", False, ("white"))

fractal_prompt_text = BIG_FONT.render("Choose a fractal", False, "white")
fractal_error_text = BIG_FONT.render("Pick a fractal!", False, "red")
mode_prompt_text = BIG_FONT.render("Select a mode", False, "white")
mode_error_text = BIG_FONT.render("Select a mode!", False, "red")
iterations_prompt_text = BIG_FONT.render("Enter iterations to generate", False, "white")
iterations_error_text = BIG_FONT.render("Invalid integer!", False, "red")

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
    "Generate", 51 / 128 * WIDTH, 5 / 6 * HEIGHT, button_width, button_height
)
generate_button.append(button)

# Start button
start_button = []
button = Button(
    "Start",
    1 / 2 * WIDTH - 1 / 2 * button_width / 4.5,
    1 / 2 * HEIGHT,
    button_width / 4.5,
    button_height
)
start_button.append(button)

# Back button
back_button = []
button = Button(
  "Back",
  1 / 16 * WIDTH, 1 / 8 * HEIGHT,
  button_width / 4.5,
  button_height
)
back_button.append(button)

# Fractal page numbers
page_numbers = []
for i in range(2):
    x = 14/15 * WIDTH
    y = 1 / 6 * HEIGHT + i * (button_height + row_padding)
    button = Button(str(i + 1), x, y, button_width / 9, button_height)
    page_numbers.append(button)

# MAIN
main_menu()