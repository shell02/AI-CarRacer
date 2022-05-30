# AI-CarRacer

# Description
This is a simple car racer game implemented with the python module Pygame. The objectif is to get a genetic AI (implement with the python module NEAT) to play the game and understand the mechanics. The cars randomly appears in one the five lanes, as long as no more than 8 cars are already on the screen and one lane is free.

# Genetic AI
The genetic AI will spawn a population of 50 players (neuron networks), all grouped in genomes with different weights and biases. Once every player lost the game, a new generation of 50 players is spawned, this time with some added parameters:
- the best genome is saved and use to spawn the new genomes (not all) in the next generation
- some mutations may occur (mutations can change weights, biases, connections between neurons...)

This will happen for a 100 generations or until the AI has become good enough.

# Fitness score
To know which genome is the best or if the AI is good enough, a fitness score is attributed to each player, and therefore each genome. 
- The longer the player stays alive, the better the fitness score
- The more cars the player avoids, the better the fitness score
- The more time the player stays in one lane, the worst the fitness score
- If a player loses, the fitness score decreases

# Input
To navigate the game, the neuron network gets 16 inputs : the x-axis position (since the player can only go left or right the y-axis stays the same) and how many cars are in the lanes (the 5 lanes are divided in three, meaning the network receives the number of cars in each of the 15 sections)

# Output
The neuron network will then give an output of three numbers \[ ex, ex, ex \], the biggest number giving the action to take:
- Turn left if the first number is the biggest,
- Turn right if the second is the biggest,
- Or do nothing if the third is the biggest.

To run the game for your own:
```
pip install -r requirements.txt
python main_neat.py
```
