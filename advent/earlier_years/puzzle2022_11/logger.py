class LogStreamer:
    def __init__(self):
        self.log_lines: list[str] = []

    def log(self, message: str):
        self.log_lines.append(message.strip())
        print(message.strip())

    def validate(self, messages: list[str]) -> bool:
        return self.log_lines == messages
