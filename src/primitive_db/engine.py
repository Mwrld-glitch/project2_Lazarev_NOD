import prompt


def welcome():
    print("Первая попытка запустить проект!\n\n***")
    
    while True:
        print("<command> exit - выйти из программы")
        print("<command> help - справочная информация")
        command = prompt.string("Введите команду: ")
        
        if command == "help":
            continue
        elif command == "exit":
            break
        else:
            print("Неизвестная команда")