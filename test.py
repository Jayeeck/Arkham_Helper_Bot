from CharacterHandler import CharacterHandler


def main():
    cHandler = CharacterHandler("***REMOVED***")
    data = ["經驗值：6", "肉體/精神：2/3", "永久卡片：無"]
    cHandler.updateCharacter("Ufb04bacba3eff7612f2e4c208abc78d2", "格妮絲", data)
if __name__ == '__main__':
    main()