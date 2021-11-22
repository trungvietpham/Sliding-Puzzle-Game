
import random  # RAMDOM trang thai bai dau
import argparse  # De viet lenh tren terminal
import time  # Tinh gio
import heapq as pq  # hang doi uu tien
# ( dùng heap nhanh hơn dùng queue piority vì mỗi lần push phần tử mới vào thì tốc độ chọn vị trí trong hàng đợi sẽ tốt hơn)

start = time.time()  # bat dau tinh gio
FLAG = 'HUMAN'  # mac dinh chay se la human
parser = argparse.ArgumentParser(
    description="Algorithm option")  # dung trong terminal
parser.add_argument("--astar", help="perform A* search", action="store_true")
parser.add_argument("--bfs", help="perform BFS search", action="store_true")
parser.add_argument(
    "--human", help="perform Human+A* search", action="store_true")
args = parser.parse_args()  # dung trong terminal

if args.astar:
    FLAG = 'A_STAR'  # python update.py --astar
elif args.bfs:
    FLAG = 'BFS'  # python update.py --bfs
elif args.human:
    FALG = 'HUMAN'  # python update.py (mac dinh)

# node class


# luu thong tin trang thai(bảng,nút cha,heuristic,độ sâu trong cây tìm kiếm)
class Node:
    def __init__(self, board, previous, heuristic, depth, direction):
        self.board = board
        self.previous = previous
        self.heuristic = heuristic
        self.depth = depth
        self.direction = direction

    def __lt__(self, other):  # dùng để so sánh trong heap
        return True

    # phát sinh nút con của nút đang sét trường hợp dùng heuristic(A* và human)
    def generate_children(self):
        for i in range(n):
            for j in range(n):
                if self.board[i][j] == 0:
                    x, y = i, j  # Tìm vị trí x,y đang chứa điểm 0
        # các cách di chuyển,(nhận thấy nên ưu tiên theo thứ tự(xuống,trái,phải,lên)
        val_list = [[x+1, y, "DOWN"], [x, y-1, "LEFT"],
                    [x, y+1, "RIGHT"], [x-1, y, "UP"]]
        children = []
        for child in val_list:
            # ở biên thì loại bỏ một số trường hợp
            if child[0] >= 0 and child[0] < n and child[1] >= 0 and child[1] < n:
                child_board = [row[:] for row in self.board]
                child_board[x][y] = child_board[child[0]][child[1]]
                child_board[child[0]][child[1]] = 0
                child_node = Node(child_board, self, node_manhattan(
                    child_board), self.depth + 1, child[2])
                children.append(child_node)
        return children

    # phát sinh nút con của nút đang sét trường dùng bfs(heuristic=0)
    def generate_children_non_heuristic(self):
        for i in range(n):
            for j in range(n):
                if self.board[i][j] == 0:
                    x, y = i, j
        # bfs thì đi hướng nào cx không có nhiều khác biệt như human
        val_list = [[x+1, y, "DOWN"], [x, y-1, "LEFT"],
                    [x, y+1, "RIGHT"], [x-1, y, "UP"]]
        children = []
        for child in val_list:
            if child[0] >= 0 and child[0] < n and child[1] >= 0 and child[1] < n:
                child_board = [row[:] for row in self.board]
                child_board[x][y] = child_board[child[0]][child[1]]
                child_board[child[0]][child[1]] = 0
                child_node = Node(child_board, self, 0,
                                  self.depth + 1, child[2])  # heuristic=0
                children.append(child_node)
        return children

    def generate_children_intentionally(self, command):
        for i in range(n):
            for j in range(n):
                if self.board[i][j] == 0:
                    x, y = i, j
        if command == "UP":
            a, b = x-1, y
        elif command == "DOWN":
            a, b = x+1, y
        elif command == "LEFT":
            a, b = x, y-1
        elif command == "RIGHT":
            a, b = x, y+1
        # if a>=0 and a<n and b>=0 and b>n:
        # print("Xet ",a,"---",b)
        child_board = [row[:] for row in self.board]
        child_board[x][y] = child_board[a][b]
        child_board[a][b] = 0
        child_node = Node(child_board, self, 0, self.depth + 1, command)
        # print("=======")
        # print(command)
        # plain_print(child_board)
        # print("=======")
        return child_node

