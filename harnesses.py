from common import *
import actor
import display

def textActor():
    ta = actor.Text(text="lolzors")
    ta.x = 10
    ta.y = 10
    display.Display.CurrentDisplay().addActor(ta)
