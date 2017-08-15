__author__ = "Jacob Ider Chitham"
__credits__ = ["Udacity"]
__version__ = "1.0.0"
__maintainer__ = "Jacob Ider Chitham"
__email__ = "jacobic@hotmail.co.uk"
__status__ = "Submitted"

import random
import math

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass
  
def cross(A, B):
    """Cross product.
    
    Useful for generating a list of elements that are at sides or corners of 
    the game board.        
    """
    return [(a,b) for a in A for b in B]

def game_dim(game):
    """Get the x and y dimensions of isolation game board (width, height).
  
    Args:
        game: isolation.Board
            An instance of isolation.Board encoding the current state of 
            the game (e.g., player locations and blocked cells).
  
    Returns:
        Dimensions of game board (width, height).      
    """
    return game.width, game.height

def loc(game, player):
    """Find the current location of the specified player on the board.
  
    Args:
        game: isolation.Board
            An instance of isolation.Board encoding the current state of 
            the game (e.g., player locations and blocked cells).
        player: object
            A player instance in the current game (i.e., an object 
            corresponding to one of the player objects game.__player_1__ or 
            game.__player_2__.)
            
    Returns:
        (int, int) or None
            The coordinate pair (row, column) of the input player, or None
            if the player has not moved.     
    """
    return game.get_player_location(player)

def n_moves(game, player):
    """Get the number of legal moves available to the player on the board at a 
     specific game state.
  
    Args:
        game: isolation.Board
            An instance of isolation.Board encoding the current state of 
            the game (e.g., player locations and blocked cells).
        player: object
            A player instance in the current game (i.e., an object 
            corresponding to one of the player objects game.__player_1__ or 
            game.__player_2__.)
            
    Returns:
        int: The number of unique legal moves.    
      """
    return len(game.get_legal_moves(player))

def board_frac(game):
    """Get ratio of blank spaces to total spaces on game board.
  
     Args:
        game: isolation.Board
            An instance of isolation.Board encoding the current state of 
            the game (e.g., player locations and blocked cells).
  
    Returns:
        float: The ratio of blank spaces to total spaces on game board.     
      """
    return len(game.get_blank_spaces()) / (game.width * game.height)

def dist_edge(coord, edge):
    """Get distance to an edge.
    
    Get x (or y) component of distance from x (or y) coordinate to the x (or y) 
    coordinate of specified edge of the board.
    
    Args:
        coord: The x (or y) component from a location tuple (x,y).
        side: An x (or y) value corresponding to one of the edges of the board.
      
    Returns:
        float: The ratio of blank spaces to total spaces on game board.     
      """
    if coord >= int(edge / 2) :
        return abs(coord - edge)
    else:
        return edge - abs(coord - edge)
 
def dist_cent(game, coords):
    """Get Euclidean distance to centre of board from specified coordinates.
  
     Args:
        game: An instance of isolation.Board encoding the current state of 
            the game (e.g., player locations and blocked cells).
        coords: a tuple (x,y) corresponding to a location on the board.
  
     Returns:
        float: Euclidean distance between centre of board and specified 
            coordinates of location.     
    """
    w, h = game_dim(game)
    return math.hypot((w / 2) - coords[0], (h / 2) - coords[1])

def dist_players(game, player):
    """Get Euclidean distance between a player and its opponent.
    
    Args:
        game: isolation.Board
            An instance of isolation.Board encoding the current state of the 
            game (e.g., player locations and blocked cells).
        player: object
            A player instance in the current game (i.e., an object 
            corresponding to one of the player objects game.__player_1__ or 
            game.__player_2__.)
    
    Returns:
        float: Euclidean distance between a player and its opponent.
    """
    loc_player = loc(game, player)
    loc_opp = loc(game, game.get_opponent(player))
    return math.hypot(loc_player[0]-loc_opp[0], loc_player[1]-loc_opp[1])

def corners(game):
    """Create list of location tuples that are at the corners of the board.
    
    Args:
        game: isolation.Board
            An instance of isolation.Board encoding the current state of the 
            game (e.g., player locations and blocked cells).
    Returns:
        list: List of location tuples that are at the corners of the board.
    """
    w, h = game_dim(game)
    return cross((0, w - 1), (0, h - 1))

def min_dist_corn(game, coords):
    """Get distance to nearest corner of the board from specified location.
    
    Args:
        game: isolation.Board
            An instance of isolation.Board encoding the current state of the game
            (e.g., player locations and blocked cells).
        coords: A tuple (x,y) corresponding to a location on the board.
  
    Returns:
        float: Distance to nearest corner of the board from specified location.
    """
    c = corners(game)
    return min([math.hypot(xc - coords[0], yc - coords[1]) for xc, yc  in c])

