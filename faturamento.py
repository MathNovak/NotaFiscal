from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql

window = Tk()

window.geometry("600x600")
window.title("Cupom Fiscal em Python")
window.configure(background='lightblue')

############ quantidade valor #############

def quantityFieldListener(a,b,c):
    global quantityVar
    global costVar
    global itemRate
    #global rateVar
    quantity = quantityVar.get()
    if quantity != "":
        try:
            quantity = float(quantity)
            #rateVar = float(rateVar.get())
            cost = quantity*itemRate
            quantityVar.set("%.2f"%quantity)
            costVar.set("%.2f"%cost)
        except ValueError:
            quantity=quantity[:-1]
            quantityVar.set(quantity)
    else:
        quantity=0
        quantityVar.set(f":.2f"%quantity)



def costFieldListener(a,b,c):
    global quantityVar
    global costVar
    global itemRate
    #global rateVar
    cost = costVar.get()
    if cost !="":
        try:
            cost = float(cost)
            #rateVar = float(rateVar)
            quantity=cost/itemRate
            quantityVar.set("%.2f"%quantity)
            costVar.set("%.2f"%cost)
        except ValueError:
            cost=cost[:-1]
            costVar.set(cost)
    else:
        cost=0
        costVar.set(cost)


######### variaveis de login ##########

usernameVar = StringVar()
passwordVar = StringVar()

########## variaveis mainwindow ##########

options = []
rateDict = {}
itemVariable = StringVar()
quantityVar = StringVar()
quantityVar.trace('w', quantityFieldListener)

itemRate = 2
rateVar = StringVar()
rateVar.set("%.2f"%itemRate)

costVar = StringVar()
costVar.trace('w', costFieldListener)

########  variaveis de itens #########

addItemNameVar = StringVar()
addItemRateVar = StringVar()
addItemTypeVar = StringVar()
addstoreVar = StringVar()
storeOptions = ['Congelado', 'Natural']
addstoreVar.set(storeOptions[0])

##################### generate bill ####################

#itemList = 
#totalCost =
#totalCostVar =

def generate_bill():
    global itemRate
    global quantityVar
    global itemVariable
    global costVar
    global rateVar
#    global itemList
#    global totalCost
#    global totalCostVar

    rate = rateVar.get()
    itemName = itemVariable.get()
    quantity = quantityVar.get()
    cost = costVar.get()

    conn = pymysql.connect(host="localhost",user="root", password="",db="billservice")
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    query =  f"insert into bill(name, quantity, rate, cost) values('{itemName}','{quantity}','{rate}','{cost}')"
    cursor.execute(query)
    conn.commit()
    conn.close()

    quantityVar.set("0")
    costVar.set("0")

################### exit ######################

def iExit():
    window.destroy()

################# read all data ######################

def readAllData():
    global options
    global rateDict
    global itemVariable
    global itemRate
    global rateVar

    options = []
    rateDict = {}

    conn = pymysql.connect(host="localhost",user="root", password="",db="billservice")
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    query = "select * from itemlist"
    cursor.execute(query)
    data = cursor.fetchall()

    count = 0
    for row in data:
        count+=1
        options.append(row['nameid'])
        rateDict[row['nameid']]=row['rate']
        itemVariable.set(options[0])
        itemRate=str(rateDict[options[0]])#int
    conn.close()
    rateVar.set(itemRate)
    if count == 0:
        remove_all_widgets()
        addItem()
    else:
        remove_all_widgets()
        mainwindow()

################### option menu Listener ########################

def optionMenuListener(event):
    global itemVariable
    global rateDict
    global itemRate
    item = itemVariable.get()
    itemRate = float(rateDict[item])
    rateVar.set("%.2f"%itemRate)



################# remove widget ######################

def remove_all_widgets():
    global window
    for widget in window.winfo_children():
        widget.grid_remove()

################ treeview #########################

billsTV = ttk.Treeview(height=15, columns=('Prod Nome','Quantidade', 'valor'))

