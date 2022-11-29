from applications.history import History


class HistoryManager:
    def __init__(self):
        self.history: History = History()

    def arrow_up(self) -> str:
        order = len(self.history.saved)
        if order != 0:
            order -= 1
        return self.history.saved[order]

    def arrow_down(self) -> str:
        order = len(self.history.saved)
        if order < len(self.history.saved):
            order += 1
        return self.history.saved[order]
