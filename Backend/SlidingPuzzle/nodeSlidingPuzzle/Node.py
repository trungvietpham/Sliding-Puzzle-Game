import sys
sys.path.append("..")
from nodeSlidingPuzzle import heuristic
class Node:
  def __init__(self, board, previous, heuristic, depth, direction,n):
    self.board = board
    self.previous = previous
    self.heuristic = heuristic
    self.depth = depth
    self.direction = direction
    self.n=n

  def __lt__(self, other):  # dùng để so sánh trong heap
    return True

  # phát sinh nút con của nút đang sét trường hợp dùng heuristic(A* và human)
  def generate_children(self):
    for i in range(self.n):
      for j in range(self.n):
        if self.board[i][j] == 0:
          x, y = i, j  # Tìm vị trí x,y đang chứa điểm 0
    # các cách di chuyển,(nhận thấy nên ưu tiên theo thứ tự(xuống,trái,phải,lên)
    val_list = [[x + 1, y, "DOWN"], [x, y - 1, "LEFT"],
                [x, y + 1, "RIGHT"], [x - 1, y, "UP"]]
    children = []
    for child in val_list:
      # ở biên thì loại bỏ một số trường hợp
      if child[0] >= 0 and child[0] < self.n and child[1] >= 0 and child[1] < self.n:
        child_board = [row[:] for row in self.board]
        child_board[x][y] = child_board[child[0]][child[1]]
        child_board[child[0]][child[1]] = 0
        child_node = Node(child_board, self, heuristic.node_manhattan(child_board, self.n), self.depth + 1, child[2], self.n)
        children.append(child_node)
    return children

  # phát sinh nút con của nút đang sét trường dùng bfs(heuristic=0)
  def generate_children_non_heuristic(self):
    x, y = 0, 0
    for i in range(self.n):
      for j in range(self.n):
        if self.board[i][j] == 0:
          x, y = i, j
    # bfs thì đi hướng nào cx không có nhiều khác biệt như human
    val_list = [[x + 1, y, "DOWN"], [x, y - 1, "LEFT"], [x, y + 1, "RIGHT"], [x - 1, y, "UP"]]
    children = []
    for child in val_list:
      if child[0] >= 0 and child[0] < self.n and child[1] >= 0 and child[1] < self.n:
        child_board = [row[:] for row in self.board]
        child_board[x][y] = child_board[child[0]][child[1]]
        child_board[child[0]][child[1]] = 0
        child_node = Node(child_board, self, 0,
                          self.depth + 1, child[2],self.n)  # heuristic=0
        children.append(child_node)
    return children

  def generate_children_intentionally(self, command):
    for i in range(self.n):
      for j in range(self.n):
        if self.board[i][j] == 0:
          x, y = i, j
    if command == "UP":
      a, b = x - 1, y
    elif command == "DOWN":
      a, b = x + 1, y
    elif command == "LEFT":
      a, b = x, y - 1
    elif command == "RIGHT":
      a, b = x, y + 1
    # if a>=0 and a<n and b>=0 and b>n:
    # print("Xet ",a,"---",b)
    child_board = [row[:] for row in self.board]
    child_board[x][y] = child_board[a][b]
    child_board[a][b] = 0
    child_node = Node(child_board, self, 0, self.depth + 1, command,self.n)
    # print("=======")
    # print(command)
    # plain_print(child_board)
    # print("=======")
    return child_node