from tkinter import *

window = Tk()

window.geometry("600x600")
window.title("Cupom Fiscal em Python")


usernameVar = StringVar()
passwordVar = StringVar()

options = ["Banana", "Arroz", "Feijão"]
itemVariable = StringVar()
itemVariable.set = (options[0])


def adminLogin():
    titleLabel = Label(window, text="CUPOM FISCAL", font="arial 30", fg="blue",)
    titleLabel.grid(row=0, column=0, columnspan=4, padx=(40,0), pady=(10,0))

    loginLabel = Label(window, text="Administrador Login:", font="arial 30")
    loginLabel.grid(row=1, column=2, padx=(50,0),columnspan=2 , pady=10)

    usernameLabel = Label(window, text="Usuário:" , font="arial 8")
    usernameLabel.grid(row=2,column=2,padx=2, pady=5)

    passwordLabel = Label(window, text="Senha:", font="arial 8")
    passwordLabel.grid(row=3,column=2,padx=2, pady=5)

    usernameEntry = Entry(window, textvariable=usernameVar)
    usernameEntry.grid(row=2, column=3,padx=20, pady=5)

    passwordEntry = Entry(window, textvariable=passwordVar, show='*')
    passwordEntry.grid(row=3,column=3,padx=20, pady=5)

    loginButton = Button(window, text='Login', width=20, height=2, font="arial 8")
    loginButton.grid(row=4, column=2, columnspan=2, padx=20, pady=10)

#############################--   main window   --######################################################################

def mainwindow():
    titleLabel = Label(window, text="CUPOM FISCAL", font="arial 30", fg="red",)
    titleLabel.grid(row=0, column=1, columnspan=3, pady=(10,0))

    addButton = Button(window, text='Add Itens', width=15, height=2, font="arial 8")
    addButton.grid(row=1, column=0, padx=(10,0), pady=(10,0))

    LogoutBtn = Button(window, text='Sair', width=15, height=2, font="arial 8")
    LogoutBtn.grid(row=1, column=4,  pady=(10,0))

    itemLabel = Label(window, text="Selecionar Item:")
    itemLabel.grid(row=2, column=0, padx=(5,0),pady=(10,0))

    itemDropDown = OptionMenu(window, itemVariable, *options)
    itemDropDown.grid(row=3, column=0, padx=(10,0), pady=(10,0))

    quantityLabel = Label(window, text="Quantidade:")
    quantityLabel.grid(row=2,column=2,padx=(5,0), pady=(10,0))

    buttonBill = Button(window, text='Gerar Nota')
    buttonBill.grid(row=2,column=4,padx=(5,0), pady=(10,0))





mainwindow()
window.mainloop()