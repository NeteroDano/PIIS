import chess
import random

def material_balance(board: chess.Board()):
    white = board.occupied_co[chess.WHITE]
    black = board.occupied_co[chess.BLACK]
    return (
        chess.popcount(white & board.pawns) - chess.popcount(black & board.pawns) +
        3 * (chess.popcount(white & board.knights) - chess.popcount(black & board.knights)) +
        3 * (chess.popcount(white & board.bishops) - chess.popcount(black & board.bishops)) +
        5 * (chess.popcount(white & board.rooks) - chess.popcount(black & board.rooks)) +
        9 * (chess.popcount(white & board.queens) - chess.popcount(black & board.queens))
    )

def numberOFPieces(board: chess.Board(), turnToMove: int):
    if turnToMove == 1:
        chosen = board.occupied_co[chess.WHITE]
    else:
        chosen = board.occupied_co[chess.BLACK]
    return (
        chess.popcount(chosen & board.pawns) +
        (chess.popcount(chosen & board.knights)) +
        (chess.popcount(chosen & board.bishops)) +
        (chess.popcount(chosen & board.rooks)) +
        (chess.popcount(chosen & board.queens))
    )

def evaluationFunction(board: chess.Board(), turnToMove: int):
    numberOfWhite = numberOFPieces(board, 1)
    numberOfBlack = numberOFPieces(board, -1)
    materialBalance = material_balance(board)
    return materialBalance * (numberOfWhite - numberOfBlack) * turnToMove

def negaMax(board: chess.Board(), depth: int, turnToMove: int) -> tuple:
    if depth == 0:
        return evaluationFunction(board, turnToMove), 0
    maxScore = float("-inf")
    bestMove = ''
    for legalMove in board.legal_moves:
        score = -(negaMax(board, depth - 1, -turnToMove)[0])
        if score == 0:
            score = random.random()
        if score > maxScore:
            maxScore = score
            bestMove = legalMove
    return maxScore, bestMove

def negaScout(depth: int, whoToMove: int, alpha: int, beta: int) -> tuple:
    if depth == 0:
        return evaluationFunction(whoToMove), 0
    bestMove = None
    for legalMove in board.legal_moves:
        score = -(negaScout(depth - 1, -whoToMove, -beta, -alpha)[0])
        if score > alpha and score < beta and depth > 1:
            score2 = -(negaScout(depth - 1, -whoToMove, -beta, -score))[0]
            score = max(score, score2)
        if score == 0:
            score = random.random()
        if score > alpha:
            alpha = score
            bestMove = legalMove
        if alpha >= beta:
            return alpha, bestMove
        beta = alpha + 1
    return alpha, bestMove

def PVC(depth: int, whoToMove: int, alpha: int, beta: int) -> tuple:
    if depth == 0:
        return evaluationFunction(whoToMove), None
    bestMove = None
    for legalMove in board.legal_moves:
        score = -(PVC(depth - 1, -whoToMove, -beta, -alpha)[0])
        if (score > alpha) and (score < beta):
            score = -(PVC(depth - 1, -whoToMove, -beta, -score))[0]
        if score == 0:
            score = random.random()
        if score > alpha:
            alpha = score
            bestMove = legalMove
        if alpha >= beta:
            return alpha, bestMove
        beta = alpha + 1
    return alpha, bestMove

board = chess.Board()
depth, turnToMove = 5, -1
algo = input(
    "Enter 1 to play against NegaMax, 2 to play against NegaScout, 3 to play against PVC: ")

while not board.is_mate():
    print("Game state:\n")
    print(board)
    move = input("Input your move: ")
    board.push_fig(move)
    if algo == "1":
        negaMove = negaMax(board, depth, turnToMove)[1]
    elif algo == "2":
        negaMove = negaScout(board, depth, turnToMove)[1]
    else:
        negaMove = PVC(board, depth, turnToMove)[1]
    board.push(negaMove)