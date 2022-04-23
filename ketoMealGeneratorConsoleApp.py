from os import system, name
from colorama import Fore, Back, Style
from termcolor import colored
#from meal import Meal
import csv
import random
from datetime import datetime, date, timedelta
import calendar

def ClearConsole():
    command = "clear"
    if name in ("nt", "dos"):
        command = "cls"
    system(command)
    #print('\n' * 30)

def ShowMainMenu():
    #ClearConsole()
    print()
    print("###################")
    print("Keto Meal Generator")
    print("###################")
    print()
    print("Maak een keuze:")
    print("1) Genereer een keto maaltijd")
    print("2) Toon planning voor de komende 7 dagen")
    print("3) Einde")
    keuze = input()
    return keuze

def ShowGenerateMealMenu():
    print("Maak een keuze:")
    print("1) Genereer opnieuw")
    print("2) Toon aankoop- en bereidingstips (voor eiwitbron)")
    print("3) Deze maaltijd plannen")
    print("4) Maak boodschappenlijstje")
    print("5) Terug naar hoofdmenu")
    keuze = input()
    return keuze

def GetRandomProteinSource():
    filenameProtein = 'data/protein_sources2.csv'
    protein_sources = []
    aankooptip = ""
    with open(filenameProtein) as file_object:
        reader = csv.reader(file_object)
        next(file_object)
        for row in reader:
            protein_sources.append(row[1] + "/" + row[8] + "/" + row[9])
    randomProteinSource = random.sample(protein_sources, 1)
    return randomProteinSource

def GetRandomVegetable():
    filenameVegetables = 'data/vegetables2.csv'
    vegetables = []
    with open(filenameVegetables) as file_object:
        reader = csv.reader(file_object)
        next(file_object)
        for row in reader:
            vegetables.append(row[1])
    randomVegetable = str(random.sample(vegetables, 1))
    return randomVegetable

def GetRandomSauce():
    filenameSauces = 'data/sauces2.csv'
    sauces = []
    with open(filenameSauces) as file_object:
        reader = csv.reader(file_object)
        next(file_object)
        for row in reader:
            sauces.append(row[1])
    randomSauce = str(random.sample(sauces, 1))
    return randomSauce

def PrintMeal():
    global mealString2
    global proteinAankooptip
    global proteinBereidingstip    
    proteinElements = str(GetRandomProteinSource()).split('/')
    proteinSourceName = str(proteinElements[0])
    proteinAankooptip = str(proteinElements[1])
    proteinBereidingstip = str(proteinElements[2])

    mealString2 = proteinSourceName + " / " + GetRandomVegetable() + " / " + GetRandomSauce()
    for character in '[]\'':
        mealString2 = mealString2.replace(character, '')

    #mealString = ""
    #meal = Meal(proteinSourceName, GetRandomVegetable(), GetRandomSauce(), None, None)
    #mealList = meal.proteinSource + meal.vegetables + meal.sauce
    #for item in mealList:
    #    mealString = mealString + item + " / "
    #mealString = mealString[:-3]

    #text = colored(mealString, 'cyan', attrs=[])
    #print(text)
    #print('\n', Fore.CYAN + mealString, '\n')
    
    print('\n', mealString2, '\n')

def PrintCalendar():
    #ClearConsole()
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    print('\n', calendar.month(currentYear, currentMonth))
    if currentMonth == 12:
        print(calendar.month(currentYear+1, 1))
    else:
        print(calendar.month(currentYear, currentMonth+1))

def IsValidDate(datum):
    format = '%d/%m/%Y'
    result = False
    try:
        result = bool(datetime.strptime(datum, format))
    except ValueError:
        print("Dit is geen geldige datum. Probeer opnieuw:")
    return result

def IsFutureDate(datum):
    result = False
    datum = datetime.strptime(datum, '%d/%m/%Y')
    if datum >= datetime.today() - timedelta(days=1):
        result = True
    return result

def RemoveMeal(datum):
    with open("data/mealplan.csv", 'r') as inp:
        datum = datetime.strptime(datum, '%d/%m/%Y')
        newRows = []
        data = csv.reader(inp)
        for row in data:
            dateOutCsv = datetime.strptime(row[0], '%d/%m/%Y')
            if dateOutCsv != datum:
                newRows.append(row)
            next(inp)
    with open("data/mealplan.csv", 'w') as out:
        writer = csv.writer(out)
        for row in newRows:
            writer.writerow(row)

def SaveMeal():
    PrintCalendar()
    print("Selecteer een datum (\"dd/mm/yyyy\"):")
    datum = input()
    while not IsValidDate(datum):
        datum = input()
    while not IsFutureDate(datum):
        print("De datum mag niet in het verleden liggen. Probeer opnieuw:")
        datum = input()
    row = [datum, mealString2]
    RemoveMeal(datum)
    with open("data/mealplan.csv", 'a') as file_object:
        writer = csv.writer(file_object)
        writer.writerow(row)

def PrintMealPlan():
    filenameMealPlan = 'data/mealplan.csv'
    listKeys = []
    listValues = []
    with open(filenameMealPlan) as file_object:
        reader = csv.reader(file_object)
        for row in reader:
            date = datetime.strptime(row[0], '%d/%m/%Y')
            listKeys.append(date)
            listValues.append(row[1])
            next(file_object)
    result = dict(zip(listKeys, listValues))
    sortedResult = dict(sorted(result.items(), reverse=False))
    stringDateOfToday = str(date.today().date())
    dateOfToday = datetime.strptime(stringDateOfToday, '%Y-%m-%d')
    print()
    
    for key in sortedResult:
        if key >= dateOfToday and key < dateOfToday + timedelta(days=7):
            print(key.date().strftime('%A %d/%m/%Y : '), sortedResult[key])
    
    #for item in sortedResult:
        #print(item)

    print("\nDruk op enter om terug te keren naar het hoofdmenu.")
    input()

def PrintAankoopEnBereidingstips():
    tip1 = proteinAankooptip
    tip2 = proteinBereidingstip
    for character in '[]\'':
        tip1 = tip1.replace(character, '')
        tip2 = tip2.replace(character, '')
    print("\n Aankooptip: ", tip1, '\n')    
    print(" Bereidingstip: ", tip2, '\n')
 
while True:
    keuze = ShowMainMenu()
    if keuze == "1":            # "Genereer een keto maaltijd"       
        PrintMeal();
        while True:
            keuze = ShowGenerateMealMenu()
            if keuze == "1":        # "Genereer opnieuw"
                PrintMeal()
            elif keuze == "2":      # "Toon aankoop- en bereidingstips"
                PrintAankoopEnBereidingstips()
            elif keuze == "3":      # "Deze maaltijd plannen"
                SaveMeal()
                break
            elif keuze == "5":      # "Terug naar hoofdmenu"
                break  
    elif keuze == "2":          # "Toon weekplanning"
        PrintMealPlan()
    elif keuze == "3":          # "Einde"   
        break





