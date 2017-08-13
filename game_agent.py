__author__ = "Jacob Ider Chitham"
__credits__ = ["Udacity"]
__version__ = "1.0.0-alpha"
__maintainer__ = "Jacob Ider Chitham"
__email__ = "jacobic@hotmail.co.uk"
__status__ = "In Progress"

import random
import math
import logging

log_file = 'debug.log'
log_format = '%(asctime)s - %(levelname)s - %(message)s'
log_level = logging.DEBUG
logging.basicConfig(filename=log_file,level=log_level,format=log_format)
logging.FileHandler(filename=log_file, mode='w')
transposition = {}

def cross(A, B):
    return [(a,b) for a in A for b in B]

def game_dim(game):
    return game.width, game.height

def loc(game, player):
    return game.get_player_location(player)

def n_moves(game, player):
    return len(game.get_legal_moves(player))

def board_frac(game):
    return len(game.get_blank_spaces()) / (game.width * game.height)

def dist_edge(coord, side):
    if coord >= int(side / 2) :
        return abs(coord - side)
    else:
        return side - abs(coord - side)
 
def dist_cent(game, coords):
    w, h = game_dim(game)
    return math.hypot((w / 2) - coords[0], (h / 2) - coords[1])

def dist_players(game, player):
    loc_player = loc(game, player)
    loc_opp = loc(game, game.get_opponent(player))
    return math.hypot(loc_player[0]-loc_opp[0], loc_player[1]-loc_opp[1])

def corners(game):
    w, h = game_dim(game)
    return cross((0, w-1), (0, h-1))

def min_dist_corn(game, coords):
    c = corners(game)
    return min([math.hypot(xc-coords[0], yc-coords[1]) for xc, yc  in c])

def min_dist_edge(game, coords):
    w, h = game_dim(game)
    return min(dist_edge(coords[0], w-1), dist_edge(coords[1], h-1))

def score_border(game, player):
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
    #logging.info('score_corn = {}, score_edge = {}, tuning = {}, score = {}'.format(score_corn, score_edge, tuning, score)) 
    return float(score) 
        
class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- do not need call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    opponent = game.get_opponent(player)
    return float(n_moves(game, player) - n_moves(game, opponent))

def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- do not need call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    
    opponent = game.get_opponent(player)
    return float(n_moves(game, player) - (1.5 * n_moves(game, opponent)))

def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- do not need call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    
    opponent = game.get_opponent(player)
    return float((n_moves(game, player))**2 - ((n_moves(game, opponent))**2))

