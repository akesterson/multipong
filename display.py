from common import *
import event
import game
import registry

class Display(event.EventHandler, registry.Registerable):
    # --- Static methods

    @staticmethod
    def CurrentDisplay():
        return getattr(Display, '__currentDisplay__')

    @staticmethod
    def NewDisplay(displayType):
        display = globals()["{}Display".format(displayType.title())]()
        setattr(Display, '__currentDisplay__', display)
        return display

    @staticmethod
    def StaticRefresh():
        display = Display.CurrentDisplay()
        display.refresh()

    # --- Member methods
    def __init__(self, *args, **kwargs):
        registry.Registerable.__init__(self, *args, **kwargs)
        event.EventHandler.__init__(self, *args, **kwargs)
        self.__lock_actors__ = threading.RLock()
        self.__lock_timer__ = threading.RLock()
        self.__lock_drawing__ = threading.RLock()
        self.__actors__ = {}
        self.__setDrawTimer__()

    def __setDrawTimer__(self):
        self.__drawTimer__ = threading.Timer(FRAMERATE, Display.StaticRefresh)
        self.__drawTimer__.start()

    def cleanup(self):
        self.__drawTimer__.cancel()

    # ---

    def checkInput(self):
        raise Exception("lol implement me")

    def refresh(self):
        try:
            with self.__lock_drawing__:
                self.__screen__.clear()
                for actor in self.__actors__.values():
                    self.drawActor(actor)
                self.__setDrawTimer__()
        except Exception, e:
            game.Game.CurrentGame().addEvent(('endGame', traceback.format_exc()))

    def addActor(self, actor):
        logger = logging.getLogger()
        with self.__lock_actors__:
            if not actor.uuid in self.__actors__.keys():
                logger.debug("Added actor {}".format(actor.uuid))
                self.__actors__[actor.uuid] = actor

    def delActor(self, actor):
        with self.__lock_actors__:
            try:
                del(self.__actors__, actor.uuid)
            except KeyError, e:
                return

class CursesDisplay(Display):
    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger()
        self.logger.info("CursesDisplay starting")
        Display.__init__(self, *args, **kwargs)
        self.__screen__ = curses.initscr()
        self.__screen__.keypad(1)
        try:
            curses.curs_set(0)
        except:
            logger.warn("I couldn't make the cursor invisible - I'm sorry")
        curses.noecho()
        curses.cbreak()

    def cleanup(self):
        self.logger.info("CursesDisplay cleaning up")
        curses.nocbreak()
        self.__screen__.keypad(0)
        curses.echo()
        curses.endwin()
        Display.cleanup(self)

    def refresh(self):
        Display.refresh(self)
        self.__screen__.refresh()

    def checkInput(self):
        key = self.__screen__.getch()
        if key == ord('q'):
            raise event.EventBubble(('endGame',
                                     'User terminated the game',
                                     '/Game/uuid/*'))
        elif key == ord('w'):
            raise event.EventBubble(('moveUp', '', '/Player/cn/player1'))
        elif key == ord('s'):
            raise event.EventBubble(('moveDown', '', '/Player/cn/player1'))
        elif key == curses.KEY_UP:
            raise event.EventBubble(('moveUp', '', '/Player/cn/player2'))
        elif key == curses.KEY_DOWN:
            raise event.EventBubble(('moveDown', '', '/Player/cn/player2'))

    def drawActor(self, actor):
        # Curses displays have it easy; actors return us a function to call
        # with a reference to ourselves, and they draw on us.
        actor.frame(self)(self)

