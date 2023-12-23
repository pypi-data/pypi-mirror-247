# Dota2Monitor

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/imbalanceinbalance/dota2monitor/blob/main/LICENSE)

Dota2Monitor allows you to use GameState Integration Monitoring to track events happening in Dota 2 matches.

## Installation

You can install Dota2Monitor using pip:

```bash
pip install dota2monitor
```
## Usage

1. Place the file gamestate_integration_monitor.cfg into ~\SteamLibrary\steamapps\common\dota 2 beta\game\dota\cfg\gamestate_integration.
```
"Dota 2 Integration Configuration"
{
    "uri"           "http://localhost:666/"
    "timeout"       "5.0"
    "buffer"        "0.1"
    "throttle"      "0.1"
    "heartbeat"     "30.0"
    "data"
    {
        "provider"      "1"
        "map"           "1"
        "player"        "1"
        "hero"          "1"
        "abilities"     "1"
        "items"         "1"
        "buildings"     "0"
        "draft"         "0"
        "events"        "1"
        "previously"    "0"
    }
}
```
2. Add the following code snippet to monitor events:
```python
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
```
## Contributing

Feel free to contribute by submitting pull requests or raising issues.
