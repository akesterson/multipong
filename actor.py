from common import *
import event
import display
import uuid
import registry
import dpath.util
import logging
logger = logging.getLogger()

class Actor(event.EventHandler, registry.Registerable):
    def __init__(self, *args, **kwargs):
        registry.Registerable.__init__(self, *args, **kwargs)
        event.EventHandler.__init__(self, *args, **kwargs)
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        dpath.util.merge(
            self.__eventHandlers__,
            {
                'moveUp': self._event_moveUp,
                'moveDown': self._event_moveDown
                }
            )

    def _event_moveUp(self, evt):
        self.y -= 1

    def _event_moveDown(self, evt):
        self.y += 1

    def frame(self, display):
        return getattr(
            self,
            "frameFor{}".format(display.__class__.__name__)
            )()

class Text(Actor):
    def __init__(self, *args, **kwargs):
        Actor.__init__(self, *args, **kwargs)
        self.__text__ = kwargs.get('text', "")

    def setText(self, text):
        self.__text__ = text

    def frameForCursesDisplay(self):
        def drawForCurses(disp):
            disp.__screen__.addstr(self.y, self.x, self.__text__)
        return drawForCurses

class Paddle(Text):
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)
        self.__text__ = "|"
