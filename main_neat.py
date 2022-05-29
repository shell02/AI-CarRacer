from player import Player
from cars import Cars
from game import Game
import pygame
import random
import pickle
import neat
import os

#Font initialization and declaration
pygame.font.init()
SCORE_FONT = pygame.font.SysFont('comicsans', 20)

#Loading Images
bigTruck = pygame.transform.scale(
    pygame.image.load('assets\\bigTruck.png'), (80, 250))
redCar= pygame.transform.scale(
    pygame.image.load('assets\\redCar.png'), (80, 100))
road = pygame.transform.scale(
    pygame.image.load('assets\\road.png'), (500, 100))
orangeCar = pygame.transform.scale(
    pygame.image.load('assets\\orangeCar.png'), (80, 100))
policeCar = pygame.transform.scale(
    pygame.image.load('assets\\policeCar.png'), (80, 100))
greenCar = pygame.transform.scale(
    pygame.image.load('assets\\greenCar.png'), (80, 100))

#Helps randomize the car and its lane
choice = [greenCar, orangeCar, policeCar, bigTruck]
lanes = [20, 110, 210, 310, 400]

#Some variables declaration + generation variable
WIDTH, HEIGHT = 500, 700
FPS = 60

#Name of the window
pygame.display.set_caption("Race Car AI")


def addObstacle(obstacles, score):
    add = random.randint(1, 100)
    lenght = len(obstacles)
    
    # 1 out of 50 chances of a car appearing
    # The max number of cars increases from 4 to 8
    # every 10 points won
    if (add == 1 or add == 50) and lenght < (4 + score // 10) \
            and lenght < 8:
        lane = lanes[random.randint(0, 4)] # randomize the lane
        car = choice[random.randint(0, 3)] # randomize the image of the car
        if car != bigTruck:
            hitbox = pygame.Rect(lane, -90, 65, 90)
        else:
            hitbox = pygame.Rect(lane, -240, 70, 210)
        obstacles.append(Cars(hitbox, car, 3)) # 3 is the speed, can also be randomize
        return obstacles
    else:
        return obstacles


def main(genomes, config):
    Obstacles = []
    Players = []
    ge = []
    neural_networks = []


    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config) #create neural_network for each player
        neural_networks.append(net)
        player = pygame.Rect(210, 580, 85, 105)
        Players.append(Player(player, redCar))
        g.fitness = 0
        ge.append(g)
    
    win = pygame.display.set_mode((WIDTH, HEIGHT)) #create the window
    clock = pygame.time.Clock()
    run = True
    score = 0
    game = Game(win, road)

    while run:
        clock.tick(FPS) #the window update at 60FPS even if the loop runs at more "FPS"
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #exit the game
                run = False
                pygame.quit()
                quit()
        
        if len(Players) == 0:
            break
        
        for x, player in enumerate(Players):
            ge[x].fitness += 0.5    # the longer the player stays without dying, the better the fitness
            lines = [1000, 1000, 1000, 1000, 1000]  # initialize at a far away distance
            danger_ahead = 0
            danger_side = 0
            for car in Obstacles:
                j = lanes.index(car.rect.x) # get the line in with the car is
                if player.getDistance(car) < lines[j] and car.rect.y + car.rect.height < player.rect.y:
                    lines[j] = player.getDistance(car) #get the distance between the player and the closest car in each lane

                #Two values to keep track of the surroundings of the player        
                if (car.rect.x <= player.rect.x + player.rect.width//2 <= car.rect.x + car.rect.width)\
                    and car.rect.y + car.rect.height + 240 >= player.rect.y > car.rect.y + car.rect.height :
                    danger_ahead = 1
                if (car.rect.y + car.rect.height >= player.rect.y)\
                    and (car.rect.x - 85 <= player.rect.x + player.rect.width//2 <= car.rect.x + car.rect.width + 85):
                    danger_side = 1
            
            state = (
            # danger in the same lane
                    danger_ahead,
            # danger close to the side
                    danger_side,
            # lanes with distance to the closest car (1000: no cars on the lane)
                    lines[0],
                    lines[1],
                    lines[2],
                    lines[3],
                    lines[4]
            )

            # Neural Network with an input of 7, 2 hidden layers and an output of 3
            output = neural_networks[x].activate(
                (state)
            )
            decision = output.index(max(output))    #get the index with the biggest output
            if decision == 0:
                player.playerMov(1) # move to the left
            elif decision == 1:
                player.playerMov(2) # move to the right
            elif decision == 2:
                pass                # stay on the same path


        Obstacles = addObstacle(Obstacles, score)
        for x, car in enumerate(Obstacles):
            if car.rect.y >= 700: # if the car in no longer in the window, remove it
                Obstacles.pop(x)
                score += 1
                for i, p in enumerate(Players):
                    ge[i].fitness += 1

        for x, player in enumerate(Players):
            if player.collision(Obstacles): # if a player hits a car, remove the player
                ge[x].fitness -= 10
                Players.pop(x)
                ge.pop(x)
                neural_networks.pop(x)
        
        game.draw_window(Players, Obstacles, SCORE_FONT, score)
        

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    
    #The next line starts the population from a checkpoint
    population = neat.Checkpointer.restore_checkpoint('neat-checkpoint-99')
    
    #The next line starts the population from zero
    #population = neat.Population(config)
    
    #Prints statistics
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(neat.Checkpointer(100))
    
    #Load the best_racer genome and run the program with it
    #with open("best_racer.pickle", "rb") as f:
    #   winner = pickle.load(f)
    #winner = winner.run(main, 100)

    winner = population.run(main, 100) # change the number to change the number of generations

    #Save the best genome in best_racer.pickle file
    with open("best_racer.pickle", "wb") as f:
        pickle.dump(winner, f)
    

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
