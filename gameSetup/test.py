import retro
import virtualGamepad.loadGamepad as loadGamepad
from gymnasium import spaces
import pygame
import pyglet
import os
import numpy as np

pyglet.options['debug_gl'] = False
if 'WSL_INTEROP' in os.environ:
    flipDisplay = False
else:
    flipDisplay = True

# Define custom action space for Punch-Out
class CustomPunchOutEnv:
    def __init__(self):
        self.env = retro.make(game="PunchOut-Nes", state="Match1.state", render_mode=None)
        self.action_space = spaces.Discrete(10)  # 8 single button actions + 2 uppercut combinations
        self.reset()

    def reset(self):
        self.env.reset()

    def step(self, action):
        # Handle the custom discrete actions
        button_array = [0] * 9  # Default all buttons to not pressed

        if action == 0:  # A button
            button_array[8] = 1  # 'A' is mapped to index 8
        elif action == 1:  # B button
            button_array[0] = 1  # 'B' is mapped to index 0
        elif action == 2:  # UP button
            button_array[4] = 1  # 'UP' is mapped to index 4
        elif action == 3:  # DOWN button
            button_array[5] = 1  # 'DOWN' is mapped to index 5
        elif action == 4:  # LEFT button
            button_array[6] = 1  # 'LEFT' is mapped to index 6
        elif action == 5:  # RIGHT button
            button_array[7] = 1  # 'RIGHT' is mapped to index 7
        elif action == 6:  # START button
            button_array[3] = 1  # 'START' is mapped to index 3
        elif action == 7:  # SELECT button
            button_array[2] = 1  # 'SELECT' is mapped to index 2
        elif action == 8:  # Uppercut (UP + A)
            button_array[4] = 1  # 'UP' is mapped to index 4
            button_array[8] = 1  # 'A' is mapped to index 8
        elif action == 9:  # Uppercut (UP + B)
            button_array[4] = 1  # 'UP' is mapped to index 4
            button_array[0] = 1  # 'B' is mapped to index 0

        # Take a step in the environment using the button array
        return self.env.step(button_array)

    def render(self):
        self.env.render()
\
# Main function to load the game
def loadGame():
    # Create custom PunchOut environment
    custom_env = CustomPunchOutEnv()
    obs = custom_env.reset()

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
    fps = 60
    clock = pygame.time.Clock()
    frame_count = 0

    # Begin running game
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return

        # Sample a random action from the custom action space
        action = custom_env.action_space.sample()  # Replace with custom action space

        pressed_buttons = []
        # Map the custom action to the corresponding pressed buttons for visualization
        if action == 0:  # 'A'
            pressed_buttons.append('A')
        elif action == 1:  # 'B'
            pressed_buttons.append('B')
        elif action == 2:  # 'UP'
            pressed_buttons.append('UP')
        elif action == 3:  # 'DOWN'
            pressed_buttons.append('DOWN')
        elif action == 4:  # 'LEFT'
            pressed_buttons.append('LEFT')
        elif action == 5:  # 'RIGHT'
            pressed_buttons.append('RIGHT')
        elif action == 6:  # 'START'
            pressed_buttons.append('START')
        elif action == 7:  # 'SELECT'
            pressed_buttons.append('SELECT')
        elif action == 8:  # 'UP + A'
            pressed_buttons.append('UP')
            pressed_buttons.append('A')
        elif action == 9:  # 'UP + B'
            pressed_buttons.append('UP')
            pressed_buttons.append('B')

        # Take a step with the chosen action
        print(f"Stepping with action: {action}")
        obs, reward, terminated, truncated, info = custom_env.step(action)

        # Convert observation to Pygame surface and render to screen
        obs = pygame.surfarray.make_surface(np.transpose(obs, (1, 0, 2)))  # Convert to Pygame surface
        obs = pygame.transform.scale(obs, (screen_width - 512, screen_height))  # Scale observation

        # Blit the observation to the left half of the screen
        screen.blit(obs, (0, 0))

        # Render the environment every frame
        custom_env.render()

        # Only update the gamepad overlay every 12 frames to avoid performance hit
        if frame_count % 12 == 0:
            loadGamepad.draw_gamepad_overlayRL(pressed_buttons, screen, gamepad_rect)
            
        frame_count += 1
        pygame.display.flip()

        # Synchronize the framerate
        clock.tick(fps)

def loadGame2():
    env = retro.make(game="PunchOut-Nes", state="Match1.state")
    env.reset()

    done = False

    while not done:
        env.render()
        action = env.action_space.sample()
        env.step(action)

if __name__ == '__main__':
   loadGame()
