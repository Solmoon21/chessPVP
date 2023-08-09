import os
from sound import *

class Config:
    def __init__(self):
        self.sounds = {}
        self.addSounds()

    def addSounds(self):
        names = ["move","capture"]
        for n in names:
            self.sounds[n] = Sound( os.path.join( f'../assets/sounds/{n}.wav' )  )