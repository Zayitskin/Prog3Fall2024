# Would you rather have unlimited games but no bacon or games, unlimited games but no games?

import random

# RPS Code
def rps(p1,p2):
  if p1=="rock":
    if p2=="rock":
      return "draw"
    elif p2=="paper":
      return "Player 2 wins"
    elif p2=="scissors":
      return "Player 1 wins"
  elif p1=="paper":
    if p2=="rock":
      return "Player 1 wins"
    elif p2=="paper":
      return "draw"
    elif p2=="scissors":
      return "Player 1 wins"
  elif p1=="scissors":
    if p2=="rock":
      return "Player 2 wins"
    elif p2=="paper":
      return "Player 1 wins"
    elif p2=="scissors":
      return "draw"
    
# TTT Code

# model the board



def is_win(layout):
    """Determines if there is a vertical, horizontal, or diagonal win"""
    r1, r2, r3 = layout[:3], layout[3:6], layout[6:]
    rows = [r1, r2, r3]
    cols = list(zip(r1, r2, r3))
    diags = [(r1[0], r2[1], r3[2]), (r1[2], r2[1], r3[0])]
    for g in rows + cols + diags:
      if '_' not in g and len(set(g)) == 1:
        return True
    return False


def print_ttt(layout):
    """Pretty print the board"""
    printed = ""
    for space in range(len(layout)):
      if layout[space] == "_":
        printed += str(space + 1)
      else:
        printed += layout[space]
    print()
    for i in range(0, 9, 3):
      print(f'{printed[i]} | {printed[i+1]} | {printed[i+2]}')
      if i < len(printed) - 3:
        print('-' * 10)
    print()

def ttt(board, move, number):
  if number%2 == 1:
    board[move - 1] = 'X'
  elif number%2 == 0:
    board[move - 1] = 'O'
    if is_win(board):
      return True, board, number
    else:
      return False, board, number


    
# C4 Code
def connect():
  pass 
