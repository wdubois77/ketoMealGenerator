import csv
import random
from datetime import datetime, date, timedelta
import calendar
import os

def GetRandomProteinSource():
    ##try:
    filePath = 'data/protein_sources2.csv'
    proteinSources = []
    with open(filePath) as fileObject:
        reader = csv.reader(fileObject)
        next(fileObject)
        for row in reader:
            proteinSources.append(row[1] + "/" + row[8] + "/" + row[9] + "/" + row[10])
    return random.sample(proteinSources, 1)
    #except:
    #    print("Exception!")
    #    raise

def GetRandomVegetable():
    vegetables = []
    with open('data/vegetables2.csv') as fileObject:
        reader = csv.reader(fileObject)
        next(fileObject)
        for row in reader:
            vegetables.append(row[1])
    return str(random.sample(vegetables, 1))

def GetRandomSauce():
    sauces = []
    with open('data/sauces2.csv_with_UTF-8_BOM.csv') as fileObject:
        reader = csv.reader(fileObject)
        encoding='utf8'
        next(fileObject)
        for row in reader:
            sauces.append(row[1])
    return str(random.sample(sauces, 1))

def PrintMeal():
    #try:
    global mealString2
    global proteinSourceName
    global proteinAankooptip
    global proteinBereidingstip
    global proteinTimeMode
    global randomVegetable
    global randomSauce
    proteinElements = str(GetRandomProteinSource()).split('/')
    proteinSourceName = str(proteinElements[0])
    proteinAankooptip = str(proteinElements[1])
    proteinBereidingstip = str(proteinElements[2])
    proteinTimeMode = str(proteinElements[3])
    randomVegetable = str(GetRandomVegetable())
    randomSauce = str(GetRandomSauce())
    if 's' in proteinTimeMode:
        mealString2 = proteinSourceName + " / " + randomVegetable
    else:
        mealString2 = proteinSourceName + " / " + randomVegetable + " / " + randomSauce
    for character in '[]\'':
        mealString2 = mealString2.replace(character, '')
        proteinSourceName = proteinSourceName.replace(character, '')
        proteinTimeMode = proteinTimeMode.replace(character, '')
        randomVegetable = randomVegetable.replace(character, '')
        randomSauce = randomSauce.replace(character, '')
    return mealString2
    #except:
    #    raise

def UpdateMeal(vegetable, sauce):
    if 's' in proteinTimeMode:
        if vegetable == "Insert seasonal vegetable":
            mealStringUpdated = proteinSourceName + " / " + randomVegetable
        else:
            mealStringUpdated = proteinSourceName + " / " + vegetable
    else:
        if vegetable == "Insert seasonal vegetable":
            mealStringUpdated = proteinSourceName + " / " + randomVegetable + " / " + sauce
        elif sauce == "Change sauce":
            mealStringUpdated = proteinSourceName + " / " + vegetable + " / " + randomSauce
        else:
            mealStringUpdated = proteinSourceName + " / " + vegetable + " / " + sauce
    return mealStringUpdated

def NeedsTime():
    result = False
    if proteinTimeMode == 's' or proteinTimeMode == 'we':
        result = True
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

def SaveMeal(datum, meal):
    datumString = datum.strftime('%d/%m/%Y')
    row = [datumString, meal]
    RemoveMeal(datumString)
    with open("data/mealplan.csv", 'a') as fileObject:
        writer = csv.writer(fileObject)
        writer.writerow(row)

def CheckIfSufficientVariation(datum):
    result = True
    for meal in GetPastTwoWeeksMeals(datum):
        if proteinSourceName in meal:
            result = False
    return result

def GetProteinSourceName():
    return proteinSourceName

def GetPastTwoWeeksMeals(datum):
    dictMeals = GetMealsDict()   
    listPastTwoWeeksMeals = []
    for key in dictMeals:
        if key.date() < datum and key.date() > datum - timedelta(days=14):
            listPastTwoWeeksMeals.append(dictMeals[key])
    return listPastTwoWeeksMeals

def GetMealsDict():
    listKeys = []
    listValues = []
    with open('data/mealplan.csv') as fileObject:
        reader = csv.reader(fileObject)
        for row in reader:
            date = datetime.strptime(row[0], '%d/%m/%Y')
            listKeys.append(date)
            listValues.append(row[1])
            next(fileObject)
    result = dict(zip(listKeys, listValues))
    sortedResult = dict(sorted(result.items(), reverse=False))
    return sortedResult

def GetAllPlannedMeals():
    dictMeals = GetMealsDict()
    listMeals = []
    for key in dictMeals:
        listMeals.append((key.date().strftime('%A %d/%m/%Y : '), dictMeals[key]))
    return listMeals

