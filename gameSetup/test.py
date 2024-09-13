import retro


# This game will load up PunchOut through the fceumm NES emulator. The RL agent will then choose a random action and perform it. 
def loadGame(): 
    env = retro.make(game="PunchOut-Nes", state="Match1.state")
    env.reset()

    done = False

    while not done:
        env.render()
        action = env.action_space.sample()
        print(action)
        env.step(action)


if __name__ == '__main__':
   loadGame()

   # create neural network via NEAT (genome evolution), cv2 or use policy-gradient algorithm
   # save neural network data so memory doesn't restart after new session via PICKLE
   # visualize neural network
   # Set up goals for nn (Mac must make it to next stage before timer runs out [by frame x])