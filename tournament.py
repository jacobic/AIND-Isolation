"""Estimate the strength rating of a student defined heuristic by competing
against fixed-depth minimax and alpha-beta search agents in a round-robin
tournament.

NOTE: All agents are constructed from the student CustomPlayer implementation,
so any errors present in that class will affect the outcome.

The student agent plays a number of "fair" matches against each test agent.
The matches are fair because the board is initialized randomly for both
players, and the     players play each match twice -- once as the first player and
once as the second player.  Randomizing the openings and switching the player
order corrects for imbalances due to both starting position and initiative.
"""
import itertools
import random
import warnings
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from collections import namedtuple

from isolation import Board
from sample_players import (RandomPlayer, open_move_score,
                            improved_score, center_score)
from game_agent import (MinimaxPlayer, AlphaBetaPlayer, custom_score,
                        custom_score_2, custom_score_3, custom_score_4, 
                        custom_score_5, custom_score_6, custom_score_7, 
                        custom_score_8, custom_score_9, custom_score_10,
                        custom_score_11, custom_score_12,custom_score_13)

NUM_MATCHES = 20  # number of matches against each opponent (default = 5)
TIME_LIMIT = 150  # number of milliseconds before timeout

DESCRIPTION = """
This script evaluates the performance of the custom_score evaluation
function against a baseline agent using alpha-beta search and iterative
deepening (ID) called `AB_Improved`. The three `AB_Custom` agents use
ID and alpha-beta search with the custom_score functions defined in
game_agent.py.
"""

Agent = namedtuple("Agent", ["player", "name"])

def play_round(cpu_agent, test_agents, win_counts, num_matches):
    """Compare the test agents to the cpu agent in "fair" matches.

    "Fair" matches use random starting locations and force the agents to
    play as both first and second player to control for advantages resulting
    from choosing better opening moves or having first initiative to move.
    """
    timeout_count = 0
    forfeit_count = 0
    for _ in range(num_matches):

        games = sum([[Board(cpu_agent.player, agent.player),
                      Board(agent.player, cpu_agent.player)]
                    for agent in test_agents], [])

        # initialize all games with a random move and response
        for _ in range(2):
            move = random.choice(games[0].get_legal_moves())
            for game in games:
                game.apply_move(move)

        # play all games and tally the results
        for game in games:
            winner, _, termination = game.play(time_limit=TIME_LIMIT)
            win_counts[winner] += 1

            if termination == "timeout":
                timeout_count += 1
            elif termination == "forfeit":
                forfeit_count += 1

    return timeout_count, forfeit_count


def update(total_wins, wins):
    for player in total_wins:
        total_wins[player] += wins[player]
    return total_wins


def play_matches(cpu_agents, test_agents, num_matches):
    """Play matches between the test agent and each cpu_agent individually. """
    total_wins = {agent.player: 0 for agent in test_agents}
    total_timeouts = 0.
    total_forfeits = 0.
    total_matches = 2 * num_matches * len(cpu_agents)

    print("\n{:^9}{:^13}".format("#", "Opp") + ''.join(['{:^5}'.format(x[1].name) for x in enumerate(test_agents)]))
    #print("{:^9}{:^13} ".format("", "") +  ' '.join(['{:^5}| {:^5}'.format("Won", "Lost") for x in enumerate(test_agents)]))
    cols = [x[1].name for x in enumerate(test_agents)]
    idxs = [x[1].name for x in enumerate(cpu_agents)]
    df = pd.DataFrame(index=idxs, columns=cols)
    df = df.append(pd.DataFrame(index=['AVG'], columns=cols))

    for idx, agent in enumerate(cpu_agents):
        wins = {key: 0 for (key, value) in test_agents}
        wins[agent.player] = 0

        print("{!s:^9}{:^13}".format(idx + 1, agent.name), end="", flush=True)

        counts = play_round(agent, test_agents, wins, num_matches)
        total_timeouts += counts[0]
        total_forfeits += counts[1]
        total_wins = update(total_wins, wins)
        _total = 2 * num_matches
        round_totals = sum([[wins[agent.player], _total - wins[agent.player]]
                            for agent in test_agents], [])
        
        for i in range(0, len(round_totals), 2):
            win_frac = (round_totals[i] / (round_totals[i] + round_totals[i+1]))
            df[cols[int(i/2)]][agent[1]] = win_frac
            print(' {:.2f}'.format(win_frac), end='')
        print('')

    win_rates = []
    for x in enumerate(test_agents):
        win_rates.append(total_wins[x[1].player] / total_matches)
        
    print("-" * 74)    
    print('{:^9}{:^13}'.format("", "Win Rate:") +
        ''.join([
            '{:^5}'.format(
                "{:.2f}".format(wr)
            ) for wr in win_rates
    ]))

    if total_timeouts:
        print(("\nThere were {} timeouts during the tournament -- make sure " +
               "your agent handles search timeout correctly, and consider " +
               "increasing the timeout margin for your agent.\n").format(
            total_timeouts))
    if total_forfeits:
        print(("\nYour ID search forfeited {} games while there were still " +
               "legal moves available to play.\n").format(total_forfeits))

    df.loc['AVG'] = win_rates
    df = df[df.columns].astype(float)
    df.to_csv('/Users/jacobic/ai-nanodegree/t1/AIND-Isolation/heuristic_data.csv')
    return df.T

