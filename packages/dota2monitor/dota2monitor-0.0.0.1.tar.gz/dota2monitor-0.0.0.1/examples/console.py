from dota2monitor.server import Dota2Monitor
from dota2monitor.models import ListeningEvents

def custom_lvl_up_notify():
    print('New level!')

def custom_death_notify():
    print('Dead!')

def custom_smoked_notify():
    print('Smoked!')

if __name__ == '__main__':
    monitor = Dota2Monitor()
    monitor.event_manager.add_event_listener("onDeath", custom_death_notify)
    monitor.event_manager.add_event_listener(ListeningEvents.LVL_UP, custom_lvl_up_notify)
    monitor.event_manager.add_event_listener(ListeningEvents.SMOKED, custom_smoked_notify)

    monitor.run(port = 666)