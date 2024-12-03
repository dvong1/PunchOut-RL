import neat
import pickle
import retro

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

env = retro.make(game="PunchOut-Nes", state="glassJoe.state")
obs = env.reset()

done = False
button_array = []

while not done:
    obs, reward, terminated, truncated, info = env.step(button_array)

    ram = env.get_ram()

    # Get memory addresses for NN inputs
    animation_value = int(ram[81])  
    time_value = int(ram[57])
    current_match_value = int(ram[8])

    nn_Input = [info['health_mac'], info['health_com'], info['heart'], info['score'], animation_value, time_value, current_match_value]

    nn_Output = net.activate(nn_Input)
    action_index = nn_Output.index(max(nn_Output))

    button_array = action_space[action_index]

    # Continue game environemnt if in splash screen
    if ram[0] != 1:
        button_array = action_space[3]
        env.step(button_array)
        for _ in range(2):  # Small delay loop (adjust as necessary)
            env.step(action_space[1])  # No Action step


    obs, reward, terminated, truncated, info = env.step(button_array)


    if truncated:
        done = True

env.close() 
