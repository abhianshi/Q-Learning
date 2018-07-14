# Importing libraries and modules
from random import randint
import random
import time
import QLearningGUI as gui
import threading


# Importing the necessary parameters from the Grid World(GUI)
# Grid Paramters
grid = gui.grid
init = gui.init
goal = gui.goal
pit = gui.pit
columns = gui.columns
rows = gui.rows

# Rewards and Penalty
living_reward = -0.05
penalty = -1
reward = 1
discount = 0.8

# 4-connectedness movements
delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

# Q-Learning Paramters
noise_same = 0.6
noise_different = 0.1

# usually decreasing function, but also can be supplied through the Grid World Controls
alpha = 0.1

# Initialize Q-values
init_Q = 0.00
Q_values = {}
for i in range(rows):
    for j in range(columns):
        if(grid[i][j] == 1):
            Q_values[(i,j)] = [0.0,0.0,0.0,0.0]
        elif([i,j] in goal):
            Q_values[(i,j)] = [reward,reward,reward,reward]
        elif([i,j] in pit):
            Q_values[(i,j)] = [penalty,penalty,penalty,penalty]
        else:
            Q_values[(i,j)] = [init_Q,init_Q,init_Q,init_Q]




# Q-Learning search method
def search():
    global alpha, Q_values

    # Maximum number of iterations allowed
    k = 0

    while(True):

        if(gui.isplay):
            # Stop until forced by user or reach the maximum limit
            while(k < 500):

                # Refresh the map
                if(gui.isstop):
                    gui.refresh()

                    alpha = 1
                    k = 0
                    # Initialize Q-values
                    init_Q = 0.01
                    Q_values = {}
                    for i in range(rows):
                        for j in range(columns):
                            if(grid[i][j] == 1):
                                Q_values[(i,j)] = [0.0,0.0,0.0,0.0]
                            elif([i,j] in goal):
                                Q_values[(i,j)] = [reward,reward,reward,reward]
                            elif([i,j] in pit):
                                Q_values[(i,j)] = [penalty,penalty,penalty,penalty]
                            else:
                                Q_values[(i,j)] = [init_Q,init_Q,init_Q,init_Q]

                    gui.isstop = False


                # Start exploring from the initialization state
                cur_state = init[:]
                next_state = init[:]

                # Number of steps in each episode
                steps = 0

                # Suspend after goal or pit is encountered
                suspend = False
                while(not suspend and steps < 250):

                    if(gui.isplay):

                        steps += 1
                        # Choose the action with maximum value
                        max_value = max(Q_values[(cur_state[0],cur_state[1])])

                        # If tie, then order is up -> left -> down -> right
                        action = Q_values[(cur_state[0],cur_state[1])].index(max_value)

                        # Exploration
                        # Generate random number between 0 and 1
                        random_number1 = random.random()
                        # if random number is less than exploration, then select random action other than desired action
                        if(random_number1 < gui.get_exploration()):

                            # Decide among all the 4 actions in exploration,
                            # If we choose from only three different actions and if exploration value is also 1,
                            # then the robot will never take the most optimal action
                            random_number1 = randint(0,3)
                            action = random_number1


                        # Select the environment - deterministic or stochastic

                        # deterministic
                        if(gui.deterministic):

                            # Action decided is taken with 100% probability
                            next_state[0] = cur_state[0] + delta[action][0]
                            next_state[1] = cur_state[1] + delta[action][1]

                            # If the robot hits the wall or tries to go out from the grid, then the robot remains in the same state
                            if(next_state[0] < 0 or next_state[1] < 0 or next_state[0] >= rows or next_state[1] >= columns or grid[next_state[0]][next_state[1]] == 1):
                                next_state[0] = cur_state[0]
                                next_state[1] = cur_state[1]

                            # Else if the robot reaches the goal or lands in the pit, then stop this iteration
                            elif(next_state in goal or next_state in pit):
                                suspend = True

                            # Update the Q-values
                            Q_values[(cur_state[0],cur_state[1])][action] = (1 - alpha) * Q_values[(cur_state[0],cur_state[1])][action] \
                                                                            + alpha * (living_reward + discount * max(Q_values[(next_state[0],next_state[1])]))

                        # Stochastic
                        else:

                            # One action where the robot does not move
                            # 10% chance of remaining in the same position
                            # Add the Q-values with noise_different
                            intermediate_val = alpha * noise_different * (living_reward + discount * max(Q_values[(cur_state[0],cur_state[1])]))

                            # Other three actions
                            # 10% chance of moving in each of the other three directions
                            # Add the Q-values for other three action with noise_different
                            for i in range(4):
                                if(i != action):
                                    next_state[0] = cur_state[0] + delta[i][0]
                                    next_state[1] = cur_state[1] + delta[i][1]

                                    if(next_state[0] < 0 or next_state[1] < 0 or next_state[0] >= rows or next_state[1] >= columns or grid[next_state[0]][next_state[1]] == 1):
                                        next_state[0] = cur_state[0]
                                        next_state[1] = cur_state[1]

                                    intermediate_val += alpha * noise_different * (living_reward + discount * max(Q_values[(next_state[0],next_state[1])]))

                            # Does the most probabilistic action
                            # As the environment is stochastic, there is 60% chance of remaining in the same position
                            # Add the Q-values for the desired action with noise_same
                            next_state[0] = cur_state[0] + delta[action][0]
                            next_state[1] = cur_state[1] + delta[action][1]
                            if(next_state[0] < 0 or next_state[1] < 0 or next_state[0] >= rows or next_state[1] >= columns or grid[next_state[0]][next_state[1]] == 1):
                                next_state[0] = cur_state[0]
                                next_state[1] = cur_state[1]
                            elif(next_state in goal or next_state in pit):
                                suspend = True

                            Q_values[(cur_state[0],cur_state[1])][action] = intermediate_val +  (1 - alpha) * Q_values[(cur_state[0],cur_state[1])][action] \
                                                                            + alpha * noise_same * (living_reward + discount * max(Q_values[(next_state[0],next_state[1])]))

                            # Decreasing function - alpha
                            alpha = (k+1) ** (-1)


                        # GUI Interaction
                        # Shows the robot and Q-values
                        gui.showRobot(cur_state[0],cur_state[1])
                        value = Q_values[(cur_state[0],cur_state[1])][action]
                        value = format(value, "0.1f")
                        gui.changeColor(cur_state[0],cur_state[1], action, value)
                        gui.changeText(cur_state[0],cur_state[1],action, value)
                        time.sleep( (10 - gui.get_sleep())/10 + 0.001)
                        gui.hideRobot(cur_state[0],cur_state[1])
                        cur_state[0] = next_state[0]
                        cur_state[1] = next_state[1]

                # End of while loop - suspend
                # Robot reached the Goal or Pit
                gui.showRobot(cur_state[0],cur_state[1])
                time.sleep( (10 - gui.get_sleep())/10 + 0.001)
                gui.hideRobot(cur_state[0],cur_state[1])

                # Increase the count of iteration value
                k += 1

                # Print the Q-values after reaching goal or pit
                print("\nIteration",k, "Q-values")
                for i in range(rows):
                    for j in range(columns):
                        print(i,j,Q_values[(i,j)])

            # Enf of while loop - maximum iterations allowed



# Making the Threads for communicating with the grid-world map
QLearningThread = threading.Thread(target = search)
QLearningThread.daemon = True
QLearningThread.start()

# Start Grid World GUI
gui.start()
