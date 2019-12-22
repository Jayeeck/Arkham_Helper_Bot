from datetime import datetime
from AdventureHandler import AdventureHandler


def main():
    aHandler = AdventureHandler("***REMOVED***")
    aHandler.newLog(["敦威智遺產", "戶外教學", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "困難", "老頭死了"])
if __name__ == '__main__':
    main()