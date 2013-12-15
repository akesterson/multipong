from common import *
import event
import display
import threading
import actor
import player
import registry
import dpath.util

class Game(event.EventHandler, registry.Registerable):

    # ---- Static methods

    # ---- This is largely unnecessary now that events are handled via exception bubbling
    @staticmethod
    def CurrentGame():
        return Game.__currentGame__

    @staticmethod
    def NewGame(flags):
        if hasattr(Game, '__currentGame__'):
            raise AttributeError("Attempted to create a new game while one was already in progress")
        if flags['type'] == 'server':
            game = ServerHost(display=flags['display'])
        elif flags['hostname']:
            game = ServerGame(display=flags['display'], hostname=flags['hostname'])
        else:
            game = LocalGame(display=flags['display'])
        setattr(Game, '__currentGame__', game)
        return game

    # ---- Member methods

    def __init__(self, *args, **kwargs):
        registry.Registerable.__init__(self, *args, **kwargs)
        event.EventHandler.__init__(self, *args, **kwargs)
        self.__eventQueue__ = Queue.Queue()
        self.__display__ = display.Display.NewDisplay(kwargs['display'])
        self.__players__ = []
        self.gameRunning = True
        logger = logging.getLogger()
        logger.info("Display is: {}".format(str(self.__display__)))

        self.__players__.append(player.Player(registryKey='player1'))
        self.__players__.append(player.Player(registryKey='player2'))
        self.__players__[1].x = 25
        logger = logging.getLogger()
        logger.debug("Adding actors {} and {}".format(self.__players__[0].uuid, self.__players__[1].uuid))
        self.__display__.addActor(self.__players__[0])
        self.__display__.addActor(self.__players__[1])

    def eventLoop(self):
        reg = registry.Registry.GetRegistry()
        logger = logging.getLogger()
        logger.info("gameRunning: {}".format(self.gameRunning))
        while self.gameRunning:
            evlist = []
            try:
                try:
                    evlist = self.__eventQueue__.get_nowait()
                except Queue.Empty, e:
                    pass
                self.__display__.checkInput()
            except event.EventBubble, e:
                evlist = e.message
            if not evlist:
                continue
            if not isinstance(evlist, list):
                evlist = [evlist]
            for ev in evlist:
                if len(ev) < 2:
                    logger.error("Malformed event : {}".format(ev))
                target = "/*/uuid/*"
                if len(ev) >= 3:
                    target = ev[2]
                logger.debug("Event: {} => {}".format(ev[0], target))
                for line in str(ev[1]).split('\n'):
                    logger.debug("    {}".format(line))
                # Targeted event?
                for pair in dpath.util.search(reg, target, yielded=True):
                    logger.debug("    processed by {}".format(pair[0]))
                    pair[1].handleEvent(ev)

    def handleEvent(self, ev):
        if ev[0] == 'endGame':
            self.gameRunning = False

    def addEvent(self, event):
        self.__eventQueue__.put(event)

    def cleanup(self):
        self.__display__.cleanup()
        for player in self.__players__:
            player.cleanup()

class LocalGame(Game):
    def __init__(self, *args, **kwargs):
        Game.__init__(self, *args, **kwargs)

    def handleEvent(self, ev):
        Game.handleEvent(self, ev)


class ServerHost(Game):
    def __init__(self, *args, **kwargs):
        Game.__init__(self, *args, **kwargs)

class ServerGame(Game):
    def __init__(self, *args, **kwargs):
        Game.__init__(self, *args, **kwargs)

