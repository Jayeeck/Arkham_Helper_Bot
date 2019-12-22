import sys
from datetime import datetime
from pymongo import MongoClient


class AdventureHandler:
    adventures = ""

    def __init__(self, clientToken):
        client = MongoClient(clientToken)
        db = client.get_database('Arkham_Helper')
        self.adventures = db.AdventureLog

    def newLog(self, user_id, data):
        if len(data) == 5:
            info = {
                'user_id': user_id,
                'story_name': data[0],
                'chapter_name': data[1],
                'record_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'difficulty': data[2],
                'logs': data[3],
            }
            self.adventures.insert_one(info)
            return "紀錄完成!"
        else:
            return "請依照正確格式輸入(4項皆須輸入)"

    def showLogs(self, user_id):
        try:
            logList = list(self.adventures.find({'user_id': user_id}))
            returnList = []
            for character in logList:
                tempList = ["故事名稱：%s" % (character['story_name']),
                            "章節名稱：%s" % (character['chapter_name']),
                            "紀錄時間：%s" % (character['record_time']),
                            "難度：%s" % (character['difficulty']),
                            "紀錄事項：\n%s" % (character['logs'])]
                returnList.append("\n".join(tempList))
            return returnList
        except:
            return "讀取失敗：%s" % (sys.exc_info()[0])
