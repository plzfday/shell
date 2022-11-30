from applications.history import History


class HistoryManager:
    def __new__(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = super(HistoryManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.history: History = History()
        self.current: int = len(self.history.saved)

    def arrow_up(self) -> str:
        if self.current - 1 < 0:
            return ""
        self.current -= 1
        return self.history.saved[self.current]

    def arrow_down(self) -> str:
        if self.current + 1 > len(self.history.saved) - 1:
            return ""
        self.current += 1
        return self.history.saved[self.current]