def custom_score_4(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- do not need call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    opponent = game.get_opponent(player)
    return float((n_moves(game, player))**2 - (1.5*((n_moves(game, opponent))**2)))

def custom_score_5(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- do not need call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
     
    opponent = game.get_opponent(player)
    eval_border = score_border(game, player) - score_border(game, opponent)
    return  float(-eval_border)


def custom_score_6(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- do not need call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    
    eval_border = 0
    opponent = game.get_opponent(player)
    n1, n2 = n_moves(game, player), n_moves(game, opponent)
    s1, s2 = score_border(game, player), score_border(game, opponent) 
    if n1 != 0 and n2 != 0:
        eval_border = ((s1/n1) - (s2/n2))       
    return  float(-eval_border)

def custom_score_7(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- do not need call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    
    eval_border = 0
    opponent = game.get_opponent(player)
    n1, n2 = n_moves(game, player), n_moves(game, opponent)
    s1, s2 = score_border(game, player), score_border(game, opponent) 
    if n1 != 0 and n2 != 0:
        eval_border = ((s1/n1) - (1.5*(s2/n2)))       
    return  float(-eval_border)


def custom_score_8(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- do not need call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    
    eval_border = 0
    opponent = game.get_opponent(player)
    n1, n2 = n_moves(game, player), n_moves(game, opponent)
    s1, s2 = score_border(game, player), score_border(game, opponent) 
    if n1 != 0 and n2 != 0:
        eval_border = (((s1/n1)**2) - ((s2/n2)**2))       
    return  float(-eval_border)

def custom_score_9(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- do not need call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    
    eval_border = 0
    opponent = game.get_opponent(player)
    n1, n2 = n_moves(game, player), n_moves(game, opponent)
    s1, s2 = score_border(game, player), score_border(game, opponent) 
    if n1 != 0 and n2 != 0:
        eval_border = (((s1/n1)**2) - (1.5*((s2/n2)**2)))       
    return  float(-eval_border)

def custom_score_10(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- do not need call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
         
    return  float(dist_cent(game, loc(game, player)))
                  
def custom_score_11(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- do not need call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    
    opponent = game.get_opponent(player)
    d1, d2 = dist_cent(game, loc(game, player)), dist_cent(game, loc(game, opponent))     
    return  float(d1 - d2)

def custom_score_12(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- do not need call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    
    opponent = game.get_opponent(player)
    d1, d2 = dist_cent(game, loc(game, player)), dist_cent(game, loc(game, opponent))     
    return  float(d1 - (1.5 * d2))

def custom_score_13(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- do not need call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    
    return float(dist_players(game, player))

def custom_score_14(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- do not need call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    
    d_p = dist_players(game, player)
    opponent = game.get_opponent(player)
    n1, n2 = n_moves(game, player), n_moves(game, opponent)
    
    return float(d_p * (n1 - n2))

def custom_score_15(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- do not need call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    
    d_p = dist_players(game, player)
    opponent = game.get_opponent(player)
    n1, n2 = n_moves(game, player), n_moves(game, opponent)
    return float(d_p * (n1 - (1.5*n2)))

def custom_score_16(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- do not need call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    
    d_p = dist_players(game, player)
    opponent = game.get_opponent(player)
    n1, n2 = n_moves(game, player), n_moves(game, opponent)
    return float(d_p * ((n1**2) - (n2**2)))

def custom_score_17(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- do not need call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    
    d_p = dist_players(game, player)
    opponent = game.get_opponent(player)
    n1, n2 = n_moves(game, player), n_moves(game, opponent)
    return float(d_p * ((n1**2) - (1.5*(n2**2))))
                 
class IsolationPlayer:
    """Base class for minimax and alphabeta agents.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
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
        
        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass

        # Return the best move from the last completed search iteration
        return best_move
    
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

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves
            
        """
        
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        return max(game.get_legal_moves(), 
                   key=lambda m: self.min_value(game.forecast_move(m), self.search_depth-1), default=(-1, -1))   


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning.
    """
    
    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout.
              
        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        depth, best_move = 3, (-1, -1)
        while True:
            try:
                # The try/except block will automatically catch the exception
                # raised when the timer is about to expire.             
                if not self.terminal_test(game):
#                         logging.debug('best_move = {}, fetching from lookup'.format(best_move))   
                    move = self.alphabeta(game, depth)
                    if move != (-1, -1):
                        best_move = move
#                         logging.debug('best_move = {}, adding to lookup'.format(best_move))
                    depth += 1
                    
                else:
#                     logging.debug('no legal moves available')
                    break                   
            except SearchTimeout:
#                 logging.warn('SearchTimeout: blank_spaces = {}, depth = {}, best move = {}'
#                              .format(len(game.get_blank_spaces()), depth, best_move))
                break
        # Return the best move from the last completed search iteration
        return best_move
    
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
            #logging.debug('min_value = {}'.format(self.min_value(game.forecast_move(a), depth-1, alpha, beta)))
            v = max(v, self.min_value(game.forecast_move(m), depth-1, alpha, beta))
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
            #logging.debug('max_value = {}'.format(self.max_value(game.forecast_move(a), depth-1, alpha, beta)))
            v = min(v, self.max_value(game.forecast_move(m), depth-1, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v   
    
    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Depth-limited minimax search algorithm with alpha-beta pruning.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves    
        """
        
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        best_move = (-1, -1)
        moves = game.get_legal_moves()
        op_moves = game.get_legal_moves(game.get_opponent(self))  
        game_hash = game.hash()
        
        if moves:
            if len(op_moves) == 1 and op_moves[0] in moves:
                transposition[game_hash] = op_moves[0]
                #logging.info('trapped. op_moves {} and moves {}'.format(op_moves, moves))
                return op_moves[0]  # trap opposite player
            best_move = moves[0]                 
            if game_hash in transposition.keys():
                best_move = transposition[game_hash]
                i = moves.index(best_move)
#                 logging.info('LOOK UP: depth = {}, best_move = {}, game_hash ={}'.format(depth, best_move, game_hash))
                moves[0], moves[i] = moves[i], moves[0]       
            v = float("-inf")
            for m in moves:     
                #logging.debug('min_value = {}'.format(self.min_value(game.forecast_move(a), depth-1, alpha, beta)))
                v_prime = self.min_value(game.forecast_move(m), depth-1, alpha, beta)
                if v < v_prime:
                    best_move = m
                    transposition[game_hash] = best_move
#                     logging.info('STORE VAL: depth = {}, best_move = {}, game_hash = {}'.format(depth, best_move, game_hash))
                    v = v_prime
                alpha = max(alpha, v)
    #           logging.debug ('game.get_legal_moves() = {}, depth = {}'.format(game.get_legal_moves(), depth))
        return best_move