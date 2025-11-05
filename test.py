from datetime import datetime


def securedInputDate(message="Please enter a date : ", separator=None):
    validity = False

    if (separator != None):
        separators = separator
    else:
        separators= ["/","-",":"," "]

    while (validity == False):
        validity = True
        string = input(message)
        for sep in separators:
            test_date = string.split(sep)
            if (len(test_date) != 3):
                continue
            else:
                try:
                    for i in range (3):
                        test_date[i] = int(test_date[i])
                    if(test_date[0]<1 or test_date[0]>31):
                        print("The day is invalide")
                        validity = False               
                    if(test_date[1]<1 or test_date[1]>12):
                        print("The month is invalide")
                        validity = False
                except:
                    validity = False   
        if (len(test_date) != 3):
            validity = False


    return test_date

print(securedInputDate())