import random
import numpy as np
from agent import *

"""
This file contains some messy quickly written code to play the agent
Run playagent.py to face your inevitable doom
"""

def game_end(board):
  full = not 0 in [e for arr in board for e in arr]
  board = np.array(board)

  for r in range(6):
    seq = board[r, :]
    if dup_count(seq) is 4 and list(seq).count(0) < 4: return True
  for c in range(7):
    seq = board[:, c]
    if dup_count(seq) is 4 and list(seq).count(0) < 4: return True
  for d in range(-2, 4):
    seq = board.diagonal(d)
    if dup_count(seq) is 4 and list(seq).count(0) < 4: return True
  for d in range(-2, 4):
    seq = np.fliplr(board).diagonal(d)
    if dup_count(seq) is 4 and list(seq).count(0) < 4: return True

  
  return full

def print_board(board):
  print("0 1 2 3 4 5 6")
  print("-------------")
  for row in board:
    r = ""
    for e in row:
      r += ("X" if e is -1 else str(e)) + " "
    print(r)
  print("")

if __name__ == "__main__":
  board = [[0] * 7 for i in range(6)]
  yourturn = random.choice([True, False])

  print("Game has begun. " + ("You start!" if yourturn else "Bot Starts!") + "\n")
  print_board(board)

  while not game_end(board):
    if yourturn:
      print("Make a move (0-6):", end =" ")
      move = int(input())
      print()
    else:
      move = minimax(board, 4)[1]

    row = -1
    while row < 5 and board[row+1][move] == 0:
      row += 1
    if row != -1:
      board[row][move] = 1 if yourturn else -1
      if not yourturn: print_board(board)
      yourturn = not yourturn
    else:
      print("Illegal move, try again")
  
  print("Game Over!")