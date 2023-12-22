class Event:
    def __init__(self, event_data):
        self.game_time = event_data.get('game_time')
        self.event_type = event_data.get('event_type')
        # Check event type and set attributes accordingly
        if self.event_type == 'roshan_killed':
            self.killed_by_team = event_data.get('killed_by_team')
            self.killer_player_id = event_data.get('killer_player_id')
        elif self.event_type == 'aegis_picked_up':
            self.player_id = event_data.get('player_id')
            self.snatched = event_data.get('snatched')
        elif self.event_type == 'bounty_rune_pickup':
            self.player_id = event_data.get('player_id')
            self.team = event_data.get('team')
            self.bounty_value = event_data.get('bounty_value')
            self.team_gold = event_data.get('team_gold')
        else:
            # Handle other event types here
            pass