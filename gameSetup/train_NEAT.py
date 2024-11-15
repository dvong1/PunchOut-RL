import neat.nn.recurrent
import retro
import neat
import numpy as np
import cv2
import pickle

env = retro.make(game="PunchOut-Nes", state="glassJoe.state")

imgarray = []

def eval_genomes(genomes, config):

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

        done = False
        
        while not done:
            env.render()
  
            obs = cv2.resize(obs, (inx, iny))
            obs = cv2.cvtColor(obs, cv2.COLOR_BGR2GRAY)
            obs = np.reshape(obs, (inx, iny))
            imgarray = np.ndarray.flatten(obs) # Downscale, then grayscale, the flatten the 2d dimenions into a 1d array

            nn_Output = net.activate(imgarray)

            button_array = [1 if output > 0.5 else 0 for output in nn_Output]

            obs, reward, terminated, truncated, info = env.step(button_array)

            fitness_current += reward

            if fitness_current > current_max_fitness:
                current_max_fitness = fitness_current
                counter = 0
            else:
                counter += 1

            if terminated or truncated or counter == 5500:
                done = True
                print(f"Genome: {genome_id}, current Fitness: {fitness_current}, max fitness: {current_max_fitness}, counter: {counter}")

            genome.fitness = fitness_current


config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'config-feedforward'        
                     )

p = neat.Population(config)

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
