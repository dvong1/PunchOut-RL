import retro
import neat
import numpy as np
import cv2
import pickle
import random

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

# game_states = ["glassJoe.state", "vonKaiser.state",
#                "pistonHonda1.state", "donFlamenco.state",
#                "kingHippo.state", "greatTiger.state",
#                "baldBull1.state", "pistonHonda2.state",
#                ]

game_states = ["glassJoe.state", "vonKaiser.state",
               "pistonHonda1.state"
               ]

# game_states = ["glassJoe.state", "vonKaiser.state"
#                ]

class Worker(object):
    def __init__(self, genome, config):
        self.genome = genome
        self.config = config

    def work(self):
        self.env = retro.make(game="PunchOut-Nes", state="glassJoe.state")
        self.env.reset()

        obs, _, _, _, _ = self.env.step(self.env.action_space.sample())

        net = neat.nn.FeedForwardNetwork.create(self.genome, self.config)

        current_max_fitness = 0
        fitness = 0
        counter = 0
        button_array = []

        done = False
        
        while not done:
            self.env.render()
            obs, reward, terminated, truncated, info = self.env.step(button_array)

            ram = self.env.get_ram()

            # Get memory addresses for NN inputs
            animation_value = int(ram[81])  
            time_value = int(ram[57])
            current_match_value = int(ram[8])

            nn_Input = [info['health_mac'], info['health_com'], info['heart'], info['score'], animation_value, time_value, current_match_value]

            nn_Output = net.activate(nn_Input)
            action_index = nn_Output.index(max(nn_Output))

            button_array = action_space[action_index]


            fitness += reward

            if fitness > current_max_fitness:
                current_max_fitness = fitness
                counter = 0
            else:
                counter += 1

            if terminated or truncated or counter == 5500:
                done = True
                
                # Randomize enemy state to increase variability in training. This prevents specialization to beating one enemy and one enemy only
                # self.env.close()
                # randomState = random.choice(game_states)
                # self.env = retro.make(game="PunchOut-Nes", state="randomState.state", render_mode=='None')
                # self.env.reset()
                
        return fitness
        
def eval_genomes(genome, config):

    worky = Worker(genome, config)
    return worky.work()


config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'config-feedforward')


p = neat.Population(config)
# p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-305')
p.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
p.add_reporter(stats)
# p.add_reporter(neat.Checkpointer(250))

p.config.genome_config.mutation_rate = 0.2
p.config.genome_config.activation_mutate_rate = 0.05
p.config.genome_config.elitism = 5
p.config.genome_config.compatibility_threshold = 1.5
p.config.genome_config.node_add_prob = 0.35
p.config.genome_config.node_delete_prob = 0.35
p.config.genome_config.aggregation_mutate_rate = 0.05 
p.config.genome_config.max_stagnation = 75


pe = neat.ParallelEvaluator(16, eval_genomes)

winner = p.run(pe.evaluate, 25)

with open('winner7.pkl', 'wb') as output:
    pickle.dump(winner, output, 1)
