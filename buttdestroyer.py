# -----------------------------------------------------------------------------------
#
# Author: JFreegman
# Contact: JFreegman@gmail.com
# Date: July 30, 2012
# v3.1
# 
# This is a rock-paper-scissors playing bot originally written for the Udacity CS212
# RPS contest and adapted for tournament play at rpscontest.com
#
# See: http://www.rpscontest.com/authorSearch?name=JFreegman
# 
# All code is written from scratch. The general idea is based off Iocaine Powder 
# by Dan Egnor -- http://ofb.net/~egnor/iocaine.html
#
# -----------------------------------------------------------------------------------

import random

def get_history_match(hist, n=15, s=False):
    start = len(hist) - min(len(hist) / 2, n)
    end = len(hist)
    for i in xrange(start, end):
        partition = hist[i:end]
        match = hist[:-1].rfind(partition)
        if match != -1:
            return hist[match+len(partition)]
    if not s:
        return random_weapon()
    return None

def get_probs(total_moves, n):
    last = get_move_freq(total_moves[-n:])
    probs = {}
    t = last['total']
    probs['R'] = float(last['R']) / t
    probs['S'] = float(last['S']) / t
    probs['P'] = float(last['P']) / t
    return probs

def get_move_freq(moves):
    mov_freq = {'R': 0, 'P': 0, 'S': 0}
    count = 0
    for move in moves:
        if move == 'R':
            mov_freq['R'] += 1
        elif move == 'P':
            mov_freq['P'] += 1
        elif move == 'S':
            mov_freq['S'] += 1
        else:
            raise ValueError, 'Invalid move'
        count += 1
    mov_freq['total'] = count
    return mov_freq

def random_weapon():
    return random.choice(['R', 'P', 'S'])

# Initialize everything on the first move
if not input:
    last_strats = {}

    winning_move = {'R': 'P', 'P': 'S', 'S': 'R'}

    losing_move = {'R': 'S', 'P': 'R', 'S': 'P'}

    plays = {'RR': 'W', 'RP': 'G', 'RS': 'E', 'PP': 'Q', 'PR': 'L', 
             'PS': 'B', 'SS': 'C', 'SR': 'A', 'SP': 'J'}

    opposite_plays = {'W': 'RR', 'G': 'RP', 'E': 'RS', 'Q': 'PP', 'L': 'PR',
                      'B': 'PS', 'C': 'SS', 'A': 'SR', 'J': 'SP'}

    strat_success = {'freq20': 0,'hist': 0, 'random': 0, 'freq100': 0, 
                     'my_hist': 0, 'c_my_seq': 0, 'c1_my_seq': 0,
                     'c_my_move_my_hist': 0, 'c1_my_move_my_hist': 0,
                     'opp_seq': 0, 'my_seq': 0, 'c_opp_seq': 0, 'c1_opp_seq': 0,
                     }
    output = random_weapon()
    opp_moves = ""
    sequences = ""
    my_moves = output

else:
    opp_moves += input
    last_opp_move = input
    sequences += plays[input+output]
    beat_opp = winning_move[last_opp_move]
    lose_opp = losing_move[last_opp_move]
    # update strategy success rates based on last round results
    for s in last_strats:
        if last_strats[s] == beat_opp:
            strat_success[s] += 1
        elif last_strats[s] == lose_opp:
            strat_success[s] -= 1

    # opponent's most probable move based on frequency and historic patterns
    opp_freq20 = get_probs(opp_moves, 20)
    opp_prob_f_20 = max(opp_freq20, key=opp_freq20.get)
    opp_freq100 = get_probs(opp_moves, 100)
    opp_prob_f_100 = max(opp_freq100, key=opp_freq100.get)
    opp_prob_h = get_history_match(opp_moves)

    # my most probable move based on history
    my_prob_h = get_history_match(my_moves)

    # moves for each strategy
    my_move_freq20 = winning_move[opp_prob_f_20]
    my_move_freq100 = winning_move[opp_prob_f_100]
    my_move_hist = winning_move[opp_prob_h]
    my_move_my_hist = losing_move[my_prob_h]
    c_my_move_my_hist = losing_move[my_move_my_hist]
    c1_my_move_my_hist = losing_move[c_my_move_my_hist]
    random_move = random_weapon()

    strats = {'freq20': my_move_freq20, 'freq100': my_move_freq100, 
              'hist': my_move_hist, 'random': random_move,
              'c1_my_move_my_hist': c1_my_move_my_hist, 'my_hist': my_move_my_hist,
              'c_my_move_my_hist': c_my_move_my_hist,
              }

    # most probable moves based on sequence pattern matches
    seq_match = get_history_match(sequences, s=True)
    if seq_match:
        opp_prob_seq = winning_move[opposite_plays[seq_match][0]]
        my_prob_seq = losing_move[opposite_plays[seq_match][1]]
        strats['opp_seq'] = opp_prob_seq
        strats['c_opp_seq'] = losing_move[opp_prob_seq]
        strats['c1_opp_seq'] = winning_move[opp_prob_seq]
        strats['my_seq'] = my_prob_seq
        strats['c_my_seq'] = losing_move[my_prob_seq]
        strats['c1_my_seq'] = winning_move[my_prob_seq]
        
    # Pick the strategy with the highest current success rate
    strat = max(strats, key=lambda x: strat_success[x])
    output = strats[strat]
    if random.random() <= .1:
        output = random_weapon()
    my_moves += output
    last_strats = strats