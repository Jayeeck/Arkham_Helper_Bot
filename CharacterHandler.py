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
