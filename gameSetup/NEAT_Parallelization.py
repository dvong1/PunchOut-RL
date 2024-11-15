import retro
import neat
import numpy as np
import cv2
import pickle

class Worker(object):
    def __init__(self, genome, config):
        self.genome = genome
        self.config = config

    def work(self):
        self.env = retro.make(game="PunchOut-Nes", state="glassJoe.state",  render_mode=None)
        self.env.reset()

        obs, _, _, _, _ = self.env.step(self.env.action_space.sample())

        inx = int(obs.shape[0]/8)
        iny = int(obs.shape[1]/8)

        net = neat.nn.FeedForwardNetwork.create(self.genome, self.config)

        current_max_fitness = 0
        fitness = 0
        counter = 0
        imgarray = []

        done = False
        
        while not done:

            obs = cv2.resize(obs, (inx, iny))
            obs = cv2.cvtColor(obs, cv2.COLOR_BGR2GRAY)
            obs = np.reshape(obs, (inx, iny))

            imgarray = np.ndarray.flatten(obs)
            imgarray = np.interp(imgarray, (0, 254), (-1, +1))

            actions = net.activate(imgarray)

            obs, reward, terminated, truncated, info = self.env.step(actions)

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
p = neat.Checkpointer.restore_checkpoint('neat-checkpoint=9')
p.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
p.add_reporter(stats)
p.add_reporter(neat.Checkpointer(10))

pe = neat.ParallelEvaluator(20, eval_genomes)

winner = p.run(pe.evaluate)

with open('winner.pkl', 'wb') as output:
    pickle.dump(winner, output, 1)
