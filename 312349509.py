# import game_of_life_interface

import numpy as np
from matplotlib import pyplot as plt


class GameOfLife:
    """ init method for class GameOfLife.
           Input size_of_board donates the size of the board, is an integer bigger than 9 and smaller than 1000.
           board_start_mode donates the starting position options, please refer to the added PDF file. Is an integer.
           rules donates the rules of the game. Is a string
           rle: is a str[optional]. the coding for a pattern, if there is an rle coding than the board_start_mode is overlooked,
                if there isn't an rle, than use the board_start_mode.
           pattern_position: is a tuple of two integers (x,y). the upper left position of the pattern on the board,
                             only used if in rle mode.
           Output None.
           """
    def __init__(self, size_of_board, board_start_mode=0, rules='B3/S23', rle='', pattern_position=(0, 0)):

        self.size_of_board = size_of_board
        self.patt_pos = pattern_position
        self.rules = rules

        self.B_nums = self.comprehend_rules(rules)[0]
        self.S_nums = self.comprehend_rules(rules)[1]
        if rle != '':
            self.board = self.position_the_pattern(rle,size_of_board,self.patt_pos)
        # elif board_start_mode == 1:
        #    self.board = self.create_board_1()
        elif board_start_mode == 2:
            self.board = self.create_board_2()
        elif board_start_mode == 3:
            self.board = self.create_board_3()
        elif board_start_mode == 4:
            self.board = self.create_board_4()
        else:
            self.board = self.create_board_1()

        self.cell_states = []
        for y in range(size_of_board):
            lst = []
            for x in range(size_of_board):
                lst.append([self.check_neighbors(y,x),self.board[y][x]])
            self.cell_states.append(lst)


        # print(self.board)
        # self.display_board()
        # for i in range(180):
        # print(i)
        # name = 'img'+ str(i) +".png"
        # self.update()
        # plt.imsave(name,self.board)
        # self.display_board()

        # raise NotImplementedError
    def cell_state(self, y, x):
        if self.board[y][x] != 0:
            return 255
        else:
            return 0

    def update(self):
        """ This method updates the board game by the rules of the game. Do a single iteration.
                Input None.
                Output None.
                """
        r = self.size_of_board
        next = self.board.copy()
        b = self.B_nums
        s = self.S_nums
        for y in range(r):
            for x in range(r):
                if self.cell_states[y][x] == [0,0]:
                    pass
                else:
                    num = self.check_neighbors(y, x)

                    if self.board[y][x] == 0 and num in b:
                        next[y][x] = 255
                        self.cell_states[y][x][1] =255

                        for e in range(-1, 2):
                            for d in range(-1, 2):
                                inc_y = (y + e) % r
                                inc_x = (x + d) % r

                                if d == 0 and e == 0:  # don't count yourself
                                    pass
                                else:
                                    self.cell_states[inc_y][inc_x][0]+=1

                    if self.board[y][x] != 0 and num not in s:
                        next[y][x] = 0
                        self.cell_states[y][x][1] = 0

                        for e in range(-1, 2):
                            for d in range(-1, 2):
                                inc_y = (y + e) % r
                                inc_x = (x + d) % r

                                if d == 0 and e == 0:  # don't count yourself
                                    pass
                                else:
                                    self.cell_states[inc_y][inc_x][0]+=1

        self.board = next

        # raise NotImplementedError

    def save_board_to_file(self, file_name):
        """ This method saves the current state of the game to a file. You should use Matplotlib for this.
        Input img_name donates the file name. Is a string, for example file_name = '1000.png'
        Output a file with the name that donates filename.
        """

        plt.imsave(file_name, self.board)

        # raise NotImplementedError

    def display_board(self):

        plt.imshow(self.board)
        plt.pause(0.1)
        """ This method displays the current state of the game to the screen. You can use Matplotlib for this.
        Input None.
        Output a figure should be opened and display the board.
        """
        # raise NotImplementedError

    def return_board(self):
        """ This method returns a list of the board position. The board is a two-dimensional list that every
        cell donates if the cell is dead or alive. Dead will be donated with 0 while alive will be donated with 255.
        Input None.
        Output a list that holds the board with a size of size_of_board*size_of_board.
        """
        return self.board
        # raise NotImplementedError

    def check_neighbors(self, y, x):
        r = self.size_of_board
        num_of_live_cells = 0
        for e in range(-1, 2):
            for d in range(-1, 2):
                check_y = (y + e) % r
                check_x = (x + d) % r

                if d == 0 and e == 0:  # don't count yourself
                    pass
                elif self.board[check_y][check_x] == 0:  # for 0 values move on
                    pass
                elif self.board[check_y][check_x] != 0:  # for nonzero values increase by 1
                    num_of_live_cells += 1
        return num_of_live_cells

    def comprehend_rules(self, rules):
        S_nums = []
        B_nums = []
        for letter in rules:
            if letter in ["B", "b"]:
                arr = B_nums
            if letter in ["S", "s"]:
                arr = S_nums
            if letter.isnumeric():
                arr.append(int(letter))
        return (B_nums, S_nums)

    def comprehend_rle_dims(self, rle):

        y_count = 0
        x_count = 0
        we_already_know_how_wide_this_pattern_is_and_have_no_need_of_further_letter_counting = False

        numeric_reminder = 0
        for letter in rle:
            #print(letter, "\t\t\t||| x =", x_count, "\t\t\t y =", y_count)
            if not we_already_know_how_wide_this_pattern_is_and_have_no_need_of_further_letter_counting:

                if letter == 'b':
                    if numeric_reminder:  ##### add multiple dead cells
                        x_count += numeric_reminder

                        numeric_reminder = 0

                    else:                   #### add exactly 1 dead cell
                        x_count += 1

                if letter == 'o':
                    if numeric_reminder:  #### add multiple live cells
                        x_count += numeric_reminder
                        numeric_reminder = 0

                    else:               ##### add exactly 1 live cell
                        x_count += 1
            if letter == '$':  # GOTO start of next line
                we_already_know_how_wide_this_pattern_is_and_have_no_need_of_further_letter_counting = True
                if numeric_reminder:
                    y_count += numeric_reminder
                    
                    numeric_reminder = 0
                else:
                    y_count += 1

            if we_already_know_how_wide_this_pattern_is_and_have_no_need_of_further_letter_counting:
                if letter == "b":
                    numeric_reminder = 0
                if letter == "o":
                    numeric_reminder =0
            if letter.isnumeric():  # A loop to log a reminder
                if numeric_reminder:  # A case in which the previous digit was probably decimal
                    numeric_reminder *= 10
                    numeric_reminder += int(letter)
                else:
                    numeric_reminder += int(letter)


            if letter == '!':  # if ! appears, wer'e done
                y_count += 1
        #print("X:",x_count ,"Y:" ,y_count)
        return (x_count,y_count)

    def position_the_pattern(self,rle,r, pos):

        patt =self.transform_rle_to_matrix(rle)

        x0 = pos[1]
        y0 = pos[0]


        board = np.zeros((r,r))
        for y in range(len(patt)):
            for x in range(len(patt[0])):
                board[y + y0][x + x0] = patt[y][x]
        return board


    def transform_rle_to_matrix(self, rle):


        dims =self.comprehend_rle_dims(rle)
        x_size = dims[0]
        y_size = dims[1]


        numeric_reminder = 0
        x = 0
        y = 0
        board = np.zeros((y_size, x_size))
        for letter in rle:

            if letter == 'b':
                if numeric_reminder:  ##### add multiple dead cells

                    for i in range(numeric_reminder):
                        pass
                        x += 1
                    numeric_reminder = 0
                else:  #### add exactly 1 dead cell
                    x += 1

            if letter == 'o':
                if numeric_reminder:  #### add multiple live cells

                    for i in range(numeric_reminder):
                        board[y][x] = 255
                        x += 1
                    numeric_reminder = 0
                else:  ##### add exactly 1 live cell
                    board[y][x] = 255
                    x += 1

            if letter == '$':  # GOTO start of next line
                if numeric_reminder:
                    y += numeric_reminder
                    numeric_reminder = 0
                else:
                    y += 1
                x = 0

            if letter == '!':  # if ! appears, wer'e done
                pass

            if letter.isnumeric():  # A loop to log a reminder
                if numeric_reminder:  # A case in which the previous digit was probably decimal
                    numeric_reminder *= 10
                    numeric_reminder += int(letter)
                else:
                    numeric_reminder += int(letter)
        # raise NotImplementedError
        return board

    def create_board_1(self):
        r = self.size_of_board
        board = np.random.choice([0, 255], r ** 2, p=[0.5, 0.5]).reshape(r, r)

        return board

    def create_board_2(self):
        r = self.size_of_board

        board = np.random.choice((0, 255), r ** 2, p=(0.2, 0.8)).reshape(r, r)

        return board

    def create_board_3(self):
        r = self.size_of_board
        board = np.zeros((r, r))
        with np.nditer(board, op_flags=['readwrite']) as it:  # A loop through all entries
            for x in it:
                x[...] = np.random.choice([0, 255], p=(0.8, 0.2))
        return board

    def create_board_4(self):
        rle = '24bo11b$22bobo11b$12b2o6b2o12b2o$11bo3bo4b2o12b2o$2o8bo5bo3b2o14b$2o8b\
                o3bob2o4bobo11b$10bo5bo7bo11b$11bo3bo20b$12b2o!'
        patt_pos = (10, 10)
        return self.position_the_pattern(rle, self.size_of_board,patt_pos)


if __name__ == '__main__':  # You should keep this line for our auto-grading code.

    size_of_board, board_start_mode, rules, rle, pattern_position = 110 , 1 , "S23/B3" , "7bo6b$6bobo5b$7bo6b2$5b5o4b$\
       4bo5bob2o$3bob2o3bob2o$3bobo2bobo3b$2obo3b2obo3b$2obo5bo4b$4b5o5b2$6bo7b$5bobo6b$6bo!" , (4,13)

    gof = GameOfLife(size_of_board, board_start_mode, rules, rle, pattern_position)

    for i in range(100):
        name = 'hey' + str(i) +'.jpg'

        #print(gof.cell_states)

        gof.update()
        print(i)
        gof.save_board_to_file(name)