################################ adminLogin #######################################

def adminLogin():
    global usernameVar
    global passwordVar

    username = usernameVar.get()
    password = passwordVar.get()

    conn = pymysql.connect(host="localhost",user="root", password="",db="billservice")
    cursor = conn.cursor()

    query = f"select * from users where username ='{username}' and password ='{password}'"
    cursor.execute(query)
    data = cursor.fetchall()
    admin = False
    for row in data:
        admin = True
    conn.close()
    if admin:
        readAllData()
    else:
        messagebox.showerror("USUARIO INVALIDO","FAVOR DIGITAR SENHA CORRETAMENTE.")
####################### funcao add item ################################

def additemListener():
    remove_all_widgets()
    addItem()

def funcAddItem():
    global addItemNameVar
    global addItemRateVar
    global addItemTypeVar
    global addstoreVar

    name = addItemNameVar.get()
    rate = addItemRateVar.get()
    type = addItemTypeVar.get()
    storeType = addstoreVar.get()
    nameID = name.replace(" ","_")

    conn = pymysql.connect(host="localhost",user="root", password="",db="billservice")
    cursor = conn.cursor()

    query =  f"insert into itemlist(name, nameid, rate, type, storetype) values('{name}','{nameID}','{rate}','{type}','{storeType}')"
    cursor.execute(query)
    conn.commit()
    conn.close()

    addItemNameVar.set("")
    addItemRateVar.set("")
    addItemTypeVar.set("")
    addstoreVar.set("")

####################### btn voltar ################################

'''def goBack():
    remove_all_widgets()
    mainwindow()'''

######################## loginWindow ############################

def loginWindow():
    window.geometry("460x350")
    titleLabel = Label(window, text="CUPOM FISCAL", font=("times new roman",35), fg="blue",bg="lightblue")
    titleLabel.grid(row=0, column=0, columnspan=4, padx=(40,0), pady=(10,0))

    loginLabel = Label(window, text="Login:", font="arial 30",bg="lightblue")
    loginLabel.grid(row=1, column=2, padx=(50,0),columnspan=2 , pady=10)

    usernameLabel = Label(window, text="Usuário:" , font=("bold", 15),bg="lightblue")
    usernameLabel.grid(row=2,column=2,padx=20, pady=5)

    passwordLabel = Label(window, text="Senha:", font=("bold", 15),bg="lightblue")
    passwordLabel.grid(row=3,column=2,padx=20, pady=5)

    usernameEntry = Entry(window, textvariable=usernameVar)
    usernameEntry.grid(row=2, column=3,padx=20, pady=5)

    passwordEntry = Entry(window, textvariable=passwordVar, show='*')
    passwordEntry.grid(row=3,column=3,padx=20, pady=5)

    loginButton = Button(window, text='Login', width=23, height=2, font="arial 17", bg="blue" ,fg="white" ,command=lambda:adminLogin())
    loginButton.grid(row=4, column=2, columnspan=2)

##################################### add item  #######################################################

def addItem():

    backButton = Button(window, text="Voltar",font="arial 10",bg="blue",fg='white',command=lambda:readAllData())
    backButton.grid(row=0, column=0, padx=(10,0))

    window.geometry("680x230")
    titleLabel = Label(window, text="CUPOM FISCAL", font="arial 30",width=25, fg="blue",bg="lightblue")
    titleLabel.grid(row=0, column=1, columnspan=4, pady=(10,0))

    itemNameLabel = Label(window, text="Nome:", font="arial 12",bg="lightblue")
    itemNameLabel.grid(row=1, column=1 , pady=(10,0))

    itemNameEntry = Entry(window, textvariable=addItemNameVar)
    itemNameEntry.grid(row=1, column=2 , pady=(10,0))

    itemRateLabel = Label(window, text="Preço Produto:", font="arial 12",bg="lightblue")
    itemRateLabel.grid(row=1, column=3 , pady=(10,0))

    itemRateEntry = Entry(window, textvariable=addItemRateVar)
    itemRateEntry.grid(row=1, column=4 , pady=(10,0))

    itemTypeLabel = Label(window, text="Tipo Produto:", font="arial 12",bg="lightblue")
    itemTypeLabel.grid(row=2, column=1 , pady=(10,0))

    itemTypeEntry = Entry(window, textvariable=addItemTypeVar)
    itemTypeEntry.grid(row=2, column=2 , pady=(10,0))

    storeTypeLabel = Label(window, text="Tipo Armazenamento:", font="arial 12",bg="lightblue")
    storeTypeLabel.grid(row=2, column=3 , pady=(10,0))

    storeTypeOptions = OptionMenu(window, addstoreVar, *storeOptions)
    storeTypeOptions.grid(row=2, column=4 , pady=(10,0))

    AddItemButton = Button(window, text="Add Item", width=15,height=2 ,font="arial 15",bg="blue",fg='white', command=lambda:funcAddItem())
    AddItemButton.grid(row=3, column=3, pady=(10,0))

