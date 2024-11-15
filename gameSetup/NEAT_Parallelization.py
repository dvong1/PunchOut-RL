import retro
import neat
import numpy as np
import cv2
import pickle

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

class Worker(object):
    def __init__(self, genome, config):
        self.genome = genome
        self.config = config

    def work(self):
        self.env = retro.make(game="PunchOut-Nes", state="glassJoe.state",  render_mode=None)
        self.env.reset()

        obs, _, _, _, _ = self.env.step(self.env.action_space.sample())

        net = neat.nn.FeedForwardNetwork.create(self.genome, self.config)

        current_max_fitness = 0
        fitness = 0
        counter = 0
        button_array = []

        done = False
        
        while not done:
            obs, reward, terminated, truncated, info = self.env.step(button_array)

            ram = self.env.get_ram()

            # Get memory addresses for NN inputs
            animation_value = int(ram[81])  
            time_value = int(ram[57])

            nn_Input = [info['health_mac'], info['health_com'], info['heart'], info['score'], animation_value, time_value]

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
            
        return fitness
        
def eval_genomes(genome, config):

    worky = Worker(genome, config)
    return worky.work()


config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'config-feedforward')

p = neat.Population(config)
# p = neat.Checkpointer.restore_checkpoint('neat-checkpoint=9')
p.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
p.add_reporter(stats)
p.add_reporter(neat.Checkpointer(10))

pe = neat.ParallelEvaluator(2, eval_genomes)

winner = p.run(pe.evaluate)

with open('winner.pkl', 'wb') as output:
    pickle.dump(winner, output, 1)
