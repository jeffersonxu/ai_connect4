# AI Lab 2: Games and ConnectFour 

# To play against your Connect Four implementations
# configure the main at the bottom and
# run this file from your lab3 directory.

from game_api import *
from boards import *
from lab2 import *
from time import time

# TESTING = False
QUIT = ['q', 'Q', 'quit', 'Quit', 'QUIT']
YES = ['y', 'yes', 'Y', 'Yes', 'YES']
NO = ['n', 'no', 'N', 'No', 'NO']
NO_LIMIT = ['inf', 'INF', "Inf", 'infinity', 'infinite', "Infinity", "Infinite",
            'INFINITY', 'INFINITE', 'none', "None", "NONE"]

def ask_user_depth_limit(nameOfPlayer, cautionaryDepth):
    print("\nPlease choose the depth limit for " + nameOfPlayer)
    print("(Picking values larger than " + cautionaryDepth + " could result in long wait times,")
    print(" while picking 1 would make for a mostly trivial game)")
    depth_limit = None
    while depth_limit is None:
        inp = input(">>> ")
        try:
            depth_limit = int(inp)
        except:
            pass
        if inp in NO_LIMIT:
            depth_limit = INF
        elif depth_limit is None or depth_limit < 1:
            depth_limit = None
            print("Oops, please give an integer value >= 1.")
    return depth_limit

def ask_user_time_limit(nameOfPlayer):
    print("\nPlease choose the time limit (in seconds) for " + nameOfPlayer)
    time_limit = None
    while time_limit is None:
        inp = input(">>> ")
        try:
            time_limit = float(inp)
        except:
            pass
        if inp in NO_LIMIT:
            time_limit = INF
        elif time_limit is None or time_limit <= 0:
            time_limit = None
            print("Oops, please give numerical value > 0.")
    return time_limit

def ask_user_verbosity(nameOfPlayer):
    verbose = None
    while verbose is None:
        print("Should " + nameOfPlayer + " be verbose?")
        inp = input(">>> ")
        if inp in YES:
            verbose = True
        elif inp in NO:
            verbose = False
        if verbose is None:
            print("Oops, please type either 'yes' or 'no'.")
    return verbose

class ConnectFourHumanPlayer(ConnectFourPlayer) :

    def __init__(self, name="Human Player"):
        self.name = name
        super().__init__()

    def set_up(self, name=None):
        if name is not None and name is not "":
            self.name = name

    def player_turn(self, state):
        print(self.get_name() + ": into which column [0-6] would you like to place a piece?")
        player_response = None
        while player_response is None:
            inp = input(">>> ")

            # Allow the player to quit gracefully
            if inp in QUIT:
                player_response = None
                break
            try:
                player_response = int(inp)
            except:
                pass
            if player_response not in range(7):
                player_response = None
                print("Oops, please pick a column between 0 and 6, inclusive")
            if player_response is not None and state.snapshot.is_column_full(player_response):
                player_response = None
                print("Oops, that column's full")
        
        if player_response is not None:
            snapshot = state.get_snapshot().add_piece(player_response)
            state = new_state(snapshot)
        else:
            state = None 
        return state


class ConnectFourMinimaxPlayer(ConnectFourPlayer) :

    def __init__(self, name="Minimax Bot", depth_limit = INF, verbose = False):
        self.name = name
        self.verbose = verbose
        self.depth_limit = depth_limit
        self.verbose = verbose
        super().__init__()

    def set_up(self, name=None, depth_limit = None, verbose = None):
        if name is not None and name is not "":
            self.name = name

        if depth_limit == None:
            depth_limit = ask_user_depth_limit("Minimax search", "4 or 5")
        self.depth_limit = depth_limit

        if verbose == None:
            verbose = ask_user_verbosity(self.name)
        self.verbose = verbose

    def player_turn(self, state):
        starttime = time()
        path, score, evals = minimax_search(
            state, heuristic_connectfour, self.depth_limit)
        new_state = path[1]
        if self.verbose:
            print(self.name +" evaluates the board value as " + str(score) + ".")
            print(self.name +" did " + str(evals) + " board evaluations.")
            print(self.name + " took " + "{0:.2f}".format(time() - starttime) + " seconds.")

        return new_state

