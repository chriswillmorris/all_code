dir_map = {'r':(0,1), 'd':(1,0), 'rd':(1,1), 'ru':(-1,1)}

def log(text):
    print text

    global log_file

    if isinstance(text, list):
        for item in text:
            log_file.write(item)
    else:
        log_file.write(text)

    log_file.write("\n")

def k_in_a_row_specific(board, k, row, col, char, dir):
    """
    board [in] - The board to be examined
    k [in] - The number of times the character must be
    listed consecutively
    row [in] - The row to start looking at
    col [in] - The col to start looking at
    char [in] - The item to look for
    dir [in] - The direction to look, where:
    'r' means to the right
    'd' means down
    'rd' means down and to the right
    'ru' means up and to the right
    """



    if k == 0:
        # There is always 0 in a row!
        return True

    highest_possible_index = len(board) - 1
    if (row > highest_possible_index) or (col > highest_possible_index) or\
    (row < 0) or (col < 0):
        # You've passed the end of the board
        return False

    #print "{0},{1}: {2}".format(row, col, board[row][col])

    if board[row][col] != char:
        # This piece is not the character you're looking
        # for
        return False

    # The piece has been found. Now try to find k-1 pieces
    # at the next spot
    global dir_map
    row_delta, col_delta = dir_map[dir]
    return k_in_a_row_specific(board, k-1, row + row_delta, col + col_delta, char, dir)

    

def k_in_a_row(board, k, char):
    """
    Returns true if there are k of the same character in
    a row in either horizontal, vertical, or diagonal
    fashion

    board [in] - The board to be examined
    k [in] - The number of times the character must be
    listed consecutively
    char [in] - The item to look for
    """

    '''
    Start at the top left.
    If the piece is not 'char,' then continue to the right
    and repeat. However, if there are no pieces to the right,
    go down one row and go to the very first column and
    continue.
    If it is 'char':
    See if there are k in a row in any direction.
    If so, you have a winner!
    If not, mark this piece as a loser and continue to
    the right (or to the next row and first column if there
    are no more to the right)
    '''
    dirs = ['r', 'd', 'rd', 'ru']
    num_rows = len(board)
    num_cols = len(board[0])
    for row in range(num_rows):
        for col in range(num_cols):
            for dir in dirs:
                if k_in_a_row_specific(board, k, row, col, char, dir) == True:
                    #print 'k in a row at {0}{1}'.format(row, col)
                    return True
    return False


def shift_piece_right(row, pos):
    """
    Shifts a piece (if there is one) to the right as
    far as possible.
    
    pos [in] - The position of the piece (if it exists)
    to shift
    """
    if pos == (len(row) - 1):
        # This is the last location in the row
        return
    
    if row[pos] != ".":
        # There is a piece at this location
        if row[pos + 1] == ".":
            # There is not a piece at the next location
            # Move the piece
            row[pos + 1] = row[pos]
            row[pos] = "."
    
            # Attempt to keep shifting the piece
            shift_piece_right(row, pos + 1)
        
        

def shift_pieces_right(row):
    """
    Shifts all pieces on a single row of the board as far
    right as possible
    """

    '''
    Start with the second-to-farthest right location.

    1. If it has a piece, attempt to shift it to the right.
    2. Go to the next farthest right location and repeat step 1.
    '''
    for pos in reversed(range(len(row))):
        shift_piece_right(row,pos)

    

def solve_case(f):
    """
    Solves a single board game case, declaring the winner
    """

    first_line = f.readline()

    # Remove new line
    first_line.strip()
    
    n,k = first_line.split(" ")
    n = int(n)
    k = int(k)

    log("N: {0}".format(n))
    log("K: {0}".format(k))

    # Process each line and populate the board
    board = []
    for i in range(n):
        row = list(f.readline().strip())
        board.append(row)

    # Print original board
    log("Original board")
    for row in board:
        log(row)

    log("")

    # Shift board to the right
    log("Shifted board")
    for row in board:
        shift_pieces_right(row)

    # Print shifted board
    for row in board:
        log(row)

    log("")

    red_wins = k_in_a_row(board, k, 'R')
    blue_wins = k_in_a_row(board, k, 'B')

    if red_wins and blue_wins:
        return "Both"
    elif red_wins:
        return "Red"
    elif blue_wins:
        return "Blue"
    else:
        return "Neither"


# Script starts here
log_file = open("log_file.txt", "w")
#f = open("A-small-practice.in")
f = open("A-large-practice.in")
#f = open("test.in")

t = int(f.readline())

print "T: {0}".format(t)

#out_file = open("small_output.txt",'w')
out_file = open("large_output.txt",'w')
for i in range(t):
    #print i
    if i != 0:
        out_file.write("\n")
    log("Case {0}".format(i))
    winner = solve_case(f)

    log("{0}\n".format(winner))
    out_file.write("Case #{0}: {1}".format(i + 1, winner))

out_file.close()
f.close()
log_file.close()
