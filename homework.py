# IMPORTS
import random
import datetime

# GLOBAL VARIABLES

template = ['stationid', 'city', 'temp', 'rain', 'wind', 'direction', 'date']
# domains
cities = ['Botosani', 'Iasi', 'Cluj', 'Timisoara', 'Bucuresti', 'Constanta', 'Brasov', 'Suceava', 'Craiova', 'Oradea']
directionList = ['N', 'S', 'E', 'V', 'NE', 'NV', 'SE', 'SV']
operators = {'stationid': ['=', '!='], 'city': ['=', '!='], 'temp': ['=', '>', '<'], 'rain': ['=', '>', '<'],
             'wind': ['=', '>', '<'], 'direction': ['=', '!='], 'date': ['=', '!=']}

# Limits
tempLimit = [-30, 30]
rainLimit = [0, 100]  # Rain percentage
windLimit = [0, 30]
daysLimit = [0, 10]
stationIdLimit = [0, 100]

# Data to configure
numberOfPublications = 10
numberOfSubscriptions = 10
percentage = [0, 100, 0, 80, 90, 10, 0]  # percentage for each field from template
percentageForEqualForCity = 50  # minimum percentage for equal for the field city


def getRandomCity():
    return random.choice(cities)


def getRandomStationId():
    return random.randrange(stationIdLimit[0], stationIdLimit[1])


def getRandomTemp():
    return random.randrange(tempLimit[0], tempLimit[1], 5)


def getRandomRain():
    return float(random.randrange(rainLimit[0], rainLimit[1], 10) / 100)


def getRandomWind():
    return random.randrange(windLimit[0], windLimit[1], 2)


def getRandomDirection():
    return random.choice(directionList)


def getRandomDate():
    return (datetime.datetime.now() + datetime.timedelta(random.randint(daysLimit[0], daysLimit[1]))).strftime(
        '%d.%m.%Y')


# Returns a list with the number of repetitions each field should have based on it's percentage
# It does NOT include the fields with 0 frequency
def getRatio():
    numberOfRepetitionsList = {}
    for i in range(len(percentage)):
        if percentage[i] != 0:
            numberOfRepetitionsList[template[i]] = round(percentage[i] / 100 * numberOfSubscriptions)
    return numberOfRepetitionsList


# Generates the publications with random values for the fields
def generatePublications():
    publications = []
    for index in range(numberOfPublications):
        pub = {template[0]: index + 1, template[1]: getRandomCity(), template[2]: getRandomTemp(),
               template[3]: getRandomRain(), template[4]: getRandomWind(), template[5]: getRandomDirection(),
               template[6]: getRandomDate()}
        publications.append(pub)
    return publications


# Decreases with one the number of repetition for a field,
# if the number is 0, the field is removed from the list
def recalculateRatio(ratioList, field):
    ratioList[field] = ratioList[field] - 1
    if ratioList[field] == 0:
        del ratioList[field]


# Adds random values ( for the operator and field value ) for a given field,
# then adds the them to the subscription given as parameter
def addSub(subscriptionList, field):
    fieldSubList = [field]
    if field == 'stationid':
        fieldSubList.append(random.choice(operators[field]))
        fieldSubList.append(getRandomStationId())
    elif field == 'city':
        fieldSubList.append(random.choice(operators[field]))
        fieldSubList.append(getRandomCity())
    elif field == 'temp':
        fieldSubList.append(random.choice(operators[field]))
        fieldSubList.append(getRandomTemp())
    elif field == 'rain':
        fieldSubList.append(random.choice(operators[field]))
        fieldSubList.append(getRandomRain())
    elif field == 'wind':
        fieldSubList.append(random.choice(operators[field]))
        fieldSubList.append(getRandomWind())
    elif field == 'direction':
        fieldSubList.append(random.choice(operators[field]))
        fieldSubList.append(getRandomDirection())
    else:
        # date
        fieldSubList.append(random.choice(operators[field]))
        fieldSubList.append(getRandomDate())

    subscriptionList.append(fieldSubList)


# Generates the subscriptions respecting the percentage for each field
def generateSubscriptions():
    subscriptionList = [[] for i in range(numberOfSubscriptions)]
    subscriptionsWithCity = []
    repetitionListForFields = getRatio()

    # while there are field to add
    while len(repetitionListForFields) != 0:
        for index in range(numberOfSubscriptions):
            # get the list of available fields for the current subscription

            # get all the possible fields
            listOfAvailableFields = list(repetitionListForFields.keys())
            # remove the fields that are already in the subscription
            for i in range(len(subscriptionList[index])):
                if subscriptionList[index][i][0] in listOfAvailableFields:
                    listOfAvailableFields.remove(subscriptionList[index][i][0])

            # if there are no more available fields move to the next subscription
            if len(listOfAvailableFields) == 0:
                continue

            # pick a random value from the list of available fields
            fieldToAdd = random.choice(listOfAvailableFields)
            # adds the field to the subscription
            addSub(subscriptionList[index], fieldToAdd)
            # decrease the number of repetitions for the field that was added
            recalculateRatio(repetitionListForFields, fieldToAdd)

            # make a list with all the indexes of the subscriptions containing city
            if fieldToAdd == template[1]:
                subscriptionsWithCity.append(index)

            # break if there are no more fields to add
            if len(repetitionListForFields) == 0:
                break

    # chose random subscription with city field to place the equal operator
    random.shuffle(subscriptionsWithCity)
    numberOfEqualRepetitionForCity = round(percentageForEqualForCity / 100 * len(subscriptionsWithCity))
    for counter in range(numberOfEqualRepetitionForCity):
        for subListSub in list(subscriptionList[subscriptionsWithCity[counter]]):
            if subListSub[0] == template[1]:
                subListSub[1] = '='

    #  sort the fields to respect the template order and put the result in the new list
    sortedSubscriptionsList = []
    for subscription in subscriptionList:
        subscription.sort(key=sortFunction)
        sortedSubscriptionsList.append(subscription)

    return sortedSubscriptionsList


# Function used as key to sort the fields in the subscriptions to respect the template order
def sortFunction(entry):
    return template.index(entry[0])


def writeInFile(publicationList, subscribeList):
    f = open('output.txt', "w")
    f.write("Publication list: ")
    f.write('\n')
    for elem in publicationList:
        f.write(str(elem))
        f.write('\n')
    f.write('\n')
    f.write('\n')
    f.write('Subscribe list: ')
    f.write('\n')
    for elem in subscribeList:
        f.write(str(elem))
        f.write('\n')
    f.close()


# Generates publications and subscriptions and writes in file
def main():
    publicationList = generatePublications()
    subscriptionList = generateSubscriptions()
    writeInFile(publicationList, subscriptionList)


if __name__ == "__main__":
    main()
