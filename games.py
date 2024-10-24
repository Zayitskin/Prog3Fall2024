# Would you rather have unlimited games but no bacon or games, unlimited games but no games?
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
def ttt():
  # games AI
# model the board

  LAYOUT =  '_' * 9

  def get_next_states(layout, val):
    """Returns all possible next game states"""
    if val == 1:
      piece = "x"
    else:
      piece = "o"
    return [layout[:i] + piece + layout[i+1:] for i,p in enumerate(layout) if p == '_']


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


  def print_board(layout):
    """Pretty print the board"""
    print()
    for i in range(0, 9, 3):
      print(f'{layout[i]} | {layout[i+1]} | {layout[i+2]}')
      if i < len(layout) - 3:
        print('-' * 10)
    print()


  def score_state(layout, val):
    """Scores an endgame state as a win, loss, or draw"""
    if is_win(layout):
      return val
    elif '_' not in layout:
      return 0
    else:
      return minimax(layout, -val, root=False)


  def minimax(layout, val, root=True):
    """Recursive minimax scoring algorithm"""
    states = get_next_states(layout, val)
    scores = {state:0 for state in states}
    for state in states:
      scores[state] += score_state(state, val)
    if root:
      return max(scores.keys(), key=lambda x: scores[x])
    elif val == 1:
      return max(scores.values())
    else:
      return min(scores.values())

  def test():
    assert minimax('__o_o___x', 1) == '__o_o_x_x'
    assert get_next_states('xooxxo___', 1) == ['xooxxox__', 'xooxxo_x_', 'xooxxo__x']
    assert not is_win('_________')
    assert is_win('___xxx___')
    assert is_win('_x__x__x_')
    assert is_win('x___x___x')
    assert is_win('__x_x_x__')
    print('all tests passed')

  test()

  print('\n 1 | 2 | 3 \n-----------\n 4 | 5 | 6 \n-----------\n 7 | 8 | 9\n')
  state = '_________'

  while True:
    state = minimax(state, 1)
    print_board(state)
    if is_win(state):
      print('Computer wins :(\n')
      break
    elif '_' not in state:
      print('It\'s a tie :|\n')
      break
    while True:
      move = input('Your move: ')
      if move.isdigit() and len(move) == 1 and move != '0':
        break
    state = state[:int(move) - 1] + 'o' + state[int(move):]
    if is_win(state):
      print('You win :)\n')
      break

# C4 Code
def connect():
  pass

# Whisper Down the Valley
def wdtv():
  pass