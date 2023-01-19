import threading
import berserk

token = 'lip_e8lT0QKAbYWOx2RQc7Py'
session = berserk.TokenSession(token)
client = berserk.Client(session=session)

class Game(threading.Thread):

    def __init__(self, client, game_id, **kwargs):

        super().__init__(**kwargs)

        self.game_id = game_id

        self.client = client

        self.stream = client.bots.stream_game_state(game_id)

        self.current_state = next(self.stream)


    def run(self):

        for event in self.stream:

            if event['type'] == 'gameState':

                self.handle_state_change(event)


    def handle_state_change(self, game_state):

        client.bots.abort_game(self.game_id)

for event in client.bots.stream_incoming_events():

    if event['type'] == 'challenge':
        client.bots.accept_challenge(event['challenge']['id'])

    elif event['type'] == 'gameStart':
        game = Game(client, game_id = event['game']['gameId'])

        game.start()
