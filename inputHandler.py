import datetime

def isSQLInjection(userInput: str) -> bool:
    # Check if the user input contains SQL injections
    if (userInput.find(";") != -1):
        return True
    if (userInput.find("--") != -1):
        return True
    if (userInput.find("\"") != -1):
        return True
    if (userInput.find("\'") != -1):
        return True
    if (userInput.find("/*") != -1):
        return True
    return False

def inputSQLData(message: str) -> str:
    """
    Get input from the user and check if it contains SQL injections
    """
    userInput: str = input(message)
    if isSQLInjection(userInput):
        print("Possible SQL Injection detected")
        print("Please do not do this again :)")
        return ""
    else:
        return userInput

def convertSpecialCharacters(userInput: str) -> str:
    userInput = userInput.replace("ø", "oe")
    userInput = userInput.replace("Ø", "OE")
    userInput = userInput.replace("æ", "ae")
    userInput = userInput.replace("Æ", "AE")
    userInput = userInput.replace("å", "aa")
    userInput = userInput.replace("Å", "AA")
    return userInput

def previewWithSpecialCharacters(userInput: str) -> str:
    userInput = userInput.replace("oe", "ø")
    userInput = userInput.replace("OE", "Ø")
    userInput = userInput.replace("ae", "æ")
    userInput = userInput.replace("AE", "Æ")
    userInput = userInput.replace("aa", "å")
    userInput = userInput.replace("AA", "Å")
    return userInput

def convertStationName(stationName: str) -> str:
    """
    Convert the station name to a format that can be used in SQL
    """
    stations: list = stationName.split(" ")
    convertedStationName: str = ' '.join([convertSpecialCharacters(station[0].upper() + station[1:].lower()) for station in stations])
    return convertedStationName

def isEnglishWeekday(weekday: str) -> bool:
    # Check if the weekday is in english
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return weekday in weekdays

def translateWeekdayToEnglish(weekday: str) -> str:
    # Translate the weekday to english
    weekdays = {
        "Mandag": "Monday",
        "Tirsdag": "Tuesday",
        "Onsdag": "Wednesday",
        "Torsdag": "Thursday",
        "Fredag": "Friday",
        "Lørdag": "Saturday",
        "Søndag": "Sunday"
    }
    return weekdays[weekday]

def translateWeekdayToNorwegian(weekday: str) -> str:
    # Translate the weekday to norwegian
    weekdays = {
        "Monday": "Mandag",
        "Tuesday": "Tirsdag",
        "Wednesday": "Onsdag",
        "Thursday": "Torsdag",
        "Friday": "Fredag",
        "Saturday": "Lørdag",
        "Sunday": "Søndag"
    }
    return weekdays[weekday]

def convertDate(date: str) -> str:
    """
    Convert the date from DD.MM.YYYY to YYYY-MM-DD
    """
    day, month, year = date.split(".")
    return year + "-" + month + "-" + day

def convertDateToWeekday(date: str) -> str:
    """
    Convert the date to a weekday
    DD.MM.YYYY -> weekday
    """
    day, month, year = date.split(".")
    datetime_object = datetime.datetime(int(year), int(month), int(day))
    weekday = datetime_object.strftime("%A")
    return translateWeekdayToNorwegian(weekday)

def previewDate(date: str) -> str:
    """
    Convert the date from YYYY-MM-DD to DD.MM.YYYY
    """
    year, month, day = date.split("-")
    return day[:2] + "." + month[:2] + "." + year[:4]

def nextDate(date: str):
    """
    Get date after the given date
    Input format: DD.MM.YYYY
    return: DD.MM.YYYY
    """ 
    day, month, year = date.split(".")
    datetime_object = datetime.datetime(int(year), int(month), int(day))
    datetime_next_day = datetime_object + datetime.timedelta(days=1)
    next_day = datetime_next_day.strftime("%d.%m.%Y")
    return next_day
