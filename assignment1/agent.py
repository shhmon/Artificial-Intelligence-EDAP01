import random
import numpy as np
from math import inf
from copy import deepcopy
from itertools import groupby

# Counts max consequtive duplicate elements in array
def dup_count(seg):
  notZero = lambda x: 0 not in x
  groups = [list(group) for _, group in groupby(seg)]
  lengths = [len(x) for x in filter(notZero, groups)]
  return 0 if len(lengths) == 0 else max(lengths)

# Evaluates a sequence in the game
def evaluate(seq):
    total = len(seq)-3
    score = 0
    
    for i in range(total):
        seg = list(seq[i:i+4])
        pos = seg.count(1)
        neg = seg.count(-1)
        _max = dup_count(seg) # Max duplicates

        if pos and not neg:
          score += pos * _max + 1000 * int(pos == 4)
        elif neg and not pos:
          score -= neg * _max + 1000 * int(neg == 4)
          
    return score

# Static evaluation of a board
def static_eval(state):
  board = np.array(state)
  score = 0

  for r in range(6):
    seq = board[r, :]
    score += evaluate(seq)
  for c in range(7):
    seq = board[:, c]
    score += evaluate(seq)
  for d in range(-2, 4):
    seq = board.diagonal(d)
    score += evaluate(seq)
  for d in range(-2, 4):
    seq = np.fliplr(board).diagonal(d)
    score += evaluate(seq)
  
  return score

# Generate all possible chilren to current node
def next_states(state, val):
  states = {}
  for col in [3,2,4,1,5,0,6]:
    empty = [r for r in range(6) if not state[r][col]]

    if empty:
      nstate = deepcopy(state)
      nstate[max(empty)][col] = val
      states[col] = nstate

  return states

# Recursive minimax function inspired by Sebastian Lague
def minimax(state, depth, alpha=-inf, beta=inf, _max=True, move=-1):
  children = next_states(state, 1 if _max else -1)

  if depth == 0 or len(children) == 0:
    return static_eval(state), move

  bestEval = -inf if _max else inf
  for col, child in children.items():
    currEval = minimax(child, depth-1, alpha, beta, not _max)[0]
    if _max:
      alpha = max(alpha, currEval)
      if currEval > bestEval:
        bestEval = currEval
        move = col
    else:
      beta = min(beta, currEval)
      if currEval < bestEval:
        bestEval = currEval
        move = col
    if beta <= alpha:
      break

  return bestEval, move
