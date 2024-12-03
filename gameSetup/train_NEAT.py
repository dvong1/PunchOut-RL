import neat.nn.recurrent
import retro
import neat
import pickle
import random

env = retro.make(game="PunchOut-Nes", state="glassJoe.state")

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

game_states = ["glassJoe.state", "vonKaiser.state",
               "pistonHonda1.state", "donFlamenco.state",
               "kingHippo.state", "greatTiger.state",
               "baldBull1.state", "pistonHonda2.state",
               ]

imgarray = []

def eval_genomes(genomes, config):
    global env

    for genome_id, genome in genomes:
        obs, _ = env.reset()
        ac = env.action_space.sample()

        inx, iny, inc = env.observation_space.shape

        # Downscale the resolution for training 
        inx = int(inx/8)
        iny = int(iny/8)

        net = neat.nn.recurrent.RecurrentNetwork.create(genome, config)

        current_max_fitness = 0
        fitness_current = 0
        counter = 0
        button_array = []

        done = False
        
        while not done:
            # env.render()
  
            # # Useless since we are no longer reading raw pixels for NN input
            # obs = cv2.resize(obs, (inx, iny))
            # obs = cv2.cvtColor(obs, cv2.COLOR_BGR2GRAY)
            # obs = np.reshape(obs, (inx, iny))
            # imgarray = np.ndarray.flatten(obs) # Downscale, then grayscale, the flatten the 2d dimenions into a 1d array


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

            mac_losses = int(ram[10])
            round_number = int(ram[6])
            comKDs = int(ram[974])
            macKDs = int(ram[973])
            current_comKDS = 0

            fitness_current += reward

            if fitness_current > current_max_fitness:
                current_max_fitness = fitness_current
                counter = 0
            else:
                counter += 1

            if terminated or truncated or counter == 5500:
                done = True
        
                '''
                # Randomize which enemy NN will fight to diversify training data 
                env.close()
                randomState = random.choice(game_states)
                env = retro.make(game="PunchOut-Nes", state=randomState)
                env.reset()
                print(f"Genome: {genome_id}, current Fitness: {fitness_current}, max fitness: {current_max_fitness}, reward: {reward}")
                '''
            genome.fitness = fitness_current


config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'config-feedforward'        
                     )

p = neat.Population(config)

# p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-49')
p.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
p.add_reporter(stats)
p.add_reporter(neat.Checkpointer(10))

winner = p.run(eval_genomes)

with open('winner.pkl', 'wb') as output:
    pickle.dump(winner, output, 1)



# 840 for NN input config file based on raw pixels
# 4 for NN input config file based on data.json memory values

# If you want to use memory values for training, normalize the values by retrieving other memory values for enemyHealth / current_enemyHealth
