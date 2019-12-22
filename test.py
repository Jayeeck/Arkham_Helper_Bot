from CharacterHandler import CharacterHandler


def main():
    cHandler = CharacterHandler("***REMOVED***")
    temp = cHandler.searchCharacter("Ufb04bacba3eff7612f2e4c208abc78d2")
    print(type(temp) == list)
if __name__ == '__main__':
    main()