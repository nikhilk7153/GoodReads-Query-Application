from simple_term_menu import TerminalMenu
import requests
import json

'''
This class will allow the user to enter their preferences and from here, the user will be given the choice 
'''

def main():
    '''
    This serves as the starting point of the function where all the submenus will be asked to be entered
    '''

    actions = ["GET", "PUT", "POST", "DELETE"]
    choice = showMenu(actions)
    object = setObjectPreference()

    if choice == "GET":
        return getProcess(object)
    elif choice == "PUT":
        return putProcess(object)
    elif choice == "DELETE":
        return deleteProcess(object)
    else:
        return postProcess(object)

def showMenu(options):
    '''
    :param options: are the list of options that are specified to the user
    :return: the choice of the user that is selected
    '''
    menu = TerminalMenu(options)
    index = menu.show()
    choice = options[index]
    return choice

def setObjectPreference():
    '''
    Returns the choice of the user on which database they want to use
    '''
    return showMenu(["book", "author"])

def getProcess(object):
    '''
    :param object: specifies the object that will be
    Returns the result of the process following the searching of the query
    '''
    searchChoice = showMenu(["search by any field", "search by id"])

    if searchChoice == "search by any field":
        expression = input("Please enter an expression for the query: ")
        result = requests.get("http://localhost:5000/search?q=" + expression)
        print(result.json())
        return requests.status_codes
    else:
        id_value = input("Please enter the id value for the " + object + " : ")
        result = requests.get("http://localhost:5000/" + object + "?id=" + str(id_value))
        print(result.json())
        return requests.status_codes

def putProcess(object):
    '''
    :param object: specifies the object which will specify the database being used
    Returns the outcome of the process upon updating
    '''

    id_value = input("Please enter the id value for the " + object + " : ")
    data = input("Please enter a json object to insert into the " + object + " database: ")
    result = requests.put("http://localhost:5000/" + object + "?id=" + str(id_value), json = json.dumps(data))
    return requests.status_codes


def deleteProcess(object):
    '''
    :param object: specifies the object which will specify the database being used
    Returns the outcome of the process upon deletion
    '''

    id_value = input("Please enter the id value for the " + object + " : ")
    result = requests.delete("http://localhost:5000/" + object + "?id=" + str(id_value))
    return requests.status_codes


def postProcess(object):
    '''
    :param object: specifies the object which will specify the database being used
    Returns the outcome of the process upon insertion
    '''
    total = 0
    while (True):
        total = input("Please enter the total number of " + object + " items that you would like scraped: ")
        if (int(total) > 0):
            break
    choice = showMenu(["Scrape", "Manual insertion"])

    if choice == "Scrape":

        link = input("Please enter a link that you would like to begin the process: ")
        r = requests.post("http://localhost:5000/scrape?object=" + object + "&total=" + str(total) + "&link=" + link)
        return requests.status_codes

    else:
        data = input("Please enter a json object to insert into the " + object + " database: ")
        if int(total) == 1:
            requests.post("http://localhost:5000/"+ object, json = data)
            return requests.status_codes
        else:
            requests.post("http://localhost:5000/" + object + "s", json = data)
        return requests.status_codes

if __name__ == "__main__":
    main()