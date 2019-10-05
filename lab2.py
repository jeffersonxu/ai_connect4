# AI Lab 2: Games and ConnectFour 

# Name(s): Jefferson Xu
# Email(s): jefxu19@bergen.org

from game_api import *
from boards import *
from toytree import GAME1
from time import time


INF = float('inf')

# Please see wiki lab page for full description of functions and API.

#### Part 1: Utility Functions #################################################

def is_game_over_connectfour(board):
    """Returns True if game is over, otherwise False."""
    if board.count_pieces() == 42:
        return True

    chains = board.get_all_chains()
    for chain in chains:
        if(len(chain) >= 4):
            return True

    return False

def next_boards_connectfour(board):
    """Returns a list of ConnectFourBoard objects that could result from the
    next move, or an empty list if no moves can be made."""
    moves = []
    if(is_game_over_connectfour(board)):
        return moves

    for i in range(7):
        if(not board.is_column_full(i)):
            moves.append(board.add_piece(i))

    return moves

def endgame_score_connectfour(board, is_current_player_maximizer):
    """Given an endgame board, returns 1000 if the maximizer has won,
    -1000 if the minimizer has won, or 0 in case of a tie."""
    playerChains = board.get_all_chains(is_current_player_maximizer)
    otherChains = board.get_all_chains(not is_current_player_maximizer)

    for chain in playerChains:
        if(len(chain) >= 4):
            return 1000
            
    for chain in otherChains:
        if(len(chain) >= 4):
            return -1000

    return 0

def endgame_score_connectfour_faster(board, is_current_player_maximizer):
    """Given an endgame board, returns an endgame score with abs(score) >= 1000,
    returning larger absolute scores for winning sooner."""
    return endgame_score_connectfour(board, is_current_player_maximizer) * (42 / board.count_pieces())

# Now we can create AbstractGameState objects for Connect Four, using some of
# the functions you implemented above.  You can use the following examples to
# test your dfs and minimax implementations in Part 2.

# This AbstractGameState represents a new ConnectFourBoard, before the game has started:
state_starting_connectfour = AbstractGameState(snapshot = ConnectFourBoard(),
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)

# This AbstractGameState represents the ConnectFourBoard "NEARLY_OVER" from boards.py:
state_NEARLY_OVER = AbstractGameState(snapshot = NEARLY_OVER,
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)

# This AbstractGameState represents the ConnectFourBoard "BOARD_UHOH" from boards.py:
state_UHOH = AbstractGameState(snapshot = BOARD_UHOH,
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)


#### Part 2: Searching a Game Tree #############################################

# Note: Functions in Part 2 use the AbstractGameState API, not ConnectFourBoard.

def dfs_maximizing(state) :
    """Performs depth-first search to find path with highest endgame score.
    Returns a tuple containing:
     0. the best path (a list of AbstractGameState objects),
     1. the score of the leaf node (a number), and
     2. the number of static evaluations performed (a number)"""
    best_score = None
    path = []
    num_evals = 0

    if state.is_game_over():
        return ([state], state.get_endgame_score(), 1)
    else:
        moves = state.generate_next_states()
        for move in moves:
            next_move = dfs_maximizing(move)
            num_evals += next_move[2]
            if best_score == None or next_move[1] > best_score:
                best_score = next_move[1]
                path = next_move[0]
                path.insert(0, state)

    return (path, best_score, num_evals)

# Uncomment the line below to try your dfs_maximizing on an
# AbstractGameState representing the games tree "GAME1" from toytree.py:

#pretty_print_dfs_type(dfs_maximizing(GAME1))

def minimax_endgame_search(state, maximize=True) :
    """Performs minimax search, searching all leaf nodes and statically
    evaluating all endgame scores.  Returns the same as dfs_maximizing:
    a tuple containing:
     0. the best path (a list of AbstractGameState objects),
     1. the score of the leaf node (a number), and
     2. the number of static evaluations performed (a number)"""
    best_score = None
    path = []
    num_evals = 0

    if state.is_game_over():
        return ([state], state.get_endgame_score(maximize), 1)
    else:
        moves = state.generate_next_states()
        for move in moves:
            next_move = minimax_endgame_search(move, not maximize)
            num_evals += next_move[2]

            if best_score == None or (maximize and next_move[1] > best_score) or (not maximize and next_move[1] < best_score):
                best_score = next_move[1]
                path = next_move[0]
                path.insert(0, state)

    return (path, best_score, num_evals)

# Uncomment the line below to try your minimax_endgame_search on an
# AbstractGameState representing the ConnectFourBoard "NEARLY_OVER" from boards.py:

#pretty_print_dfs_type(minimax_endgame_search(state_NEARLY_OVER))


#### Part 3: Cutting off and Pruning search #############################################


def heuristic_connectfour(board, is_current_player_maximizer):
    """Given a non-endgame board, returns a heuristic score with
    abs(score) < 1000, where higher numbers indicate that the board is better
    for the maximizer."""
    heuristic = 0
    player_chains  = board.get_all_chains(is_current_player_maximizer);
    other_chains = board.get_all_chains(not is_current_player_maximizer)

    for p_chain in player_chains:
      if len(p_chain) == 3:
        heuristic += 25

    for o_chain in other_chains:
      if len(o_chain) == 3:
        heuristic -= 25

    return heuristic

