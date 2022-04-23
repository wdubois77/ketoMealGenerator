class Meal:
    def __init__(self, proteinSource, vegetables, sauce, aankooptip, bereidingstip):
        self.proteinSource = proteinSource
        self.vegetables = vegetables
        self.sauce = sauce
        self.aankooptip = aankooptip
        self.bereidingstip = bereidingstip


from tkinter import *
from tkinter import messagebox
from tkinter import Image
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from ketoMealGenRepository import *

top = Tk()
top.title("Keto Meal Generator")
top.geometry("950x600")

bgimg = PhotoImage(file='data/avo2.png')#, master=top)
lblBg = Label(top, image=bgimg)
lblBg.place(x=0, y=0, relwidth=1, relheight=1)
lblBg.image = bgimg
lblBg.config(image=lblBg.image)

mealString = StringVar()
buyingTip = StringVar()
cookingTip = StringVar()
clickedVegetables = StringVar()  
clickedSauces = StringVar()

def OpenNewWindow():
    
    def LoadSevenDayMealPlan(mealPlan):
        for item in mealPlan:
            mealWithDate = item[0] + item[1]
            lbxMealPlan.insert("end", mealWithDate)
    
    def CheckVariation(mealPlan):
        pass

    newWindow = Toplevel(top)
    newWindow.title("Seven day meal plan") 
    newWindow.geometry("700x450")     
    #top.rowconfigure(0, weight=1)
    #top.rowconfigure(1, weight=10)    
    lblMessage = Label(newWindow, text ="The following meal plan was succesfully saved as sevenDayMealPlan.txt :")
    lblMessage.grid(column=0, row=0, sticky='w')
    lbxMealPlan = Listbox(newWindow, width=80)
    lbxMealPlan.grid(row=1, column=0, sticky="nsew")
    LoadSevenDayMealPlan(GetSevenDayMealPlan())

def btnExportWeekPlanClicked():
    ExportSevenDayMealPlan()
    OpenNewWindow()

def LoadAllMeals():
    listAllMeals = GetAllPlannedMeals()
    lbxMeals.delete(0, END)
    for item in listAllMeals:
        mealWithDate = item[0] + item[1]
        lbxMeals.insert("end", mealWithDate)

def btnGenerateKetoMealClicked():
    mealString.set(PrintMeal())
    btnShowBuyingTip["state"] = "normal"
    btnShowCookingTip["state"] = "normal"
    btnSaveMeal["state"] = "normal"
    buyingTip.set("")
    cookingTip.set("")
    #clickedVegetables.set( "Change vegetable*" )
    #clickedSauces.set("Change sauce")
    #lblInfoSaveMeal1.config(text="This meal can be added to meal planning.")

def ChangedVegetables(*args):
    selectedVegetable = clickedVegetables.get()
    generatedMeal = mealString.get()
    if generatedMeal != "":
        mealString.set(UpdateMealVegetable(selectedVegetable))

def ChangedSauces(*args):
    selectedSauce = clickedSauces.get()
    generatedMeal = mealString.get()
    if generatedMeal != "":
        mealString.set(UpdateMealSauce(selectedSauce))

def Changed(*args):
    selectedVegetable = clickedVegetables.get()
    selectedSauce = clickedSauces.get()
    generatedMeal = mealString.get()
    if generatedMeal != "":
        mealString.set(UpdateMeal(selectedVegetable, selectedSauce))


def btnShowBuyingTipClicked():
    buyingTip.set(PrintAankooptip())

def btnShowCookingTipClicked():
    cookingTip.set(PrintBereidingstip())

def btnSaveMealClicked():
    datum = datePicker.get_date()
    datumString = datum.strftime('%d/%m/%Y')
    listWeekendDays = ['Saturday','Sunday']
    nameSelectedDay = datum.strftime('%A')
    message = ""
    result = True
    if NeedsTime():
        if nameSelectedDay not in listWeekendDays:
            message = "It might be better to plan this meal for the weekend because it takes some time to prepare.\nDo you still want to save this meal?"
            result = messagebox.askyesno('Time consuming preparation', message)
    if result == True:
        if CheckIfSufficientVariation(datum) == False:
            message = GetProteinSourceName() + " was/is already planned less than two weeks prior to " + datumString + ".\nDo you still want to save this meal?"
            result = messagebox.askyesno('Ensure sufficient variation', message)
            if result == True:
                SaveMeal(datum)
                LoadAllMeals()
        else:
            SaveMeal(datum)
            LoadAllMeals()

def btnDeleteMealClicked():
    if lbxMeals.curselection():
        selectedItem = lbxMeals.get(lbxMeals.curselection())
        itemElements = selectedItem.split(':')
        datumString = itemElements[0]
        RemoveMeal(datumString[-11:-1])
        LoadAllMeals()

top.columnconfigure(0, minsize=250)
top.columnconfigure(1, weight=2)
top.columnconfigure(2, minsize=40)

btnGenerateKetoMeal = Button(top, text="Generate Keto Meal", command=btnGenerateKetoMealClicked, bg="#c15653", fg="white")
btnGenerateKetoMeal.grid(row=0, column=1, padx=20, pady=10, sticky='w')

#btnGenerateKetoMeal.grid(row=0, column=0, columnspan=2, padx=10, pady=20)

