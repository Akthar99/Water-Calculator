# process of the Water Calculation App

## App Structure

(App has a button that can count a water amount you take each day). I will seperate every weeks water calculation of mine and store it in the database. there for I can track all my data.

About the button : this button must contain 3 child buttons to determine the amount of water  user take. when the user inputed the information the app give an instruction to the user and also put a time count down to enter another input. acording to the app instruction user has to drink water in that time count down. when the count down expires app will send a notification to the user(every 2 min ).

    if the user didn't input enything for 10 min of time. anoter countdown automatically start(In this countdown user have ability to input a data that missed ). if user input an information during that time the system add that missed time to the next time counter.
    

### Output Section 

Every time user add an input the output section show the time and the date and amount user added and also save it to the database.

## Other Things 

This app has to be run on the device background 

## Importent Thing

when the user accidentaly close or intentionaly close the app : Before user exit the app always it must save the time user exit the app on the database. Therefor when user again start the app next time App will check the time gap user skipped or if it is a new day.