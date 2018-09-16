import urllib.request
import json
from collections import Counter
import config.config as config
import data.gameModeData as gameModeFile
import data.championData as championFile
auth = '?api_key=' + config.API_KEY

class Player:

    def __init__(self, name):
        self.name = name
        http = urllib.request.urlopen(config.SUMMONER_URL + self.name + auth)
        httpData = http.read().decode("utf-8")
        jsonData = json.loads(httpData)

        self.accountId = jsonData['accountId']
        self.id = jsonData['id']
        self.summonerLevel = jsonData['summonerLevel']
    #end def __init__

    # Previous Match Functions
    #---------------------------------------------------------------------------------------------------------------
    def getPreviousMatchesData(self):
        http = urllib.request.urlopen(config.PREVIOUS_MATCH_URL + str(self.accountId) + auth +'&beginIndex=0&endIndex=20') # Get total games (find better way of getting this data?)
        httpData = http.read().decode("utf-8")
        jsonData = json.loads(httpData)
        return jsonData["matches"]
    #end def getPreviousMatchIds

    # Champion Functions
    #---------------------------------------------------------------------------------------------------------------
    def convertIdToChampion(self, previousChampionsList):
        toReturn = []
        championDict = championFile.championData
        for i in range(0,len(previousChampionsList)):
            currentChampionId = previousChampionsList[i]
            toReturn.append(championDict[currentChampionId]['name'])
        return toReturn
    #end def convertIdToChampion
    #---------------------------------------------------------------------------------------------------------------

    # Game Mode Functions
    #---------------------------------------------------------------------------------------------------------------
    def convertIdToGameMode(self, previousGameModesList):
        toReturn = []
        gameModeDict = gameModeFile.gameModeData
        for i in range(0, len(previousGameModesList)):
            currentGameMode = previousGameModesList[i]
            toReturn.append(gameModeDict[currentGameMode])
        return toReturn
    #end def convertIdToGameMode
    #---------------------------------------------------------------------------------------------------------------

    # List functions
    #---------------------------------------------------------------------------------------------------------------
    def formatList(self, templateList):
        temp = [[x, templateList.count(x)] for x in set(templateList)] # Set list to contain count of each item
        temp.sort(key = lambda x: x[1], reverse = True) # Orders list by number of occurences descending
        return temp
    #end def formatList

    def createList(self, data, identifier):
        toReturn = []
        if identifier != 'previousPlayers':
            for match in data:
                toReturn.append(str(match[identifier]))
        else:
            i = 1
            for match in data:
                http = urllib.request.urlopen(config.MATCH_URL + str(match) + auth)
                httpData = http.read().decode("utf-8")
                jsonData = json.loads(httpData)
                print("Fetching game: " + str(i))
                i += 1
                matchPlayersInfo = jsonData["participantIdentities"]
                for summoner in matchPlayersInfo:
                    toReturn.append(summoner['player']['summonerName'])    
        return toReturn
    #end def createList

    def printSortedList(self, templateList):
        print(" ")
        for x in templateList:
            print(x[0], ":", x[1])
    #end def printPreviousPlayers