from datetime import datetime

def log_main(msg):
    print(f"[MAIN] {datetime.now()}\t\t{msg}")

class Logger:
    def __init__(self, name_logger):
        self.name_logger = name_logger
        self.start = datetime.now()

    def log(self, msg):
        print(f"[{self.name_logger}] {datetime.now()}\t\t{msg}")

    def end_script(self):
        end = datetime.now()
        self.log(f"Tiempo de ejecución: {end-self.start}")