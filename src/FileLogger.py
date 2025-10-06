import datetime as dt

class FileLogger:
    def setupLogging(self):
        with open("../logs/logging.txt", 'x') as f:
            f.write("Logging: START")

    def writeToFile(self, info):
        timestamp = str(dt.datetime.now().timestamp())
        with open("../logs/logging.txt", 'w') as f:
            f.write("[" + timestamp + "]: " + info )

