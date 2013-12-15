from common import *

# Raise an EventBubble with a tuple(eventName, eventMessage) to post a new
# message to the queue. If you bubble a list of tuples - [(), (), ()] - then
# each tuple in the list of events is added to the queue.
class EventBubble(Exception):
    pass

# Events are just tuples of (eventName, eventMessage), where eventMessage
# can be any object appropriate for eventName
class EventHandler:
    def __init__(self, *args, **kwargs):
        self.__eventHandlers__ = {}

    def handleEvent(self, event):
        self.__eventHandlers__[event[0]](event[1])

    def bindEvent(self, eventName, function):
        self.__eventHandlers__ = getattr(self, "__eventHandlers__", {})
        self.__eventHandlers__[eventName] = function

