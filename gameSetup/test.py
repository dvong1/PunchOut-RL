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
        self.env = retro.make(game="PunchOut-Nes", state="Match1.state")
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
        # img = self.env.render(mode='rgb_array')

        # if flipDisplay:
        #     img = np.flipud(img)

        # self.env.viewer.imshow(img)

# Main function to load the game
def loadGame(): 
    loadGamepad.initialize_display()  # Initialize the gamepad display

    # Use the custom Punch-Out environment
    custom_env = CustomPunchOutEnv()
    custom_env.reset()

    done = False

    # Frame rate synchronization
    fps = 60
    clock = pygame.time.Clock()

    frame_count = 0

    while not done:
        # Synchronize to the frame rate
        clock.tick(fps)

        # Sample a random action from the custom action space
        action = custom_env.action_space.sample()  # Replace with custom action space

        # Take a step with the chosen action
        obs, reward, terminated, truncated, info = custom_env.step(action)

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

        # Render the environment every frame
        custom_env.render()

        # Only update the gamepad overlay every 12 frames to avoid performance hit
        if frame_count % 12 == 0:
            loadGamepad.draw_gamepad_overlayRL(pressed_buttons)

        frame_count += 1

def loadGame2():
    env = retro.make(game="PunchOut-Nes", state="Match1.state")
    env.reset()

    done = False

    while not done:
        env.render()
        action = env.action_space.sample()
        env.step(action)

def linuxTest():
    loadGamepad.initialize_display()  # Initialize the gamepad display

    # Use the custom Punch-Out environment
    custom_env = CustomPunchOutEnv()
    custom_env.reset()

    done = False

    while not done:
        action = custom_env.action_space.sample()

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

        loadGamepad.draw_gamepad_overlayRL(pressed_buttons)

if __name__ == '__main__':
   linuxTest()