optionsVegetables = GetVegetables()
clickedVegetables.set( "Change vegetable*" )
dropVegetable = OptionMenu(top, clickedVegetables, *optionsVegetables)
dropVegetable.grid(row=0, column=1, sticky='w', padx=165, pady=10)

clickedVegetables.trace("w", Changed)

optionsSauces = GetSauces()
clickedSauces.set("Change sauce")
dropSauces = OptionMenu(top, clickedSauces, *optionsSauces)
dropSauces.grid(row=0, column=1, padx=0, sticky='e')

clickedSauces.trace("w", Changed)
  
lblKetoMeal = Label(top, textvariable=mealString, font=("bold", 16))#, bg="#FFC14D")
lblKetoMeal.grid(row=1, column=1, columnspan=2, padx=30, sticky='w')

top.rowconfigure(2, minsize=30)
top.rowconfigure(6, minsize=30)
top.rowconfigure(7, minsize=30)
top.rowconfigure(8, minsize=30)
top.rowconfigure(9, minsize=30)
top.rowconfigure(10, minsize=30)
top.rowconfigure(11, minsize=30)
top.rowconfigure(12, minsize=30)
top.rowconfigure(13, minsize=30)
top.rowconfigure(14, minsize=30)
top.rowconfigure(15, minsize=30)
top.rowconfigure(16, minsize=30)
top.rowconfigure(17, minsize=30)

#lblInfoTips = Label(top) #, text="")  #"Tips for buying and cooking available")
#lblInfoTips.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

#btnFrame = Frame(top, bg='#9FD996')
#btnFrame.grid(row=3, column=0, columnspan=2, padx=50, sticky="nsew")

btnShowBuyingTip = Button(top, text="Show Buying Tip", state="disabled", command=btnShowBuyingTipClicked) 
btnShowBuyingTip.grid(row=3, column=0, padx=25, sticky='w')
btnShowCookingTip = Button(top, text="Show Cooking Tip", state="disabled", command=btnShowCookingTipClicked)
btnShowCookingTip.grid(row=3, column=0, sticky='e')

#btnShowBuyingTip = Button(btnFrame, text="Show Buying Tip", state="disabled", command=btnShowBuyingTipClicked) #.grid(row=3, column=0, columnspan=2, sticky='w')
#btnShowCookingTip = Button(btnFrame, text="Show Cooking Tip", state="disabled", command=btnShowCookingTipClicked) #.grid(row=3, column=0, columnspan=2, sticky='e')
#btnShowBuyingTip.pack(side="left")
#btnShowCookingTip.pack(side="right")

lblTip1 = Label(top, textvariable=buyingTip, bg="#fce17c")
lblTip1.grid(row=4, column=0, columnspan=3, padx=25, pady=20, sticky='w')
lblTip2 = Label(top, textvariable=cookingTip, bg="#fce17c")
lblTip2.grid(row=5, column=0, columnspan=3, padx=25, sticky='w')

#lblEmpty = Label(top, text="", bg="#9FD996")
#lblEmpty.grid(row=6, column=0)
#lblInfoSaveMeal1 = Label(top, text="This meal can be added to meal planning.", bg="#9FD996")
#lblInfoSaveMeal1.grid(row=7, column=0, padx=10) 
#lblInfoSaveMeal2 = Label(top, text="Please select date:", bg="#9FD996")
#lblInfoSaveMeal2.grid(row=8, column=0)

datePicker = DateEntry(top, width=16, bg="#9FD996", foreground="white", mindate=datetime.now())
datePicker.grid(row=8, column=0) #, bd=2)

btnSaveMeal = Button(top, text="Add Meal", state="disabled", command=btnSaveMealClicked)
btnSaveMeal.grid(row=10, column=0, padx=10)#, pady=10)

#lbxFrame = Frame(top, bg='#9FD996')
#lbxFrame.grid(row=6, rowspan=5, column=1, padx=30, pady=20, sticky="nsew") #columnspan=2, 

lbxMeals = Listbox(top, width=75)
lbxMeals.grid(row=6, rowspan=8, column=1, pady=20, sticky="nsew")
scrollbar = Scrollbar(top, orient=VERTICAL)
scrollbar.grid(row=6, rowspan=8, column=2, pady=20, sticky="nsw")
lbxMeals.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=lbxMeals.yview)

#lbxMeals = Listbox(lbxFrame, width=75)
#lbxMeals.pack(side="left", fill = BOTH)
#scrollbar = Scrollbar(lbxFrame, orient=VERTICAL)
#lbxMeals.config(yscrollcommand=scrollbar.set)
#scrollbar.config(command=lbxMeals.yview)
#scrollbar.pack(side="right", fill = BOTH)

btnFrameBottom = Frame(top)#, bg='#9FD996')
btnFrameBottom.grid(row=14, column=1, padx=100, sticky="nsew")

btnDeleteMeal = Button(btnFrameBottom, text="Delete Meal", state="normal", command=btnDeleteMealClicked)
btnExportWeekPlan = Button(btnFrameBottom, text="Export 7 day Meal Plan", state="normal", command=btnExportWeekPlanClicked)
btnDeleteMeal.pack(side="left")
btnExportWeekPlan.pack(side="right")

#LoadListSevenDayMealPlan()
LoadAllMeals()

mainloop()

#Label(text="I'm in the first window!").pack()
#second = Toplevel()
#Label(second, text="I'm in the second window!").pack()


