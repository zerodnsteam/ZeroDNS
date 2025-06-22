from datetime import datetime

class ProgressLogger:
    def __init__(self):
        self.logs = []
    def log(self, msg):
        t = datetime.now().strftime("%H:%M:%S")
        log = f"[{t}] {msg}"
        self.logs.append(log)
        print(log)
    def save(self, fn="output/last_run.log"):
        with open(fn, "w", encoding="utf-8") as f:
            f.write("\n".join(self.logs))
