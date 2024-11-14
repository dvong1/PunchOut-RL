import neat.nn.recurrent
import retro
import neat
import numpy as np
import cv2
import pickle

env = retro.make(game="PunchOut-Nes", state="Match1.state")

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
        frame = 0
        counter = 0
        health_com = 0
        health_mac = 0
        heart = 0
        score = 0

        done = False
        
        while not done:
            env.render()
            frame += 1

            print(f"obs type: {type(obs)}")
            print(f"obs shape: {obs.shape}")
            
            obs = cv2.resize(obs, (inx, iny))
            obs = cv2.cvtColor(obs, cv2.COLOR_BGR2GRAY)
            obs = np.reshape(obs, (inx, iny))

            imgarray = np.ndarray.flatten(obs) # Downscale, then grayscale, the flatten the 2d dimenions into a 1d array

            nn_Output = net.activate(imgarray)

            print(nn_Output)

            obs, reward, terminated, truncated, info = env.step(nn_Output)


config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'config-feedforward'        
                     )

p = neat.Population(config)

winner = p.run(eval_genomes)





# def loadGame2():
#     env = retro.make(game="PunchOut-Nes", state="Match1.state")
#     obs = env.reset()
#     inx, iny, inc = env.observation_space.shape
#     print(inx, iny)

#     done = False

#     while not done:
#         action = env.action_space.sample()
#         env.render()
#         obs, reward, terminated, truncated, info = env.step(action)

#         pStamina = info['heart']

#         print(pStamina)

# if __name__ == '__main__':
#    print("tada")


# 840 for NN input config file based on raw pixels
# 4 for NN input config file based on data.json memory values

# If you want to use memory values for training, normalize the values by retrieving other memory values for enemyHealth / current_enemyHealth
