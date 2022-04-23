from tkinter import *
from tkinter import messagebox
from tkinter import Image
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from ketoMealGenRepository import *

top = Tk()
top.title("Keto Meal Generator")
top.geometry("800x550")
top.resizable(width=False, height=False)

bgimg = PhotoImage(file='data/avo2.png')
lblBg = Label(top, image=bgimg)
lblBg.place(x=0, y=0, relwidth=1, relheight=1)
lblBg.image = bgimg
lblBg.config(image=lblBg.image)

mealString = StringVar()
buyingTip = StringVar()
cookingTip = StringVar()
clickedVegetables = StringVar()  
clickedSauces = StringVar()
message = StringVar()

def OpenNewWindow():
    
    def LoadSevenDayMealPlan(mealPlan):
        for item in mealPlan:
            mealWithDate = item[0] + item[1]
            lbxMealPlan.insert("end", mealWithDate)    

    def btnSavePlanClicked():
        ExportSevenDayMealPlan()
        message.set("Meal plan successfully saved!")

    def btnAnalysePlanClicked():
        analysis = CheckVariation(GetSevenDayMealPlan())
        message.set(analysis)

    newWindow = Toplevel(top)
    newWindow.title("Seven day meal plan") 
    newWindow.geometry("751x500")
    newWindow.resizable(width=False, height=False)    
    bgimg2 = PhotoImage(file='data/ketoFood2.png')
    lblBg2 = Label(newWindow, image=bgimg2)
    lblBg2.place(x=0, y=0, relwidth=1, relheight=1)
    lblBg2.image = bgimg2
    lblBg2.config(image=lblBg2.image)
    newWindow.rowconfigure(0, minsize=40)
    newWindow.rowconfigure(1, weight=1)
    newWindow.rowconfigure(2, weight=1)
    newWindow.rowconfigure(3, weight=1)
    newWindow.rowconfigure(4, weight=1)
    newWindow.rowconfigure(5, weight=1)
    newWindow.columnconfigure(0, minsize=40)
    newWindow.columnconfigure(1, weight=2, uniform='column')
    newWindow.columnconfigure(2, weight=1, uniform='column')
    #newWindow.columnconfigure(3, weight=1)

    lbxMealPlan = Listbox(newWindow)#, width=80)
    lbxMealPlan.grid(row=1, column=1, sticky="nsew")

    btnSavePlan = Button(newWindow, text="Save plan as txt-file", command=btnSavePlanClicked)
    btnSavePlan.grid(row=2, column=1)
    btnAnalysePlan = Button(newWindow, text="Analyse meal plan", command=btnAnalysePlanClicked)
    btnAnalysePlan.grid(row=2, column=1, sticky='e')

    lblMessages = Label(newWindow, textvariable=message, bg="#271916", fg="white")
    lblMessages.grid(row=4, column=1, sticky='w')

    LoadSevenDayMealPlan(GetSevenDayMealPlan())
    message.set("")


def btnExportWeekPlanClicked():
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
    dropVegetable.configure(state="normal")
    dropSauces.configure(state="normal")
    #clickedVegetables.set( "Change vegetable*" )
    #clickedSauces.set("Change sauce")

def Changed(*args):
    selectedVegetable = clickedVegetables.get()
    selectedSauce = clickedSauces.get()
    generatedMeal = mealString.get()
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
                SaveMeal(datum, mealString.get())
                LoadAllMeals()
        else:
            SaveMeal(datum, mealString.get())
            LoadAllMeals()

def btnDeleteMealClicked():
    if lbxMeals.curselection():
        selectedItem = lbxMeals.get(lbxMeals.curselection())
        itemElements = selectedItem.split(':')
        datumString = itemElements[0]
        RemoveMeal(datumString[-11:-1])
        LoadAllMeals()

