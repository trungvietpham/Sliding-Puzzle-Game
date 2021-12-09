import sys
import os
sys.path.append("")
## Các module bên trong folder
##Các thuật toán
from algorithms import astarAlgorithms,bfsAlgorithms, dfsAlgorithms ,idsAlgorithms ,hummanAlgorithms
from nodeSlidingPuzzle import goalState,initializationBoard

##
# ( dùng heap nhanh hơn dùng queue piority vì mỗi lần push phần tử mới vào thì tốc độ chọn vị trí trong hàng đợi sẽ tốt hơn)


def createBoard(options, n):#tạo broad đề bài, có 2 cách
    board = []
    # C1:dùng bảng cho sẵn trong file input để so sánh hiệu năng
    if options == 1:
        path = os.path.join(os.path.dirname(__file__), 'inputOutput', 'input.txt')
        with open(path) as file:
            for line in file:
                board.append([int(x) for x in line.split()])
    # C2:dùng bảng random
    else:
        board = initializationBoard.create_random_board(n)

    return board



def findGoalState(algorithms,n):#với mỗi kiểu thuật toán sẽ cho các goal state khác nhau
    goal_states=[]
    goal_states_point=[]
    if algorithms == 'HUMAN':
        # chỉ có HUMAN là dùng row_col vs in_order
        goal_states_all = goalState.row_col_goal_states(n)
        goal_states = goal_states_all[0]
        goal_states_point = goal_states_all[1]
    elif algorithms == 'A*' or algorithms == "BFS" or algorithms == "DFS" or algorithms == "IDS":
        goal_states = goalState.finish_goal_states(n)

    return [goal_states,goal_states_point]

def Solve(algorithms,root,goal_states,goal_states_point,n):#giải theo các thuật toán
    if algorithms == "A*":
        astarAlgorithms.astar(root, goal_states, n)
    elif algorithms == "BFS":
        bfsAlgorithms.bfs(root, goal_states, n)
    elif algorithms == "DFS":
        dfsAlgorithms.dfs(root, goal_states, n)
    elif algorithms == "IDS":
        idsAlgorithms.ids(root, goal_states, n)
    elif algorithms == "HUMAN":
        hummanAlgorithms.humman(root, goal_states, goal_states_point, n) #chỉ có humman là cần goal state point do dùng nhiều if else trong humanAlgorithms
