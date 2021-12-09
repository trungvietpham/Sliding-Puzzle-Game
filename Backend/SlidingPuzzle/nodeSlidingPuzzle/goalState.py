
# xuất ra trạng thái đích theo các lớp layer(layer 0: row 0 và colum 0
def row_col_goal_states(n):
    # ,layer 1: row 1 và colum 1) cứ thế đến n-2
    goal_states = []
    goal_states_point=[]
    for layer in range(n-1):  # xét layer

        for i in range(n - layer):  # xét hàng
            # goal states có dạng [{1},{1,2},{1,2,3}]
            goal_states.append(set([n * layer + i + layer + 1]))
            # goal states point có dạng [{1},{2},{3}] áp dụng cho hàm FIND ở dưới
            goal_states_point.append(n * layer + i + layer + 1)
            if len(goal_states) > 1:
                goal_states[-1] = goal_states[-1].union(goal_states[-2])

        for i in range(n - layer - 1):  # xét cột
            goal_states.append(set([n+1 + (i+layer) * (n)+layer]))
            goal_states_point.append(n+1 + (i+layer) * (n)+layer)
            goal_states[-1] = goal_states[-1].union(goal_states[-2])

    return [goal_states,goal_states_point]


# do trạng thái đích bfs vs A* chỉ có 1 nên chỉ cần như thế này thôi
def finish_goal_states(n):
    goal_states = []
    goal_states.append(set(range(1, n*n)))
    return goal_states

def isGoal(board, goal_nums,n):
  count = 0
  for i in range(n):
    for j in range(n):
      count += 1
      if count in goal_nums and board[i][j] != count:
        return False
  return True