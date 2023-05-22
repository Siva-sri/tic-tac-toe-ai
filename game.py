import time
from player import HumanPlayer, RandomComputerPlayer, GeniusComputerPlayer

class TicTacToe:
    def __init__(self):
        # we are going to use single list to represent 3X3 board
        self.board = [' ' for _ in range(9)] 
        # keep track of the winner
        self.current_winner = None

    def print_board(self):
        # to get the rows of the board
        for row in [self.board[i*3 : (i+1)*3] for i in range(3)]:
            print('| '+' | '.join(row)+ ' |')
            # i => 0,1,2 => List is divided into 3 parts
        # row takes individual values from the respective part of the list i.e from 0-2, 3-5, 6-8
    
    
    @staticmethod
    # A static method is a method which is bound to the class and not the object of the class, 
    # can be called using Class name instead of object name
    def print_board_nums():
        # 0 | 1 | 2 etc => tells us what number corresponds to what box
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print('| '+' | '.join(row)+ ' |')
    
    # to get the empty spots in the board
    def available_moves(self):
        return [i for i,spot in enumerate(self.board) if spot == ' ']
        # enumerate() => returns a list of tuples with the index and value
        # Ex - ['x','x','o'] --> [(0,'x'),(1,'x'),(2,'o')]
        # The above code is for the following code
        # moves = []
        # for (i, spot) in enumerate(self.board):
        #     if spot == ' ':
        #         moves.append(i)
        # return moves

    def empty_squares(self):
        return ' ' in self.board
    
    def num_empty_squares(self):
        return self.board.count(' ')
    
    def make_move(self, square, letter):
        # if valid move, then make the move (assign letter to square) and return True
        # else, return False
        if self.board[square] == ' ':
            self.board[square] = letter
            # Check for the winner
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False
    
    def winner(self, square, letter):
        # winner if 3 in a row, column or diagonal

        # checking row
        row_ind = square // 3
        row = self.board[row_ind * 3 : (row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True
        
        # checking column
        col_ind = square%3
        column = [self.board[col_ind + i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        
        # checking diagonals
        # to win a diagonal, the square should be an even number
        # check both the diagonals
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0,4,8]] # left top to right bottom diagonal
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2,4,6]] # right top to left bottom diagonal
            if all([spot == letter for spot in diagonal2]):
                return True
        # if all of these fail, return False
        return False


def play(game, x_player, o_player, print_game = True):
    # returns the Winner of the game(the letter)! of None for a tie
    if print_game:
        game.print_board_nums()
    letter = 'X' # Starting letter
    # Iterate while the game still has empty squares
    # We do not have to worry about winner because we will just return who breaks the loop    
    while game.empty_squares():
        # get move from the appropriate player
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)
        # Call make_move() to make a move
        if game.make_move(square, letter):
            if print_game:
                print(letter + f' makes a move to square {square}')
                game.print_board()
                print('') # Print empty line
            if game.current_winner:
                if print_game:
                    print(letter + ' wins!')
                return letter

            # after a game, we need alternate letter
            letter = 'O' if letter == 'X' else 'X' # switches player
        # small break
        if print_game:
            time.sleep(0.8)
        
    if print_game:
        print('It\'s a tie!')

if __name__ == '__main__':
    print('TIC-TAC-TOE')
    print('Choose the game options:')
    print('1. Human vs Random Computer')
    print('2. Human vs Genius Computer')
    print('3. Random vs Genius Computer')
    choice = 'y'
    option = 0
    while choice.lower() == 'y':
        option = int(input('Enter the option:- '))
        if option == 1:
            x_player = HumanPlayer('X')
            o_player = RandomComputerPlayer('O')
            t = TicTacToe()
            play(t, x_player, o_player, print_game=True) 
        elif option == 2:
            x_player = HumanPlayer('X')
            o_player = GeniusComputerPlayer('O')
            t = TicTacToe()
            play(t, x_player, o_player, print_game=True) 
        elif option == 3:
            x_wins = 0
            o_wins = 0
            ties = 0
            for _ in range(100):
                x_player = RandomComputerPlayer('X')
                o_player = GeniusComputerPlayer('O')
                t = TicTacToe()
                result = play(t, x_player, o_player, print_game=False)
                if result == 'X':
                    x_wins += 1
                elif result == 'O':
                    o_wins += 1
                else:
                    ties += 1
            print(f'After 100 iterations, we see {x_wins} X wins, {o_wins} O wins and {ties} ties.')
        else:
            print('Invalid option')
        choice = input('Do you want to continue?(y/n) ')
    
        
