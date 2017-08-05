from isolation.isolation import Board
__author__ = "Jacob Ider Chitham"
__credits__ = ["Udacity"]
__version__ = "1.0.0-alpha"
__maintainer__ = "Jacob Ider Chitham"
__email__ = "jacobic@hotmail.co.uk"
__status__ = "In Progress"

#  Note: this function should be called from within a Player instance as
#     `self.score()` -- you should not need to call this function directly.

# My apologies. The AIMA textbook talks about some other strategies (like “killer
# heuristic”, transposition tables, and dynamic move ordering), and there are a
# number of other tricks and optimizations that have been developed for other 
# games (like chess or checkers) that might be applicable to Isolation.


"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""

import random
# import logging
# 
# log_file = 'debug.log'
# log_format = '%(asctime)s - %(levelname)s - %(message)s'
# log_level = logging.DEBUG
# logging.basicConfig(filename=log_file,level=log_level,format=log_format)
# logging.FileHandler(filename=log_file, mode='w')

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

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
    # TODO: finish this function!
    
    # delta player distances to center, penalize peripheral positions, adjust move 
    # heuristics etc. got me to 77%  in one run. these are purely context free 
    # heuristic. if we add look ahead moves etc we can improve it further.
    # @barni if you look ahead in moves for heuristics that's equivalent of doing a recursive search inside a recursive. imo unnecessary to finish this project, but to each his own. a more efficient way is running some simple policy mapping similar to the case in q learning, by running tons of games, run some statistics, and derive weights to to each cell as a function of the number of move played.
    # Han Lee 
    # @barni aka supervised learning a policy network, put that down as your 
    # heuristics function. effectively turning a simple search into reinforcement 
    # learning search w/o policy gradients
    
    w, h = game.width / 2., game.height / 2.
    x1, y1 = game.get_player_location(player)
    x2, y2 = game.get_player_location(game.get_opponent(player))  
    return float(((w - x1)**2 + (h - y1)**2) - ((w - x2)**2 + (h - y2)**2))


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

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
    # TODO: finish this function!
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return own_moves - opp_moves


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

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
    # TODO: finish this function!
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return own_moves - opp_moves


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

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
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

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
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move
    
    def terminal_test(self, game):
        """ Return True if the game is over for the active player
        and False otherwise.
        """
    
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        return not bool(game.get_legal_moves())
    
    def max_value(self, game, depth):
        """ Return the utility of the current game state from the perspective
        of the specified player if the game is over, otherwise return the 
        maximum value over all legal child nodes.
        """
        
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if self.terminal_test(game) or depth == 0:     
            return self.score(game, game._player_1)
        v = float("-inf")
        for a in game.get_legal_moves():
            v = max(v, self.min_value(game.forecast_move(a), depth-1))
        return v
    
    def min_value(self, game, depth):
        """ Return the utility of the current game state from the perspective
        of the specified player if the game is over, otherwise return the 
        minimum value over all legal child nodes.
        """
        
        if self.time_left() < self.TIMER_THRESHOLD:
            return self.score(game, game._player_1)
            raise SearchTimeout()
        if self.terminal_test(game) or depth == 0:     
            return self.score(game, game._player_1)
        v = float("inf")
        for a in game.get_legal_moves():
            v = min(v, self.max_value(game.forecast_move(a), depth-1))
        return v   
    
    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

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

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        #print(game.to_string())
        # TODO: finish this function!
        return max(game.get_legal_moves(), 
                   key=lambda m: self.min_value(game.forecast_move(m), self.search_depth), default=(0,0))   


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """
    
    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

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
        board_look_up = {}
        while True:
            try:
                # The try/except block will automatically catch the exception
                # raised when the timer is about to expire.
                
                if not self.terminal_test(game):
#                     if game in board_look_up.keys():
#                         best_move = board_look_up[game]
#                         logging.debug('best_move = {}, fetching from lookup'.format(best_move))   
#                     else:
                
                    move = self.alphabeta(game, depth)
                    if move != (-1, -1):
                        best_move = move
                        board_look_up[game] = best_move
#                         logging.debug('best_move = {}, adding to lookup'.format(best_move))
                    depth += 1
                    
                else:
#                     logging.debug('no legal moves available')
                    break                   
            except SearchTimeout:
                # Handle any actions required after timeout as needed
#                 logging.warn('SearchTimeout: blank_spaces = {}, depth = {}, best move = {}'
#                              .format(len(game.get_blank_spaces()), depth, best_move))
                break
        # Return the best move from the last completed search iteration
        return best_move
    
    def terminal_test(self, game):
        """ Return True if the game is over for the active player
        and False otherwise.
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
            return self.score(game, game._player_1)

        v = float("-inf")
        for a in game.get_legal_moves():
            #logging.debug('min_value = {}'.format(self.min_value(game.forecast_move(a), depth-1, alpha, beta)))
            v = max(v, self.min_value(game.forecast_move(a), depth-1, alpha, beta))
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
            winner = (game.is_winner(game._player_1), game.is_winner(game._player_2))
#             logging.warn('terminal_test = {}, winner(p1,p2) = {}, score = {}, depth = {}, '
#                          .format(self.terminal_test(game), winner, self.score(game, game._player_1), depth))     
            return self.score(game, game._player_1)
        v = float("inf")
        for a in game.get_legal_moves():
            #logging.debug('max_value = {}'.format(self.max_value(game.forecast_move(a), depth-1, alpha, beta)))
            v = min(v, self.max_value(game.forecast_move(a), depth-1, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v   
    
    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

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

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        # TODO: finish this function!
#         logging.debug ('game.get_legal_moves() = {}, depth = {}'.format(game.get_legal_moves(), depth))
        return max(game.get_legal_moves(), 
                   key=lambda m: self.min_value(game.forecast_move(m), depth, alpha, beta), default=(-1,-1))   

