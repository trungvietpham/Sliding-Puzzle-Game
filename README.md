A.cách chạy:
python .\SlidingPuzzle\slidingPuzzleGame.py

B.các thay đổi được cài đặt trong slidingPuzzleGame.py:

1.Thay đổi size
n=10,3,7,20,...

2.Thay đổi thuật toán
algorithms="HUMAN","BFS","IDS","DFS","A*"

3.chọn chơi random hay nhập input
board = createBoard(1,n) là dùng file input.txt

board = createBoard(2,n) là dùng bảng random

C.ngoài ra: 

1.file output.txt để xuất các bước đi

2.nếu chỉ muốn hiện (Left,Right,DOWN,UP) trong file output mà không muốn hiện số thì
chỉ cần vào utils/utils trong hàm SAVE khoảng dòng 35,36 ẩn "f.write(to_string(i[1]))" là đc
