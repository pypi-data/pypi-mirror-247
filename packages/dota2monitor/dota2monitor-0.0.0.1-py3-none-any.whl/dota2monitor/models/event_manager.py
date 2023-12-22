from enum import Enum

class ListeningEvents(Enum):
    """Enum representing different types of listening events."""
    SMOKED = "onSmoke"
    LVL_UP = "onLvlUp"
    DEATH = "onDeath"
    ASSIST = "onAssist"
    KILL = "onKill"
    STUNNED = "onStunned"
    DISARMED = "onDisarmed"
    SILENCED = "onSilenced"
    HEXED = "onHexed"
    MUTED = "onMuted"
    BREAK = "onBreak"


    # roshan_killed
    # runes??

class EventManager:
    """Manages event listeners and triggers events accordingly."""

    def __init__(self):
        """Initializes the EventManager."""
        self._listeners = {}

    def add_event_listener(self, event_type: ListeningEvents, callback):
        """Adds a listener for a specific event type.

        Args:
            event_type (ListeningEvents): The type of event to listen for.
            callback (function): The function to be called when the event occurs.

        Raises:
            ValueError: If the event_type is not a valid ListeningEvents enum member.
            TypeError: If the event_type is not a string or a ListeningEvents enum member.
        Examples:
            # Event can be set in both ways
            event_manager.add_event_listener("onDeath", custom_death_notify)
            event_manager.add_event_listener(ListeningEvents.DEATH, custom_death_notify)
        """
        if isinstance(event_type, str):
            event_type = ListeningEvents(event_type)  # Convert string to enum member
            if event_type not in ListeningEvents:
                raise ValueError(f"{event_type} is not a valid event type.")
        elif not isinstance(event_type, ListeningEvents):
            raise TypeError("Event type should be either a string or a ListeningEvents enum member.")
        
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)

    def remove_event_listener(self, event_type: ListeningEvents, callback):
        """Removes a listener for a specific event type.

        Args:
            event_type (ListeningEvents): The type of event to remove the listener from.
            callback (function): The function that was being called for that event type.
        """
        if event_type in self._listeners and callback in self._listeners[event_type]:
            self._listeners[event_type].remove(callback)

    def trigger_event(self, event_type: ListeningEvents):
        """Triggers the specified event by calling all associated callbacks.

        Args:
            event_type (ListeningEvents): The type of event to trigger.
        """
        if event_type in self._listeners:
            for callback in self._listeners[event_type]:
                callback()
