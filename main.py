import pyautogui

NUMBER_OF_HOR_FIELDS = 10
NUMBER_OF_VER_FIELDS = 10

class Board():
    def __init__(self, x_start, y_start, width, height, num_of_fields_hor, num_of_fields_ver):
        self.x_start = int(x_start)
        self.y_start = int(y_start)
        self.width = int(width)
        self.height = int(height)
        self.num_of_fields_hor = num_of_fields_hor
        self.num_of_fields_ver = num_of_fields_ver
        self.board = self.init_board()
        self.print_board()

    def init_board(self):
        box_hor_size = int(self.width / self.num_of_fields_hor)
        box_ver_size = int(self.height / self.num_of_fields_ver)
        board = []
        for i in range(self.x_start, self.x_start + self.width, box_hor_size):
            row_of_boxes = []
            for j in range(self.y_start, self.y_start + self.height, box_ver_size):
                row_of_boxes.append(Box(i,j,box_hor_size, box_ver_size))
            board.append(row_of_boxes)
        return board
    
    def print_board(self):
        for row_of_boxes in self.board:
            for box in row_of_boxes:
                print(box.x_start, box.y_start, end=', ')
            print()
    
    def get_box(self, i, j):
        return self.board[i][j]



class Box():
    def __init__(self, x_start, y_start, width, height):
        self.x_start = x_start
        self.y_start = y_start
        self.width = width
        self.height = height

    def click(self):
        pyautogui.click(x=self.x_start + (self.width /2), y=self.y_start + (self.height /2))

    def get_picture(self):
        im = pyautogui.screenshot('screenshot.png', region=(self.x_start, self.y_start, self.width, self.height))

def main():
    #pyautogui.screenshot('test.png')
    #im = pyautogui.screenshot('screenshot.png', region=board)
    #print(board)
    #pyautogui.click(x=board.left, y=board.top)
    board_loc = pyautogui.locateOnScreen('board.png')
    board = Board(board_loc.left, board_loc.top, board_loc.width, board_loc.height, NUMBER_OF_HOR_FIELDS,NUMBER_OF_VER_FIELDS)
    box = board.get_box(0,0)
    box.click()

    
    
def mouse_coord():
    print('Press Ctrl-C to quit.')
    try:
        while True:
            x, y = pyautogui.position()
            positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
            print(positionStr, end='')
            print('\b' * len(positionStr), end='', flush=True)
    except KeyboardInterrupt:
        print('\n')
if __name__ == "__main__":
    main()