import retro
import numpy as np
import pygame

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

def emulate():
    # Create PunchOut environment
    env = retro.make(game="PunchOut-Nes", state="Match1.state")
    env.reset()

    # Initialize Pygame
    pygame.init()

    # Set up a scaled display for the rendered frames
    scale_factor = 4  # Change this to increase/decrease zoom (e.g., 2 for double size)
    original_width, original_height = 256, 240  # NES native resolution
    screen_width, screen_height = original_width * scale_factor, original_height * scale_factor
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Punch-Out!!')

    # Limit frame rate to match the game's intended speed
    clock = pygame.time.Clock()
    fps = 60  # NES games usually run at 60 FPS

    # Begin running game
    running = True
    while running:
        action = np.array(noop_action)  # Start with no buttons pressed

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

        action = action.astype(int)

        # Step the environment and get the rendered frame
        obs, reward, done, truncated, info = env.step(action.tolist())
        obs = pygame.surfarray.make_surface(np.transpose(obs, (1, 0, 2)))  # Convert to Pygame surface

        # Scale the image to the desired size
        obs = pygame.transform.scale(obs, (screen_width, screen_height))

        # Blit the frame to the screen
        screen.blit(obs, (0, 0))

        pygame.display.flip()

        # Limit the frame rate
        clock.tick(fps)

if __name__ == '__main__':
    emulate()