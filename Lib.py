from datetime import datetime
# import ctypes  # Це костыль для отображения цветов в консоли Windows
# kernel32 = ctypes.windll.kernel32
# kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
class Logger:
    #TODO Попробовать реализовать универсальный логгер комманд, без ручного добавления в логгирование
    @staticmethod
    def get_time():
        iso = datetime.now().isoformat()
        return iso[11:19]

    def log(self, text):
        print(f"\033[32m {self.get_time()} [Logs] \033[37m{str(text)}")

    def warn(self, text):
        print(f"\033[33m\033[3m {self.get_time() + ' [Warning] ' + str(text)}")

    def error(self, text):
        print(f"\033[31m\033[1m {self.get_time() + ' [Error] ' + str(text)}")

    def comm(self, text):
        print(f"\033[32m {self.get_time()} [Logs][Command] \033[37m{str(text)}")

