from flask import Flask, request
from dota2monitor.models.dota2_data import Dota2Data
from dota2monitor.models.event_manager import EventManager, ListeningEvents

class Dota2Monitor:
    def __init__(self):
        self.app = Flask('Dota2Monitor GSI-Server')
        self.event_manager = EventManager()

        # Initialize Dota2Data with an empty dictionary and the event manager
        self.global_dota2_data = Dota2Data({}, self.event_manager)

        @self.app.route('/', methods=['POST'])
        def gsi_webhook():
            if request.method == 'POST':
                data = request.json  # Get the JSON data sent from Dota 2
                self.handle_gsi_data(data)
                return 'Received GSI data', 200
            else:
                return 'Invalid request', 400

    def handle_gsi_data(self, data):
        if data.get('player') is not None and data.get('player'):
            # Updating Dota2Data instance with the received data
            self.global_dota2_data.update(data)

    def run(self, port = 228):
        self.app.run(host='0.0.0.0', port = port)