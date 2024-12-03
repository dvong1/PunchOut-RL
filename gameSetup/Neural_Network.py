import neat
import pickle
import retro
import pygame
import virtualGamepad.loadGamepad as loadGamepad
import numpy as np
# import visualize # Uncomment to generate new graph for neural network

action_space = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0],  # Left Punch
    [0, 1, 0, 0, 0, 0, 0, 0, 0],  # No Action
    [0, 0, 1, 0, 0, 0, 0, 0, 0],  # Select
    [0, 0, 0, 1, 0, 0, 0, 0, 0],  # Start
    [0, 0, 0, 0, 1, 0, 0, 0, 0],  # UP
    [0, 0, 0, 0, 0, 1, 0, 0, 0],  # Duck
    [0, 0, 0, 0, 0, 0, 1, 0, 0],  # Dodge Left
    [0, 0, 0, 0, 0, 0, 0, 1, 0],  # Dodge Right
    [0, 0, 0, 0, 0, 0, 0, 0, 1],  # Right Punch
    [0, 0, 0, 0, 1, 0, 0, 0, 1],  # Right Uppercut
    [1, 0, 0, 0, 1, 0, 0, 0, 0],  # Left Uppercut
]


# Load the winner genome
with open('winner.pkl', 'rb') as f:
    winner = pickle.load(f)

# Load the NEAT configuration file
config = neat.config.Config(
    neat.DefaultGenome,
    neat.DefaultReproduction,
    neat.DefaultSpeciesSet,
    neat.DefaultStagnation,
    'config-feedforward'  # Replace with the name of your NEAT config file
)


net = neat.nn.FeedForwardNetwork.create(winner, config)


# Create .svg file of neural network. Requires visualize.py
# node_names = {0: 'A [Right Punch]', 1: 'B [Left Punch]',
#               2: 'UP [Up]', 3: 'DOWN [Block]', 
#               4: 'LEFT [Dodge Left]', 5: 'RIGHT [Dodge Right]', 
#               6: 'START [Start]', 7: 'Select [SELECT]', 
#               8: 'Right Uppercut [UP + A]', 9: 'Left Uppercut [UP + B]', 
#               10: 'DUCK [Down + Down]', 11: 'None [No Action]', 
#               }
# visualize.draw_net(config, winner, True, node_names=node_names)

env = retro.make(game="PunchOut-Nes", state="glassJoe.state", render_mode='None')
obs = env.reset()

done = False
button_array = []

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
button_mapping = ['B', 'No Action', 'SELECT', 'START', 'UP', 'DOWN', 'LEFT', 'RIGHT', 'A']


while not done:
    obs, reward, terminated, truncated, info = env.step(button_array)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    
    ram = env.get_ram()

    # Get memory addresses for NN inputs
    animation_value = int(ram[81])  
    time_value = int(ram[57])
    current_match_value = int(ram[8])

    nn_Input = [info['health_mac'], info['health_com'], info['heart'], info['score'], animation_value, time_value, current_match_value]

    nn_Output = net.activate(nn_Input)
    action_index = nn_Output.index(max(nn_Output))

    button_array = action_space[action_index]

    pressed_buttons = [button_mapping[i] for i, pressed in enumerate(button_array) if pressed]

    # Continue game environemnt if in splash screen
    if ram[0] != 1:
        button_array = action_space[3]
        env.step(button_array)
        for _ in range(2):  # Small delay loop (adjust as necessary)
            env.step(action_space[1])  # No Action step


    obs, reward, terminated, truncated, info = env.step(button_array)

    obs = pygame.surfarray.make_surface(np.transpose(obs, (1, 0, 2)))  # Convert to Pygame surface

    # Scale the image to the desired size
    obs = pygame.transform.scale(obs, (screen_width - 512, screen_height)) # The removed 512 pixels will be used for neural network and gamepad overlay

    # Blit the frame to the screen
    screen.blit(obs, (0, 0))

    # Blit a black rectangle for the future neural network visualization (top right)
    pygame.draw.rect(screen, (0, 0, 0), nn_visualization_rect)

    # Call the gamepad rendering function from the imported module (bottom right)
    loadGamepad.draw_gamepad_overlayRL(pressed_buttons, screen, gamepad_rect)

    pygame.display.flip()

    # Limit the frame rate
    clock.tick(fps)


    if truncated:
        done = True

env.close() 
