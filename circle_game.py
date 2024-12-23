import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
DISPLAYSURF = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption('Circle game')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
rainbow_colours = [
    (255, 0, 0),   # Red
    (255, 165, 0), # Orange
    (255, 255, 0), # Yellow
    (0, 255, 0),   # Green
    (0, 0, 255),   # Blue
    (75, 0, 130),  # Indigo
    (238, 130, 238) # Violet
]

# Global Variables
gravity = 0.5

# Circle class
class Circle:
    def __init__(self, position, radius, color):
        self.x_position = position[0]
        self.y_position = position[1]
        self.radius = radius
        self.color = color
        self.color_index = 0
        self.y_velocity = 0
        self.x_velocity = 0
        self.stopped_counter = 0
        self.stopped = False

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x_position, self.y_position), self.radius)

    def cycle_color(self):
        self.color_index = (self.color_index + 1) % len(rainbow_colours)
        self.color = rainbow_colours[self.color_index]
    
    def update_position(self):
        
        # Reverse direction when circle hits edge
        if self.y_position >= DISPLAYSURF.get_height() - self.radius:
            self.y_velocity = ( self.y_velocity * -1 ) * 0.8 # 'Bounce' and lose a bit of speed 
            
            # If we're at the edge with low velocity, squish ("dampen") the bounce.
            # Count how many times we've been around the loop whilst stopped.
            # After 30 'stopped' loops, set the 'stopped' variable so that this circle is deleted.
            if abs( self.y_velocity ) < 4:
                self.y_velocity = self.y_velocity / 2 # Low velocity. Don't let it bounce much.
                self.stopped_counter += 1
                if self.stopped_counter >= 16:
                    self.stopped = True

        # Update the position. If we are 'below' the ground, set our position to the ground.
        self.y_position = self.y_position - self.y_velocity
        if( self.y_position > DISPLAYSURF.get_height() - self.radius ):
            self.y_position = DISPLAYSURF.get_height() - self.radius

        self.y_velocity = self.y_velocity - gravity # Added gravity to y velocity

