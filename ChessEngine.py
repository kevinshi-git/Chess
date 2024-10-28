"""
Engine that runs chess logic
"""
import copy
import time
class ChessEngine:
    def __init__(self,board=None,white_move=None,move_history=None):
        
        #first letter in each board element (b or w) represents black or white
        #second letter in each board element represents piece (Q = queen, K = king, etc)
        #'--' is an empty space
        if (board is not None) or (white_move is not None) or (move_history is not None):
            self.test=True
        else:
            self.test=False
        
        if board is not None:
            self.board=board
        else:
            self.board = [
                ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunctions = {"p": self.pawn_moves, "R": self.rook_moves, "N": self.knight_moves, #map pieces to functions that find valid moves
                              "B": self.bishop_moves, "Q": self.queen_moves, "K": self.king_moves}
        if white_move is not None:
            self.white_move=white_move
        else:
            self.white_move=True

        if move_history:
            self.move_history=move_history
        else:
            self.move_history = []
        
        self.can_castle={"w_king_side":True,"w_queen_side":True,"b_king_side":True,"b_queen_side":True} #keeps track of castling eligibility
        dummy=self.update_castle_rights() #update castle rights based on custom __init__
        self.can_castle=dummy
        self.castle_history=[self.can_castle] #history of castle eligiblity per move

        self.ally,self.enemy=self.find_ally_enemy() #colors of the enemy and ally, either "w" or "b" depending on turn 


        self.black_king_location,self.white_king_location = self.get_kings_location() #locations of the 2 kings in the form of (king row, king col)

        self.checkmate = False
        self.stalemate = False
        self.pins = dict() #pieces that are pined
        self.checks = [] #information about pieces that check the king
        self.move_log_file="game_logs/"+str(time.time_ns())+".txt" 
    def is_white_move(self):
        return self.white_move
    def is_checkmate(self):
        return self.checkmate
    def is_stalemate(self):
        return self.stalemate
    def get_board(self):
        return self.board
    def get_current_turn_number(self):
        return len(self.move_history)+1
    
    def make_move(self,move,ai_thinking=False):
        #move pieces 
        if not self.test and not ai_thinking:
            with open(self.move_log_file, "a") as myfile:
                myfile.write(move.move_log()+"\n")

        start_row,start_col,end_row,end_col=move.get_coordinates()
        piece_moved,piece_captured=move.get_pieces()
        enpassant,castle=move.get_special_moves()
        self.board[start_row][start_col] = "--"
        self.board[end_row][end_col] = move.piece_moved

        #pawn promotion
        if (piece_moved=="wp" and end_row==0) or (piece_moved=="bp" and end_row==7):
            self.board[end_row][end_col]=self.ally+"Q"
        
        if enpassant:
            # capture enemy pawn
            self.board[start_row][end_col] = "--"  

        if castle:
            if end_col - start_col == 2:  # king side castle move
                self.board[end_row][end_col - 1] = self.board[end_row][end_col + 1]  # moves the rook to its new square
                self.board[end_row][end_col + 1] = '--'  # erase old rook
            else:  # queen side castle move
                self.board[end_row][end_col + 1] = self.board[end_row][end_col - 2]  # moves the rook to its new square
                self.board[end_row][end_col - 2] = '--'  # erase old rook

        #update history
        self.move_history.append(move)

        #update castling rights
        new_castle_rights=self.update_castle_rights()
        self.castle_history.append(new_castle_rights)
        self.can_castle=new_castle_rights

        #change turn
        self.change_turn()

    def undo_move(self,ai_thinking=False):
        if not self.move_history: #only undo if it is not turn 1
            return
        #get previous move
        move = self.move_history.pop()
        self.castle_history.pop()
        self.can_castle=self.castle_history[-1]

        if not self.test and not ai_thinking: #log move if not test
            with open(self.move_log_file, "a") as myfile:
                myfile.write("undo "+move.move_log()+"\n")

        #get move information
        start_row,start_col,end_row,end_col=move.get_coordinates()
        piece_moved,piece_captured=move.get_pieces()
        enpassant,castle=move.get_special_moves()

        #undo move
        self.board[start_row][start_col] = move.piece_moved
        self.board[end_row][end_col] = move.piece_captured

       

        # undo en passant move
        if enpassant:
            self.board[end_row][end_col] = "--"  # leave landing square blank
            self.board[start_row][end_col] = piece_captured
        
        #undo castling 
        if castle:
            if end_col - start_col == 2:  # undo king side castle
                self.board[end_row][end_col + 1] = self.board[end_row][end_col - 1]
                self.board[end_row][end_col - 1] = '--'
            else:  # undo queen side castle
                self.board[end_row][end_col - 2] = self.board[end_row][end_col + 1]
                self.board[end_row][end_col + 1] = '--'
        #change turn
        self.change_turn()
        self.checkmate = False
        self.stalemate = False

    def update_castle_rights(self): #checks if rooks/king have been moved or captured. This determines if you can castle
        new_can_castle=copy.deepcopy(self.can_castle)
        if self.board[0][0]!="bR" or self.board[0][4]!="bK":
            new_can_castle["b_queen_side"]=False
        if self.board[0][7]!="bR" or self.board[0][4]!="bK":
            new_can_castle["b_king_side"]=False 
        if self.board[7][0]!="wR" or self.board[7][4]!="wK":
            new_can_castle["w_queen_side"]=False
        if self.board[7][7]!="wR" or self.board[7][4]!="wK":
            new_can_castle["w_king_side"]=False 
        #print("updated ", new_can_castle)
        return new_can_castle
        
    def legal_moves(self): #gets all legal options for user
        moves = set()
        self.pins, self.checks = self.pins_checks()
        if self.white_move:
            king_row,king_col=self.white_king_location
        else:
            king_row,king_col=self.black_king_location
        if len(self.checks)>=2: #king checked from multiple angles, only option is to move king
            moves.update(self.king_moves(king_row,king_col))
        else:   #king is either checked by one piece or not checked at all
            valid_squares = set()  # squares that pieces are allowed to move to. Only filled when king is in check
            if len(self.checks)==1: #only 1 check
                check = self.checks[0]  # check information
                check_row = check[0]
                check_col = check[1]
                direction=(check[2],check[3])
                piece_checking = self.board[check_row][check_col]
                # if knight is the checking piece, must capture the knight or move your king because you can't block a knight
                if piece_checking[1] == "N":
                    valid_squares.add((check_row, check_col))
                else:
                    for i in range(1, 8):
                        valid_square = (king_row + direction[0] * i,
                                        king_col + direction[1] * i)  
                        valid_squares.add(valid_square) #get squares that pieces have to move to stop the check
                        if valid_square[0] == check_row and valid_square[1] == check_col:  # once you get to checking piece
                            break

            for row in range(len(self.board)): #get all possible moves regardless of checks and pins
                for col in range(len(self.board[row])):
                    color = self.board[row][col][0]
                    if (color == "w" and self.white_move) or (color == "b" and not self.white_move):
                        piece = self.board[row][col][1]
                        moves.update(self.moveFunctions[piece](row, col))

            moves_filtered=set()
            for move in moves: #filter moves that satisfy check and pin conditions
                move_dir_row,move_dir_col=move.get_direction()
                move_start_row,move_start_col,move_end_row,move_end_col=move.get_coordinates()
                piece,_=move.get_pieces()
                #print(move_start_row,move_start_col,move_end_row,move_end_col,piece)

                if piece[1]=="K": #checks if piece is king because king is special and has already been filtered by checks/pins in king_moves function
                    moves_filtered.add(move)
                    continue
                if (move_start_row,move_start_col) in self.pins: #check if this move is invalid becasue of pins
                    pin_direction=self.pins[(move_start_row,move_start_col)]
                    if (move_dir_row,move_dir_col)!=pin_direction and (-1* move_dir_row,-1 *move_dir_col)!=pin_direction:
                        continue
                if valid_squares and (move_end_row,move_end_col) not in valid_squares: #checks if piece cannot protect king in case of check
                    continue
                moves_filtered.add(move)
            moves=moves_filtered
           
            if len(self.checks)==0: #no checks
                castle_moves=self.castle_moves() #get castle moves
                moves.update(castle_moves)

        if len(moves) == 0:
            if len(self.checks)>0:
                self.checkmate = True
            else:
                self.stalemate = True
        elif self.only_kings(): #stalemate because kings just move around doing nothing and that's pointless
            self.checkmate = False
            self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False  
        return moves
    
    def is_square_safe(self,row,col): #checks if square can be taken by enemy piece
            if self.ally=="w":
                king_row=self.white_king_location[0]
                king_col=self.white_king_location[1]
            else:
                king_row=self.black_king_location[0]
                king_col=self.black_king_location[1]
            
            #swapes king position with position of square in question
            capture_piece=self.board[row][col]
            self.board[row][col]=self.ally+"K"
            self.board[king_row][king_col]="--"
            self.black_king_location,self.white_king_location = self.get_kings_location()

            _, checks=self.pins_checks() #reuses pins_checks function to determine if square is dangerous
            self.board[king_row][king_col]=self.ally+"K"
            self.board[row][col]=capture_piece
            self.black_king_location,self.white_king_location = self.get_kings_location()
            if checks: #if putting the king into this square puts the king in danger, it is not a safe square
                return False
            else:
                return True
    def castle_moves(self): #gets all possible castling moves (if possible)
        moves=set()        
        row=0 if self.ally=="b" else 7
        #check king side castle
        if self.can_castle[self.ally+"_king_side"]: #check if we have not moved king and rook
            if self.board[row][5]=="--" and self.board[row][6]=="--": #check if space is empty
                is_space_safe=True #check if empty spaces are in direct line of attack from enemy
                for col in range(5,7):
                   is_space_safe=is_space_safe and self.is_square_safe(row,col)    
                if is_space_safe:
                    moves.add(Move(row,4,row,6,self.board))
        #check queen side castle
        if self.can_castle[self.ally+"_queen_side"]: #check if we have not moved king and rook
            if self.board[row][1]=="--" and self.board[row][2]=="--" and self.board[row][3]: #check if space is empty
                is_space_safe=True #check if empty spaces are in direct line of attack from enemy
                for col in range(1,4):
                    is_space_safe=is_space_safe and self.is_square_safe(row,col)    
                if is_space_safe:
                    moves.add(Move(row,4,row,2,self.board))
        return moves

    def only_kings(self): #checks if only kings are on the board
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col][1]!="K" and self.board[row][col]!="--":
                    return False
        return True
    def pins_checks(self): #looks for pieces that pinned and checking king
        pins=dict() # key = (pined row, pined col) : value = (direction row, direction col)
        checks=[]
        if self.white_move:
            king_row,king_col=self.white_king_location
        else:
            king_row,king_col=self.black_king_location
        
        up_down_left_right=[(-1, 0), (0, -1), (1, 0), (0, 1)]
        up_diag=[(-1, -1), (-1, 1)]
        down_diag=[(1, -1), (1, 1)]
        directions = up_down_left_right+up_diag+down_diag
        for direction in directions:
            potential_pin = ()  # a pineed piece that we will confirm if actually pinned later
            for i in range(1, 8):
                end_row = king_row + direction[0] * i
                end_col = king_col + direction[1] * i
                if self.out_of_bounds(end_row,end_col): #out of bounds
                    break
                end_piece= end_piece = self.board[end_row][end_col]
                if end_piece[0] == self.ally and end_piece[1] != "K": 
                    if potential_pin == ():  # first allied piece that could be pinned
                        potential_pin = (end_row, end_col, direction[0], direction[1])
                    else:  # 2nd allied piece - no check or pin from this direction
                        break
                elif end_piece[0] == self.enemy:
                    enemy_piece = end_piece[1]
                    #check if enemy piece can attack king from this position
                    
                    if (direction in up_down_left_right and enemy_piece == "R") or ((direction in down_diag or direction in up_diag) and enemy_piece == "B") or (i == 1 and enemy_piece == "p" 
                        and ((self.enemy == "w" and direction in down_diag) or (self.enemy == "b" and direction in up_diag))) or (
                            enemy_piece == "Q") or (i == 1 and enemy_piece == "K"):
                        if potential_pin == ():  # no piece blocking, so king in check
                            checks.append((end_row, end_col, direction[0], direction[1]))
                            break
                        else:  # piece blocking enemy from attacking king so pin
                            pins[(potential_pin[0],potential_pin[1])]=(potential_pin[2],potential_pin[3])
                            break
                    else:  # enemy piece not threatening king
                        break
        # look for knight checks
        knight_moves = [(-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2)]
        for move_row,move_col in knight_moves:
            end_row = king_row + move_row
            end_col = king_col + move_col
            if self.out_of_bounds(end_row,end_col):
                continue
            end_piece = self.board[end_row][end_col]
            if end_piece[0] == self.enemy and end_piece[1] == "N":  # enemy knight attacking king
                checks.append((end_row, end_col, move_row, move_col))
        return pins, checks

    def change_turn(self):
        self.black_king_location,self.white_king_location = self.get_kings_location()
        self.white_move=not self.white_move
        self.ally,self.enemy=self.find_ally_enemy()
    def find_ally_enemy(self): # returns ally,enemy based on color
        if self.white_move:
            return "w","b"
        else:
            return "b","w"
    def out_of_bounds(self,row,col): #check if piece is out of bounds
        return not ((0<=row<=7) and (0<=col<=7))
    def get_kings_location(self): #finds coordinates of both kings
        black_king_location=()
        white_king_location=()
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col]=="bK":
                    if black_king_location==():
                        black_king_location=(row,col)
                    else:
                        print(self.board)
                        raise Exception("multiple black kings"+" bk:"+str(black_king_location)+" wk: "+str(white_king_location))

                if self.board[row][col]=="wK":
                    if white_king_location==():
                        white_king_location=(row,col)
                    else:
                        print(self.board)
                        raise Exception("multiple white kings"+" bk:"+str(black_king_location)+" wk: "+str(white_king_location))

        if not black_king_location or not white_king_location:
            for row in self.board:
                print(row)
            print(self.pins)
            print(self.checks)
            
            raise Exception("Could not locate kings"+" bk:"+str(black_king_location)+" wk: "+str(white_king_location))
        return black_king_location,white_king_location
    
    def pawn_moves(self,start_row,start_col): #finds possible pawn move regardless of pins/checks
        moves=set()
        if self.white_move:
            sign=-1
        else:
            sign=1
        
        if (self.white_move and start_row==6) or (not self.white_move and start_row==1): #check if pawn can move up 2 spaces
            new_row=start_row+sign*2
            new_col=start_col
            if self.board[new_row][new_col]=="--" and self.board[new_row-sign][new_col]=="--":
                moves.add(Move(start_row,start_col,new_row,new_col,self.board))
        
        #check if pawn can move up 1
        new_row=start_row+sign 
        new_col=start_col
        if not self.out_of_bounds(new_row,new_col) and self.board[new_row][new_col]=="--":
            moves.add(Move(start_row,start_col,new_row,new_col,self.board))
        
        #check en passant
        enpassant_square=()
        if self.move_history: #check if this is not the first turn
            previous_move=self.move_history[-1]
            enpassant,castle=previous_move.get_special_moves()
            if not enpassant and not castle: #check if previous move was a special move
                prev_start_row,prev_start_col,prev_end_row,prev_end_col=previous_move.get_coordinates()
                moved_piece,captured_piece=previous_move.get_pieces()
                if moved_piece==self.enemy+"p": #check if previous move was a pawn
                    if (self.enemy=="w" and prev_start_row==6 and prev_end_row==4) or (self.enemy=="b" and prev_start_row==1 and prev_end_row==3): #check if previous move was a pawn 2 step move
                        if self.board[prev_end_row+sign][prev_end_col]=="--": #check if there is anything behind pawn
                            enpassant_square=(prev_end_row+sign,prev_end_col) #potential enpassant


        #check diagnal moves
        directions=[(sign,-1),(sign,1)]
        for row_d,col_d in directions:
            new_row=start_row+row_d
            new_col=start_col+col_d
            if not self.out_of_bounds(new_row,new_col):
                if self.board[new_row][new_col][0]==self.enemy: #if enemy, diagnal capture
                    moves.add(Move(start_row,start_col,new_row,new_col,self.board))
                if self.board[new_row][new_col]=="--" and (new_row,new_col)==enpassant_square:    #enpassant 
                    moves.add(Move(start_row,start_col,new_row,new_col,self.board))

        return moves

    def bishop_moves(self,start_row,start_col): #finds possible bishop move regardless of pins/checks
        directions=((1,1),(1,-1),(-1,1),(-1,-1)) #diagnal vectors
        moves=set()
        for row_d,col_d in directions: 
            for i in range(1,8):
                new_row=start_row+i*row_d
                new_col=start_col+i*col_d
                if self.out_of_bounds(new_row,new_col) or self.board[new_row][new_col][0]==self.ally:
                    break
                moves.add(Move(start_row,start_col,new_row,new_col,self.board))
                if self.board[new_row][new_col][0]==self.enemy:
                    break
        return moves

    def knight_moves(self,start_row,start_col):#finds possible knight move regardless of pins/checks
        moves=set()
        directions = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2),
                        (1, -2))
        for row_d,col_d in directions:
            new_row=start_row+row_d
            new_col=start_col+col_d
            if self.out_of_bounds(new_row,new_col) or self.board[new_row][new_col][0]==self.ally: 
                continue
            moves.add(Move(start_row,start_col,new_row,new_col,self.board))
        return moves

    def rook_moves(self,start_row,start_col): #finds possible rook move regardless of pins/checks
        moves=set()
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))   #horizontal and vertical vectors
        for row_d,col_d in directions:
            for i in range(1,8):
                new_row=start_row+i*row_d
                new_col=start_col+i*col_d
                if self.out_of_bounds(new_row,new_col) or self.board[new_row][new_col][0]==self.ally:
                    break
                moves.add(Move(start_row,start_col,new_row,new_col,self.board))
                if self.board[new_row][new_col][0]==self.enemy:
                    break
        return moves

    def queen_moves(self,start_row,start_col): #finds possible queen move regardless of pins/checks
        moves=set()
        moves.update(self.rook_moves(start_row,start_col))
        moves.update(self.bishop_moves(start_row,start_col))
        return moves

    def king_moves(self,start_row,start_col): #finds all king moves, need to account for checks because king is special -_-
        directions=((-1, -1), (-1, 1), (1, 1), (1, -1),(-1, 0), (0, -1), (1, 0), (0, 1)) #all possible moves
        moves=set()
        for row_d,col_d in directions:
            new_row=start_row+row_d
            new_col=start_col+col_d
            if self.out_of_bounds(new_row,new_col) or self.board[new_row][new_col][0]==self.ally: #check if out of bounds or ally piece
                continue
            if self.is_square_safe(new_row,new_col): #check if moving to new square would put king in danger
                moves.add(Move(start_row,start_col,new_row,new_col,self.board))
        return moves


