
def main():
    txt = "hello,my name is Peter I, am 26 ,years old"
    x = txt.split(",")
    del x[0]
    print(x)
if __name__ == '__main__':
    main()