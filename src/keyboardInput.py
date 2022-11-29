class HistoryManager:
    def __init__(self):
        self.saved = []
        FILE_PATH = "/comp0010/history.txt"
        with open(FILE_PATH, "r") as f:
            lines = f.readlines()
            for line in lines:
                self.saved.append(line)

    def arrow_up(self) -> str:
        order = len(self.saved)
        if order != 0:
            order -= 1
        return self.saved[order]

    def arrow_down(self) -> str:
        order = len(self.saved)
        if order < len(self.saved):
            order += 1
        return self.saved[order]
