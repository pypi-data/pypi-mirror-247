from enum import Enum
from time import sleep as wait
from random import randint
from . import exception as ex

def mkenum(name, args):
    """
    Create an enum class.
    """
    return Enum(name, args)

def exit(message:str="Exit"):
    """
    Exit the program.
    """
    raise ex.ExitOnCommand(message)