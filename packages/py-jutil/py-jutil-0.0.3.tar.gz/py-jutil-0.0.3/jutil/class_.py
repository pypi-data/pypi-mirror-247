import enum
from enum import Enum
import io
from . import function as func

FileType = io.TextIOWrapper



class styling:
    """
    A bunch of style and color codes.
    """

    class fore:
        """
        Foreground colors.
        """
        black = "\033[30m"
        red = "\033[31m"
        green = "\033[32m"
        yellow = "\033[33m"
        blue = "\033[34m"
        magenta = "\033[35m"
        cyan = "\033[36m"
        white = "\033[37m"
        def from_rgb(self, r, g, b):
            return f"\033[38;2;{r};{g};{b}m"

    class back:
        """
        Background colors.
        """
        black = "\033[40m"
        red = "\033[41m"
        green = "\033[42m"
        yellow = "\033[43m"
        blue = "\033[44m"
        magenta = "\033[45m"
        cyan = "\033[46m"
        white = "\033[47m"
        def from_rgb(self, r, g, b):
            return f"\033[48;2;{r};{g};{b}m"

    class style:
        """
        Style codes.
        """
        bold = "\033[1m"
        dim = "\033[2m"
        italic = "\033[3m"
        underline = "\033[4m"
        blink = "\033[5m"
        reverse = "\033[7m"
        hidden = "\033[8m"
        
    reset = "\033[0m"


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

class inp:
    """
    Holder for console input functions.
    Quick and easy inputs!
    """

    def ask(self, prompt:str=""):
        return input(prompt+"\n> ")
    def ask_yn(self, prompt:str=""):
        inpt = input(prompt+"\n(y/n) > ")
        if inpt.lower() == "y":
            return True
        elif inpt.lower() == "n":
            return False
        else:
            return None
    def ask_list(self, prompt:str="", list_obj:list=[]):
        print(prompt)
        for i in list_obj:
            print(f"[{list_obj.index(i)}] {i}")
        return list_obj[int(input("> "))]



class logs:
    """
    Holder for console log functions.
    Quick and easy logs!
    """
    def log(self, msg:str=""):
        print(styling.style.italic+styling.fore.cyan+msg+styling.reset)

    def warn(self, msg:str=""):
        print(styling.style.bold+styling.fore.yellow+msg+styling.reset)

    def error(self, msg:str=""):
        print(styling.style.bold+styling.fore.red+msg+styling.reset)

    def success(self, msg:str=""):
        print(styling.style.bold+styling.fore.green+msg+styling.reset)
