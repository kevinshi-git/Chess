import random
class ChessAI():
    def __init__(self):
        self.piece_value = {"K": 90, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1} #values of pieces 

        #how valuable each piece is when on certain parts of board
        self.knight_scores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                        [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                        [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                        [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                        [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                        [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                        [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                        [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

        self.bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                        [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                        [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                        [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                        [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                        [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                        [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                        [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

        self.rook_scores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                    [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
                    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                    [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

        self.queen_scores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                        [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                        [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                        [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                        [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                        [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                        [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                        [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

        self.pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
                    [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
                    [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
                    [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
                    [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
                    [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
                    [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
                    [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

        self.location_scores = {"wN": self.knight_scores,
                                "bN": self.knight_scores[::-1],
                                "wB": self.bishop_scores,
                                "bB": self.bishop_scores[::-1],
                                "wQ": self.queen_scores,
                                "bQ": self.queen_scores[::-1],
                                "wR": self.rook_scores,
                                "bR": self.rook_scores[::-1],
                                "wp": self.pawn_scores,
                                "bp": self.pawn_scores[::-1]}
        self.check_mate = 1000 #checkmate score
        self.stalemate = 0 #stalemate score
        self.max_depth = 3 #max depth of minmax algorithm
        self.next_move=None
        
    def random_move(self,legal_moves): #returns random move
        legal_moves=list(legal_moves)
        return random.choice(legal_moves)
    
    def find_move(self,game_state, legal_moves, return_queue): #finds the best possible move
        self.next_move = None
        legal_moves=list(legal_moves)
        random.shuffle(legal_moves) #shuffles list of moves so we don't choose same move for every situation
        self.findMoveAlphaBeta(game_state, legal_moves, 0, float("-inf"), float("inf"))
        return_queue.put(self.next_move)


    def findMoveAlphaBeta(self,game_state, valid_moves, current_depth, alpha, beta): #
        if current_depth == self.max_depth: 
            return self.calc_score(game_state)
    
        if game_state.is_white_move(): #white chooses highest scoring move
            #best = -1*self.check_mate
            best=float("-inf")
            for move in valid_moves: 
                game_state.make_move(move,ai_thinking=True)
                next_moves = game_state.legal_moves()
                current_score=self.findMoveAlphaBeta(game_state, next_moves, current_depth+1, alpha, beta)
                game_state.undo_move(ai_thinking=True)
                if current_score > best:
                    best = current_score
                    if current_depth == 0:
                        self.next_move = move
                alpha = max(alpha, best) 
                # Alpha Beta Pruning 
                if beta <= alpha: 
                    break
            return best 
        else: #black chooses lowest scoring move
            #best = self.check_mate
            best=float("inf")
            for move in valid_moves: 
                game_state.make_move(move,ai_thinking=True)
                next_moves = game_state.legal_moves()
                current_score=self.findMoveAlphaBeta(game_state, next_moves, current_depth+1, alpha, beta)
                game_state.undo_move(ai_thinking=True)
                if current_score < best:
                    best = current_score
                    if current_depth == 0:
                        self.next_move = move
                beta=min(beta,best)
                # Alpha Beta Pruning 
                if beta <= alpha: 
                    break
            return best 


    def calc_score(self,game_state): #calculates the score of a board
        if game_state.is_checkmate():
            if game_state.is_white_move():
                return -1*self.check_mate  # black wins
            else:
                return self.check_mate  # white wins
        elif game_state.is_stalemate():
            return self.stalemate
        score = 0
        board=game_state.get_board()
        for row in range(len(board)):
            for col in range(len(board[row])):
                piece = board[row][col]
                if piece != "--": #get piece score 
                    piece_position_score = 0 if piece[1] == "K" else self.location_scores[piece][row][col]
                    if piece[0] == "w":
                        score += (self.piece_value[piece[1]] + piece_position_score)
                    if piece[0] == "b":
                        score -= (self.piece_value[piece[1]] + piece_position_score)
                    #print(row,col,piece,score)
        return score
    
