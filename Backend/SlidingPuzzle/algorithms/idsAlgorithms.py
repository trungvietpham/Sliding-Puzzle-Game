import sys
import os
sys.path.append("..")
from utils import  utils
from nodeSlidingPuzzle import goalState


def ids(root,goal_states,n):
    path = os.path.join(os.path.dirname(__file__), '..', 'inputOutput', 'solution.txt')
    f = open(path, "w")
    f.truncate(0)
    curr_goal = 0
    count, countChild, countNode, step = 0, 0, 0, 0
    limit=0
    finish=False
    while (not finish):
        limit=limit+1
        visited = set()
        h=[]
        h.append(root)
        while len(h) > 0:
            count += 1
            node = h.pop()
            t = utils.to_tuple(node.board, n)
            visited.add(t)#khi luu visited the nay neu co mot nut dang xet da visited thi no huy luon ca nhanh day =>ko giong bfs
            if goalState.isGoal(node.board, goal_states[curr_goal], n):
                print("reached goal", curr_goal, goal_states[curr_goal])
                utils.plain_print(node.board)
                # print()
                h = []
                # SAVE này khác human là nó chỉ có 1 bước nên không chuyền thành các tệp nhỏ đươc(chỉ 1 tệp lớn)
                step= utils.SAVE(node, step, f)
                finish=True
                break

            if node.depth<=limit:
                children = node.generate_children_non_heuristic()
                for child in children:
                    t = utils.to_tuple(child.board, n)
                    countChild = countChild + 1
                    if t in visited:
                        continue
                    countNode = countNode + 1
                    h.append(child)

    f.close()
    print("Thuật toán:                                                 IDS ")
    print("Số bước in ra màn hình:                                    ", step)
    print("Số node đã duyệt:                                          ", count)
    print("Số node child đã tạo ra(kể cả đã visited):                 ", countChild)
    print("Số node child đã được cho vào hàng đợi (không kể visited): ", countNode)