class ConnectFourAlphaBetaPlayer(ConnectFourPlayer) :

    def __init__(self, name="Alpha-Beta Bot", depth_limit = INF, verbose = False):
        self.name = name
        self.depth_limit = depth_limit
        self.verbose = verbose
        super().__init__()

    def set_up(self, name=None, depth_limit = None, verbose = None):
        if name is not None and name is not "":
            self.name = name
        if depth_limit == None:
            depth_limit = ask_user_depth_limit(self.name, "6 or 7")
        self.depth_limit = depth_limit

        if verbose == None:
            verbose = ask_user_verbosity(self.name)
        self.verbose = verbose
                

    def player_turn(self, state):
        starttime = time()
        path, score, evals = minimax_search_alphabeta(
            state, -INF, INF, heuristic_connectfour, self.depth_limit)
        new_state = path[1]
        if self.verbose:
            print(self.name +" evaluates the board value as " + str(score) + ".")
            print(self.name +" did " + str(evals) + " board evaluations.")
            print(self.name + " took " + "{0:.2f}".format(time() - starttime) + " seconds.")
        return new_state

class ConnectFourProgressiveDeepeningPlayer(ConnectFourPlayer) :

    def __init__(self, name="ProgressiveDeepening Bot",  depth_limit = INF, time_limit = INF, verbose = False):
        self.name = name
        self.depth_limit = depth_limit
        self.time_limit = time_limit
        self.verbose = verbose

        super().__init__()

    def set_up(self, name=None, depth_limit = None, time_limit = None, verbose = None):
        if name is not None and name is not "":
            self.name = name
        if depth_limit == None:
            depth_limit = ask_user_depth_limit(self.name, "6 or 7")
        self.depth_limit = depth_limit
        if time_limit == None:
            time_limit = ask_user_time_limit(self.name)
        self.time_limit = time_limit
        if verbose == None:
            verbose = ask_user_verbosity(self.name)
        self.verbose = verbose


    def player_turn(self, state):
        starttime = time()
        anytime_val = progressive_deepening(state, heuristic_connectfour, self.depth_limit,True,self.time_limit)
        path, score, evals = anytime_val.get_value()
        new_state = path[1]

        if self.verbose:
            print(self.name + " evaluated up to depth " + str(len(anytime_val.get_history())) + ".")
            print(self.name +" evaluates the board value as " + str(score) + ".")
            print(self.name +" did " + str(anytime_val.get_total_evaluations()) + " total board evaluations.")
            print(self.name + " took " + "{0:.2f}".format(time() - starttime) + " seconds.")
        return new_state

class ConnectFourTournamentPlayer(ConnectFourPlayer) :

    def __init__(self, name="Tournament Bot",  depth_limit = INF, time_limit = INF, verbose = False):
        self.name = name
        self.depth_limit = depth_limit
        self.time_limit = time_limit
        self.verbose = verbose

        super().__init__()

    def set_up(self, name=None, depth_limit = None, time_limit = None, verbose = None):
        if name is not None and name is not "":
            self.name = name
        if depth_limit == None:
            depth_limit = ask_user_depth_limit(self.name, "6 or 7")
        self.depth_limit = depth_limit
        if time_limit == None:
            time_limit = ask_user_time_limit(self.name)
        self.time_limit = time_limit
        if verbose == None:
            verbose = ask_user_verbosity(self.name)
        self.verbose = verbose


    def player_turn(self, state):
        starttime = time()
        anytime_val = progressive_deepening(state, heuristic_connectfour, self.depth_limit,True,self.time_limit)
        path, score, evals = anytime_val.get_value()
        new_state = path[1]

        if self.verbose:
            print(self.name + " evaluated up to depth " + str(len(anytime_val.get_history())) + ".")
            print(self.name +" evaluates the board value as " + str(score) + ".")
            print(self.name +" did " + str(anytime_val.get_total_evaluations()) + " total board evaluations.")
            print(self.name + " took " + "{0:.2f}".format(time() - starttime) + " seconds.")
        return new_state




