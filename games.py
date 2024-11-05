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

def connect(board, data, player):
  board.reverse()
  new_board = [[],[],[],[],[]]
  for i in range(len(board[0])):
    for c in board:
      new_board[i].append(c[i])
  board = new_board
  print(board, new_board)
  data = int(data.decode(encoding="UTF-8"))-1
  column = board[data]
  for space in range(len(column)):
    if column[space] == "_":
      column[space] = player
      break
  print(board)
  new_board = [[],[],[],[],[]]
  for i in range(len(board[0])):
    for c in board:
      new_board[i].append(c[i])
  new_board.reverse()
  return new_board

# Whisper Down the Valley
def anagram(input):
  output = ''
  for _ in range(0, len(input)):
    i = random.randint(0, len(input) - 1)
    output += input[i]
    input = input[:i] + input[i+1:]
  return output

def shift(input):
  output = ''
  for _ in range(0, len(input)):
      i = random.randint(0, len(input) - 1)
      output = output[:i] + chr(random.randint(97, 122)) + output[i+1:]
  return output

def wdtv(input, mode):
  output = []
  input = input.lower()
  words = input.split()
  if mode == 0:
    for w in words:
      output.append(anagram(w))
  if mode == 1:
    for w in words:
      output.append(shift(w))
  return output

#print(wdtv('long ago, the four nations lived together in harmony. then, everything changed when the fire nation attacked. only the avatar, master of all four elements could stop them, but when the world needed him most, he vanished. one hundred years passed, and my brother and i found the new avatar, an airbender named aang. and although his airbending skills are great, he has a lot to learn before he can save anyone. but i believe, aang can save the world.', 0))
#print(wdtv('long ago, the four nations lived together in harmony. then, everything changed when the fire nation attacked. only the avatar, master of all four elements could stop them, but when the world needed him most, he vanished. one hundred years passed, and my brother and i found the new avatar, an airbender named aang. and although his airbending skills are great, he has a lot to learn before he can save anyone. but i believe, aang can save the world.', 1))