import json
def convertToList(title='',divider='',options=[],extraDict={}):
    _list = []
    _tempDict = {}
    _tempDict['title'] = title
    _tempDict['divider'] = divider
    for option in options:
        _list.append(option)
    _tempDict['options'] = _list
    for x in extraDict.keys():
        _tempDict[x] = extraDict[x]
    return _tempDict

def outputJson(dict):
    with open('Resources/menu.json','w+') as file:
        try:
            json.dump(dict,file,indent=4)
            print('Output success!')
        except:
            print('JSON DUMP ERROR!')

def generateJson():
    dict = {}
    # main menu
    options = []
    title = 'Holiday Menu'
    divider = '=' * len(title)
    options.append('1. Add a Holiday')
    options.append('2. Remove a Holiday')
    options.append('3. Save Holiday List')
    options.append('4. View Holidays')
    options.append('5. Exit')
    dict['main-menu'] = convertToList(title,divider,options)

    # add holiday
    options = []
    attrDict = {}
    title = 'Add a Holiday'
    divider = '=' * len(title)
    attrDict['error'] = '\nError:\nInvalid date. Please try again. (format: yyyy-mm-dd)'
    attrDict['success'] = '\nSuccess:\n{holiday} has been added to the holiday list.'
    dict['addHoliday'] = convertToList(title,divider,options,attrDict)

    #remove holiday
    options = []
    attrDict = {}
    title = 'Remove a Holiday'
    divider = '=' * len(title)
    attrDict['error']= '\nSuccess:\n{holiday} not found.'
    attrDict['success'] = '\nSuccess:\n{holiday} has been removed from the holiday list.'
    dict['removeHoliday'] = convertToList(title,divider,options,attrDict)


    #save holiday
    options = []
    attrDict = {}
    title = 'Save Holiday List'
    divider = '=' * len(title)
    options.append('Are you sure you want to save your changes? [y/n]: ')
    attrDict['canceled'] = '\nCanceled:\nHoliday list file save canceled.'
    attrDict['success'] = '\nSuccess:\nYour changes have been saved.'
    dict['saveHoliday'] = convertToList(title,divider,options,attrDict)

    #view holiday
    options = []
    attrDict = {}
    title = 'View Holidays'
    divider = '=' * len(title)
    options.append('Leave blank for current year or week.')
    attrDict['view'] = '\nThese are the holidays for {year} week # {week}:'
    attrDict['error-year'] = '\nError:\nEnter a year between 2020-2024.'
    attrDict['error-week'] = '\nError:\nEnter a week number between 1-52.'
    attrDict['weather'] = 'Would you like to see this week\'s weather? [y/n]:'
    dict['viewHoliday'] = convertToList(title,divider,options,attrDict)

    #exit
    options = []
    attrDict = {}
    title = 'Exit'
    divider = '=' * len(title)
    options.append('Are you sure you want to exit? [y/n]')
    attrDict['no-save'] = 'Your changes will be lost.'
    attrDict['yes'] = 'Goodbye!'
    dict['exit'] = convertToList(title,divider,options,attrDict)
    outputJson(dict)



