class Log:
    def __init__(self):


        # Colors
        self.HEADER = '\033[95m'
        self.OKBLUE = '\033[94m'
        self.OKCYAN = '\033[96m'
        self.OKGREEN = '\033[92m'
        self.WARNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'
        self.BOLD = '\033[1m'
        self.UNDERLINE = '\033[4m'

    def log(self, text, level = None):
        text = text
        level = level

        if level == "nice" or level == "success" or level == "ok" or level == "great":
            print((f"{self.OKGREEN} LOG >>> {self.ENDC} {text}"))
        elif level == "warning":
            print((f"{self.WARNING} WARNING >>> {self.ENDC} {text}"))
        elif level == "error":
            print((f"{self.FAIL} ERROR >>> {self.ENDC} {text}"))
        else:
            print((f"{self.OKBLUE} INFO >>> {self.ENDC} {text}"))
