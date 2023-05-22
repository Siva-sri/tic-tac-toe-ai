import math
import random

# Base class
class Player:
    def __init__(self, letter):
        # letter is x or o
        self.letter = letter
    
    # We want all players to get the next move given in a game
    # We will define it in the the sub classes
    def get_move(self, game):
        pass

# Sub class of Player
class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)
    
    def get_move(self, game):
        # get a random valid spot for our next move
        square = random.choice(game.available_moves())
        return square

# Sub class of Player
class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)
    
    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0-8) ')
            # Check whether user entered an integer or not => If not, try again
            # If it is an integer, check if that spot is available or not => If not try again
            # If that spot is available i.e valid, return the spot
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Try again.')
        return val

class GeniusComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves())== 9:
            square = random.choice(game.available_moves()) # randomly choose a square
        else:
            # get a square based on MiniMax algorithm
            square = self.minimax(game, self.letter)['position']
        return square
    
    def minimax(self, state, player):
        # Recursive function
        max_player = self.letter # the User
        other_player = 'O' if player == 'X' else 'X' # the other player is opposite to user
        # Base case
        # Check if current move is a winner
        if state.current_winner == other_player:
            # return position and score to make minimax function work
            return {'position': None,
                    'score': 1 * (state.num_empty_squares()+1) if other_player == max_player 
                    else -1 * (state.num_empty_squares()+1)
                    }
        elif not state.empty_squares():
            return {'position':None,
                    'score':0
                    }
        if player == max_player:
            best = {'position':None, 'score': -math.inf} # each score should maximize (should be larger)
        else:
            best = {'position':None, 'score': math.inf} # each score should minimize (should be smaller)
        
        for possible_move in state.available_moves():
            # Step 1: make a move, try that spot
            state.make_move(possible_move, player)

            # Step 2: recurse using minimax to simulate a game after making that move for alternate player
            sim_score = self.minimax(state, other_player) # state is now updated after Step 1

            # Step 3: undo the move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move # otherwise this will get messed up from the recursion

            # Step 4: update the dictionaries if neccessary
            if player == max_player: # maximize the max player
                if sim_score['score'] > best['score']:
                    best = sim_score # replace with best
            else:                    # minimize the other player
                if sim_score['score'] < best['score']:
                    best = sim_score # replece with best
        return best
        

    