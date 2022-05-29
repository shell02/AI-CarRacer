# AI-CarRacer

A simple car racer game where a genetic AI evolves to avoid the cars coming in the lanes. 

50 players at a time get attributed a fitness score, that gets better the longer they stay alive. After every player is dead, the best player genes are preserved, the worst players are scraped and some mutations occur to try and find the best combination to get the furthest. This procees goes on for 100 generations.

There are three decision the AI can make :
- go to the left
- go to the right
- stay in place

To decide, 7 arguments are given in input :
- if a car is present right ahead
- if a car is present right on the side
- the location of the closest car in each lane (if a car is present on the lane)

To run the game for your own:
```
pip install -r requirements.txt
python main_neat.py
```
