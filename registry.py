from common import *
import dpath.util
import uuid
import pprint

class Registry(dict):
    @staticmethod
    def GetRegistry():
        try:
            ret = getattr(Registry, '__curRegistry__')
        except AttributeError, e:
            ret = Registry()
            setattr(Registry, '__curRegistry__', ret)
        return ret

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        # Circular dependencies, ye are my bane
        import event
        import display
        import actor
        import game
        import player
        # --
        self.__validClasses__ = (
            event.EventHandler,
            actor.Actor,
            player.Player,
            game.Game,
            display.Display
            )

    def search(self, path):
        res = []
        for item in dpath.util.search(self, path, yielded=True):
            res.append(item)
        return res

    def register(self, value, key = None):
        logger = logging.getLogger()
        if not issubclass(value.__class__, self.__validClasses__):
            raise TypeError("Registry only accepts objects of type: {}"
                            "".format(self.__validClasses__))
        for baseClass in self.__validClasses__:
            if issubclass(value.__class__, baseClass):
                cn = baseClass.__name__
        ouuid = uuid.uuid4()
        uuidpath =  "/{}/uuid/{}".format(cn, ouuid)
        cnpath = "/{}/cn/{}".format(cn, key)
        dpath.util.new(self, uuidpath, value)
        if key:
            dpath.util.new(self, cnpath, value)
        logger.debug("Registered {} as {} | {}".format(value, uuidpath, cnpath))
        for line in pprint.pformat(self, indent=4).split('\n'):
            logger.debug("registry: {}".format(line))
        return ouuid

class Registerable:
    def __init__(self, *args, **kwargs):
        self.uuid = Registry.GetRegistry().register(
            self,
            kwargs.get('registryKey', None)
            )
