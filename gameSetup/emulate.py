import retro
import numpy as np
import pygame
import virtualGamepad.loadGamepad as loadGamepad
import struct

keys_to_action = { # Dictionary that maps keyboard buttons to multibinary list that is read by the emulator 
    # Punch buttons
    (ord('z'),): [1, 0, 0, 0, 0, 0, 0, 0, 0],  # B (Left punch)
    (ord('x'),): [0, 0, 0, 0, 0, 0, 0, 0, 1],  # A (Right punch)
    # Directional buttons
    (pygame.K_UP,): [0, 0, 0, 0, 1, 0, 0, 0, 0],  # Up (Hold Up + B/A = Uppercut)
    (pygame.K_DOWN,): [0, 0, 0, 0, 0, 1, 0, 0, 0],  # Down (Block or duck if pressed twice in a row)
    (pygame.K_LEFT,): [0, 0, 0, 0, 0, 0, 1, 0, 0],  # Left (Dodge left)
    (pygame.K_RIGHT,): [0, 0, 0, 0, 0, 0, 0, 1, 0],  # Right (Dodge right)
    # Start and Select
    (pygame.K_RETURN,): [0, 0, 0, 1, 0, 0, 0, 0, 0],  # Start
    (pygame.K_RSHIFT,): [0, 0, 1, 0, 0, 0, 0, 0, 0],  # Select
}

# A 'noop' action to pass when no keys are pressed (9 zeros for 9 buttons on the NES controller)
noop_action = [0] * 9

def read_memory_value(env, address):
    """Reads the memory at the specified address in the retro environment."""
    memory = env.get_ram()  # Get the full memory block
    value = struct.unpack('B', memory[address:address+1])[0]
    return value

def emulate():
    # Create PunchOut environment
    env = retro.make(game="PunchOut-Nes", state="vonKaiser.state", render_mode=None)
    env.reset()

    # Initialize Pygame
    pygame.init()

    # Set up a scaled display for the rendered frames
    scale_factor = 4  # Change this to increase/decrease zoom (e.g., 2 for double size)
    original_width, original_height = 256, 240  # NES native resolution
    screen_width, screen_height = original_width * scale_factor + 512 , original_height * scale_factor

    # Set up the area for gamepad visualization (bottom right corner)
    gamepad_width = 512
    gamepad_height = screen_height // 2  # Bottom half of the extra space
    gamepad_rect = pygame.Rect(1024, screen_height // 2, gamepad_width, gamepad_height)

    # Set up the area for the NN visualization (top right corner, blank for now)
    nn_visualization_rect = pygame.Rect(1024, 0, gamepad_width, screen_height // 2)

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Punch-Out!!')

    # Limit frame rate to match the game's intended speed
    clock = pygame.time.Clock()
    fps = 60  # NES games usually run at 60 FPS

    # Begin running game
    running = True
    while running:
        action = np.array(noop_action)  # Start with no buttons pressed
        pressed_buttons = []  # Save buttons pressed to a list to update gamepad image

        # Close game after clicking quit corner button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return

        keys_pressed = pygame.key.get_pressed()

        # Loop through the key mappings and update the action array
        for key_combination, action_array in keys_to_action.items():
            if all(keys_pressed[key] for key in key_combination):
                action = np.logical_or(action, action_array)  # Combine actions

                # Check which buttons are pressed and add to pressed_buttons so this can be read by the gamepad overlay. Remember that the emulator can only read multibinary lists and not direct key presses like gamepad overlay
                if key_combination == (ord('z'),):
                    pressed_buttons.append('B')
                elif key_combination == (ord('x'),):
                    pressed_buttons.append('A')
                elif key_combination == (pygame.K_UP,):
                    pressed_buttons.append('UP')
                elif key_combination == (pygame.K_DOWN,):
                    pressed_buttons.append('DOWN')
                elif key_combination == (pygame.K_LEFT,):
                    pressed_buttons.append('LEFT')
                elif key_combination == (pygame.K_RIGHT,):
                    pressed_buttons.append('RIGHT')
                elif key_combination == (pygame.K_RETURN,):
                    pressed_buttons.append('START')
                elif key_combination == (pygame.K_RSHIFT,):
                    pressed_buttons.append('SELECT')

        action = action.astype(int)

        # Step the environment and get the rendered frame
        obs, reward, done, truncated, info = env.step(action.tolist())
        obs = pygame.surfarray.make_surface(np.transpose(obs, (1, 0, 2)))  # Convert to Pygame surface

        # Scale the image to the desired size
        obs = pygame.transform.scale(obs, (screen_width - 512, screen_height)) # The removed 512 pixels will be used for neural network and gamepad overlay

        # Blit the frame to the screen
        screen.blit(obs, (0, 0))

        # Blit a black rectangle for the future neural network visualization (top right)
        pygame.draw.rect(screen, (0, 0, 0), nn_visualization_rect)

        # Call the gamepad rendering function from the imported module (bottom right)
        loadGamepad.draw_gamepad_overlay(pressed_buttons, screen, gamepad_rect)

        pygame.display.flip()

        # Limit the frame rate
        clock.tick(90)

if __name__ == '__main__':
    emulate()