# Pause Menu
def pause_menu():
    global DISPLAYSURF  # Ensure DISPLAYSURF is treated as a global variable
    font = pygame.font.SysFont(None, 48)
    button_font = pygame.font.SysFont(None, 36)

    # Pause Menu title
    pause_text = font.render('Paused', True, (255, 255, 255))
    resume_button = pygame.Rect(150, 150, 100, 50)
    exit_button = pygame.Rect(150, 220, 100, 50)

    while True:
        DISPLAYSURF.fill((0, 0, 0))

        # Draw pause text and buttons
        DISPLAYSURF.blit(pause_text, (DISPLAYSURF.get_width() // 2 - pause_text.get_width() // 2, DISPLAYSURF.get_height() // 2 - 100))
        pygame.draw.rect(DISPLAYSURF, (100, 100, 100), resume_button)
        pygame.draw.rect(DISPLAYSURF, (100, 100, 100), exit_button)

        resume_text = button_font.render('Resume', True, (255, 255, 255))
        exit_text = button_font.render('Exit', True, (255, 255, 255))

        DISPLAYSURF.blit(resume_text, (resume_button.centerx - resume_text.get_width() // 2, resume_button.centery - resume_text.get_height() // 2))
        DISPLAYSURF.blit(exit_text, (exit_button.centerx - exit_text.get_width() // 2, exit_button.centery - exit_text.get_height() // 2))

        # Event handling for pause menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if resume_button.collidepoint(mouse_pos):
                    return True  # Return True to resume the game
                elif exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()

        pygame.display.update()

# Start Menu
def start_menu():
    global DISPLAYSURF  # Ensure DISPLAYSURF is treated as a global variable
    font = pygame.font.SysFont(None, 48)
    subtitle_font = pygame.font.SysFont(None, 32)
    button_font = pygame.font.SysFont(None, 36)

    # Start Menu title and buttons
    title_text = font.render('Circle Game', True, (255, 255, 255))
    subtitle_text = subtitle_font.render('by Django Wright', True, (255, 255, 255))
    start_button = pygame.Rect(300, 300, 200, 50)
    exit_button = pygame.Rect(300, 370, 200, 50)

    while True:
        DISPLAYSURF.fill((0, 0, 0))

        # Draw start menu title and subtitle
        DISPLAYSURF.blit(title_text, (DISPLAYSURF.get_width() // 2 - title_text.get_width() // 2, 100))
        DISPLAYSURF.blit(subtitle_text, (DISPLAYSURF.get_width() // 2 - subtitle_text.get_width() // 2, 160))

        # Draw start and exit buttons
        pygame.draw.rect(DISPLAYSURF, (100, 100, 100), start_button)
        pygame.draw.rect(DISPLAYSURF, (100, 100, 100), exit_button)

        start_text = button_font.render('Start Game', True, (255, 255, 255))
        exit_text = button_font.render('Exit', True, (255, 255, 255))

        DISPLAYSURF.blit(start_text, (start_button.centerx - start_text.get_width() // 2, start_button.centery - start_text.get_height() // 2))
        DISPLAYSURF.blit(exit_text, (exit_button.centerx - exit_text.get_width() // 2, exit_button.centery - exit_text.get_height() // 2))

        # Event handling for start menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if start_button.collidepoint(mouse_pos):
                    return True  # Return True to start the game
                elif exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()

        pygame.display.update()

# Main game loop
def main_game():
    global DISPLAYSURF  # Ensure DISPLAYSURF is treated as a global variable
    mainLoop = True
    rainbow_mode = False
    eraser_mode = False
    paused = False  # Flag for pause state
    clock = pygame.time.Clock()
    cycle_delay = 0
    CYCLE_DELAY_LIMIT = 10  # Adjust this value to control speed (higher is slower)
    show_game_menu = False

    # Pause button location
    pause_button = pygame.Rect(10, 10, 50, 30)
    menu_button = pygame.Rect(DISPLAYSURF.get_width() // 2 - 50, 10, 100, 30)  # MENU button at top center

    circles = []

    while mainLoop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainLoop = False

            if event.type == pygame.VIDEORESIZE:
                DISPLAYSURF = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                menu_button = pygame.Rect(DISPLAYSURF.get_width() // 2 - 50, 10, 100, 30)

            # Check for mouse button down event
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    # Get the mouse position
                    mouse_pos = event.pos

                    # Check if pause button was clicked
                    if pause_button.collidepoint(mouse_pos):
                        paused = not paused  # Toggle pause state

                    # Check if the "MENU" button was clicked
                    if menu_button.collidepoint(mouse_pos):
                        show_game_menu = not show_game_menu  # Toggle game menu visibility

                    # Check if reset button area was clicked
                    elif DISPLAYSURF.get_width() - 50 <= mouse_pos[0] <= DISPLAYSURF.get_width() - 10 and 10 <= mouse_pos[1] <= 50:
                        circles.clear()
                        if rainbow_mode:
                            rainbow_mode = False

                    # Check if game menu is open and buttons within it
                    elif show_game_menu:
                        if DISPLAYSURF.get_width() // 2 - 125 <= mouse_pos[0] <= DISPLAYSURF.get_width() // 2 + 125:
                            if 80 <= mouse_pos[1] <= 100:
                                rainbow_mode = not rainbow_mode  # Toggle RGB Mode
                            elif 120 <= mouse_pos[1] <= 140:
                                eraser_mode = not eraser_mode  # Toggle Eraser Mode
                            elif 160 <= mouse_pos[1] <= 180:
                                circles.clear()  # Clear all circles
                            elif 200 <= mouse_pos[1] <= 220:
                                mainLoop = False  # Exit game
                        show_game_menu = not show_game_menu  # Toggle game menu visibility

                    else:
                        if eraser_mode:
                            # Check if a circle was clicked and remove it
                            for circle in circles[:]:
                                if (circle.x_position - mouse_pos[0])**2 + (circle.y_position - mouse_pos[1])**2 <= circle.radius**2:
                                    circles.remove(circle)
                                    break
                        else:
                            if not paused:  # Prevent circle creation when paused
                                # Generate random circle size and color
                                circle_radius = random.randint(10, 20)
                                circle_color = (
                                    random.randint(0, 255),  # Red
                                    random.randint(0, 255),  # Green
                                    random.randint(0, 255)   # Blue
                                )

                                # Create a new circle and add it to the list
                                new_circle = Circle(mouse_pos, circle_radius, circle_color)
                                circles.append(new_circle)

        if paused:
            # Pass control to pause menu, and if the user resumes, set paused = False
            paused = not pause_menu()
        else:
            # Clear the screen
            DISPLAYSURF.fill((0, 0, 0))

            # Remove all 'stopped' circles
            circles = [circle for circle in circles if circle.stopped == False ]

              # Draw all circles and update position of circles
            for circle in circles:
                circle.update_position()
                circle.draw(DISPLAYSURF)

            # If rainbow mode is active, cycle colors
            if rainbow_mode:
                cycle_delay += 1
                if cycle_delay >= CYCLE_DELAY_LIMIT:
                    for circle in circles:
                        circle.cycle_color()
                    cycle_delay = 0

            # Draw the pause button
            pygame.draw.rect(DISPLAYSURF, (255, 255, 255), pause_button)
            pause_text = pygame.font.SysFont(None, 24).render('Pause', True, (0, 0, 0))
            DISPLAYSURF.blit(pause_text, (pause_button.centerx - pause_text.get_width() // 2, pause_button.centery - pause_text.get_height() // 2))

            # Draw the MENU button at the top center
            pygame.draw.rect(DISPLAYSURF, (255, 255, 255), menu_button)
            menu_text = pygame.font.SysFont(None, 24).render('MENU', True, (0, 0, 0))
            DISPLAYSURF.blit(menu_text, (menu_button.centerx - menu_text.get_width() // 2, menu_button.centery - menu_text.get_height() // 2))

            # Draw the Game Menu if active
            if show_game_menu:
                pygame.draw.rect(DISPLAYSURF, (50, 50, 50), (DISPLAYSURF.get_width() // 2 - 150, 50, 300, 250))

                font = pygame.font.SysFont(None, 24)
                rgb_text = font.render('RGB Mode', True, (255, 255, 255))
                eraser_text = font.render('Eraser', True, (255, 255, 255))
                clear_text = font.render('Clear All', True, (255, 255, 255))
                exit_text = font.render('Exit', True, (255, 255, 255))

                DISPLAYSURF.blit(rgb_text, (DISPLAYSURF.get_width() // 2 - 125, 80))
                DISPLAYSURF.blit(eraser_text, (DISPLAYSURF.get_width() // 2 - 125, 120))
                DISPLAYSURF.blit(clear_text, (DISPLAYSURF.get_width() // 2 - 125, 160))
                DISPLAYSURF.blit(exit_text, (DISPLAYSURF.get_width() // 2 - 125, 200))

        pygame.display.update()
        clock.tick(60)

# Show the start menu first
if start_menu():
    main_game()

# Quit pygame
pygame.quit()
