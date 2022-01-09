import datetime
import json
from os import error
from typing import Dict
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass,field
import datetime
from time import sleep
fileLocation = 'Resources/'
# -------------------------------------------
# Modify the holiday class to 
# can it be passed as date?
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
class Holiday:
    def __init__(self, name, date):
        self.name = name
        #self.daysofweek = daysofweek
        #self.weeknumber = weeknumber
        if type(date) == datetime.date:
            self.date = date
        else: 
            print('unable to add holiday, date data type must be datetime.date!')
        return
    
    def __str__ (self):
        return f'{self.name} ({self.date})'
        # **
        # String output
        # Holiday output when printed.

# ----------------------
# Function Declaration
# ----------------------
# convert string into datetime.date
def strToDate(string,year='',month='',day=''):
    # String must in the format of yyyy-mm-dd
    if not not year and not not month and not not day: #if not empty
        string = f'{year}-{month}-{day}'
    try:
        date = datetime.datetime.strptime(string,'%Y-%m-%d').date()
        return date
    except:
        return -1

# stack overflow
def get_start_and_end_date_from_calendar_week(year, calendar_week):       
    monday = datetime.datetime.strptime(f'{year}-{calendar_week}-1', "%Y-%W-%w").date()
    return monday, monday + datetime.timedelta(days=6.9)

# returns the week number given a date (datetime.date)
def dateToWeeknum_(date):
    if type(date) != datetime.date:
        date = strToDate(date)
    # # // prevent cases where 12-31 becomes week #1 of next year
    # if date.isocalendar()[1] == 1 and date.month == 12:
    #     return 52
    # # // prevent cases where 1-1 becomes week #52 of previous year
    # elif date.isocalendar()[1] == 52 and date.month == 1:
    #     return 1
    else:
        return date.isocalendar()[1]

# Checks for str integrity
def textValidate(text):
    text = text.lower()
    if text == 'y' or text == 'yes':
        return True
    elif  text == 'no' or text == 'n':
        return False
    else: 
        return -1

# handles all menu display logistics
@dataclass
class menu:
    obj: Holiday
    code: str='main-menu'

    def importMenu(self):
        try:
            with open('Resources/menu.json','r') as file:
                self.dict = json.load(file)
        except:
            print('Error loading the file.')
            return

    def displayMenu(self):
        self.displayHeader()

        if self.code == 'main-menu':
            self.mainMenu()
        elif self.code == 'addHoliday':
            self.addHoliday()
        elif self.code == 'removeHoliday':
            self.removeHoliday()
        elif self.code == 'saveHoliday':
            self.saveHoliday()
        elif self.code == 'viewHoliday':
            self.viewHoliday()
        elif self.code == 'exit':
            self.exit()
        return

    def displayHeader(self):
        print('')
        print(self.dict[self.code]['title'])
        print(self.dict[self.code]['divider'])
        for option in self.dict[self.code]['options']:
            print(option)
        return
    
    def mainMenu(self):
        _menu = {'1':'addHoliday','2':'removeHoliday','3':'saveHoliday','4':'viewHoliday','5':'exit'}
        _input = input()
        if _input in _menu.keys():
            self.code = _menu[_input]
        else:
            print('Please enter the correct selection.')
        self.displayMenu()
        return
    
    def addHoliday(self):
        _input_holiday = input('Holiday: ')
        _input_date = strToDate(input('Date (yyyy-mm-dd): '))
        while _input_date == -1: #error
            print(self.dict[self.code]["error"])
            _input_holiday = input('Holiday: ')
            _input_date = strToDate(input('Date (yyyy-mm-dd): '))
        else:
            self.obj.addHoliday(Holiday(_input_holiday,_input_date))
            print(self.dict[self.code]["success"].format(holiday=_input_holiday))
            # Return to main menu
            self.returnMain()
        return

    def removeHoliday(self):
        _input_holiday = input('Holiday: ').capitalize()
        if self.obj.removeHoliday(_input_holiday):
            print(self.dict[self.code]["success"].format(holiday=_input_holiday))
        else:
            print(self.dict[self.code]["error"].format(holiday=_input_holiday))
        # Return to main menu
        self.returnMain()
        return

    def saveHoliday(self):
        _input = textValidate(input(''))
        while _input == -1: # wrong input type
            print("Please enter 'y' or 'no'.")
            _input = textValidate(input(''))
        else:
            if _input: #true
                self.obj.save_to_json(fileLocation + 'holidays.json') # save file
                print(self.dict[self.code]["success"])
            elif not _input: #false
                print(self.dict[self.code]["canceled"])
            # Return to main menu
            self.returnMain()
        return

    def viewHoliday(self):
        currentYear = datetime.date.today().year
        currentWeek = datetime.date.today().isocalendar()[1]
        _input_year = input(f'Year: ')
        _input_week = input(f'Week #[1-52]: ')
        if not _input_year: _input_year = currentYear # if empty, set default value
        if not _input_week: _input_week = currentWeek # if empty, set default value
        # input integrity check
        try:
            _input_year = int(_input_year)
            _input_week = int(_input_week)
        except:
            print('Please enter a number.')
            # Return to main menu
            self.returnMain()
            return

        # prompt weather for current week
        if _input_year == currentYear and _input_week == currentWeek:
            _input_weather = textValidate(input(self.dict[self.code]['weather'])) # prompt weather
            while _input_weather == -1: #input type error
                print("Please enter 'y' or 'no'.")
                _input_weather = textValidate(input(self.dict[self.code]['weather']))
            else:
                if _input_weather: #true
                    print(self.dict[self.code]['view'].format(year= _input_year, week= _input_week))
                    self.obj.displayHolidaysInWeek(self.obj.filter_holidays_by_week(_input_year,_input_week),self.obj.getWeather())
                    # Return to main menu
                    self.returnMain()
                    return
        
        # regular view
        print(self.dict[self.code]['view'].format(year= _input_year, week= _input_week))
        self.obj.displayHolidaysInWeek(self.obj.filter_holidays_by_week(_input_year,_input_week))
        # Return to main menu
        self.returnMain()
        return

    def exit(self):
        if not self.obj.saveChanges: print(self.dict[self.code]['no-save']) # print msg if changes are not saved

        _input_exit = textValidate(input())
        while _input_exit == -1: # type error
            print("Please enter 'y' or 'n'.")
            _input_exit = textValidate(input())
        else:
            if _input_exit:
                self.obj.exitReport()
                print(f"\n{self.dict[self.code]['yes']}")
            elif not _input_exit:
                # Return to main menu
                self.returnMain()
        return
    
    def returnMain(self):
        input('\nPress any key to return to the main menu.')
        self.code = 'main-menu'
        self.displayMenu()

# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------

class HolidayList:
    def __init__(self):
       self.innerHolidays = []
       self.saveChanges = True #use to identify if changes were saved in 'exit'
       # for initialization & exit report
       self.removeCount = 0
       self.duplicateCount = 0
       self.addCount = 0
       self.readCount = 0 # sub of add
       self.scrapeCount = 0 # sub of add
       return
   
    def addHoliday(self,holidayObj):
        if type(holidayObj) == Holiday:
            #duplicate check
            if self.findHoliday(holidayObj.name,holidayObj.date) != None:
                print('This holiday already exists.')
                return
            else:
                self.addCount += 1
                self.innerHolidays.append(holidayObj)
                self.saveChanges = False
                print(f'added holiday: {holidayObj.name}')  
        else:
            print(f'error adding holiday: wrong data type.')  
        return

        # ***
        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday

    def findHoliday(self, HolidayName, Date):
        # should only be 1 entity or None
        for holiday in list(filter(lambda x: x.name == HolidayName and x.date == Date ,self.innerHolidays)):
            return holiday
        # **
        # Find Holiday in innerHolidays
        # Return Holiday

    def removeHoliday(self, HolidayName):
        originalLen = len(self.innerHolidays)
        self.innerHolidays = list(filter(lambda x: x.name.lower() != HolidayName.lower(), self.innerHolidays))
        if originalLen > len(self.innerHolidays): #found match
            self.saveChanges = False
            print(f'Removed holiday: {HolidayName}, occurence: {originalLen-len(self.innerHolidays)}')
            self.removeCount += originalLen-len(self.innerHolidays)
            return True
        else: 
            print('Unable to find holiday') 
            return False
        
        # ***
        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday

    def read_json(self,filelocation):
        try: 
            with open(filelocation, 'r') as file:
                _json = json.load(file)
        except:
            print('Error loading file.')
        try:
            for holiday in _json:
                self.readCount += 1
                self.addHoliday(Holiday(holiday['name'],strToDate(holiday['date'])))
        except:
            print('Error loading data into obj')

        return

        # **
        # Read in things from json file location
        # Use addHoliday function to add holidays to inner list.

    def save_to_json(self,filelocation):
        temp_dict = {}
        temp_json = []
        for holiday in self.innerHolidays:
            temp_dict['name'] = holiday.name
            temp_dict['date'] = str(holiday.date)
            temp_json.append(temp_dict.copy())
        for x in temp_json:
            print(x)

        try: 
            with open(filelocation,'w+') as file:
                json.dump(temp_json,file,indent=4)
                self.saveChanges = True
                print(f'File successfully saved to holidays.json. ({len(temp_json)} records)')
        except TypeError as err:
            print(f'Error writing the file! {err}')
        # Write out json file to selected file.
        return

    def scrapeHolidays(self):
        for i in range(-2,3): # loop from 2020 to 2024
            _date = []
            _holidayDesc = []
            year = i + datetime.date.today().year
            soup = BeautifulSoup(requests.get(f'https://www.timeanddate.com/holidays/us/{year}').text,'html.parser')
            for x in soup.find('table',attrs={'id':'holidays-table'}).find('tbody'):
                try:
                    _temp_date = x.find('th',attrs={'class':'nw'}).get_text() + ' ' + str(year)
                    _date.append(datetime.datetime.strptime(_temp_date,'%b %d %Y').date()) #convert to datetime
                    _holidayDesc.append(x.find('a').get_text())
                    # _dayofweek = x.find('td',attrs={'class':'nw'}).get_text()
                    _holidayobj = Holiday(_holidayDesc[-1],_date[-1])
                    # duplicate check
                    if self.findHoliday(_holidayobj.name,_holidayobj.date) != None: #repeat found
                            self.duplicateCount += 1
                            print('repeat found!')
                            print(f'\tname:{_holidayobj.name}')
                            print(f'\tdate:{_holidayobj.date}')
                    else:
                        self.scrapeCount += 1
                        self.addHoliday(_holidayobj)

                except AttributeError as err:
                    print('ERR',err)
        return

        # *****  
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        # Check to see if name and date of holiday is in innerHolidays array
        # Add non-duplicates to innerHolidays
        # Handle any exceptions.     

    def numHolidays(self):
        return len(self.innerHolidays)
        # *    
        # Return the total number of holidays in innerHolidays

    def filter_holidays_by_week(self,year, week_number):
        return list(filter(lambda x: dateToWeeknum_(x.date) == week_number and x.date.year == year, self.innerHolidays))
        # ****
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays

    def displayHolidaysInWeek(self,holidayList,weather={}):
        for holiday in holidayList:
            if not weather: # if weather is empty
                print(f'\t{holiday}')
            else:
                try:
                    print(f'\t{holiday} - {weather[str(holiday.date)]}') # print weather
                except:
                    print('\tError while loading weather data.')
        
        # ***
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.

    def getWeather(self):
        year = datetime.date.today().year
        weekNum = datetime.date.today().isocalendar()[1]
        weather = {}
        _week = get_start_and_end_date_from_calendar_week(year,weekNum)
        url = "https://weatherapi-com.p.rapidapi.com/history.json"
        querystring = {"q":"Minneapolis","dt":_week[0],"lang":"en","end_dt":_week[1]}
        headers = {
                'x-rapidapi-host': "weatherapi-com.p.rapidapi.com",
                'x-rapidapi-key': "dfac59e93amsh62ca0d4f8fe24c3p183edcjsne376ede901f6"}
        try:
            response = requests.request("GET", url, headers=headers, params=querystring).json()
            for x in response['forecast']['forecastday']:
                weather[x['date']] = x['day']['condition']['text'] 
            return weather
        except:
            print('ERR retreiving weather data.')
            return None

        # ****
        # Convert weekNum to range between two days
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # Format weather information and return weather string.

    def viewCurrentWeek(self):
        holidays = self.filter_holidays_by_week(datetime.date.today().isocalendar()[0],datetime.date.today().isocalendar()[1])
        self.displayHolidaysInWeek(holidays)
        #prompt weather
        self.displayHolidaysInWeek(holidays,self.getWeather())
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results
        pass 

    def viewAllHolidays(self):
        for holiday in self.innerHolidays:
            print(holiday)
        return
    
    def initializationReport(self):
        print(f'\nAdded Holidays: {self.addCount}')
        print(f'\tScraped Records: {self.scrapeCount}')
        print(f'\tRead-in Records: {self.readCount}')
        print(f'\tDuplicate Records: {self.duplicateCount}')
        self.addCount = 0
    
    def exitReport(self):
        print('\nReport for this session')
        print('=======================')
        print(f'Added Holidays: {self.addCount}')
        print(f'Removed Holidays: {self.removeCount}')
        print(f'Save Status: {self.saveChanges}')

def main():
    holiday = HolidayList()
    holiday.read_json('Resources/holidays.json')
    holiday.scrapeHolidays()
    print('\nInitialization complete. Now loading initialization report...')
    sleep(1)
    holiday.initializationReport()
    print('\nLoading main menu in 3 seconds...')
    sleep(3)
    _menu = menu(holiday)
    _menu.importMenu()
    _menu.displayMenu()

    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    # 2. Load JSON file via HolidayList read_json function
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    # 3. Create while loop for user to keep adding or working with the Calender
    # 4. Display User Menu (Print the menu)
    # 5. Take user input for their action based on Menu and check the user input for errors
    # 6. Run appropriate method from the HolidayList object depending on what the user input is
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 

if __name__ == "__main__":
    main()


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.





