import threading
import berserk

# Useful Websites
# https://berserk.readthedocs.io/en/master/usage.html
# https://lichess.org/api#tag/Bot

token = 'lip_e8lT0QKAbYWOx2RQc7Py'
session = berserk.TokenSession(token)
client = berserk.Client(session=session)

class Game(threading.Thread):
    def __init__(self, client, game_id, color, **kwargs):

        super().__init__(**kwargs)

        self.game_id = game_id

        self.client = client

        self.stream = client.bots.stream_game_state(game_id)

        self.current_state = next(self.stream)

        if(color == 'white'):
            client.bots.make_move(self.game_id, 'e2e4')


    def run(self):

        for event in self.stream:

            if event['type'] == 'gameState':

                self.handle_state_change(event)

    def handle_state_change(self, game_state):
        print(self.game_id)

        

for event in client.bots.stream_incoming_events():

    if event['type'] == 'challenge':
        client.bots.accept_challenge(event['challenge']['id'])

    elif event['type'] == 'gameStart':
        game = Game(client, game_id = event['game']['gameId'], color = event['game']['color'])

        game.start()
