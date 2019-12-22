import sys
from pymongo import MongoClient


class CharacterHandler:
    characters = ""

    def __init__(self, clientToken):
        client = MongoClient(clientToken)
        db = client.get_database('Arkham_Helper')
        self.characters = db.Characters

    def createCharacter(self, user_id, data):
        if len(data) == 5:
            info = {
                'user_id': user_id,
                'player': data[0],
                'character': data[1],
                'exp': data[2],
                'permanent_injured': data[3],
                'permanent_card': data[4]
            }
            self.characters.insert_one(info)
            return "建立成功!"
        else:
            return "請依照正確格式輸入(5項皆須輸入)"

    def searchCharacter(self, user_id):
        try:
            characterList = list(self.characters.find({'user_id': user_id}))
            returnList = []
            for character in characterList:
                tempList = ["玩家名稱：%s" % (character['player']),
                            "角色名稱：%s" % (character['character']),
                            "經驗值：%s" % (character['exp']),
                            "肉體創傷/精神創傷：%s" % (character['permanent_injured']),
                            "永久卡片：%s" % (character['permanent_card'])]
                returnList.append("\n".join(tempList))
            return returnList
        except:
            return "讀取失敗：%s" % (sys.exc_info()[0])