# f=h+g
# helper functions


def create_random_board(n, solvable=True):  # tao bảng random
    board = [[0 for i in range(n)] for j in range(n)]
    s = list(set([i for i in range(n * n)]))
    for i in range(n):
        for j in range(n):
            item = random.sample(s, 1)
            board[i][j] = item[0]
            s.remove(item[0])
    if solvable:
        if not isSolvable(board):
            if board[2][1] != 0 and board[2][2] != 0:
                temp = board[2][1]
                board[2][1] = board[2][2]
                board[2][2] = temp
            else:
                temp = board[0][0]
                board[0][0] = board[0][1]
                board[0][1] = temp
    return board


def plain_print(b):  # hàm in bảng(dùng nhiều nên tách riêng)
    for i in b:
        for j in i:
            print(j, end=" ")
        print()


# tính heuristic toàn bộ các vị trí từ 1->(n^2-1)   (thường dùng cho a*)
def node_manhattan(board):
    sum = 0
    n = len(board)
    for i in range(n):
        for j in range(n):
            x = int((board[i][j] - 1)/n)  # row number
            y = int((board[i][j] - 1) % n)  # col num
            if board[i][j] == 0:
                continue
            sum += abs(x-i) + abs(y - j)
    return sum


def manhattan(board, goal_nums):  # tính heuristic cho có goal state (dùng cho human)
    sum = 0
    count = 0
    for i in range(n):
        for j in range(n):
            if board[i][j] in goal_nums:
                x = int((board[i][j] - 1)/n)
                y = int((board[i][j] - 1) % n)
                sum += abs(x-i) + abs(y - j)
    return sum


def to_tuple(board):  # chuyển sang tuple để thành dạng ordered(các vị trí cố định) để xét visited[]
    lst = []
    for i in range(n):
        for j in range(n):
            lst.append(board[i][j])
    return tuple(lst)


def isGoal(board, goal_nums):  # so sánh (trạng thái đang xét có ==trạng thái đích không)
    count = 0
    for i in range(n):
        for j in range(n):
            count += 1
            if count in goal_nums and board[i][j] != count:
                return False
    return True


def isSolvable(board):
    n = len(board)
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


h = []
visited = set()
n = 5
# f=g+h
board = []
# dùng bảng random
board = create_random_board(n)
while not isSolvable(board):
    board = create_random_board(n)

# #dùng bảng cho sẵn trong file input để so sánh hiệu năng
# with open('input.txt') as file:
#   for line in file:
#     board.append([int(x) for x in line.split()])


print("Problem")
plain_print(board)  # in ra bài toán
goal_states = []
goal_states_point = []
count = 0  # số nút đã xét
# số node trong hàng đợi(trong human, mỗi khi tìm được 1 trạng thái đích thì ta xóa sạch hàng đợi
countNode = 0
# (chuyền bài toán từ n^2-1 thành n^2-2)

countChild = 0  # số nút con đã phát sinh(tính cả những nút bị visited)
step = 0  # số bước đi cuối cùng tìm được(trong file solution.txt)


# xuất ra trạng thái đích theo hàng(giải theo kiểu hết hàng này đến hàng kia)
def in_order_goal_states(n):
    goal_states = []
    c = 1
    for i in range(n):
        for j in range(n):
            if i == n-1 and j == n-1:
                break
            goal_states.append(set([c]))
            if i > 0 or j > 0:
                # ghép 2 trạng thái cuối của bài toán
                goal_states[-1] = goal_states[-1].union(goal_states[-2])
                # ví dụ đang [{1},{2}] thành [{1},{1,2}],[{1},{1,2}] thàn [{1},{1,2},{1,2,3}]
                #  để làm các đích goal state
            c += 1
    return goal_states


