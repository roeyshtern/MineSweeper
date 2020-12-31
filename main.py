import pyautogui
from PIL import Image


NUMBER_OF_HOR_FIELDS = 10
NUMBER_OF_VER_FIELDS = 10
CLEAN = 0
UNPRESSED = -1
FLAGGED = -2
BOMB = -3

class Board():
    def __init__(self, x_start, y_start, width, height, num_of_fields_hor, num_of_fields_ver, image_c):
        self.x_start = int(x_start)
        self.y_start = int(y_start)
        self.width = int(width)
        self.height = int(height)
        self.num_of_fields_hor = num_of_fields_hor
        self.num_of_fields_ver = num_of_fields_ver
        self. image_c = image_c
        self.board = self.init_board()
        self.start_box = Box(768, 252, 48, 47, image_c)
        self.game_over = False
        #self.print_board()

    def init_board(self):
        box_hor_size = int(self.width / self.num_of_fields_hor)
        box_ver_size = int(self.height / self.num_of_fields_ver)
        board = []
        for i in range(self.y_start, self.y_start + self.height, box_hor_size):
            row_of_boxes = []
            for j in range(self.x_start, self.x_start + self.width, box_ver_size):
                row_of_boxes.append(Box(j,i,box_hor_size, box_ver_size, self.image_c))
            board.append(row_of_boxes)
        return board
    
    def print_board(self):
        i = 0
        j = 0
        for row_of_boxes in self.board:
            j=0
            for box in row_of_boxes:
                print("{0},{1}:({2},{3})".format(i,j,box.x_start, box.y_start), end=', ')
                j+=1
            print()
            i +=1
    
    def get_box(self, i, j):
        if i<0 or i> NUMBER_OF_VER_FIELDS-1 or j<0 or j>NUMBER_OF_HOR_FIELDS -1:
            return None
        return self.board[i][j]
    
    def get_picture(self):
        return self.image_c.image
    
    def play(self, i, j):
        if self.game_over ==True:
            return BOMB
        current_box = self.get_box(i,j)
        current_box.click()
        current_type = current_box.get_type()
        if current_type == BOMB:
            self.game_over = True
        self.read_current_board()
        return current_type
    
    def read_current_board(self):
        for row_of_boxes in self.board:
            for box in row_of_boxes:
                box.init_type()


class Box():
    def __init__(self, x_start, y_start, width, height, image_c):
        self.x_start = x_start
        self.y_start = y_start
        self.width = width
        self.height = height
        self.image_c = image_c
        self.type = None

    def click(self):
        pyautogui.click(x=self.x_start + (self.width /2), y=self.y_start + (self.height /2))
        self.image_c.screenshot()

    def click_right(self):
        pyautogui.click(x=self.x_start + (self.width /2), y=self.y_start + (self.height /2), button='right')
        self.image_c.screenshot()

    def click_right_and_left(self):
        pyautogui.mouseDown(x=self.x_start + (self.width /2), y=self.y_start + (self.height /2), button='right')
        pyautogui.mouseDown(x=self.x_start + (self.width /2), y=self.y_start + (self.height /2), button='left')
        pyautogui.mouseUp(button='left')
        pyautogui.mouseUp(button='right')
        self.image_c.screenshot()
        
        
    def get_picture(self):
        return self.image_c.crop_box(self)

    def get_type(self):
        if self.type is None or self.type != CLEAN:
            self.type = self.init_type()
        return self.type

    def init_type(self):
        color = self.image_c.get_color(self.get_picture())
        if color == (18,18, 249):
            return 1
        elif color == (0, 123, 0):
            return 2
        elif color == (221,190, 85):
            return 3
        elif color == (119, 85, 123):
            return 4
        elif color == (123,0, 0):
            return 5
        elif color == (255,127, 126):
            return 6
        elif color == (0,255, 170):
            return 7
        elif color == (197,59, 204):
            return 8
        elif color == (222,222, 222): #clean
            return CLEAN
        elif color == (81,81, 81): #unpressed
            return UNPRESSED
        elif color == (255,255, 255): #flagged
            return FLAGGED
        elif color == (255,0, 0): #bomb
            return BOMB
        
        return BOMB
        

