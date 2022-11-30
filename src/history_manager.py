from applications.history import History


class HistoryManager:
    def __new__(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = super(HistoryManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.history: History = History()
        self.len_history: int = len(self.history.saved)
        self.current: int = self.len_history

    def arrow_up(self) -> str:
        if self.len_history == 0:
            return ""
        self.current = max(0, self.current - 1)
        return self.history.saved[self.current]

    def arrow_down(self) -> str:
        if self.len_history == 0 or self.current + 1 == self.len_history:
            return ""
        self.current = min(self.len_history - 1, self.current + 1)
        return self.history.saved[self.current]
