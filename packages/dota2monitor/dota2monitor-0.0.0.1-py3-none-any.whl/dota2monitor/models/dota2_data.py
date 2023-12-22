from dota2monitor.models.backpack import Backpack
from dota2monitor.models.event import Event
from dota2monitor.models.event_managed import EventManaged
from dota2monitor.models.event_manager import EventManager
from dota2monitor.models.hero import Hero
from dota2monitor.models.map_info import MapInfo
from dota2monitor.models.player import Player
from dota2monitor.models.provider import Provider
from dota2monitor.models.spells import Spells


class Dota2Data(EventManaged):
    def __init__(self, data, event_manager: EventManager):
        super().__init__(event_manager)
        self.provider = Provider(data.get('provider', {}))
        self.map = MapInfo(data.get('map', {}))
        self.player = Player(data.get('player', {}), event_manager)
        self.hero = Hero(data.get('hero', {}), event_manager)
        self.items = Backpack(data.get('items', {}))
        self.spells = Spells(data.get('abilities', {}))
        # Check for events data and instantiate Event objects accordingly
        events_data = data.get('events', [])
        self.events = [Event(event) for event in events_data]
        self._listeners = {}

        # comes on put item in backpack
        # self.added
        # towers status
        # self.building  
    
    # To not create a new entity, but to track changes
    def update(self, data):
        self.provider = Provider(data.get('provider', {}))
        self.map = MapInfo(data.get('map', {}))
        self.items = Backpack(data.get('items', {}))
        self.spells = Spells(data.get('abilities', {}))
        events_data = data.get('events', [])
        self.events = [Event(event) for event in events_data]

        self.player.update(data.get('player'))
        self.hero.update(data.get('hero'))


