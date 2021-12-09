import heapq as pq  # hang doi uu tien
import os
import sys
sys.path.append("..")
from utils import  utils
from nodeSlidingPuzzle import goalState, heuristic
from nodeSlidingPuzzle.Node import Node
def humman(root,goal_states,goal_states_point,n):  # Cách giải human

# "UP" : 1
# "DOWN": 2
# "LEFT": 3
# "RIGHT": 4

    h = []
    curr_goal = 0
    path = os.path.join(os.path.dirname(__file__), '..', 'inputOutput', 'solution.txt')
    f = open(path, "w")
    f.truncate(0)
    count, countChild, countNode, step = 0, 0, 0, 0
    visited = set()


    # f.write("Problem\n")
    # f.write(utils.to_string(root.board))
    # f.write('\n')
    # chọn scale=3 vì 3*h(x)+g(x) sẽ giải nhanh hơn h(x)+g(x) như bình thường (ưu tiên heuristic)
    h_scale_factor = 7
    # push phần tử đầu tiên vào hàng đợi ưu tiên
    pq.heappush(h, (root.depth + h_scale_factor * root.heuristic, root))
    node = pq.heappop(h)[1]
    # tìm vị trí số 1 ở đâu rồi chuyền ô số 0 về đấy
    intentional_direction = utils.FIND(root.board, goal_states_point[curr_goal], n)
    # f.write("Bat dau tim kiem ")
    # f.write(str(goal_states_point[curr_goal]))
    # f.write('\n')
    if (intentional_direction[1] > 0):
        for i in range(intentional_direction[1]):
            # print("move down ", i)
            node = node.generate_children_intentionally("DOWN")
    elif intentional_direction[1] < 0:
        for i in range(intentional_direction[1], 0):
            # print("move up ", i)
            node = node.generate_children_intentionally("UP")

    if (intentional_direction[0] > 0):
        for i in range(intentional_direction[0]):
            # print("move right ", i)
            node = node.generate_children_intentionally("RIGHT")
    elif intentional_direction[0] < 0:
        for i in range(intentional_direction[0], 0):
            # print("move left ", i)
            node = node.generate_children_intentionally("LEFT")

    step= utils.SAVE(node, step, f)
    node = Node(node.board, None, heuristic.manhattan(node.board, goal_states[curr_goal], n), 0, "da thay cai dau", n)
    pq.heappush(h, (node.depth + h_scale_factor * heuristic.manhattan(node.board, goal_states[curr_goal], n), node))

    while len(h) > 0:  # dừng lại khi tìm thấy đích cuối cùng (curr_goal == len(goal_states)) hoặc heap hết

        count += 1  # đếm số phần tử xét
        # print("heuristic=",h[0])
        node = pq.heappop(h)[1]
        # plain_print(node.board)
        # print("------------")
        # lấy nút vừa pop biến thành tuple để xét visited
        t = utils.to_tuple(node.board, n)
        visited.add(t)
        # print(node.board)
        # if(curr_goal==4):
        #   print("Xet ")
        # print("**********")
        # print(curr_goal," va point ",goal_states_point[curr_goal])
        # print(int(goal_states_point[curr_goal]%n)+2,"     ",goal_states_point[curr_goal]/n,"   ", node.board[n-1][goal_states_point[curr_goal]%n])
        # Trường hợp xét ô góc phải
        if (int(goal_states_point[curr_goal]/n)+2 <= n and goal_states_point[curr_goal] % n == 0 and node.board[int(goal_states_point[curr_goal]/n)][n-1] == goal_states_point[curr_goal]):

            if node.board[int(goal_states_point[curr_goal]/n)+1][n-1] == 0:
                # print(curr_goal," ",goal_states_point[curr_goal])
                # print("Tien hanh thuat toan corner")
                # plain_print(node.board)
                # f.write("dua bai toan ve dang corner")
                # f.write(str(goal_states_point[curr_goal]))
                # f.write('\n')
                step= utils.SAVE(node, step, f)
                node = Node(node.board, None, heuristic.manhattan(node.board, goal_states[curr_goal], n), 0, "nut corner phai", n)
                # f.write("Xac dinh bai toan corner")
                # f.write("\n")
                node = node.generate_children_intentionally("UP")
                node = node.generate_children_intentionally("LEFT")
                node = node.generate_children_intentionally("UP")
                node = node.generate_children_intentionally("RIGHT")
                node = node.generate_children_intentionally("DOWN")
                node = node.generate_children_intentionally("LEFT")
                node = node.generate_children_intentionally("UP")
                node = node.generate_children_intentionally("RIGHT")
                node = node.generate_children_intentionally("DOWN")
                node = node.generate_children_intentionally("DOWN")
                node = node.generate_children_intentionally("LEFT")
                node = node.generate_children_intentionally("UP")
                node = node.generate_children_intentionally("UP")
                node = node.generate_children_intentionally("RIGHT")
                node = node.generate_children_intentionally("DOWN")
                count += 15
                step= utils.SAVE(node, step, f)
                # phai khoi tao lai node de cat duoi cho previous=0 ko no bi trung
                node = Node(node.board, None, heuristic.manhattan(node.board, goal_states[curr_goal], n), 0, node.direction, n)
                # print("Hoan thanh thuat toan corner")

        # Trường hợp xét ô góc dưới
        elif (int(goal_states_point[curr_goal] % n)+2 <= n and int(goal_states_point[curr_goal]/n) == n-1 and node.board[n-1][goal_states_point[curr_goal] % n] == goal_states_point[curr_goal]):
            # print(curr_goal," ",goal_states_point[curr_goal])
            if node.board[n-1][goal_states_point[curr_goal] % n+1] == 0:
                # print(curr_goal," ",goal_states_point[curr_goal])
                # print("Tien hanh thuat toan corner doc")
                # plain_print(node.board)
                # f.write("dua bai toan ve dang corner doc")
                # f.write(str(goal_states_point[curr_goal]))
                # f.write('\n')
                step= utils.SAVE(node, step, f)
                node = Node(node.board, None, heuristic.manhattan(node.board, goal_states[curr_goal], n), 0, "corner trai", n)
                # f.write("Xac dinh bai toan corner doc")
                # f.write('\n')
                node = node.generate_children_intentionally("LEFT")
                node = node.generate_children_intentionally("UP")
                node = node.generate_children_intentionally("LEFT")
                node = node.generate_children_intentionally("DOWN")
                node = node.generate_children_intentionally("RIGHT")
                node = node.generate_children_intentionally("UP")
                node = node.generate_children_intentionally("LEFT")
                node = node.generate_children_intentionally("DOWN")
                node = node.generate_children_intentionally("RIGHT")
                node = node.generate_children_intentionally("RIGHT")
                node = node.generate_children_intentionally("UP")
                node = node.generate_children_intentionally("LEFT")
                node = node.generate_children_intentionally("LEFT")
                node = node.generate_children_intentionally("DOWN")
                node = node.generate_children_intentionally("RIGHT")
                count+=15
                step= utils.SAVE(node, step, f)
                node = Node(node.board, None, heuristic.manhattan(node.board, goal_states[curr_goal], n), 0, node.direction, n)  # phai khoi tao lai node de cat duoi cho previous=0 ko no bi trung
                # print("Hoan thanh thuat toan corner doc")

        # nếu đúng trạng thái đích thì chúng ta phải xét cả vòng lặp while
        if goalState.isGoal(node.board, goal_states[curr_goal], n):
            # vì nếu không một số trường hợp
            while curr_goal < len(goal_states) and goalState.isGoal(node.board, goal_states[curr_goal], n):
                # 1 2 3                                              1 2 3
                # 4 5 6 ở đích thứ 7 khi xét ở đích thứ 8 sẽ thành   4 5 6 sẽ bị treo vô hạn vì visited
                # 7 8 0                                              7 0 8
                print("reached goal", curr_goal, goal_states[curr_goal])
                utils.plain_print(node.board)

                # f.write("bat dau tim trang thai dich ")
                # f.write(str(goal_states_point[curr_goal]))
                # f.write('\n')
                # mỗi khi tính được goal state sẽ lưu lại để cho GUI xử lý, vừa giải vừa update hình
                step= utils.SAVE(node, step, f)
                # mục đích của bước này là xóa previous nút cha
                node = Node(node.board, None, heuristic.manhattan(node.board, goal_states[curr_goal], n), 0,
                            "goal state hoan thanh", n)
                # .vì đôi khi tính rất lâu, nên không thể chỉ xuất khi mà problem được giải hết được.
                curr_goal += 1  # tăng goal state
            if curr_goal == len(goal_states):  # hoàn thành đích thì thoát luôn
                break


            # vì chúng ta đã lưu ở utils.SAVE rồi, không thì sẽ bị trùng
            # tìm vị trí nút cần tìm goal_state_point[cur_goal] ở đâu rồi chuyền ô số 0 về đấy
            intentional_direction = utils.FIND(node.board, goal_states_point[curr_goal], n)
            # f.write("Bat dau tim kiem ")
            # f.write(str(goal_states_point[curr_goal]))
            # f.write('\n')
            if(intentional_direction[1] > 0):
                for i in range(intentional_direction[1]):
                    # print("move down ",i)
                    count+=1
                    node = node.generate_children_intentionally("DOWN")

            if (intentional_direction[0] > 0):
                for i in range(intentional_direction[0]):
                    # print("move right ", i)
                    count += 1
                    node = node.generate_children_intentionally("RIGHT")

            if intentional_direction[1] < 0:
                for i in range(intentional_direction[1], 0):
                    # print("move up ",i)
                    count += 1
                    node = node.generate_children_intentionally("UP")

            if intentional_direction[0] < 0:
                for i in range(intentional_direction[0], 0):
                    # print("move left ", i)
                    count += 1
                    node = node.generate_children_intentionally("LEFT")

            # plain_print(node.board)
            step= utils.SAVE(node, step, f)

            node = Node(node.board, None, heuristic.manhattan(node.board, goal_states[curr_goal], n), 0, " goal state da thay", n)
            h = []  # reset lại heap đỡ tốn bộ nhớ
            visited = set()  # xóa visited
            # pq.heappush(h,h_scale_factor * heuristic.manhattan(node.board, goal_states[curr_goal]), node)

        children = node.generate_children_non_heuristic()  # generate ra các nút con

        for child in children:
            t = utils.to_tuple(child.board, n)
            countChild = countChild+1
            if t in visited:
                continue

            countNode = countNode+1  # các nút con đã được generate
            # print("depth ",child.depth," va heuristic ",h_scale_factor * heuristic.manhattan(child.board, goal_states[curr_goal]))
            # push vào heap với heuristic update trạng thái đích mới nhất
            pq.heappush(h, (child.depth + h_scale_factor * heuristic.manhattan(child.board, goal_states[curr_goal], n), child))
        # print("h= ", len(h)," va visited=",len(visited))

    f.close()
    print("Thuật toán:                                                 Human-based ")
    print("Số bước in ra màn hình:                                    ",step)
    print("Số node đã duyệt:                                          ", count)
    print("Số node child đã tạo ra(kể cả đã visited):                 ", countChild)
    print("Số node child đã được cho vào hàng đợi (không kể visited): ", countNode)

