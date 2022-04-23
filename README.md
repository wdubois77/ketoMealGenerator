# ketoMealGenerator
Generate random keto meal ideas and insert meals in week plan.

The user can generate random keto meals. 
Three csv files with proven keto components are used: protein_sources2.csv; vegetables2.csv and sauces2.csv. 
Certain protein sources (e.g. 'osso buco') imply a stew: in that case, only a vegetable is shown and no sauce,
because the stewed protein source in itself provides a sauce.

For the protein source (e.g. 'tenderloin') of the generated meal, a buying respectively cooking tip (if available) can be shown in the screen.

If desired, the generated vegetable can be replaced by another vegetable; in a drop-down menu the user can choose from the seasonal vegetables available in the current month.

The generated sauce can also be changed, also from a drop-down menu at the top of the screen.

In addition the user has the possibility to add the generated meal, adjusted or not, to his meal plan (mealplan.csv). 
To do this he has to select a date and click on the 'Add Meal' button. The added meal appears in the list on the screen. The list is sorted by date. 
Every meal in the list can be deleted again by selecting it.

When adding a meal, the application checks:
-	Whether a meal with the same protein source has not been planned before, and this in the period of two weeks preceding the selected date. 
If this is the case, the user is informed that it is best to provide sufficient variation and he is asked, to answer with yes or no,
whether he still wants to save the meal.
-	If the protein source in question does not imply a dish that requires a reasonable amount of preparation time, either because it is a stew (e.g. 'stewed rabbit') 
or because it otherwise takes a reasonable amount of time to prepare (e.g. 'duck confit'). 
In such a case, if the user wants to save this dish on a normal weekday, he gets the suggestion (also by means of a message box) 
to save this dish on a day in the weekend. Nevertheless, by choosing 'yes' the user can still save the meal on the chosen weekday.

The user can also display his meal plan for the next seven days. To do so, he clicks on the button 'Export 7 Day Meal Plan'. 
This opens a second screen in which the saved meals for the next seven days are shown in a list. 
The user can then save this 7 Day Meal Plan, with the associated buying and cooking tips, as a text file. 

TO DO: Still in this second screen, the user can also have an analysis made of the compiled meal plan, in the sense that the application then checks 
whether there is sufficient variation between meat, fish and poultry and between the available vegetables.

TO DO: For a selected meal, also in the second screen, a list is shown with the classis keto ingredients 
(of which we think the user should always have them in stock, such as butter, full cream, parmesan cheese,...) 
that are needed for that specific meal.

