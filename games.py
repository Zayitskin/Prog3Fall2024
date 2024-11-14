# Would you rather have unlimited games but no bacon or games, unlimited games but no games?

import random

# RPS Code
import os
def rps(p1,p2):
  choices=["rock","gun","lightning","devil","dragon","water","air","paper","spounge","wolf","tree","human","snake","scissors","fire"]
  # choices=["r","g","l","d","dr","w","a","p","sp","wo","t","h","sn","s","f"]
  if p1 not in choices and p2 not in choices:
    return "Not a valid option"
  for chip in range(len(choices)):
    # print(p1,p2,chip,choices[chip])
    if p1==choices[chip]:
      p1=chip
    if p2==choices[chip]:
      p2=chip
  # print(p1,p2,(p1-p2),len(choices))
  if p1+1<len(choices)-1 and p2+1>len(choices)-((len(choices)-1)/2-p1):
    return "Player 1 wins"
  elif p2+1<len(choices)-1 and p1+1>len(choices)-((len(choices)-1)/2-p2):
    return "Player 2 wins"

  if p1==p2:
    return "Draw"
  elif p2-p1>=(len(choices)-1)/2:
    return "Player 2 wins"
  elif p1-p2>=(len(choices)-1)/2:
    return "Player 1 wins"

# p1=input("p1 choose somthing?")
# os.system("clear")
# p2=input("p2 choose another something?")
# print(f"Player 1 chose {p1}\n"+f"Player 2 chose {p2}\n"+str(rps(p1,p2)))
    
# TTT Code

# model the board



def is_win(layout):
    """Determines if there is a vertical, horizontal, or diagonal win"""
    r1, r2, r3 = layout[:3], layout[3:6], layout[6:]
    rows = [r1, r2, r3]
    print(rows)
    cols = list(zip(r1, r2, r3))
    print(cols)
    diags = [(r1[0], r2[1], r3[2]), (r1[2], r2[1], r3[0])]
    print(diags)
    for g in rows + cols + diags:
      if '_' not in g and len(set(g)) == 1:
        return True
    return False


def print_ttt(layout):
    """Pretty print the board"""
    layout = [x for x in layout]
    printed = ""
    for space in range(len(layout)):
      if layout[space] == "_":
        printed += str(space + 1)
      elif layout[space] in ["X", "O"]:
        printed += layout[space]
    print()
    for i in range(0, 9, 3):
      print(f'{printed[i]} | {printed[i+1]} | {printed[i+2]}')
      if i < len(printed) - 3:
        print('-' * 10)
    print()

def ttt(board, move, number):
  board = [x for x in board]
  if number%2 == 1:
    board[move - 1] = 'X'
  elif number%2 == 0:
    board[move - 1] = 'O'
  board2 = ""
  for x in board:
    board2 += x
  if is_win(board):
    return True, board2, number
  else:
    return False, board2, number

def connect(board, data, player):
  data = int(data.decode(encoding="UTF-8"))-1
  c = 5
  while True:
    if board[data + (c*7)] == "_":
      board[data + (c*7)] = str(player)
      break
    c -= 1
    if c == -4:
      return b"Enter a valid column"
  print(board)
  return board

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
  for l in input:
      vowels = ['a', 'e', 'i', 'o', 'u']
      i = random.randint(0, 1)
      if i == 0:
        if l in vowels:
          vowels.remove(l)
          l = random.choice(vowels)
        else:
          while True:
            l = chr(random.randint(97, 122))
            if l not in vowels:
              break
      output += l
  return output

def wdtv(mode, inp):
  output = ''
  inp = inp.lower()
  words = inp.split()
  if mode == 0:
    for w in words:
      output += anagram(w)
      output += ' '
    print('\n' * 100)
    print(output)
    wdtv(mode, input('guess: '))
  if mode == 1:
    for w in words:
      output += shift(w)
      output += ' '
    print('\n' * 100)
    print(output)
    wdtv(mode, input('guess: '))

#wdtv(int(input('type 0 for anagram mode or 1 for shift mode: ')), input('type a word or phrase: '))
