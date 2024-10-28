import unittest
from ChessEngine import ChessEngine,Move

class TestChessEngine(unittest.TestCase):
        def __init__(self, methodName: str = "runTest") -> None:
                super().__init__(methodName)
                self.default_board=[
                        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                        ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
                self.custom_board=[
                        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                        ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        
        def test_initiation(self): 
                #test default board
                gamestate=ChessEngine() 
                self.assertEqual(gamestate.board,self.default_board)
                self.assertTrue(gamestate.white_move)
                self.assertEqual(gamestate.ally,"w")
                self.assertEqual(gamestate.enemy,"b")

                #test custom board
                self.custom_board=[
                        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                        ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "wp", "--", "--", "--", "--"],
                        ["wp", "wp", "wp", "--", "wp", "wp", "wp", "wp"],
                        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
                move_history=[Move(6,3,5,3,self.custom_board)]
                gamestate=ChessEngine(board=self.custom_board,white_move=False,move_history=move_history)
                self.assertEqual(gamestate.board,self.custom_board)
                self.assertFalse(gamestate.white_move)
                self.assertEqual(gamestate.white_king_location,(7,4))
                self.assertEqual(gamestate.black_king_location,(0,4))
                self.assertEqual(gamestate.ally,"b")
                self.assertEqual(gamestate.enemy,"w")
                self.assertEqual(gamestate.move_history,move_history)
        def test_pins_checks(self):
                #no pins or checks
                self.custom_board=[
                        ["bb", "--", "--", "wK", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "bN", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "bp", "--", "--", "bR", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "bK", "--", "--", "--", "--"]]
                gamestate=ChessEngine(board=self.custom_board)
                pins,checks=gamestate.pins_checks()
                self.assertEqual(pins,dict())
                self.assertEqual(checks,list())

                #test pins
                self.custom_board=[
                        ["bR", "--", "wQ", "wK", "wQ", "--", "bR", "bQ"],
                        ["--", "--", "wQ", "wQ", "wQ", "--", "--", "--"],
                        ["--", "--", "--", "--", "bp", "--", "--", "--"],
                        ["bB", "--", "--", "--", "--", "--", "bB", "--"],
                        ["--", "--", "--", "bR", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "bK", "--", "--", "--", "--"]]
                gamestate=ChessEngine(board=self.custom_board)
                pins,checks=gamestate.pins_checks()
                self.assertEqual(pins,{(0, 2): (0, -1), (1, 3): (1, 0), (0, 4): (0, 1), (1, 2): (1, -1), (1, 4): (1, 1)})
                self.assertEqual(checks,list())

                #test checks
                self.custom_board=[
                        ["bR", "--", "--", "wK", "--", "--", "bR", "bQ"],
                        ["--", "bN", "--", "--", "bp", "bN", "--", "--"],
                        ["--", "--", "--", "--", "bN", "--", "--", "--"],
                        ["bB", "--", "--", "--", "--", "--", "bB", "--"],
                        ["--", "--", "--", "bR", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "bK", "--", "--", "--", "--"]]
                gamestate=ChessEngine(board=self.custom_board)
                pins,checks=gamestate.pins_checks()
                self.assertEqual(pins,{})
                self.assertEqual(checks,[(0, 0, 0, -1), (4, 3, 1, 0), (0, 6, 0, 1), (3, 0, 1, -1), (1, 5, 1, 2), (2, 4, 2, 1), (1, 1, 1, -2)])

                #test both
                self.custom_board=[
                        ["bR", "--", "wQ", "wK", "--", "--", "bR", "--"],
                        ["--", "--", "wp", "wp", "--", "--", "--", "--"],
                        ["--", "--", "bN", "--", "--", "bN", "--", "--"],
                        ["bB", "--", "--", "--", "--", "--", "bB", "--"],
                        ["--", "--", "--", "bQ", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "bK", "--", "--", "--", "--"]]
                gamestate=ChessEngine(board=self.custom_board)
                pins,checks=gamestate.pins_checks()
                self.assertEqual(pins,{(0, 2): (0, -1), (1, 3): (1, 0), (1, 2): (1, -1)})
                self.assertEqual(checks,[(0, 6, 0, 1), (2, 2, 2, -1)])

        def test_pawn(self):
                #test pawn basic
                self.custom_board=[
                        ["--", "--", "--", "bK", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["wR", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "wR", "wp", "--", "wp", "wR", "bp", "--"],
                        ["wp", "wp", "--", "--", "--", "wp", "--", "wp"],
                        ["--", "--", "--", "wK", "--", "--", "--", "--"]]
                gamestate=ChessEngine(board=self.custom_board)
                test_moves=gamestate.pawn_moves(6,0)
                expected_moves={Move(6,0,5,0,self.custom_board)}
                self.assertEqual(test_moves,expected_moves)

                test_moves=gamestate.pawn_moves(6,1)
                self.assertEqual(test_moves,set())

                test_moves=gamestate.pawn_moves(5,2)
                expected_moves={Move(5,2,4,2,self.custom_board)}
                self.assertEqual(test_moves,expected_moves)

                test_moves=gamestate.pawn_moves(6,5)
                expected_moves={Move(6,5,5,6,self.custom_board)}
                self.assertEqual(test_moves,expected_moves)

                test_moves=gamestate.pawn_moves(6,7)
                #print_move_coordinates(test_moves)
                expected_moves={Move(6,7,5,6,self.custom_board),Move(6,7,5,7,self.custom_board),Move(6,7,4,7,self.custom_board)}
                self.assertEqual(test_moves,expected_moves)

                #test pins and checks
                self.custom_board=[
                        ["--", "--", "--", "--", "bK", "--", "--", "bR"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "bN", "--"],
                        ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                        ["wR","wR", "wR", "wR", "wR", "wR", "wR", "wK"]]
                gamestate=ChessEngine(board=self.custom_board)
                possible_moves=gamestate.legal_moves()
                self.assertEqual(possible_moves,{Move(6,5,5,6,self.custom_board)})

                #test promotion
                self.custom_board=[
                        ["--", "--", "--", "bK", "--", "--", "--", "--"],
                        ["--", "wp", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "wK", "--", "--", "--", "--"]]
                gamestate=ChessEngine(board=self.custom_board)
                possible_moves=gamestate.legal_moves()
                pawn_move=Move(1,1,0,1,self.custom_board)
                self.assertTrue(pawn_move in possible_moves)
                gamestate.make_move(pawn_move)
                board_result=[
                        ["--", "wQ", "--", "bK", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "wK", "--", "--", "--", "--"]]
                self.assertEqual(gamestate.board,board_result)
                self.assertFalse(gamestate.white_move)

                #test enpassant
                previous_move_board=[
                        ["--", "--", "--", "bK", "--", "--", "--", "--"],
                        ["bp", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "wp", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "wK", "--", "--", "--", "--"]]
                self.custom_board=[
                        ["--", "--", "--", "bK", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["bp", "wp", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "wK", "--", "--", "--", "--"]]
                gamestate=ChessEngine(board=self.custom_board,move_history=[Move(1,0,3,0,previous_move_board)])
                possible_moves=gamestate.legal_moves()
                pawn_move=Move(3,1,2,0,self.custom_board)
                self.assertTrue(pawn_move in possible_moves)
                gamestate.make_move(pawn_move)
                board_result=[
                        ["--", "--", "--", "bK", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["wp", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "wK", "--", "--", "--", "--"]]
                #print(gamestate.board)
                self.assertEqual(gamestate.board,board_result)


        def test_bishop_moves(self):
                #basic test
                self.custom_board=[
                        ["--", "--", "--", "wK", "--", "--", "--", "--"],
                        ["--", "wp", "--", "--", "--", "--", "--", "--"],
                        ["wp", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "wB", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "bp", "--", "--"],
                        ["--", "--", "--", "--", "bp", "--", "--", "--"],
                        ["--", "--", "--", "bK", "--", "--", "--", "--"]]
                gamestate=ChessEngine(board=self.custom_board)
                test_moves=gamestate.bishop_moves(4,2)
                answers_list=[[4,2,2,4],[4,2,6,0],[4,2,3,1],[4,2,6,4],[4,2,3,3],[4,2,0,6],[4,2,1,5],[4,2,5,1],[4,2,5,3]]
                expected_moves=build_move_set(answers_list,self.custom_board)
                self.assertEqual(test_moves,expected_moves)
                
                #test with checks and pins
                self.custom_board=[
                        ["--", "--", "wB", "wK", "wB", "--", "--", "--"],
                        ["--", "wp", "wB", "wB", "--", "--", "wB", "--"],
                        ["wp", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "bQ", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "bQ", "--", "bp", "--", "--"],
                        ["--", "--", "--", "--", "bp", "--", "--", "--"],
                        ["--", "--", "--", "bK", "--", "--", "--", "--"]]
                gamestate=ChessEngine(board=self.custom_board)
                test_moves=gamestate.legal_moves()
                #print_move_coordinates(test_moves)
                expected_moves={Move(1,6,2,5,self.custom_board)}
                self.assertEqual(test_moves,expected_moves)
        def test_rook_moves(self):
                #test basic
                self.custom_board=[
                        ["--", "--", "--", "bK", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "bp", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["wp", "--", "--", "--", "--", "wR", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "wK", "--", "--", "--", "--"]]
                gamestate=ChessEngine(board=self.custom_board)
                test_moves=gamestate.rook_moves(4,5)
                answers_list=[[4,5,4,4],[4,5,4,6],[4,5,1,5],[4,5,4,7],[4,5,7,5],[4,5,5,5],[4,5,2,5],[4,5,6,5],[4,5,3,5],[4,5,4,1],[4,5,4,2],[4,5,4,3]]
                expected_moves=build_move_set(answers_list,self.custom_board)
                self.assertEqual(test_moves,expected_moves)
                #test with pins and checks
                self.custom_board=[
                        ["--", "--", "--", "bK", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "wR", "--", "--"],
                        ["--", "--", "--", "bQ", "--", "wR", "--", "--"],
                        ["--", "--", "--", "--", "--", "wR", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "wR", "--", "wR", "--", "--", "--"],
                        ["--", "--", "wR", "wK", "wR", "--", "--", "--"]]
                gamestate=ChessEngine(board=self.custom_board)
                test_moves=gamestate.legal_moves()
                answers_list=[[3,5,3,3],[6,2,6,3],[6,4,6,3],[4,5,4,3]]
                expected_moves=build_move_set(answers_list,self.custom_board)
                self.assertEqual(test_moves,expected_moves)
        def test_knight_moves(self):
                #test basic
                self.custom_board=[
                        ["--", "--", "--", "bK", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "bp", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "wN", "--", "--", "--", "--"],
                        ["--", "bp", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "bp", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "wK", "--", "--", "--", "--"]]
                gamestate=ChessEngine(board=self.custom_board)
                test_moves=gamestate.knight_moves(4,3)
                answers_list=[[4,3,2,2],[4,3,5,5],[4,3,2,4],[4,3,6,2],[4,3,3,1],[4,3,6,4],[4,3,3,5],[4,3,5,1]]
                expected_moves=build_move_set(answers_list,self.custom_board)
                self.assertEqual(test_moves,expected_moves)

                #test with allies in destination
                self.custom_board=[
                        ["--", "--", "--", "bK", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "wp", "--", "wp", "--", "--", "--"],
                        ["--", "wp", "--", "--", "--", "wp", "--", "--"],
                        ["--", "--", "wR", "wN", "bR", "--", "--", "--"],
                        ["--", "wp", "--", "--", "--", "wp", "--", "--"],
                        ["--", "--", "wp", "--", "wp", "--", "--", "--"],
                        ["--", "--", "--", "wK", "--", "--", "--", "--"]]
                gamestate=ChessEngine(board=self.custom_board)
                test_moves=gamestate.knight_moves(4,3)
                self.assertEqual(test_moves,set())

                #test with checks and pins
                self.custom_board=[
                        ["--", "--", "--", "bK", "--", "--", "--", "--"],
                        ["--", "--", "--", "bQ", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "wN", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "wN", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "wN", "--", "wN", "--", "--", "--"],
                        ["--", "--", "wN", "wK", "wN", "--", "--", "--"]]
                gamestate=ChessEngine(board=self.custom_board)
                test_moves=gamestate.legal_moves()
                #print_move_coordinates(test_moves)
                answers_list=[[6,2,4,3],[6,4,4,3],[3,2,1,3],[7,2,5,3],[3,2,5,3],[7,4,5,3]]
                expected_moves=build_move_set(answers_list,self.custom_board)
                self.assertEqual(test_moves,expected_moves)

        def test_king_moves(self):
                # test basic
                self.custom_board=[
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "wK", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "bK", "--", "--", "--", "--"]]
                gamestate=ChessEngine(board=self.custom_board)
                test_moves=gamestate.king_moves(1,3)
                answers_list=[[1,3,1,2],[1,3,1,4],[1,3,2,2],[1,3,2,3],[1,3,2,4],[1,3,0,2],[1,3,0,3],[1,3,0,4]]
                expected_moves=build_move_set(answers_list,self.custom_board)
                self.assertEqual(test_moves,expected_moves)
                self.assertEqual(self.custom_board,gamestate.board)
                test_moves=gamestate.legal_moves() 
                self.assertEqual(test_moves,expected_moves)
                self.assertTrue(gamestate.stalemate)
                self.assertFalse(gamestate.checkmate)

                #test stalemate
                self.custom_board=[
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["bB", "--", "bK", "--", "--", "bp", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "bN", "--"],
                        ["--", "--", "--", "wK", "--", "--", "--", "--"],
                        ["bR", "--", "--", "--", "--", "--", "--", "--"]]
                gamestate=ChessEngine(board=self.custom_board)
                test_moves=gamestate.king_moves(6,3)
                self.assertEqual(test_moves,set())
                test_moves=gamestate.legal_moves()
                self.assertEqual(test_moves,set())
                self.assertTrue(gamestate.stalemate)
                self.assertFalse(gamestate.checkmate)


                #test checkmate
                self.custom_board=[
                        ["--", "--", "--", "bK", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "bR", "--", "--", "--", "--", "--", "--"],
                        ["bR", "--", "--", "wK", "--", "--", "--", "--"]]
                gamestate=ChessEngine(board=self.custom_board)
                test_moves=gamestate.king_moves(7,3)
                self.assertEqual(test_moves,set())
                test_moves=gamestate.legal_moves()
                self.assertEqual(test_moves,set())
                self.assertTrue(gamestate.checkmate)
                self.assertFalse(gamestate.stalemate)

                #test check and movement options
                self.custom_board=[
                        ["--", "--", "--", "bK", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "bp", "--", "--", "--", "bp", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["bR", "--", "--", "wK", "--", "--", "--", "--"]]
                gamestate=ChessEngine(board=self.custom_board)
                test_moves=gamestate.legal_moves()
                #print_move_coordinates(test_moves)
                self.assertEqual(test_moves,{Move(7,3,6,3,self.custom_board)})
        def test_castling(self):
                #test default
                gamestate=ChessEngine(board=self.default_board)
                self.assertEqual(gamestate.can_castle,{"w_king_side":True,"w_queen_side":True,"b_king_side":True,"b_queen_side":True})
                self.assertEqual(gamestate.castle_moves(),set())

                #test senerios
                self.custom_board=[["--", "--", "--", "--", "bK", "--", "--", "--"],
                                ["--", "--", "--", "--", "--", "--", "--", "--"],
                                ["--", "--", "--", "--", "--", "--", "--", "--"],
                                ["--", "--", "--", "--", "--", "--", "--", "--"],
                                ["--", "--", "--", "--", "--", "--", "--", "--"],
                                ["--", "--", "--", "--", "--", "bp", "--", "--"],
                                ["--", "--", "--", "--", "--", "--", "--", "--"],
                                ["--", "--", "--", "--", "wK", "wB", "--", "wR"]]
                gamestate=ChessEngine(board=self.custom_board)
                self.assertEqual(gamestate.castle_moves(),set())
                self.assertEqual(gamestate.can_castle,{'w_king_side': True, 'w_queen_side': False, 'b_king_side': False, 'b_queen_side': False})
                move=Move(7,4,7,3,self.custom_board)
                self.assertTrue(move in gamestate.legal_moves())
                gamestate.make_move(move)
                self.assertEqual(gamestate.can_castle,{'w_king_side': False, 'w_queen_side': False, 'b_king_side': False, 'b_queen_side': False})

                self.custom_board=[["--", "--", "--", "--", "bK", "--", "--", "--"],
                                ["--", "--", "--", "--", "--", "--", "--", "--"],
                                ["--", "--", "--", "--", "--", "--", "--", "--"],
                                ["--", "--", "--", "--", "--", "--", "--", "--"],
                                ["--", "bR", "--", "--", "--", "--", "--", "--"],
                                ["--", "--", "--", "--", "--", "--", "--", "--"],
                                ["--", "--", "--", "--", "--", "--", "--", "--"],
                                ["wR", "--", "--", "--", "wK", "--", "--", "wR"]]
                gamestate=ChessEngine(board=self.custom_board)
                self.assertEqual(gamestate.can_castle,{'w_king_side': True, 'w_queen_side': True, 'b_king_side': False, 'b_queen_side': False})
                move=Move(7,4,7,6,self.custom_board)
                self.assertEqual(gamestate.castle_moves(),{move})
                self.assertTrue(move in gamestate.legal_moves())
                gamestate.make_move(move)
                result_board=[["--", "--", "--", "--", "bK", "--", "--", "--"],
                                ["--", "--", "--", "--", "--", "--", "--", "--"],
                                ["--", "--", "--", "--", "--", "--", "--", "--"],
                                ["--", "--", "--", "--", "--", "--", "--", "--"],
                                ["--", "bR", "--", "--", "--", "--", "--", "--"],
                                ["--", "--", "--", "--", "--", "--", "--", "--"],
                                ["--", "--", "--", "--", "--", "--", "--", "--"],
                                ["wR", "--", "--", "--", "--", "wR", "wK", "--"]]
                self.assertEqual(result_board,gamestate.board)
                self.assertEqual(gamestate.can_castle,{'w_king_side':False, 'w_queen_side': False, 'b_king_side': False, 'b_queen_side': False})
        
        def test_make_move_and_undo(self):
                #test basic
                gamestate=ChessEngine(board=self.default_board)
                move=Move(6,0,4,0,self.default_board)
                self.assertTrue(move in gamestate.legal_moves())
                gamestate.make_move(move)
                result_board=[
                        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                        ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["wp", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
                self.assertEqual(result_board,gamestate.board)
                self.assertEqual(gamestate.move_history[-1],move)
                self.assertFalse(gamestate.white_move)
                self.assertTrue(gamestate.ally,"b")
                self.assertTrue(gamestate.enemy,"w")
                gamestate.undo_move()
                self.assertEqual(self.default_board,gamestate.board)
                self.assertTrue(len(gamestate.move_history)==0)
                self.assertTrue(gamestate.white_move)
                self.assertTrue(gamestate.ally,"w")
                self.assertTrue(gamestate.enemy,"b")
                self.assertTrue(move in gamestate.legal_moves())

                #test promotion
                self.custom_board=[["--", "--", "--", "--", "bK", "--", "--", "--"],
                                ["wp", "--", "--", "--", "--", "--", "--", "--"],
                                ["--", "--", "--", "--", "--", "--", "--", "--"],
                                ["--", "--", "--", "--", "--", "--", "--", "--"],
                                ["--", "--", "--", "--", "--", "--", "--", "--"],
                                ["--", "--", "--", "--", "--", "--", "--", "--"],
                                ["--", "--", "--", "--", "--", "--", "--", "--"],
                                ["wR", "--", "--", "--", "wK", "--", "--", "wR"]]
                gamestate=ChessEngine(board=self.custom_board)
                move=Move(1,0,0,0,self.custom_board)
                self.assertTrue(move in gamestate.legal_moves())
                gamestate.make_move(move)
                result_board=[["wQ", "--", "--", "--", "bK", "--", "--", "--"],
                                ["--", "--", "--", "--", "--", "--", "--", "--"],
                                ["--", "--", "--", "--", "--", "--", "--", "--"],
                                ["--", "--", "--", "--", "--", "--", "--", "--"],
                                ["--", "--", "--", "--", "--", "--", "--", "--"],
                                ["--", "--", "--", "--", "--", "--", "--", "--"],
                                ["--", "--", "--", "--", "--", "--", "--", "--"],
                                ["wR", "--", "--", "--", "wK", "--", "--", "wR"]]
                self.assertEqual(result_board,gamestate.board)
                self.assertEqual(gamestate.move_history[-1],move)
                self.assertFalse(gamestate.white_move)
                self.assertTrue(gamestate.ally,"b")
                self.assertTrue(gamestate.enemy,"w")
                gamestate.undo_move()
                self.assertEqual(self.custom_board,gamestate.board)
                self.assertTrue(len(gamestate.move_history)==0)
                self.assertTrue(gamestate.white_move)
                self.assertTrue(gamestate.ally,"w")
                self.assertTrue(gamestate.enemy,"b")
                self.assertTrue(move in gamestate.legal_moves())

                #test enpassant
                self.custom_board=[
                        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                        ["bp", "--", "bp", "bp", "bp", "bp", "bp", "bp"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "bp", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
                gamestate=ChessEngine(board=self.custom_board)
                move1=Move(6,0,4,0,self.custom_board)
                self.assertTrue(move1 in gamestate.legal_moves())
                gamestate.make_move(move1)

                move1_board=[
                        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                        ["bp", "--", "bp", "bp", "bp", "bp", "bp", "bp"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["wp", "bp", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
                self.assertEqual(move1_board,gamestate.board)
                self.assertEqual(gamestate.move_history[-1],move1)
                self.assertFalse(gamestate.white_move)
                self.assertTrue(gamestate.ally,"b")
                self.assertTrue(gamestate.enemy,"w")

                move2=Move(4,1,5,0,move1_board)
                self.assertTrue(move2 in gamestate.legal_moves())
                gamestate.make_move(move2)

                move2_board=[
                        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                        ["bp", "--", "bp", "bp", "bp", "bp", "bp", "bp"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["bp", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
                self.assertEqual(move2_board,gamestate.board)
                self.assertEqual(gamestate.move_history[-1],move2)
                self.assertTrue(gamestate.white_move)
                self.assertTrue(gamestate.ally,"w")
                self.assertTrue(gamestate.enemy,"b")

                gamestate.undo_move()
                self.assertEqual(move1_board,gamestate.board)
                self.assertEqual(gamestate.move_history[-1],move1)
                self.assertFalse(gamestate.white_move)
                self.assertTrue(gamestate.ally,"b")
                self.assertTrue(gamestate.enemy,"w")
                move2=Move(4,1,5,0,move1_board)
                self.assertTrue(move2 in gamestate.legal_moves())
                
                #test castling
                self.custom_board=[
                        ["bR", "bN", "bB", "bQ", "bK", "--", "--", "bR"],
                        ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                        ["wR", "--", "--", "--", "wK", "wB", "wN", "wR"]]
                gamestate=ChessEngine(board=self.custom_board)
                can_castle_1={"w_king_side":True,"w_queen_side":True,"b_king_side":True,"b_queen_side":True}
                self.assertEqual(gamestate.can_castle,can_castle_1)
                self.assertEqual(gamestate.castle_history[-1],can_castle_1)
                move1=Move(7,4,7,2,self.custom_board)
                self.assertTrue(move1 in gamestate.legal_moves())
                gamestate.make_move(move1)

                move1_board=[
                        ["bR", "bN", "bB", "bQ", "bK", "--", "--", "bR"],
                        ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                        ["--", "--", "wK", "wR", "--", "wB", "wN", "wR"]]
                self.assertEqual(move1_board,gamestate.board)
                self.assertEqual(gamestate.move_history[-1],move1)
                self.assertFalse(gamestate.white_move)
                self.assertTrue(gamestate.ally,"b")
                self.assertTrue(gamestate.enemy,"w")
                can_castle_2={"w_king_side":False,"w_queen_side":False,"b_king_side":True,"b_queen_side":True}
                self.assertEqual(gamestate.can_castle,can_castle_2)
                self.assertEqual(gamestate.castle_history[-1],can_castle_2)
                move2=Move(0,4,0,6,self.custom_board)
                self.assertTrue(move2 in gamestate.legal_moves())
                gamestate.make_move(move2)

                move2_board=[
                        ["bR", "bN", "bB", "bQ", "--", "bR", "bK", "--"],
                        ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                        ["--", "--", "wK", "wR", "--", "wB", "wN", "wR"]]
                #print(gamestate.board)
                self.assertEqual(move2_board,gamestate.board)
                self.assertEqual(gamestate.move_history[-1],move2)
                self.assertTrue(gamestate.white_move)
                self.assertTrue(gamestate.ally,"w")
                self.assertTrue(gamestate.enemy,"b")
                can_castle_3={"w_king_side":False,"w_queen_side":False,"b_king_side":False,"b_queen_side":False}
                self.assertEqual(gamestate.can_castle,can_castle_3)
                self.assertEqual(gamestate.castle_history[-1],can_castle_3)

                gamestate.undo_move()
                self.assertEqual(move1_board,gamestate.board)
                self.assertEqual(gamestate.move_history[-1],move1)
                self.assertFalse(gamestate.white_move)
                self.assertTrue(gamestate.ally,"b")
                self.assertTrue(gamestate.enemy,"w")
                self.assertEqual(gamestate.can_castle,can_castle_2)
                self.assertEqual(gamestate.castle_history[-1],can_castle_2)
                self.assertTrue(move2 in gamestate.legal_moves())

                gamestate.undo_move()
                self.assertEqual(gamestate.can_castle,can_castle_1)
                self.assertEqual(gamestate.castle_history[-1],can_castle_1)
                self.assertTrue(move1 in gamestate.legal_moves())





               

               
      




        

def build_move_set(move_list,board):
    res=set()
    for move in move_list:
        res.add(Move(move[0],move[1],move[2],move[3],board))
    return res


def print_move_coordinates(moves):
    print_list=[]
    for move in moves:
        x="["+str(move.start_row)+","+str(move.start_col)+","+str(move.end_row)+","+str(move.end_col)+"]"
        print_list.append(x)
    res = "["+",".join(print_list)+"]"
    print(res)
    return res
    



if __name__ == '__main__':
    unittest.main()