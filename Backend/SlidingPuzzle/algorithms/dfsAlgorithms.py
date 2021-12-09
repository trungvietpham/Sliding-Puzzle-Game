import sys
import os
sys.path.append("..")
from utils import  utils
from nodeSlidingPuzzle import goalState


def dfs(root,goal_states,n):
    h = []
    curr_goal = 0
    path = os.path.join(os.path.dirname(__file__), '..', 'inputOutput', 'solution.txt')
    f = open(path, "w")
    f.truncate(0)
    count, countChild, countNode, step = 0, 0, 0, 0
    visited = set()
    h.append(root)
    while len(h) > 0:
        count += 1
        node = h.pop()
        t = utils.to_tuple(node.board, n)
        visited.add(t)
        if goalState.isGoal(node.board, goal_states[curr_goal], n):
            print("reached goal", curr_goal, goal_states[curr_goal])
            utils.plain_print(node.board)
            step= utils.SAVE(node, step, f)
            break

        children = node.generate_children_non_heuristic()
        for child in children:
            t = utils.to_tuple(child.board, n)
            countChild = countChild + 1
            if t in visited:
                continue
            countNode = countNode + 1
            h.append(child)

    f.close()
    print("Thuật toán:                                                 DFS ")
    print("Số bước in ra màn hình:                                    ", step)
    print("Số node đã duyệt:                                          ", count)
    print("Số node child đã tạo ra(kể cả đã visited):                 ", countChild)
    print("Số node child đã được cho vào hàng đợi (không kể visited): ", countNode)