## Note that the signature of heuristic_fn is heuristic_fn(board, maximize=True)

def minimax_search(state, heuristic_fn=always_zero, depth_limit=INF, maximize=True) :
    """Performs h-minimax, cutting off search at depth_limit and using heuristic_fn
    to evaluate non-terminal states. 
    Same return type as dfs_maximizing, a tuple containing:
     0. the best path (a list of AbstractGameState objects),
     1. the score of the leaf node (a number), and
     2. the number of static evaluations performed (a number)"""
    best_score = None
    path = []
    num_evals = 0

    if state.is_game_over():
      return ([state], state.get_endgame_score(maximize), 1)
    elif depth_limit == 0:
      return ([state], heuristic_fn(state.get_snapshot(), maximize), 1)
    else:
      moves = state.generate_next_states()
      for move in moves:
        next_move = minimax_search(move, heuristic_fn, depth_limit - 1, not maximize)
        num_evals += next_move[2]

        if best_score == None or (maximize and next_move[1] > best_score) or (not maximize and next_move[1] < best_score):
          best_score = next_move[1]
          path = next_move[0]
          path.insert(0, state)

    return (path, best_score, num_evals)

# Uncomment the line below to try minimax_search with "BOARD_UHOH" and
# depth_limit=1. Try increasing the value of depth_limit to see what happens:

# pretty_print_dfs_type(minimax_search(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=2))

def minimax_search_alphabeta(state, alpha=-INF, beta=INF, heuristic_fn=always_zero,
                             depth_limit=INF, maximize=True) :
    """"Performs minimax with alpha-beta pruning. 
    Same return type as dfs_maximizing, a tuple containing:
     0. the best path (a list of AbstractGameState objects),
     1. the score of the leaf node (a number), and
     2. the number of static evaluations performed (a number)"""
    best_score = None
    path = []
    num_evals = 0

    if state.is_game_over():
      return ([state], state.get_endgame_score(maximize), 1)
    elif depth_limit == 0:
      return ([state], heuristic_fn(state.get_snapshot(), maximize), 1)
    else:
      moves = state.generate_next_states()
      for move in moves:
        next_move = minimax_search_alphabeta(move, alpha, beta, heuristic_fn, depth_limit - 1, not maximize)
        num_evals += next_move[2]
        
        if maximize:
          if next_move[1] > alpha:
            alpha = next_move[1]
        else:
          if next_move[1] < beta:
            beta = next_move[1]

        if best_score == None or (maximize and next_move[1] > best_score) or (not maximize and next_move[1] < best_score):
          best_score = next_move[1]
          path = next_move[0]
          path.insert(0, state)

        if alpha >= beta:
          return (path, best_score, num_evals)

    return (path, best_score, num_evals)


# Uncomment the line below to try minimax_search_alphabeta with "BOARD_UHOH" and
# depth_limit=4. Compare with the number of evaluations from minimax_search for
# different values of depth_limit.

#pretty_print_dfs_type(minimax_search_alphabeta(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4))

def progressive_deepening(state, heuristic_fn=always_zero, depth_limit=INF,
                          maximize=True, time_limit=INF) :
    """Runs minimax with alpha-beta pruning. At each level, updates anytime_value
    with the tuple returned from minimax_search_alphabeta. 
    Returns anytime_value."""
    anytime_value = AnytimeValue()
    start_time = time()
    depth = 1

    while time() - start_time < time_limit:
        if depth == depth_limit + 1:
            break;
        minimax_tup = minimax_search_alphabeta(state, heuristic_fn=heuristic_fn, depth_limit=depth, maximize=maximize)
        anytime_value.set_value(minimax_tup)
        depth += 1

    return anytime_value

# Uncomment the line below to try progressive_deepening with "BOARD_UHOH" and
# depth_limit=4. Compare the total number of evaluations with the number of
# evaluations from minimax_search or minimax_search_alphabeta.

# progressive_deepening(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4).pretty_print()


# Progressive deepening is NOT optional. However, you may find that 
#  the tests for progressive deepening take a long time. If you would
#  like to temporarily bypass them, set this variable False. You will,
#  of course, need to set this back to True to pass all of the local
#  and online tests.
TEST_PROGRESSIVE_DEEPENING = True
if not TEST_PROGRESSIVE_DEEPENING:
    def not_implemented(*args): raise NotImplementedError
    progressive_deepening = not_implemented




#
# If you want to enter the tournament, implement your final contestant 
# in this function. You may write other helper functions/classes 
# but the function must take these arguments (though it can certainly ignore them)
# and must return an AnytimeValue.
#
def tournament_search(state, heuristic_fn=always_zero, depth_limit=INF,
                          maximize=True, time_limit=INF) :
    """Runs some kind of search (probably progressive deepening).
    Returns an AnytimeValue."""
    raise NotImplementedError