# xuất ra trạng thái đích theo các lớp layer(layer 0: row 0 và colum 0
def row_col_goal_states(n):
    # ,layer 1: row 1 và colum 1) cứ thế đến n-2
    goal_states = []
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

    return goal_states


# do trạng thái đích bfs vs A* chỉ có 1 nên chỉ cần như thế này thôi
def finish_goal_states(n):
    goal_states = []
    goal_states.append(set(range(1, n*n)))
    return goal_states


if FLAG == 'A_STAR':
    goal_states = finish_goal_states(n)
elif FLAG == "BFS":
    goal_states = finish_goal_states(n)
elif FLAG == 'HUMAN':
    # chỉ có HUMAN là dùng row_col vs in_order
    goal_states = row_col_goal_states(n)
    # goal_states = in_order_goal_states(n)#có thể dùng option in_order

for liststate in goal_states:  # in ra thử các đích
    print(liststate)

# for liststate in goal_states_point:#in ra thử các đích
#   print(liststate)
curr_goal = 0  # bắt đầu trạng thái đích 0
# khởi tạo node đề bài và tính heuristic
root = Node(board, None, manhattan(board, goal_states[curr_goal]), 0, "Start")

f = open("solution.txt", "w")
f.truncate(0)


def to_string(board):  # chuyển board ở trạng thái list về string để viết vào file txt
    s = ""
    for i in board:
        for j in i:
            s += str(j) + " "
    return s


def SAVE(temp):  # lưu vào file txt khi tìm được đích
    boards = []
    while temp != None:
        global step
        step = step+1
        tempDirection = [temp.direction, temp.board]
        boards.append(tempDirection)
        temp = temp.previous
    step = step - 1  # phai tru 1 set vi no luu trung
    boards = boards[:-1]  # xóa phần tử cuối cùng vì bị trùng
    boards.reverse()  # đảo ngược để đúng thứ tự giải
    for i in boards:
        f.write(i[0])
        f.write(":  ")
        f.write(to_string(i[1]))
        f.write("\n")


def FIND(board, goal_point):  # hàm định vị goal state point cách số 0 bao nhiêu
    # print(goal_nums)
    # hunt=list(goal_point)
    # print("Tim goal point ",goal_point)
    x0, y0, x1, y1 = 0, 0, 0, 0
    for i in range(n):
        for j in range(n):
            if board[i][j] == 0:
                x0 = j
                y0 = i
            if board[i][j] == goal_point:
                x1 = j
                y1 = i
    # print("vertical: ",x1-x0,"  horizontal:  ",y1-y0)
    return [x1-x0, y1-y0]