def ExportSevenDayMealPlan():
    mealPlan = GetSevenDayMealPlan()
    mealsWithDates = []
    for item in mealPlan:
        mealsWithDates.append(item[0] + item[1])
        aankooptip = GetTips(item[1])[1]
        bereidingstip = GetTips(item[1])[2]
        if aankooptip == "":
            mealsWithDates.append('\tNog geen aankooptip beschikbaar')
        else:
            mealsWithDates.append('\t' + str(aankooptip))
        if bereidingstip == "":
            mealsWithDates.append('\tNog geen bereidingstip beschikbaar')
        else:
            mealsWithDates.append('\t' + str(bereidingstip))
        mealsWithDates.append('\n')
    with open('data/sevenDayMealPlan.txt', 'w') as fileObject:
        fileObject.write('\n'.join(mealsWithDates))

def GetAllProteinSources():
    proteinSources = []
    with open('data/protein_sources2.csv') as fileObject:
        reader = csv.reader(fileObject)
        next(fileObject)
        for row in reader:
            proteinSources.append(row[1] + "/" + row[8] + "/" + row[9])
    return proteinSources

def GetVegetables():
    vegetables = []    
    stringDateOfToday = str(date.today())
    dateElements = stringDateOfToday.split('-')
    currentMonthNumber = dateElements[1]
    with open('data/vegetables2.csv') as fileObject:
        reader = csv.reader(fileObject)
        next(fileObject)
        for row in reader:
            if currentMonthNumber in row[6]:
                vegetables.append(row[1])
    return vegetables

def GetSauces():
    sauces = []
    with open('data/sauces2.csv_with_UTF-8_BOM.csv') as fileObject:
        reader = csv.reader(fileObject)
        next(fileObject)
        for row in reader:
            sauces.append(row[1])
    return sauces

def GetAllEssentials():
    essentials = []
    with open('data/sauces2.csv_with_UTF-8_BOM.csv') as fileObject:
        reader = csv.reader(fileObject)
        next(fileObject)
        for row in reader:
            essentials.append(row[7])
    essentialsSplitted = []
    for item in essentials:
        essentialsElements = item.split(' ')
        for element in essentialsElements:
            essentialsSplitted.append(element)
    essentialsSplitted = list(set(essentialsSplitted))
    return essentialsSplitted

def GetSauceEssentials(sauce):
    sauceEssentialsString = ""
    with open('data/sauces2.csv_with_UTF-8_BOM.csv') as fileObject:
        reader = csv.reader(fileObject)
        next(fileObject)
        for row in reader:
            if sauce == row[1]:
                sauceEssentialsString = row[7]
    sauceEssentials = sauceEssentialsString.split(' ')
    return sauceEssentials

def GetTips(meal):    
    mealElements = str(meal).split('/')
    for item in GetAllProteinSources():
        mealElement = mealElements[0][:-1]
        if mealElement in item:
            itemElements = item.split('/')
            return itemElements

def PrintAankooptip():
    tip = proteinAankooptip
    for character in '[]\'':
        tip = tip.replace(character, '')
    if tip == "":
        tip = "Nog geen aankooptip beschikbaar."
    return tip

def PrintBereidingstip():
    tip = proteinBereidingstip
    for character in '[]\'':
        tip = tip.replace(character, '')
    if tip == "":
        tip = "Nog geen bereidingstip beschikbaar."
    return tip

def GetSevenDayMealPlan():
    dictMeals = GetMealsDict()
    listSevenDaysMeals = []
    stringDateOfToday = str(date.today())
    dateOfToday = datetime.strptime(stringDateOfToday, '%Y-%m-%d')
    for key in dictMeals:
        if key >= dateOfToday and key < dateOfToday + timedelta(days=7):
            listSevenDaysMeals.append((key.date().strftime('%A %d/%m/%Y : '), dictMeals[key]))
    return listSevenDaysMeals

def CheckVariation(mealplan):
    listProteinSources = []
    for item in mealplan:
        mealElements = item[1].split(' / ')
        listProteinSources.append(mealElements[0])
    listMeats = []
    with open('data/protein_sources2.csv') as fileObject:
        reader = csv.reader(fileObject)
        next(fileObject)
        for row in reader:
            if row[3] == 'vlees' or row[3] == 'wild':
                listMeats.append(row[1])
    counterMeat = 0
    for item in listProteinSources:
        if item in listMeats:
            counterMeat += 1
    maxMeatRatio = 4 / 7
    numberOfEntriesInPlan = len(listProteinSources)
    if counterMeat / numberOfEntriesInPlan > maxMeatRatio:
        result = "Meat is planned on " + str(counterMeat) + " of the " + str(numberOfEntriesInPlan) + " days. \nTry to provide more variety and plan more often for fish and/or poultry."
    else:
        result = "Meat is only planned on " + str(counterMeat) + " of the " + str(numberOfEntriesInPlan) + " days. \nThis means sufficient variety between meat and other protein sources."
    return result

 