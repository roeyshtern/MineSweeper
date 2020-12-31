import pyautogui
from PIL import Image


NUMBER_OF_HOR_FIELDS = 10
NUMBER_OF_VER_FIELDS = 10

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
        #self.print_board()

    def init_board(self):
        box_hor_size = int(self.width / self.num_of_fields_hor)
        box_ver_size = int(self.height / self.num_of_fields_ver)
        board = []
        for i in range(self.x_start, self.x_start + self.width, box_hor_size):
            row_of_boxes = []
            for j in range(self.y_start, self.y_start + self.height, box_ver_size):
                row_of_boxes.append(Box(i,j,box_hor_size, box_ver_size, self.image_c))
            board.append(row_of_boxes)
        return board
    
    def print_board(self):
        for row_of_boxes in self.board:
            for box in row_of_boxes:
                print(box.x_start, box.y_start, end=', ')
            print()
    
    def get_box(self, i, j):
        return self.board[i][j]
    
    def get_picture(self):
        return self.image_c.image
    


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

    def get_picture(self):
        return self.image_c.crop_box(self)

    def get_type(self):
        self.type = self.init_type(self.image_c.get_color(self.get_picture()))
        return self.type

    def init_type(self, color):
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
        elif color == (81,81, 81): #unpressed
            return -2
        elif color == (255,255, 255): #flagged
            return -3
        elif color == (222,222, 222): #clean
            return 0
        elif color == (255,0, 0): #bomb
            return -1
        
        return -1
        

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
        print("r= {0}, g={1}, b={2}".format(r,g,b))
        return (r,g,b)

def auto_loc_picture(path):
    return pyautogui.locateOnScreen(path)

def auto_loc_board():
    return auto_loc_picture('board_tiny.png')

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

def main():
    #pyautogui.screenshot('test.png')
    #pyautogui.screenshot('screenshot.png', region=board)
    #print(board)
    #pyautogui.click(x=board.left, y=board.top)
    #mouse_coord()
    board_loc = auto_loc_board()
    board_loc = pyautogui.pyscreeze.Box(left=board_loc.left, top=board_loc.top, width = NUMBER_OF_HOR_FIELDS*30, height = NUMBER_OF_VER_FIELDS*30)
    #board_loc = pyautogui.pyscreeze.Box(left=642, top=320, width=300, height=300)
    #pyautogui.screenshot('first_screenshot.png', region=board_loc)
    im = Image.open('first_screenshot.png')
    image_c = ImageCreator(im, board_loc)
    board = Board(board_loc.left, board_loc.top, board_loc.width, board_loc.height, NUMBER_OF_HOR_FIELDS,NUMBER_OF_VER_FIELDS, image_c)
    board.start_box.click()
    box = board.get_box(5,5)
    box.click()
    box.get_picture().show()
    print(box.get_type())
    
    

if __name__ == "__main__":
    main()