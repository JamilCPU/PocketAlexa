import datetime as dt
import os 

class FileLogger:
    def setupLogging(self):
            if not os.path.exists("../logs/logging.txt"):
                with open("../logs/logging.txt", 'x') as f:
                    f.write("Logging: START\n")
            self.wipeLog()

    def writeToFile(self, info):
        timestamp = str(dt.datetime.now().timestamp())
        with open("../logs/logging.txt", 'a') as f:
            f.write("[" + timestamp + "]: " + info  + "\n")

    def wipeLog(self):
        with open("../logs/logging.txt", 'w') as f:
            f.write("Logging: START\n")
        print('wipe log ran')