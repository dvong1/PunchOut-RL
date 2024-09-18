import pygame

gamepad_image = pygame.image.load('gameSetup/virtualGamepad/nes_gamepad_transparent/base_gamepad.png')

highlight_images = {
'A': pygame.image.load('gameSetup/virtualGamepad/nes_gamepad_transparent/A.png'),
'B': pygame.image.load('gameSetup/virtualGamepad/nes_gamepad_transparent/B.png'),
'START': pygame.image.load('gameSetup/virtualGamepad/nes_gamepad_transparent/START.png'),
'SELECT': pygame.image.load('gameSetup/virtualGamepad/nes_gamepad_transparent/SELECT.png'),
'UP': pygame.image.load('gameSetup/virtualGamepad/nes_gamepad_transparent/UP.png'),
'DOWN': pygame.image.load('gameSetup/virtualGamepad/nes_gamepad_transparent/DOWN.png'),
'LEFT': pygame.image.load('gameSetup/virtualGamepad/nes_gamepad_transparent/LEFT.png'),
'RIGHT': pygame.image.load('gameSetup/virtualGamepad/nes_gamepad_transparent/RIGHT.png')
}

button_positions = {
    'A': (0, 0),  # Example coordinates
    'B': (0, 0),
    'START': (0, 0),
    'SELECT': (0, 0),
    'UP': (0, 0),
    'DOWN': (0, 0),
    'LEFT': (0, 0),
    'RIGHT': (0, 0)
}

def initialize_display():
    global screen
    screen = pygame.display.set_mode((gamepad_image.get_width() / 4, gamepad_image.get_height() / 4)) # Scale controller window down by factor of 4
    pygame.display.set_caption('Gamepad Overlay')

def draw_gamepad_overlay(pressed_buttons, screen, gamepad_rect):
    # Draw the base gamepad image in the specified rectangle and scale it accordingly to fit the bottom right corner
    gamepad_scaled = pygame.transform.scale(gamepad_image, (gamepad_rect.width, gamepad_rect.height))
    screen.blit(gamepad_scaled, gamepad_rect.topleft)

    for button in pressed_buttons:
        if button in highlight_images:
            updated_gamepad = pygame.transform.scale(highlight_images[button], (gamepad_rect.width, gamepad_rect.height)) # Scale the specific presssed button images 
            screen.blit(updated_gamepad, gamepad_rect.topleft) #Update the screen to reflect the button pressed

# Overload function for RL agent
def draw_gamepad_overlayRL(pressed_buttons):
    # Clear the screen
    screen.fill((0, 0, 0))
    
    # Draw the base gamepad image
    gamepad_scaled = pygame.transform.scale(gamepad_image, (gamepad_image.get_width() / 4, gamepad_image.get_height() / 4))
    screen.blit(gamepad_scaled, (0, 0))
    
    # Highlight pressed buttons
    for button in pressed_buttons:
        if button in highlight_images:
            updated_gamepad = pygame.transform.scale(highlight_images[button], (gamepad_image.get_width() / 4, gamepad_image.get_height() / 4))
            screen.blit(updated_gamepad, button_positions[button])
    
    # Update the display
    pygame.display.flip()

# Example to emulate game with button press tracking
def emulate_with_visualization():
    screen = pygame.display.set_mode((gamepad_image.get_width(), gamepad_image.get_height()))

    pygame.init()
    running = True
    screen = pygame.display.set_mode((1536, 960))  # Dummy window for standalone visualization
    gamepad_rect = pygame.Rect(1024, 960 // 2, 512, 480)  # Adjust as needed

    while running:
        pressed_buttons = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get which keys are pressed (e.g., user input or RL agent input)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:  # Map to 'START'
            pressed_buttons.append('START')
        if keys[pygame.K_RSHIFT]:  # Map to 'START'
            pressed_buttons.append('SELECT')
        if keys[pygame.K_z]:  # Map to 'B'
            pressed_buttons.append('B')
        if keys[pygame.K_x]:  # Map to 'A'
            pressed_buttons.append('A')
        if keys[pygame.K_UP]:
            pressed_buttons.append('UP')
        if keys[pygame.K_DOWN]:
            pressed_buttons.append('DOWN')
        if keys[pygame.K_LEFT]:
            pressed_buttons.append('LEFT')
        if keys[pygame.K_RIGHT]:
            pressed_buttons.append('RIGHT')

        # # Call the drawing function to update visualization
        screen.fill((0, 0, 0))
        draw_gamepad_overlay(pressed_buttons, screen, gamepad_rect)
        pygame.display.flip()

    pygame.quit()
    
if __name__=='__main__':
    emulate_with_visualization()