def min_dist_edge(game, coords):
    """Get distance to nearest edge of the board.
    
    Args:
        game: An instance of isolation.Board encoding the current state of the 
            game (e.g., player locations and blocked cells).
        coords: A tuple (x,y) corresponding to a location on the board.
  
    Returns:
        float: Distance to nearest edge of the board from specified location.
    """
    w, h = game_dim(game)
    return min(dist_edge(coords[0], w - 1), dist_edge(coords[1], h - 1))

def score_border(game, player):
    """Calculate the heuristic component of a game state from the point of view 
    of the given player that uses the distance to/from the border of the game 
    board as features (i.e. edges and corners).
     
    Args:
        game: isolation.Board
            An instance of isolation.Board encoding the current state of the 
            game (e.g., player locations and blocked cells).
        player: object
            A player instance in the current game (i.e., an object 
            corresponding to one of the player objects game.__player_1__ or 
            game.__player_2__.)
  
    Returns:
        float: Heuristic score which uses the distance to/from edges and 
        corners of the board as features.
    """
    moves = game.get_legal_moves(player)
    score_corn, score_edge = 0, 0 
     
    if board_frac(game) > 0.85:
        tuning = 3 
    elif board_frac(game) > 0.5:
        tuning = 2
    else:
        tuning = 1
        
    for m in moves:
        if (min_dist_corn(game, m) == 0):
            score_corn += 1
        if (min_dist_edge(game, m) == 0):
            score_edge += 1         
    score = float(10 * tuning * (0.7 * score_corn) + (0.3 * score_edge))
    return float(score) 
    
def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
  
    Note: this function should be called from within a Player instance as
    self.score() -- do not need call this function directly.
  
     Args:
        game: isolation.Board
            An instance of isolation.Board encoding the current state of the
            game (e.g., player locations and blocked cells).
        player: object
            A player instance in the current game (i.e., an object 
            corresponding to one of the player objects game.__player_1__ or 
            game.__player_2__.)
    Returns:
            float: The heuristic value of the current game state to the specified 
                player.
    """
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")
    
    opponent = game.get_opponent(player)
    return float((n_moves(game, player))**2 - ((n_moves(game, opponent))**2))

def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
  
    Note: this function should be called from within a Player instance as
    self.score() -- do not need call this function directly.
  
     Args:
        game: isolation.Board
            An instance of isolation.Board encoding the current state of the
            game (e.g., player locations and blocked cells).
        player: object
            A player instance in the current game (i.e., an object 
            corresponding to one of the player objects game.__player_1__ or 
            game.__player_2__.)
    Returns:
          float: The heuristic value of the current game state to the specified 
                player.
    """
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")
    
    d_p = dist_players(game, player)
    opponent = game.get_opponent(player)
    n1, n2 = n_moves(game, player), n_moves(game, opponent)
    return float(d_p * (n1 - (1.5 * n2)))

