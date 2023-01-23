import threading
import berserk
import chess
import random

# Useful Websites
# https://berserk.readthedocs.io/en/master/usage.html
# https://lichess.org/api#tag/Bot

token = 'lip_e8lT0QKAbYWOx2RQc7Py'
session = berserk.TokenSession(token)
client = berserk.Client(session=session)

def randomMoveGenerator(board):
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8']
    while(True):
        l1 = letters[random.randint(0,7)]
        l2 = letters[random.randint(0,7)]
        n1 = numbers[random.randint(0,7)]
        n2 = numbers[random.randint(0,7)]
        try:
            if chess.Move.from_uci(l1+n1+l2+n2) in board.legal_moves:
                return l1+n1+l2+n2
        except:
            pass


class Game(threading.Thread):
    lastMove = ''
    board = chess.Board()

    def __init__(self, client, game_id, color, **kwargs):

        super().__init__(**kwargs)

        self.game_id = game_id

        self.client = client

        self.stream = client.bots.stream_game_state(game_id)

        self.current_state = next(self.stream)

        if(color == 'white'):
            move = randomMoveGenerator(self.board)
            client.bots.make_move(game_id, move)
            self.board.push_uci(move)
            self.lastMove = move

    def run(self):

        for event in self.stream:

            if event['type'] == 'gameState':

                self.handle_state_change(event)

    def handle_state_change(self, game_state):
        a = game_state['moves'].split(' ')

        if(a[len(a)-1] != self.lastMove):
            self.board.push_uci(a[len(a)-1])
            move = randomMoveGenerator(self.board)
            client.bots.make_move(self.game_id, move)
            self.board.push_uci(move)
            self.lastMove = move

        

        

for event in client.bots.stream_incoming_events():

    if event['type'] == 'challenge':
        client.bots.accept_challenge(event['challenge']['id'])

    elif event['type'] == 'gameStart':
        game = Game(client, game_id = event['game']['gameId'], color = event['game']['color'])

        game.start()