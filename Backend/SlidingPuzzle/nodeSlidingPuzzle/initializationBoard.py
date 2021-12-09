import random  # RAMDOM trang thai bai dau

def create_random_board(n, solvable=True):  # tao bảng random
    board = [[0 for i in range(n)] for j in range(n)]
    s = list(set([i for i in range(n * n)]))
    for i in range(n):
        for j in range(n):
            item = random.sample(s, 1)
            board[i][j] = item[0]
            s.remove(item[0])
    if solvable:
        if not isSolvable(board,n):
            if board[2][1] != 0 and board[2][2] != 0:
                temp = board[2][1]
                board[2][1] = board[2][2]
                board[2][2] = temp
            else:
                temp = board[0][0]
                board[0][0] = board[0][1]
                board[0][1] = temp
    return board

def isSolvable(board,n):
  lst = []
  blank_on_even = False
  for i in range(n):
    for j in range(n):
      if board[i][j] != 0:
        lst.append(board[i][j])
      else:
        if i % 2 == 0:
          blank_on_even = True
  inversions = 0

  for i in range(len(lst)):
    for j in range(i + 1, len(lst)):
      if lst[i] > lst[j]:
        inversions += 1

  if n % 2 == 1:
    if inversions % 2 == 1:
      return False
    else:
      return True
  if (inversions % 2 == 0 and blank_on_even) or (inversions % 2 == 1 and not blank_on_even):
    return False

  return True