import heapq as pq  # hang doi uu tien
import sys
import os
sys.path.append("..")
import utils 
from nodeSlidingPuzzle import goalState


def astar(root,goal_states,n):  # giải bfs khác human là không cần vòng lặp while vì nó chỉ có 1 bước đích
    h_scale_factor = 1
    h=[]
    curr_goal=0
    path = os.path.join(os.path.dirname(__file__), '..', 'inputOutput', 'solution.txt')
    f = open(path, "w")
    f.truncate(0)
    count,countChild,countNode,step=0,0,0,0
    visited = set()
    pq.heappush(h, (root.depth + h_scale_factor * root.heuristic, root))
    while len(h) > 0:
        count += 1
        node = pq.heappop(h)[1]
        t = utils.to_tuple(node.board, n)
        visited.add(t)
        if goalState.isGoal(node.board, goal_states[curr_goal], n):
            print("reached goal", curr_goal, goal_states[curr_goal])
            utils.plain_print(node.board)
            # SAVE này khác human là nó chỉ có 1 bước nên không chuyền thành các tệp nhỏ đươc(chỉ 1 tệp lớn)
            step= utils.SAVE(node, step, f)
            break

        children = node.generate_children()
        for child in children:
            t = utils.to_tuple(child.board, n)
            countChild = countChild + 1
            if t in visited:
                continue
            countNode = countNode + 1
            pq.heappush(h, (child.depth + h_scale_factor * child.heuristic, child))

    f.close()
    print("Thuật toán:                                                 A* ")
    print("Số bước in ra màn hình:                                    ",step)
    print("Số node đã duyệt:                                          ", count)
    print("Số node child đã tạo ra(kể cả đã visited):                 ", countChild)
    print("Số node child đã được cho vào hàng đợi (không kể visited): ", countNode)