class ImageCreator():
    def __init__(self, image, board_loc):
        self.image = image
        self.board_loc = board_loc

    def screenshot(self):
        pyautogui.screenshot('current_screenshot.png', region=self.board_loc)
        self.image = Image.open('current_screenshot.png')

    def crop_box(self, box):
        left = box.x_start - self.board_loc.left
        upper = box.y_start - self.board_loc.top
        return self.image.crop((left, upper, left + box.width, upper + box.height))

    
    def get_color(self, image):
        r, g, b = image.getpixel((0,0))
        return (r,g,b)

def auto_loc_picture(path):
    return pyautogui.locateOnScreen(path)

def auto_loc_board():
    return auto_loc_picture('board.png')

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


def play(board, i, j):
    type_of_clicked = board.play(i,j)
    if type_of_clicked == BOMB:
        print("you lost {0},{1} was a bomb".format(i,j))
        exit()

def get_all_around(board, i, j):
    #print("getting all around for {0},{1} from {2},{3} to {4},{5}".format(i,j, i-1,j-1,i+1,j+1))
    list_of_boxes = []
    for i2 in range(i-1, i+2,1):
        for j2 in range(j-1, j+2,1):
            if not (i2 == i and j2 ==j):
                current_box = board.get_box(i2,j2)
                if current_box is not None:
                    list_of_boxes.append(current_box)

    return list_of_boxes

def get_num_of_type(list_of_around, type_of_box):
    count = 0
    for box in list_of_around:
        if box.get_type() == type_of_box:
            count += 1
    return count



def get_all_pressed(board):
    count = 0
    for i in range(0,NUMBER_OF_VER_FIELDS, 1):
        for j in range(0,NUMBER_OF_HOR_FIELDS, 1):
            box = board.get_box(i,j)
            type_of_box = box.get_type()
            if type_of_box != CLEAN and type_of_box != UNPRESSED and type_of_box != FLAGGED:
                list_of_around = get_all_around(board, i,j)
                num_of_unpressed = get_num_of_type(list_of_around, UNPRESSED)
                num_of_flagged = get_num_of_type(list_of_around, FLAGGED)
                #print("num of unpressed for {0},{1} type: {2} is {3}".format(i,j,type_of_box, num_of_unpressed))
                if type_of_box- num_of_flagged == num_of_unpressed:
                    for box in list_of_around:
                        if box.get_type() == UNPRESSED:
                            count +=1
                            box.click_right()
                            board.read_current_board()
                if type_of_box == num_of_flagged and num_of_unpressed > 0:
                    count += 1
                    box.click_right_and_left()
                    box.click_right()
                    board.read_current_board()
    return count

def strategery(board):
    play(board,0,0)
    play(board,0,NUMBER_OF_HOR_FIELDS-1)
    play(board,NUMBER_OF_VER_FIELDS-1,0)
    play(board,NUMBER_OF_VER_FIELDS-1,NUMBER_OF_HOR_FIELDS-1)

    count = 1
    while count > 0:
        count = get_all_pressed(board)

def main():
    #pyautogui.screenshot('test.png')
    #pyautogui.screenshot('screenshot.png', region=board)
    #print(board)
    #pyautogui.click(x=board.left, y=board.top)
    #mouse_coord()
    #board_loc = auto_loc_board()
    #board_loc = pyautogui.pyscreeze.Box(left=board_loc.left, top=board_loc.top, width = NUMBER_OF_HOR_FIELDS*30, height = NUMBER_OF_VER_FIELDS*30)
    board_loc = pyautogui.pyscreeze.Box(left=642, top=320, width=300, height=300)
    #pyautogui.screenshot('first_screenshot.png', region=board_loc)
    im = Image.open('first_screenshot.png')
    image_c = ImageCreator(im, board_loc)
    board = Board(board_loc.left, board_loc.top, board_loc.width, board_loc.height, NUMBER_OF_HOR_FIELDS,NUMBER_OF_VER_FIELDS, image_c)
    board.start_box.click()
    strategery(board)
    
    

if __name__ == "__main__":
    main()