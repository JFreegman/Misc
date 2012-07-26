# Author: JFreegman@gmail.com
# Date: July 25, 2012

# This is the BUTT DESTROYER 9001, a rock paper scissors playing bot written for
# Udacity's CS212 rock paper scissors tournament.

# All code is written from scratch. The general idea is based off Iocaine Powder 
# by Dan Egnor (http://ofb.net/~egnor/iocaine.html).

# What this bot attempts to do is create a prediction heuristic based on
# frequency of the opponent's moves and patterns in their history. The bot will
# keep track of the performance of a number of strategies and meta-strategies 
# while playing the move that its current most successfull strategy comes up with.

import random

# Keeps history of each strategy's move for each round
STRAT_HISTORY = []

# Keeps track of the success rate of each strategy
STRAT_SUCCESS = {'freq20': 0, 'c1_freq20': 0, 'c2_freq20': 0, 'hist': 0, 'random': 0,
                 'c1_hist': 0, 'c2_hist': 0, 'c1_freq100': 0, 'c2_freq100': 0,
                 'freq100': 0, 'freqtot': 0, 'c1_freqtot': 0, 'c2_freqtot': 0}

# Keeps track of opponent move patterns
PATTERNS = {}

def player(my_moves, opp_moves):
    # first move is always random
    if not my_moves:
        STRAT_HISTORY.append({})
        return random_weapon()

    # update strategy success rates based on last round results
    last_opp_move = opp_moves[-1]
    beat_opp = winning_move(last_opp_move)
    lose_opp = losing_move(last_opp_move)
    last_strats = STRAT_HISTORY[-1]
    for s in last_strats:
        if last_strats[s] == beat_opp:
            STRAT_SUCCESS[s] += 1
        elif last_strats[s] == lose_opp:
            STRAT_SUCCESS[s] -= 1

    update_patterns(opp_moves, last_opp_move)

    # get opponent's most probable move based on frequency (last 20, 100 and
    # full history) and history pattern matches
    opp_freq20 = get_probs(opp_moves, 20)
    opp_prob_f_20 = max(opp_freq20, key=opp_freq20.get)
    opp_freq100 = get_probs(opp_moves, 100)
    opp_prob_f_100 = max(opp_freq100, key=opp_freq100.get)
    opp_freqtot = get_probs(opp_moves, len(opp_moves))
    opp_prob_f_tot = max(opp_freqtot, key=opp_freqtot.get)
    opp_prob_h = get_history_match(opp_moves)

    # naive moves for each strategy
    my_move_freq20 = winning_move(opp_prob_f_20)
    my_move_freq100 = winning_move(opp_prob_f_100)
    my_move_freqtot = winning_move(opp_prob_f_tot)
    my_move_hist = winning_move(opp_prob_h)
    random_move = random_weapon()

    # counter-moves in case opp predicts my naive moves
    c1_move_freq20 = losing_move(my_move_freq20)
    c1_move_freq100 = losing_move(my_move_freq100)
    c1_move_freqtot = losing_move(my_move_freqtot)
    c1_move_hist = losing_move(my_move_hist)

    # counter-counter moves in case opp predicts my first counter
    c2_move_freq20 = losing_move(c1_move_freq20)
    c2_move_freq100 = losing_move(c1_move_freq100)
    c2_move_freqtot = losing_move(c1_move_freqtot)    
    c2_move_hist = losing_move(c1_move_hist)

    # dict of all available strategies and their move
    strats = {'freq20': my_move_freq20, 'freq100': my_move_freq100, 
              'hist': my_move_hist, 'random': random_move,
              'c1_freq20': c1_move_freq20, 'c2_freq20': c2_move_freq20, 
              'c1_freq100': c1_move_freq100, 'c2_freq100': c2_move_freq100, 
              'c1_hist': c1_move_hist, 'c2_hist': c2_move_hist,
              'freqtot': my_move_freqtot, 'c1_freqtot': c1_move_freqtot,
              'c2_freqtot': c2_move_freqtot}

    # Pick the strategy with the highest current success rate
    strat = max(strats, key=lambda x: STRAT_SUCCESS[x])
    move = strats[strat]
    STRAT_HISTORY.append(strats)
    return move

def update_patterns(hist, last_move):
    """
    updates pattern history with all possible new sequences 
    based on last 20 moves
    """
    k = len(hist)
    t_hist = tuple(hist)
    PATTERNS[t_hist[-20:-1]] = last_move
    for i in xrange(k-20, k+1):
        t = t_hist[i:-1]
        if t not in PATTERNS:
            PATTERNS[t] = last_move
    return None

def get_history_match(moves):
    """
    Searches moves history and tries to find previous patterns that match
    the last n moves (n starting at half the number of moves and decrementing).
    If match found, returns the move made after the last pattern match.
    """
    start = len(moves) / 2
    end = start * 2 + 1
    for i in xrange(start, end):
        if tuple(moves[i:]) in PATTERNS:
            return PATTERNS[tuple(moves[i:])]
    return random_weapon()

def get_probs(total_moves, n):
    """
    Returns a dictionary containing the probabilities that the opponent
    will make a given move based on their last n moves.
    """
    last = get_move_freq(total_moves[-n:])
    probs = {}
    probs['rock'] = float(last['rock']) / last['total'] * 100
    probs['scissors'] = float(last['scissors']) / last['total'] * 100
    probs['paper'] = float(last['paper']) / last['total'] * 100
    return probs

def get_move_freq(moves):
    """
    Returns a dictionary containing frequencies of moves, as well as
    a count for the total number of moves
    """
    mov_freq = {'rock': 0, 'paper': 0, 'scissors': 0}
    count = 0
    for move in moves:
        if move == 'rock':
            mov_freq['rock'] += 1
        elif move == 'paper':
            mov_freq['paper'] += 1
        elif move == 'scissors':
            mov_freq['scissors'] += 1
        else:
            raise ValueError, 'Invalid move'
        count += 1
    mov_freq['total'] = count
    return mov_freq

def winning_move(m):
    "Returns the move that beats m"
    d = {'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock'}
    return d[m]
    raise ValueError, 'Invalid move'

def losing_move(m):
    "Returns the move that loses to m"
    d = {'rock': 'scissors', 'paper': 'rock', 'scissors': 'paper'}
    return d[m]
    raise ValueError, 'Invalid move'

def random_weapon():
    "Randomly chooses rock, paper or scissors"
    moves = ['rock', 'paper', 'scissors']
    return random.choice(moves)
