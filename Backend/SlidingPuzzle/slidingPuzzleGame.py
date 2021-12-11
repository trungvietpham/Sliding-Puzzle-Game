import time  # Tinh gio
import sys, os
path = os.path.join(os.path.dirname(__file__))
sys.path.insert(1, path)
import slidingPuzzleController as controller
from utils import utils


from nodeSlidingPuzzle import heuristic
from nodeSlidingPuzzle.Node import Node

def run_algo(n, algorithms):
    start = time.time()  # bat dau tinh gio

    #Khỏi tạo n và tên thuật toán
    ##khởi tạo giá trị cho n
    # algorithms="HUMAN"# A_STAR,BFS,DFS,IDS

    ##Creat Board  2 tùy chọn  cách 1 là dùng file input
    board = controller.createBoard(1,n)#board = createBoard(1,n) cách 2 là auto
    n = len(board[0])
    print("Problem")
    utils.plain_print(board)  # in thử ra bài toán
    ##Find goalStates
    goal_states_all=controller.findGoalState(algorithms,n)
    goal_states=goal_states_all[0]
    goal_states_point=goal_states_all[1]#cần với human do human dùng nhiều if else
    for liststate in goal_states:  # in ra thử các đích
        print(liststate)
    ##Solve
    root = Node(board, None, heuristic.manhattan(board, goal_states[0],n), 0, "Start",n)#tạo node root
    controller.Solve(algorithms,root,goal_states,goal_states_point,n)#giải

    print("Thời gian:                                                 ",time.time()-start)
    return 