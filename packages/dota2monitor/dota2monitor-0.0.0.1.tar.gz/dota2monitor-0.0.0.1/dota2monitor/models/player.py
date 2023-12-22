from dota2monitor.models.event_managed import EventManaged
from dota2monitor.models.event_manager import EventManager, ListeningEvents


class Player(EventManaged):
    def __init__(self, player_data, event_manager: EventManager):
        super().__init__(event_manager)
        self.name = player_data.get('name')
        self.team_name = player_data.get('team_name')
        self.kills = player_data.get('kills', 0)
        self.deaths = player_data.get('deaths', 0)
        self.assists = player_data.get('assists', 0)
        self.last_hits = player_data.get('last_hits', 0)
        self.denies = player_data.get('denies')
        self.gold = player_data.get('gold', 0)
        self.gold_reliable = player_data.get('gold_reliable')
        self.gold_unreliable = player_data.get('gold_unreliable')
        self.gold_from_hero_kills = player_data.get('gold_from_hero_kills')
        self.gold_from_creep_kills = player_data.get('gold_from_creep_kills')
        self.gold_from_income = player_data.get('gold_from_income')
        self.gold_from_shared = player_data.get('gold_from_shared')
        self.gpm = player_data.get('gpm', 0)
        self.xpm = player_data.get('xpm', 0)
        self.steamid = player_data.get('steamid')
        self.accountid = player_data.get('accountid')
        self.activity = player_data.get('activity')
        self.kill_streak = player_data.get('kill_streak')
        self.commands_issued = player_data.get('commands_issued')
        self.kill_list = player_data.get('kill_list')
        self.player_slot = player_data.get('player_slot')
        self.team_slot = player_data.get('team_slot')

    def update(self, player_data):
        self.name = player_data.get('name')
        self.team_name = player_data.get('team_name')
        self.kills = player_data.get('kills', 0)
        self.assists = player_data.get('assists', 0)
        self.last_hits = player_data.get('last_hits', 0)
        self.denies = player_data.get('denies', 0)
        self.gold = player_data.get('gold', 0)
        self.gold_reliable = player_data.get('gold_reliable')
        self.gold_unreliable = player_data.get('gold_unreliable')
        self.gold_from_hero_kills = player_data.get('gold_from_hero_kills')
        self.gold_from_creep_kills = player_data.get('gold_from_creep_kills')
        self.gold_from_income = player_data.get('gold_from_income')
        self.gold_from_shared = player_data.get('gold_from_shared')
        self.gpm = player_data.get('gpm', 0)
        self.xpm = player_data.get('xpm', 0)
        self.steamid = player_data.get('steamid')
        self.accountid = player_data.get('accountid')
        self.activity = player_data.get('activity')
        self.kill_streak = player_data.get('kill_streak')
        self.commands_issued = player_data.get('commands_issued')
        self.kill_list = player_data.get('kill_list')
        #print(self.kill_list) res: {'victimid_6': 1}
        # res {'victimid_5': 1, 'victimid_6': 1}
        self.player_slot = player_data.get('player_slot')
        self.team_slot = player_data.get('team_slot')

        if self.event_manager and self.deaths < player_data.get('deaths', 0):
            self.trigger_event(ListeningEvents.DEATH)

        self.deaths = player_data.get('deaths', 0)
