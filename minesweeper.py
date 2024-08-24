import random 
import re


# lets create a board object to represent the minesweeper game
# this is so that we can just say "create a new board object", or
# "dig here", or "render this game for this object"
class Board:
    def __init__(self, dim_size, num_bombs):
        # lets keep track of these parameters. They will be helpful
        self.dim_size = dim_size 
        self.num_bombs = num_bombs

        # lets create the board
        # helper function!
        self.board = self.make_new_board()
        self.assign_values_to_board()
        #initialize a set to keep a track of which location's uncovered
        # we will save (row, col) tuples into this set
        self.dug = set() # if we dig at 0, 0 then self.dig = {(0, 0)}

    def make_new_board(self):
        # construct a new board based on the dim_size and num_bombs
        # we should construct the list of lists here (since we have a 2-D board, list of lists
        # is most natural)


        #generate a new board
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        # this created an array like this:
        # [[None, None, ..., None],
        #  [None, None, ..., None],
        #  [...                  ],
        #  [None, None, ..., None]]
        # we can see how this represents a board!

        # plant the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2-1) # return a random integer N such that a <= N <= b
            row = loc // self.dim_size #we want number of times dim_size goes into loc to tell us
            col = loc % self.dim_size #we want the remainder to tell us what index in that row to loop
            
            if board[row][col] == '*':
                # this means we have actually planted a bomb there already so keep going
                continue

            board[row][col] = '*' # plant the bomb
            bombs_planted += 1
        
        return board


    def assign_values_to_board(self):
        # now that we have the bombs planted, let's assign a number 0-8 for all empty spaces, which
        # represents how many neighboring bombs there are. we can precompute these and it'll save some
        # effort checking what's around the board later on:)
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    # if this is already a bomb, we don't want to calculate anything
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):
        # let's iterate through each of the neighboring positions and sum number of bombs



        #make sure to not go out of bounds!
        num_neighboring_bombs = 0
        for r in range(max(0, row-1), min(self.dim_size-1, row+1) + 1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if r == row and c == col:
                    # our original location, don't check
                    continue 
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1

        return num_neighboring_bombs

    def dig(self, row, col):
        # dig at the location
        # return True if successful dig, False if bomb dug

        # a few scenarios:
        # hit a bomb --> game over
        # dig at the location with neighboring bombs --> finish dig
        # dig at location with no neighboring bombs --> recursively dig neighbors!

        self.dug.add((row, col)) # keep track that we dug here

        if self.board[row][col] == '*':
            return False 
        elif self.board[row][col] > 0 :
            return True 
        
        # self.board[row][col] == 0
        for r in range(max(0, row-1), min(self.dim_size-1, row+1) + 1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if (r, c) in self.dug:
                    continue # don't dug where you've already dug
                self.dig(r, c)

        # if our intial dug didn't hit a bomb, we *shouldn't* hit a bomb there
        return True 

    def __str__(self):
        # this a magic function where if you call print on this object,
        # it'll print out what this function returns!
        # return a string that shows the board to the player

        #first let's create a new array that represents what the user would see
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '
        
        # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep



# play the game
def play(dim_size=10, num_bombs=10):
    # Step 1 : create the game and plant the bomb
    board = Board(dim_size, num_bombs)
    # Step 2 : show the user the board and ask for where they want to dig

    # Step 3a: if location is a bomb, show game over message
    # Step 3b: If location is not a bomb, dig recusrively until each square is at least
    #          next to a bomb
    # Step 4 : repeat steps 2 and 3a/b until there are no more places to dig --> VICTORY
    
    safe = True

    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        # 0,0 or 0, 0 or 0,   0
        user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as row, col: ") )# '0, 3'
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print("Invalid location. Try again.")
            continue

        # if it's valid, we dig
        safe = board.dig(row, col)
        if not safe:
            # dug a bomb ahhhhhh
            break # (game over rip)

    # 2 ways to end loop, lets check which one
    if safe:
        print("CONGRATULATIONS!!!! YOU ARE VICTORIOUS!")
    else:
        print("SORRY GAME OVER :(")
        # lets reveal the whole board
        board.dug = [(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)

if __name__ == '__main__': # good practice :)
    play()