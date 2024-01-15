from ToDoDb import ToDoDb
from ToDoGuiCtk import ToDoGuiCtk

def main():
    db = ToDoDb(init=False, dbName='ToDoDb.csv')
    app = ToDoGuiCtk(dataBase=db)
    app.mainloop()

if __name__ == "__main__":
    main()