#####################
# phần thuật toán chính để giải
if(FLAG == 'HUMAN'):  # Cách giải human
    f.write("Proble\n")
    f.write(to_string(root.board))
    f.write('\n')
    # chọn scale=3 vì 3*h(x)+g(x) sẽ giải nhanh hơn h(x)+g(x) như bình thường (ưu tiên heuristic)
    h_scale_factor = 5
    # push phần tử đầu tiên vào hàng đợi ưu tiên
    pq.heappush(h, (root.depth + h_scale_factor * root.heuristic, root))
    node = pq.heappop(h)[1]
    # tìm vị trí số 1 ở đâu rồi chuyền ô số 0 về đấy
    intentional_direction = FIND(root.board, goal_states_point[curr_goal])
    f.write("Bat dau tim kiem ")
    f.write(str(goal_states_point[curr_goal]))
    f.write('\n')
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

    SAVE(node)
    node = Node(node.board, None, manhattan(
        board, goal_states[curr_goal]), 0, "da thay cai dau")
    pq.heappush(h, (node.depth+h_scale_factor *
                manhattan(node.board, goal_states[curr_goal]), node))

    while len(h) > 0:  # dừng lại khi tìm thấy đích cuối cùng (curr_goal == len(goal_states)) hoặc heap hết

        count += 1  # đếm số phần tử xét
        # print("heuristic=",h[0])
        node = pq.heappop(h)[1]
        # plain_print(node.board)
        # print("------------")
        # lấy nút vừa pop biến thành tuple để xét visited
        t = to_tuple(node.board)
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
                f.write("dua bai toan ve dang corner")
                f.write(str(goal_states_point[curr_goal]))
                f.write('\n')
                SAVE(node)
                node = Node(node.board, None, manhattan(
                    board, goal_states[curr_goal]), 0, "nut corner phai")
                f.write("Xac dinh bai toan corner")
                f.write("\n")
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
                SAVE(node)
                # phai khoi tao lai node de cat duoi cho previous=0 ko no bi trung
                node = Node(node.board, None, manhattan(
                    board, goal_states[curr_goal]), 0, node.direction)
                # print("Hoan thanh thuat toan corner")

        # Trường hợp xét ô góc dưới
        elif (int(goal_states_point[curr_goal] % n)+2 <= n and int(goal_states_point[curr_goal]/n) == n-1 and node.board[n-1][goal_states_point[curr_goal] % n] == goal_states_point[curr_goal]):
            # print(curr_goal," ",goal_states_point[curr_goal])
            if node.board[n-1][goal_states_point[curr_goal] % n+1] == 0:
                # print(curr_goal," ",goal_states_point[curr_goal])
                # print("Tien hanh thuat toan corner doc")
                # plain_print(node.board)
                f.write("dua bai toan ve dang corner doc")
                f.write(str(goal_states_point[curr_goal]))
                f.write('\n')
                SAVE(node)
                node = Node(node.board, None, manhattan(
                    board, goal_states[curr_goal]), 0, "corner trai")
                f.write("Xac dinh bai toan corner doc")
                f.write('\n')
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
                SAVE(node)
                node = Node(node.board, None, manhattan(board, goal_states[curr_goal]), 0,
                            node.direction)  # phai khoi tao lai node de cat duoi cho previous=0 ko no bi trung
                # print("Hoan thanh thuat toan corner doc")

        # nếu đúng trạng thái đích thì chúng ta phải xét cả vòng lặp while
        if isGoal(node.board, goal_states[curr_goal]):
            # vì nếu không một số trường hợp
            while curr_goal < len(goal_states) and isGoal(node.board, goal_states[curr_goal]):
                # 1 2 3                                              1 2 3
                # 4 5 6 ở đích thứ 7 khi xét ở đích thứ 8 sẽ thành   4 5 6 sẽ bị treo vô hạn vì visited
                # 7 8 0                                              7 0 8
                print("reached goal", curr_goal, goal_states[curr_goal])
                plain_print(node.board)

                f.write("bat dau tim trang thai dich ")
                f.write(str(goal_states_point[curr_goal]))
                f.write('\n')
                # mỗi khi tính được goal state sẽ lưu lại để cho GUI xử lý, vừa giải vừa update hình
                SAVE(node)
                # .vì đôi khi tính rất lâu, nên không thể chỉ xuất khi mà proble được giải hết được.
                curr_goal += 1  # tăng goal state
            if curr_goal == len(goal_states):  # hoàn thành đích thì thoát luôn
                break

            # mục đích của bước này là xóa previous nút cha
            node = Node(node.board, None, manhattan(
                board, goal_states[curr_goal]), 0, "goal state hoan thanh")
            # vì chúng ta đã lưu ở SAVE rồi, không thì sẽ bị trùng
            # tìm vị trí nút cần tìm goal_state_point[cur_goal] ở đâu rồi chuyền ô số 0 về đấy
            intentional_direction = FIND(
                node.board, goal_states_point[curr_goal])
            f.write("Bat dau tim kiem ")
            f.write(str(goal_states_point[curr_goal]))
            f.write('\n')
            if(intentional_direction[1] > 0):
                for i in range(intentional_direction[1]):
                    # print("move down ",i)
                    node = node.generate_children_intentionally("DOWN")

            if (intentional_direction[0] > 0):
                for i in range(intentional_direction[0]):
                    # print("move right ", i)
                    node = node.generate_children_intentionally("RIGHT")

            if intentional_direction[1] < 0:
                for i in range(intentional_direction[1], 0):
                    # print("move up ",i)
                    node = node.generate_children_intentionally("UP")

            if intentional_direction[0] < 0:
                for i in range(intentional_direction[0], 0):
                    # print("move left ", i)
                    node = node.generate_children_intentionally("LEFT")

            print("da thay")
            # plain_print(node.board)
            SAVE(node)

            node = Node(node.board, None, manhattan(
                board, goal_states[curr_goal]), 0, " goal state da thay")
            h = []  # reset lại heap đỡ tốn bộ nhớ
            visited = set()  # xóa visited
            # pq.heappush(h,h_scale_factor * manhattan(node.board, goal_states[curr_goal]), node)

        children = node.generate_children()  # generate ra các nút con

        for child in children:
            t = to_tuple(child.board)
            countChild = countChild+1
            if t in visited:
                continue

            countNode = countNode+1  # các nút con đã được generate
            # print("depth ",child.depth," va heuristic ",h_scale_factor * manhattan(child.board, goal_states[curr_goal]))
            # push vào heap với heuristic update trạng thái đích mới nhất
            pq.heappush(h, (child.depth + h_scale_factor *
                        manhattan(child.board, goal_states[curr_goal]), child))
        # print("h= ", len(h)," va visited=",len(visited))


