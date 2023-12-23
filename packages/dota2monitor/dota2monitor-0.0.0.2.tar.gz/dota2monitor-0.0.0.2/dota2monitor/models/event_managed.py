from dota2monitor.models.event_manager import EventManager

class EventManaged:
    """A base class that enables triggering events managed by an EventManager."""

    def __init__(self, event_manager: EventManager):
        """
        Initializes an EventManaged instance with an EventManager.

        Args:
            event_manager (EventManager): The event manager instance used to trigger events.
        """
        self.event_manager = event_manager

    def trigger_event(self, event_type):
        """
        Triggers a specific event using the associated EventManager.

        Args:
            event_type: The type of event to trigger.
        """
        if self.event_manager:
            self.event_manager.trigger_event(event_type)
