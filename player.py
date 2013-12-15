from common import *
import event
import actor

class Player(actor.Paddle, event.EventHandler):
    def __init__(self, *args, **kwargs):
        actor.Paddle.__init__(self, *args, **kwargs)

    def cleanup(self):
        raise Exception("lol implement me")