def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
  
    Note: this function should be called from within a Player instance as
    self.score() -- do not need call this function directly.
  
     Args:
        game: isolation.Board
            An instance of isolation.Board encoding the current state of the
            game (e.g., player locations and blocked cells).
        player: object
            A player instance in the current game (i.e., an object 
            corresponding to one of the player objects game.__player_1__ or 
            game.__player_2__.)
    Returns:
        float: The heuristic value of the current game state to the specified 
            player.
    """
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")
    
    d_p = dist_players(game, player)
    opponent = game.get_opponent(player)
    n1, n2 = n_moves(game, player), n_moves(game, opponent)
    return float(d_p * ((n1**2) - (n2**2)))
                 
class IsolationPlayer:
    """Base class for minimax and alphabeta agents.

     Args:
        search_depth: int (optional)
            A strictly positive integer (i.e., 1, 2, 3,...) for the number of
            layers in the game tree to explore for fixed-depth search. (i.e.
            a depth of one (1) would only explore the immediate sucessors of 
            the current state.)
        score_fn: callable (optional)
            A function to use for heuristic evaluation of game states.
        timeout: float (optional)
            Time remaining (in milliseconds) when search is aborted. Should 
            be a positive value large enough to allow the function to return 
            before the timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=1.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search.
    """
    
    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents.
        
         Args:
            game: isolation.Board
                An instance of isolation.Board encoding the current state of 
                the game (e.g., player locations and blocked cells).
            time_left: callable
                A function that returns the number of milliseconds left in the
                current turn. Returning with any less than 0 ms remaining 
                forfeits the game.
      
        Returns:    
        (int, int):
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialise the best move in case the search fails due to timeout
        best_move = (-1, -1)
        
        # The try/except block will automatically catch the exception
        # raised when the timer is about to expire.
            
        try:
            return self.minimax(game, self.search_depth)
        except SearchTimeout:
            pass
        return best_move  # Return the best move from the last search iteration
    
    def terminal_test(self, game):
        """ Return True if the game is over for the active player and False 
        otherwise.
        """ 
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        return not bool(game.get_legal_moves())
    
    def max_value(self, game, depth):
        """ Return the utility of the current game state from the perspective
        of the specified player if the game is over, otherwise return the 
        minimum value over all legal child nodes.
        """ 
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if self.terminal_test(game) or depth == 0:     
            return self.score(game, self)
        v = float("-inf")
        for m in game.get_legal_moves():
            v = max(v, self.min_value(game.forecast_move(m), depth-1))
        return v
    
    def min_value(self, game, depth):
        """ Return the utility of the current game state from the perspective
        of the specified player if the game is over, otherwise return the 
        minimum value over all legal child nodes.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if self.terminal_test(game) or depth == 0:     
            return self.score(game, self)
        v = float("inf")
        for m in game.get_legal_moves():
            v = min(v, self.max_value(game.forecast_move(m), depth-1))
        return v   
    
    def minimax(self, game, depth):
        """Depth-limited minimax search algorithm.
  
         Args:
            game: isolation.Board
                An instance of isolation.Board encoding the current state of 
                the game (e.g., player locations and blocked cells).
            depth: int
                Depth is an integer representing the maximum number of plies to
                search in the game tree before aborting
  
         Returns:
            (int, int)
                The board coordinates of the best move found in the current 
                search; (-1, -1) if there are no legal moves
              
        """  
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
          
        return max(game.get_legal_moves() , key=lambda m: 
                   self.min_value(game.forecast_move(m), self.search_depth-1), 
                   default=(-1, -1))   

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning.
    """
    
    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.
              
         Args:
            game: isolation.Board
                An instance of isolation.Board encoding the current state of 
                the game (e.g., player locations and blocked cells).
            time_left: callable
                A function that returns the number of milliseconds left in the
                current turn. Returning with any less than 0 ms remaining 
                forfeits the game.
  
         Returns:
          (int, int)
              Board coordinates corresponding to a legal move; may return
              (-1, -1) if there are no available legal moves.
        """    
        self.time_left = time_left

        # Initialise the best move in case the search fails due to timeout
        depth, best_move = 3, (-1, -1)
        
        # The try/except block will automatically catch the exception
        # raised when the timer is about to expire. 
        
        while True:   
            try:            
                if not self.terminal_test(game):
                    move = self.alphabeta(game, depth)
                    if move != (-1, -1):
                        best_move = move
                    depth += 1                 
                else:
                    break                   
            except SearchTimeout:
                break
        return best_move  # Return the best move from the last search iteration
    
    def terminal_test(self, game):
        """ Return True if the game is over for the active player and False 
        otherwise.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        return not bool(game.get_legal_moves())
    
    def max_value(self, game, depth, alpha, beta):
        """ Return the utility of the current game state from the perspective
        of the specified player if the game is over, otherwise return the 
        maximum value over all legal child nodes.
        """   
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if self.terminal_test(game) or depth == 0:   
            return self.score(game, self)

        v = float("-inf")
        for m in game.get_legal_moves():
            v = max(v, self.min_value(game.forecast_move(m), depth-1,
                                      alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v
    
    def min_value(self, game, depth, alpha, beta):
        """ Return the utility of the current game state from the perspective
        of the specified player if the game is over, otherwise return the 
        minimum value over all legal child nodes.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if self.terminal_test(game) or depth == 0:
            return self.score(game, self)
          
        v = float("inf")
        for m in game.get_legal_moves():
            v = min(v, self.max_value(game.forecast_move(m), depth-1,
                                      alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v   
    
    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Depth-limited minimax search algorithm with alpha-beta pruning.

        Args:
            game: isolation.Board
                An instance of the Isolation game Board class representing the
                current game state
            depth: int
                Depth is an integer representing the maximum number of plies to
                search in the game tree before aborting
            alpha: float
                Alpha limits the lower bound of search on minimizing layers
            beta: float
                Beta limits the upper bound of search on maximizing layers

        Returns:
            (int, int):
                The board coordinates of the best move found in the current search;
                (-1, -1) if there are no legal moves    
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        transposition = {}
        game_hash = game.hash()   
        best_move = (-1, -1) 
        moves = game.get_legal_moves()
        op_moves = game.get_legal_moves(game.get_opponent(self))  

        if moves:
            if len(op_moves) == 1 and op_moves[0] in moves:
                transposition[game_hash] = op_moves[0]
                return op_moves[0]  # Trap opposite player if possible
            best_move = moves[0]  # Select any legal move to prevent forfeit                 
            
            # Prioritise previous best moves to improve IDFS performance
            if game_hash in transposition.keys():
                best_move = transposition[game_hash]
                i = moves.index(best_move)
                moves[0], moves[i] = moves[i], moves[0]
            
            # Modified version of helper functions for the top of the game tree      
            v = float("-inf")
            for m in moves:
                v_prime = self.min_value(game.forecast_move(m), depth-1,
                                          alpha, beta)
                if v < v_prime:
                    best_move = m
                    transposition[game_hash] = best_move
                    v = v_prime
                alpha = max(alpha, v)
        return best_move