#############################--   main window   --######################################################################

def mainwindow():
    window.geometry("950x600")
    titleLabel = Label(window, text="CUPOM FISCAL", font="arial 30", fg="blue",bg='lightblue')
    titleLabel.grid(row=0, column=1, columnspan=3, pady=(10,0))

    addButton = Button(window, text='Add Itens', width=15, height=2, font="arial 8", command=lambda:additemListener())
    addButton.grid(row=1, column=0, padx=(10,0), pady=(10,0))

    LogoutBtn = Button(window, text='Sair', width=15, height=2, font="arial 8", command=lambda:iExit())
    LogoutBtn.grid(row=1, column=4,  pady=(10,0))

    itemLabel = Label(window, text="Selecionar Item:",bg='lightblue')
    itemLabel.grid(row=2, column=0, padx=(5,0),pady=(10,0))

    itemDropDown = OptionMenu(window, itemVariable, *options, command=optionMenuListener)
    itemDropDown.grid(row=2, column=1, padx=(10,0), pady=(10,0))

    ############################### taxa ###############################################

    rateLabel = Label(window, text="Preço:", font="arial 8",bg='lightblue')
    rateLabel.grid(row=3,column=0,padx=(10,0), pady=(10,0))

    rateValue = Label(window, textvariable=rateVar,bg='lightblue')
    rateValue.grid(row=3,column=1,padx=(10,0), pady=(10,0))

    ############################ preco ##################################################

    costLabel = Label(window, text="Valor:",bg='lightblue')
    costLabel.grid(row=3,column=2,padx=(10,0), pady=(10,0))

    costEntry = Entry(window, textvariable=costVar)
    costEntry.grid(row=3, column=3,padx=(10,0), pady=(10,0))

    #############################################################

    quantityLabel = Label(window, text="Quantidade:",bg='lightblue')
    quantityLabel.grid(row=2,column=2,padx=(5,0), pady=(10,0))

    quantityEntry = Entry(window, textvariable=quantityVar)
    quantityEntry.grid(row=2, column=3,padx=(5,0), pady=(10,0))

    buttonBill = Button(window, text='Gerar Nota', command=lambda:generate_bill())
    buttonBill.grid(row=2,column=4,padx=(5,0), pady=(10,0))

    ################### tree view ##############################

    billLabel = Label(window, text="Produtos Listados:" ,font="Arial 25",bg='lightblue')
    billLabel.grid(row=4,column=2)

    billsTV.grid(row=5, column=0, columnspan=4, padx=(5))

    scrollBar = Scrollbar(window, orient="vertical", command=billsTV.yview)
    scrollBar.grid(row=5,column=3, sticky="NSE")

    billsTV.configure(yscrollcommand=scrollBar.set)

    billsTV.heading('#0', text="Nome Prod")
    billsTV.heading('#1', text="Preço")
    billsTV.heading('#2', text="Quantidade")
    billsTV.heading('#3', text="Valor")

    
    


loginWindow()

window.mainloop()