top.columnconfigure(0, weight=1, uniform='column')
top.columnconfigure(1, weight=3, uniform='column')
top.columnconfigure(2, minsize=40)
top.rowconfigure(0, weight=1)
top.rowconfigure(1, weight=1)
top.rowconfigure(2, weight=1)
top.rowconfigure(3, weight=1)
top.rowconfigure(4, weight=1)
top.rowconfigure(5, weight=1)
top.rowconfigure(6, weight=1)
top.rowconfigure(7, weight=1)
top.rowconfigure(8, weight=1)
top.rowconfigure(9, weight=1)
top.rowconfigure(9, weight=1)
top.rowconfigure(10, weight=1)
top.rowconfigure(11, weight=1)
top.rowconfigure(12, weight=1)
top.rowconfigure(13, weight=1)
top.rowconfigure(14, weight=1)
top.rowconfigure(15, weight=1)
top.rowconfigure(16, weight=1)
top.rowconfigure(17, weight=1)
top.rowconfigure(18, weight=1)
top.rowconfigure(19, weight=1)
top.rowconfigure(20, weight=1)

btnFrameTop = Frame(top)
btnFrameTop.grid(row=1, column=1, sticky="nsew")

btnGenerateKetoMeal = Button(btnFrameTop, text="Generate Keto Meal", command=btnGenerateKetoMealClicked, bg="#c15653", fg="white")
btnGenerateKetoMeal.pack(side=LEFT, padx=10)

optionsVegetables = GetVegetables()
clickedVegetables.set( "Insert seasonal vegetable" )
dropVegetable = OptionMenu(btnFrameTop, clickedVegetables, *optionsVegetables)
dropVegetable.configure(state="disabled")
dropVegetable.pack(side=LEFT, padx=10)

clickedVegetables.trace("w", Changed)

optionsSauces = GetSauces()
clickedSauces.set("Change sauce")
dropSauces = OptionMenu(btnFrameTop, clickedSauces, *optionsSauces)
dropSauces.configure(state="disabled")
dropSauces.pack(side=LEFT, padx=10)

clickedSauces.trace("w", Changed)
  
lblKetoMeal = Label(top, textvariable=mealString, font=("bold", 16))
lblKetoMeal.grid(row=2, column=0, columnspan=2)

btnShowBuyingTip = Button(top, text="Show Buying Tip", state="disabled", command=btnShowBuyingTipClicked) 
btnShowBuyingTip.grid(row=4, column=0)
btnShowCookingTip = Button(top, text="Show Cooking Tip", state="disabled", command=btnShowCookingTipClicked)
btnShowCookingTip.grid(row=4, column=1, sticky='w')

lblTip1 = Label(top, textvariable=buyingTip, bg="#fce17c")
lblTip1.grid(row=5, column=0, columnspan=2, padx=25, sticky='w')
lblTip2 = Label(top, textvariable=cookingTip, bg="#fce17c")
lblTip2.grid(row=6, column=0, columnspan=2, padx=25, sticky='w')

datePicker = DateEntry(top, width=16, bg="#9FD996", foreground="white", mindate=datetime.now())
datePicker.grid(row=9, column=0)

btnSaveMeal = Button(top, text="Add Meal", state="disabled", command=btnSaveMealClicked)
btnSaveMeal.grid(row=10, column=0, sticky='n')

lbxMeals = Listbox(top)
lbxMeals.grid(row=9, rowspan=4, column=1, sticky="nsew")
scrollbar = Scrollbar(top, orient=VERTICAL)
scrollbar.grid(row=9, rowspan=4, column=2, sticky="nsw")
lbxMeals.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=lbxMeals.yview)

btnDeleteMeal = Button(top, text="Delete Meal", state="normal", command=btnDeleteMealClicked)
btnExportWeekPlan = Button(top, text="Export 7 day Meal Plan", state="normal", command=btnExportWeekPlanClicked)
btnDeleteMeal.grid(row=14, column=1)
btnExportWeekPlan.grid(row=14, column=1, sticky='e')

LoadAllMeals()

mainloop()



