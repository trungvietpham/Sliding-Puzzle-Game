
def node_manhattan(board,n):
  sum = 0
  n = len(board)
  for i in range(n):
    for j in range(n):
      x = int((board[i][j] - 1)/n) # row number
      y = int((board[i][j] - 1) % n) # col num
      if board[i][j] == 0:
        continue
      sum += abs(x-i) + abs(y - j)
      # changed return to 0 for BFS, sum for A*
  return sum

def manhattan(board, goal_nums,n):
  sum = 0
  count = 0
  for i in range(n):
    for j in range(n):
      if board[i][j] in goal_nums:
        x = int((board[i][j] - 1)/n) # row number
        y = int((board[i][j] - 1) % n) # col num
        sum += abs(x-i) + abs(y - j)
  return sum
