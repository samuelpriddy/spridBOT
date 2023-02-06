import threading
import berserk
import chess

# Useful Websites
# https://berserk.readthedocs.io/en/master/usage.html
# https://lichess.org/api#tag/Bot
## https://python-chess.readthedocs.io/en/latest/

token = 'lip_e8lT0QKAbYWOx2RQc7Py'
session = berserk.TokenSession(token)
client = berserk.Client(session=session)

def findPointDifferential(board):
    whiteSum = 0
    blackSum = 0
    whiteSum += len(list(board.pieces(1, True)))
    whiteSum += len(list(board.pieces(2, True))) * 3
    whiteSum += len(list(board.pieces(3, True))) * 3
    whiteSum += len(list(board.pieces(4, True))) * 5
    whiteSum += len(list(board.pieces(5, True))) * 9
    blackSum += len(list(board.pieces(1, False)))
    blackSum += len(list(board.pieces(2, False))) * 3
    blackSum += len(list(board.pieces(3, False))) * 3
    blackSum += len(list(board.pieces(4, False))) * 5
    blackSum += len(list(board.pieces(5, False))) * 9
    return whiteSum - blackSum

def findBestMove(board, color):
    bestMove = None
    bestMovePointDiff = None

    for move in board.legal_moves:
        board.push(move)
        pointDiff = findPointDifferential(board)
        if(bestMove == None): 
            bestMove = move
            bestMovePointDiff = pointDiff
        elif(color == 'white' and pointDiff > bestMovePointDiff):
            bestMove = move
            bestMovePointDiff = pointDiff
        elif(color == 'black' and pointDiff < bestMovePointDiff):
            bestMove = move
            bestMovePointDiff = pointDiff
        board.pop()

    return bestMove
        


class Game(threading.Thread):
    lastMove = ''
    board = chess.Board()

    def __init__(self, client, game_id, color, **kwargs):

        super().__init__(**kwargs)

        self.game_id = game_id

        self.client = client

        self.stream = client.bots.stream_game_state(game_id)

        self.current_state = next(self.stream)

        self.color = color

        if(color == 'white'):
            move = findBestMove(self.board, self.color)
            client.bots.make_move(game_id, move)
            self.board.push(move)
            self.lastMove = move.uci()

    def run(self):

        for event in self.stream:

            if event['type'] == 'gameState':

                self.handle_state_change(event)

    def handle_state_change(self, game_state):
        a = game_state['moves'].split(' ')
        print(a)
        if(a[len(a)-1] != self.lastMove):
            self.board.push_uci(a[len(a)-1])
            move = findBestMove(self.board, self.color)
            client.bots.make_move(self.game_id, move)
            self.board.push(move)
            self.lastMove = move.uci()

for event in client.bots.stream_incoming_events():

    if event['type'] == 'challenge':
        client.bots.accept_challenge(event['challenge']['id'])

    elif event['type'] == 'gameStart':
        game = Game(client, game_id = event['game']['gameId'], color = event['game']['color'])

        game.start()