def main():

    # Define two agents to compare -- these agents will play from the same
    # starting position against the same adversaries in the tournament
    test_agents = [
        Agent(AlphaBetaPlayer(score_fn=improved_score), "ABIM"),
        Agent(AlphaBetaPlayer(score_fn=custom_score), "AB01"),
        Agent(AlphaBetaPlayer(score_fn=custom_score_2), "AB02"),
        Agent(AlphaBetaPlayer(score_fn=custom_score_3), "AB03"),
        Agent(AlphaBetaPlayer(score_fn=custom_score_4), "AB04"),
        Agent(AlphaBetaPlayer(score_fn=custom_score_5), "AB05"),
        Agent(AlphaBetaPlayer(score_fn=custom_score_6), "AB06"),
        Agent(AlphaBetaPlayer(score_fn=custom_score_7), "AB07"),
        Agent(AlphaBetaPlayer(score_fn=custom_score_8), "AB08"),
        Agent(AlphaBetaPlayer(score_fn=custom_score_9), "AB09"),
        Agent(AlphaBetaPlayer(score_fn=custom_score_10), "AB10"),
        Agent(AlphaBetaPlayer(score_fn=custom_score_11), "AB11"),
        Agent(AlphaBetaPlayer(score_fn=custom_score_12), "AB12"),
        Agent(AlphaBetaPlayer(score_fn=custom_score_13), "AB13")
    ]

    # Define a collection of agents to compete against the test agents
    cpu_agents = [
        Agent(RandomPlayer(),"RAN"),
        Agent(MinimaxPlayer(score_fn=open_move_score), "MMO"),
        Agent(MinimaxPlayer(score_fn=center_score), "MMC"),
        Agent(MinimaxPlayer(score_fn=improved_score), "MMI"),
        Agent(AlphaBetaPlayer(score_fn=open_move_score), "ABO"),
        Agent(AlphaBetaPlayer(score_fn=center_score), "ABC"),
        Agent(AlphaBetaPlayer(score_fn=improved_score), "ABIM")
    ]

    print(DESCRIPTION)
    print("{:^74}".format("**************************************************"))
#     print("{:^74}".format("Playing Matches"))
    title = "{} {} {}".format("Playing", (2*NUM_MATCHES), "Matches" )
    print("{:^74}".format(title))
    print("{:^74}".format("**************************************************"))
    results = play_matches(cpu_agents, test_agents, NUM_MATCHES)
    sns.heatmap(results, annot=True, fmt='.2f', sqauare=True, cmap="YlGnBu", 
                cbar_kws={'label': 'Win-rate'})
    plt.title('Heuristic Evaluation Function Analysis - {} Games'
              .format((2*NUM_MATCHES)))
    plt.ylabel('Test Agents')
    plt.xlabel('CPU Agents')
    plt.savefig('/Users/jacobic/ai-nanodegree/t1/AIND-Isolation/heuristic_plot.png')
    plt.show()

if __name__ == "__main__":
    main()
