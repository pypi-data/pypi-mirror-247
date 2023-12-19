import enum
from enum import Enum
from . import function as func

class File:
    modes = (
        'r',
        'w',
        'a',
        'x',
        'r+',
        'w+',
        'a+',
        'x+',
        'rb',
        'wb',
        'ab',
        'xb',
        'rb+',
        'wb+',
        'ab+',
        'xb+',
    )
    def __init__(self, fp:str, mode:func.mkenum("Modes", modes)="r+"):
        self.mode = mode
        self.file = open(fp, mode)
    def write(self, data:str|bytes=""):
        self.file.write(data)
    def read(self, size:int|None=None):
        return self.file.read(size)
    def close(self):
        self.file.close()

    def wc(self, data:str|bytes=""):
        self.write(data)
        self.close()
    def rc(self, size:int|None=None):
        rd = self.read(size)
        self.close()
        return rd
    def __call__(self):
        try:
            return self.file
        except:
            return None

