import time
import random
import numpy as np


timeout = time.time() + 5
# first value is the current floor the elevator is on, second one is a list with 1 person, target_floor of the person and waiting time of the person
elevator = [0]            

# First value =  amount of person waiting on that floor
# Second value = amount of time the persons are waiting on that floor
dict_elevator = {"Floor 0": [],
                 "Floor 1": [],
                 "Floor 2": [],
                 "Floor 3": [],
                 "Floor 4": [],
                 "Floor 5": [],
                 "Floor 6": [],
                 "Floor 7": [],
                 "Floor 8": [],
                 "Floor 9": []
}

final_elevator = {"Floor 0": [],
                  "Floor 1": [],
                  "Floor 2": [],
                  "Floor 3": [],
                  "Floor 4": [],
                  "Floor 5": [],
                  "Floor 6": [],
                  "Floor 7": [],
                  "Floor 8": [],
                  "Floor 9": []
}
  



# Add people to random floors
while True:
    if time.time() > timeout:
        break
    time.sleep(0.5)

    floor, persons = random.choice(list(dict_elevator.items()))             # Get random floor 
    wait_time = random.randint(1, 20)                                       # create a random wait time
    target_floor = random.randint(1, len(dict_elevator) - 1)                # Give random target floor
    travel_time = 0
    dict_elevator[floor] += [[1, target_floor, wait_time]]     # Add to the floor a person with a random target_floor/wait_time


reward_array = []
amount_episodes = 1
amount_iterations = 20

for episodes in range(amount_episodes):
    print(f"Episode: {episodes}")
    weights = np.random.rand(4)
    temperature = 1e5
    cooling_rate = 0.99
    total_reward = 0
    previous_reward = 0
    for iterations in range(amount_iterations):
        print(f"Iteration: {iterations}")
        new_weights = weights + np.random.normal(loc=0, scale=0.1)
        done = False
        current_reward = 0

        max_value = 0
            
        while not done:
            # check for highest waiting time
            listvalues = []
            for i in dict_elevator:
                    for extract_item in dict_elevator[i]:
                        listvalues.append(extract_item)
            for i in listvalues:
                if i[2] > max_value: 
                    max_value = i[2]
            
            def Sort(listvalues):
                length = len(listvalues)
                for i in range(0, length):
                    for j in range(0, length-i-1):
                        if (listvalues[j][2] > listvalues[j + 1][2]):
                            tempo = listvalues[j]
                            listvalues[j] = listvalues[j + 1]
                            listvalues[j + 1] = tempo
                return listvalues
            
            Sort(listvalues)
            listvalues.reverse()

            if len(listvalues) != 0:
                highest_waiting_time = listvalues[0]
                floor_highest_waiting_time = [key for key, value in dict_elevator.items() if highest_waiting_time in value]

                if floor_highest_waiting_time[0] in dict_elevator.keys():
                    floor_value = dict_elevator.get(floor_highest_waiting_time[0])
                    if floor_value != None and len(floor_value) != 0:                                      # If the list of floor_value is different then None or the length of it is different from 0 continue
                        print(f"Got a call from person {dict_elevator.get(floor_highest_waiting_time[0])[0]}")
                        target_floor_elevator = floor_value[0][1]                                          # This variable show to which floor the elevator needs to go
                        difference_floor = target_floor_elevator - elevator[0]                             # calculate the absolute value between target and elevator floor


                        elevator += [floor_value[0]]                                                       # adds the first value to the elevator



                        start_time = time.time()
                        while elevator[0] != elevator[1][1]:                                               # if the lvl of the floor is different from it targets continue
                            if difference_floor > 0:
                                elevator[0] += 1
                                print(f"Elevator is going up: {elevator[0]}")
                            elif difference_floor < 0:
                                elevator[0] -= 1
                                print(f"Elevator is going down {elevator[0]}")
                            time.sleep(1)

                        end_time = time.time()
                        travel_time = end_time - start_time                                                    # Calculates the duration the elevator does from start to end floor
                        floor_value[0].append(round(travel_time))                                              # This adds the travel time 

                        
                        print(f"Duration = {round(travel_time)} seconds")                                      # prints the duration the elevator takes to deliver persons from start to end floor
                        final_elevator[f"Floor {elevator[0]}"].append(floor_value[0]) 
                        print(f"Elevator arrived at floor {elevator[0]} with passenger {floor_value[0]}\n")      # prints where the elevator has arrived with the person         
                        dict_elevator[floor_highest_waiting_time[0]].remove(floor_value[0])                                	 # remove the person that went to its destination


                        
                        elevator = [elevator[0]]                                                          # update the floor the elevator is on
                    
                    elif floor_value == None or len(floor_value) == 0: 
                        length_dict = len(dict_elevator)
                        if elevator[0] == (length_dict - 1):   
                            elevator[0] -= length_dict - 1
                        elif elevator[0] >= 0:
                            elevator[0] += 1
                            print(f"Elevator is going up: {elevator[0]}")
                        print(f"Arrived on floor: {elevator[0]}\n")

                    current_reward += 5
            done = True




        if previous_reward < current_reward:
            weights = new_weights
            previous_reward = current_reward
        else:
            delta = previous_reward - current_reward
            p = np.exp(delta / temperature)
            if np.random.rand() < p:
                weights = new_weights
                previous_reward = current_reward
        temperature *= cooling_rate
        total_reward += (current_reward / amount_episodes)
    reward_array.append({
        "average_reward": total_reward, 
        "weights": weights
    })

best_reward = 0
for reward in reward_array:
    if reward["average_reward"] > best_reward:
        best_reward = reward["average_reward"]
        best_weights = reward["weights"]

print(f"Best reward is {best_reward} for weights = {best_weights}")