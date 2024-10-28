"""
Main file used to display board and handle inputs 
"""

import ChessEngine, ChessAI
import sys
from multiprocessing import Process, Queue
import pygame


"""
------------------------------------parameters------------------------------------------------------
"""

light_color=pygame.Color("white")
dark_color=pygame.Color("pink")

#image_file="cool_images/"
image_file="images/"

player_one = False  # True: White is Player, False: White is AI
player_two = False # True: Black is Player, False: Black is AI

"""
------------------------------------parameters------------------------------------------------------
"""

class ChessGame:
    def __init__(self,light_color,dark_color,image_file,player_one,player_two):
        self.light_color=light_color
        self.dark_color=dark_color
        self.image_file=image_file
        self.player_one=player_one
        self.player_two=player_two
                
        self.board_length = 700

        self.squares_per_row = 8
        self.square_size = self.board_length // self.squares_per_row
        self.images = {}
        self.pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
        for piece in self.pieces: #loads chess images
            self.images[piece] = pygame.transform.scale(pygame.image.load(image_file + piece + ".png"), (self.square_size, self.square_size))
        self.game_state = ChessEngine.ChessEngine()
        self.ai=ChessAI.ChessAI()

    def run_game(self): #function we call to start the game
        legal_moves = self.game_state.legal_moves()
        current_square_selected = ()  # last square clicked (row,col)
        player_clicks = []  # list of current_square_selected

        # keeps track of game state
        game_over = False
        ai_currently_thinking = False
        move_made = False  

        pygame.init()
        screen = pygame.display.set_mode((self.board_length, self.board_length+50))

        while True: 
            screen.fill(pygame.Color("white"))

            human_turn = (self.game_state.is_white_move() and player_one) or (not self.game_state.is_white_move() and player_two)
            
            # AI move finder
            if not game_over and not human_turn:
                if not ai_currently_thinking:
                    ai_currently_thinking = True
                    return_queue = Queue()  
                    move_finder_process = Process(target=self.ai.find_move, args=(self.game_state, legal_moves, return_queue))
                    move_finder_process.start()

                if not move_finder_process.is_alive(): #if ai is finished making move
                    ai_move = return_queue.get() #get move
                    if ai_move is None: #in case there is no move
                        ai_move = self.ai.random_move(legal_moves)
                    #ai_move.print_data()
                    self.game_state.make_move(ai_move) #make move
                    move_made = True
                    ai_currently_thinking = False
        
            for e in pygame.event.get(): #for user inputs
                if e.type == pygame.QUIT: #when user presses the x in the top right corner
                    if ai_currently_thinking:
                            move_finder_process.terminate()
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.MOUSEBUTTONDOWN and not game_over and human_turn:  # mouse handler
                    location = pygame.mouse.get_pos()  # (x, y) location of the mouse
                    col = location[0] // self.square_size
                    row = location[1] // self.square_size
                    #print(location,row,col)
                    if current_square_selected == (row, col) or col >= 8 or row>=8:  # user clicked the same square twice or clicked out of bounds
                        current_square_selected = ()  # deselect
                        player_clicks = []  # clear clicks
                    else:
                        current_square_selected = (row, col)
                        player_clicks.append(current_square_selected)  # append for both 1st and 2nd click

                    if len(player_clicks) == 2 and human_turn:  # after 2nd click
                        move = ChessEngine.Move(player_clicks[0][0], player_clicks[0][1],player_clicks[1][0],player_clicks[1][1], self.game_state.board)
                        if move in legal_moves: #make move if legal
                            self.game_state.make_move(move)
                            move_made = True
                            current_square_selected = ()  # reset user clicks
                            player_clicks = []

                        else: #if can't make move, make the current square clicked the first square
                            player_clicks = [current_square_selected]

                # key handler
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_z:  # undo when z is pressed
                        self.game_state.undo_move()
                        move_made = True
                        game_over = False
                    if e.key == pygame.K_r:  # reset the game when r is pressed
                        self.game_state = ChessEngine.ChessEngine()
                        legal_moves = self.game_state.legal_moves()
                        current_square_selected = ()
                        player_clicks = []
                        move_made = False
                        game_over = False
                    
                    if e.key==pygame.K_r or e.key==pygame.K_z: #ai handler when key is pressed
                        if ai_currently_thinking:
                            move_finder_process.terminate()
                            ai_currently_thinking = False

            if move_made:
                legal_moves = self.game_state.legal_moves()
                move_made = False
            
            #visualize game screen
            self.visualize_board(screen, self.game_state, legal_moves, current_square_selected)
            self.visualize_turn_text(screen)

            if self.game_state.is_checkmate():
                game_over = True
                if self.game_state.is_white_move():
                    self.visualize_end_text(screen, "Black wins by checkmate")
                else:
                    self.visualize_end_text(screen, "White wins by checkmate")
            elif self.game_state.is_stalemate():
                game_over = True
                self.visualize_end_text(screen, "Stalemate")
            
            pygame.display.flip() #update game screen

    def visualize_board(self,screen, game_state, valid_moves, square_selected): #draws board and pieces
        board=game_state.get_board()
        for row in range(self.squares_per_row): #draw squares on board
            for column in range(self.squares_per_row):
                if ((row + column) % 2): #get color for square
                    color=self.light_color
                else:
                    color=self.dark_color
                pygame.draw.rect(screen, color, pygame.Rect(column * self.square_size, row * self.square_size, self.square_size, self.square_size))
        
        if square_selected: #highlight move options for selected square
            row, col = square_selected
            
            piece=board[row][col]
            white_move=game_state.is_white_move()
            if (piece[0]=="w" and white_move) or (piece[0]=="b" and not white_move): # square_selected has a piece for team that can move

                # highlight selected square
                s = pygame.Surface((self.square_size, self.square_size)) #create highlight square
                s.set_alpha(100)  # transparency value 0=transparent, 255=can't see through
                s.fill(pygame.Color('blue'))
                screen.blit(s, (col * self.square_size, row * self.square_size)) #overlay highlight square on board
                
                # highlight moves from that square
                s.fill(pygame.Color('yellow')) #create highlight square
                for move in valid_moves:#overlay highlight square on board
                    if move.start_row == row and move.start_col == col:
                        screen.blit(s, (move.end_col * self.square_size, move.end_row * self.square_size))
        
        for row in range(self.squares_per_row): # draw pieces on top of squares
            for column in range(self.squares_per_row):
                piece = board[row][column]
                if piece != "--":
                    screen.blit(self.images[piece], pygame.Rect(column * self.square_size, row * self.square_size, self.square_size, self.square_size))

        
    def visualize_end_text(self,screen, text): #colors for text that pops up in endgame senerios
        font = pygame.font.SysFont("Times New Roman", 32, True, False)
        text_object = font.render(text, False, pygame.Color("black"))

        #move text to middle of board
        text_row=self.board_length / 2 - text_object.get_width() / 2
        text_col=self.board_length / 2 - text_object.get_height() / 2
        text_location = pygame.Rect(0, 0, self.board_length, self.board_length).move(text_row,text_col)
        screen.blit(text_object, text_location)
        
    def visualize_turn_text(self,screen): #text for bottom of chess board
        
        #get the text that will be displayed
        current_turn_number=self.game_state.get_current_turn_number()
        turn_color="White" if current_turn_number%2==1 else "Black"
        text="Turn "+str(current_turn_number)+": "+turn_color
        if (not self.player_one and current_turn_number%2==1) or (not self.player_two and current_turn_number%2==0):
            text+=" (AI)"
        
        font = pygame.font.SysFont("Times New Roman", 32, True, False)
        text_object = font.render(text, False, pygame.Color("black"))
        #move text to bottom center
        text_location = pygame.Rect(0, 0, self.board_length, self.board_length).move(self.board_length/2 -text_object.get_width() / 2,self.board_length)
        screen.blit(text_object, text_location)

if __name__ == '__main__':
   
    chess=ChessGame(light_color,dark_color,image_file,player_one,player_two)
    chess.run_game()