elif FLAG == 'BFS':  # giải bfs khác human là không có heuristic=0, và cũng không cần vòng lặp while vì nó chỉ có 1 bước đích
    pq.heappush(h, (root.depth, root))
    while len(h) > 0:
        count += 1
        node = pq.heappop(h)[1]
        t = to_tuple(node.board)
        visited.add(t)
        if isGoal(node.board, goal_states[curr_goal]):
            print("reached goal", curr_goal, goal_states[curr_goal])
            plain_print(node.board)
            # print()
            h = []
            curr_goal += 1
            # SAVE này khác human là nó chỉ có 1 bước nên không chuyền thành các tệp nhỏ đươc(chỉ 1 tệp lớn)
            SAVE(node)
            break

        children = node.generate_children_non_heuristic()
        for child in children:
            t = to_tuple(child.board)
            countChild = countChild + 1
            if t in visited:
                continue
            countNode = countNode + 1
            pq.heappush(h, (child.depth, child))
elif FLAG == 'A_STAR':  # giải bfs khác human là không cần vòng lặp while vì nó chỉ có 1 bước đích
    h_scale_factor = 1
    pq.heappush(h, (root.depth + h_scale_factor * root.heuristic, root))
    while len(h) > 0:
        count += 1
        node = pq.heappop(h)[1]
        t = to_tuple(node.board)
        visited.add(t)
        if isGoal(node.board, goal_states[curr_goal]):
            print("reached goal", curr_goal, goal_states[curr_goal])
            plain_print(node.board)
            # SAVE này khác human là nó chỉ có 1 bước nên không chuyền thành các tệp nhỏ đươc(chỉ 1 tệp lớn)
            SAVE(node)
            break

        children = node.generate_children()
        for child in children:
            t = to_tuple(child.board)
            countChild = countChild + 1
            if t in visited:
                continue
            countNode = countNode + 1
            pq.heappush(
                h, (child.depth + h_scale_factor * child.heuristic, child))

f.close()
print("FLAG ", FLAG, " - Time ", time.time()-start, " - So step di ", step,
      "- So buoc duyet ", count, " - So node ", countNode, "- So generate child", countChild)