class Move: #holds information about 1 possible move
    def __init__(self, start_row, start_col,end_row,end_col, board):
        self.start_row =  start_row
        self.start_col = start_col
        self.end_row = end_row
        self.end_col = end_col
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.moveID = self.start_row*1000 + self.start_col*100 + self.end_row*10 + self.end_col #unique id for each move
        self.direction=self.calc_direction()
        
        #check if move is a special move
        self.castle=False
        self.enpassant=True if self.piece_moved[1]=="p" and self.piece_captured=="--" and self.start_col!=self.end_col else False
        self.castle=True if self.piece_moved[1]=="K" and abs(self.start_col-self.end_col)>=2 else False
        if self.enpassant:
            self.piece_captured = "wp" if self.piece_moved == "bp" else "bp"
    def get_special_moves(self):
        return self.enpassant, self.castle
    def get_direction(self):
        return self.direction
    def get_coordinates(self):
        return self.start_row,self.start_col,self.end_row,self.end_col
    def get_pieces(self):
        return self.piece_moved,self.piece_captured
    
    def calc_direction(self): #gets vector for direction of move in the forum of (row,col) row or col can either be 1,0, or -1 unless its a knight, then it can be -2 or 2
        row_diff=self.end_row-self.start_row
        col_diff=self.end_col-self.start_col
        if self.piece_moved[1]=="N":
            return row_diff,col_diff
        
        if row_diff>0:
            row_dir=1
        elif row_diff<0:
            row_dir=-1
        else:
            row_dir=0
        
        if col_diff>0:
            col_dir=1
        elif col_diff<0:
            col_dir=-1
        else:
            col_dir=0
        return row_dir,col_dir

    def print_data(self): #print information for debugging
        data="["+str(self.start_row)+","+str(self.start_col)+","+str(self.end_row)+","+str(self.end_col)+"]"
        print(data)
        return data
    def move_log(self):
        return str(self.start_row)+","+str(self.start_col)+","+str(self.end_row)+","+str(self.end_col)
    def __eq__(self, other): #override equals method to compare move class to another move class
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    def __hash__(self): #used to put moves into data structures like hashmaps and sets
        return self.moveID