def new_state(snapshot=None):
    board = ConnectFourBoard() if snapshot is None else snapshot
    state_starting_connectfour = AbstractGameState(
        snapshot=board,
        is_game_over_fn=is_game_over_connectfour,
        generate_next_states_fn=next_boards_connectfour,
        endgame_score_fn=endgame_score_connectfour_faster)
    return state_starting_connectfour


def start_game(player1=ConnectFourHumanPlayer(), 
    player2=ConnectFourHumanPlayer(), 
    state = new_state(), move_time_limit = None):
    print("\n\n\n")

    player1, player2, move_time_limit = say_hi(player1, player2, move_time_limit)

    cont = True
    player_one_move = True

    while cont:
        # Print the board state, then have someone take a turn
        print_board_state(state)
        time_start = time()
        if player_one_move:
            state = player1.player_turn(state)
            if move_time_limit and ((time() - time_start) > move_time_limit) :
                state = None
            if state is not None:
                print(player1.get_name() + "'s move: " + state.describe_previous_move())
        else:
            state = player2.player_turn(state)
            if move_time_limit and ((time() - time_start) > move_time_limit) :
                state = None
            if state is not None:
                print(player2.get_name() + "'s move: " + state.describe_previous_move())

        # If the player wants to exit, or if the game is over,
        #  print who wins and decide if a new game should be started
        if state is None or state.is_game_over():
            cont = print_endgame(state, player1 if player_one_move else player2)
            state = new_state()
            player_one_move = False # to be flipped to True if replaying

        # Switch whose turn it is
        player_one_move = not player_one_move
    print("Thanks for playing!")

def was_a_draw(state):
    for chain in state.snapshot.get_all_chains():
        if len(chain) >= 4:
            return False
    return True


def print_endgame(state, current_player):
    if state is None:
        print("\n\n" + current_player.get_name() + " concedes (or ran out of time)! Good game, everyone.")
    else:
        print_board_state(state, game_over=True)
        if was_a_draw(state):
            print("Nice, it was a draw!")
        else:
            print("Congrats! " + current_player.get_name() + " won.")

    print("Salty runback?")
    play_again = input(">>> ") in YES
    return play_again


def print_board_state(state, game_over=False):
    if game_over:
        print("\n\n\nFinal board state:")
    else:
        print("\n\nCurrent board state:")
    print(state.snapshot)
    print("0 1 2 3 4 5 6")
    print("")


def say_hi(player1, player2, move_time_limit):
    print("\nWelcome!")
    if move_time_limit is None:
        move_time_limit = ask_user_time_limit(" each player (enforced hard limit)")

    print("First, let's get Player 1's name (" + player1.get_name() + "): ")
    player1.set_up(name = input(">>> "))
    print("Next, let's get Player 2's name (" + player2.get_name() + "): ")
    player2.set_up(name = input(">>> "))


    first = None
    while first is None:
        print("\nOkay, is " + player1.get_name() + " going first?")
        inp = input(">>> ")
        if inp in YES:
            first = True
        elif inp in NO:
            temp = player1
            player1 = player2
            player2 = temp
            first = False
        if first is None:
            print("Oops, please type either 'yes' or 'no'.")
    
    print("\nCool. Human players can type 'q' at any point to quit (or <Ctrl-c>)")
    print("Let's play Connect 4!")
    if move_time_limit is not None:
        print("Each player has " + str(move_time_limit) + " seconds to make a move, or else they forfeit.")
    print("\n\n")
    return player1, player2, move_time_limit


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
    