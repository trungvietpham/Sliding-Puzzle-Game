
def plain_print(b):#dùng để in ra board các bước khi giải
  for i in b:
    for j in i:
      print(j, end = " ")
    print()

def to_tuple(board,n):#dùng tuple để gắn cố định các phần từ dùng cho visited
  lst = []
  for i in range(n):
    for j in range(n):
      lst.append(board[i][j])
  return tuple(lst)

def to_string(board):  # chuyển board ở trạng thái list về string để viết vào file txt
    s = ""
    for i in board:
        for j in i:
            s += str(j) + " "
    return s


def SAVE(temp,step,f):  # lưu vào file txt khi tìm được đích
    boards = []
    while temp != None:
        step = step+1
        tempDirection = [temp.direction, temp.board]
        boards.append(tempDirection)
        temp = temp.previous
    step = step - 1  # phai tru 1 set vi no luu trung
    boards = boards[:-1]  # xóa phần tử cuối cùng vì bị trùng
    boards.reverse()  # đảo ngược để đúng thứ tự giải
    for i in boards:
        f.write(i[0])
        # f.write(":  ")
        # f.write(to_string(i[1]))
        f.write("\n")

    return step


def FIND(board, goal_point,n):  # hàm định vị goal state point cách số 0 bao nhiêu
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
