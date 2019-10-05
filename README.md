# ai_connect4
AI Lab where we had to write methods to represent states of a Connect 4 game as a game tree. Afterwards, we implemented depth-first search (DFS) and basic endgame minimax search within our game trees. Lastly, we wrote an evaluation heurisitc for each game state with alpha-beta pruning and progressive deepening. (my heuristic is not that great just so you know)

## Running
```
python play_game.py
```

To see the different variations of the game, edit the main method to decide who is playing and which algorithm is being used

```python
if __name__ == '__main__':
    # Play a game between two humans:
    start_game(ConnectFourHumanPlayer(), ConnectFourHumanPlayer())
    # Play against your minimax player
    # start_game(ConnectFourMinimaxPlayer(), ConnectFourHumanPlayer())
    # Play against your alphabeta player
    # start_game(ConnectFourAlphaBetaPlayer(), ConnectFourAlphaBetaPlayer())
    # Play against your progressive deepening player
    # start_game(ConnectFourProgressiveDeepeningPlayer(), ConnectFourProgressiveDeepeningPlayer())
    # Play against your tournament player
    # start_game(ConnectFourTournamentPlayer(), ConnectFourProgressiveDeepeningPlayer())
    
    # You can easily set up a game against two bots! 
    # start_game(ConnectFourMinimaxPlayer(), ConnectFourAlphaBetaPlayer())
```

Big shout to my teacher Mr. Wang for creating this fun lab and teaching us Artificial Intelligence :) 
