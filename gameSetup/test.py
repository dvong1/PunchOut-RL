import retro

def loadGame():
    env = retro.make(game="PunchOut-Nes", state="Match1.state")
    env.reset()

    done = False

    # buttons = env.buttons
    # for button in buttons:
    #     print(button)

    while not done:
        env.render()
        action = env.action_space.sample()
        # print(action)
        env.step(action)

    # while True:
    #     env.render()
    #     env.step(env.action_space.sample()) #take a random action


if __name__ == '__main__':
   loadGame()

   # create neural network via NEAT, cv2
   # save neural network data so memory doesn't restart after new session via PICKLE
   # visualize neural network
   # Set up goals for nn (Mac must make it to next stage before timer runs out [by frame x])