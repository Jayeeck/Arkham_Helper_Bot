class CharacterHandler:
    info = {
        'line_id': "",
        'player': "",
        'character': "",
        'exp': "",
        'permanent_injured': "",
        'permanent_card': ""
    }
    clientToken = ""

    def __init__(self, clientToken):
        self.clientToken = clientToken
