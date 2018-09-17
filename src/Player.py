import urllib.request
import json
import sys
from collections import Counter
import config.config as config
import data.gameModeData as gameModeFile
import data.championData as championFile
auth = '?api_key=' + config.API_KEY

class Player:

    def __init__(self, name):
        self.name = name
        tempName = urllib.parse.quote(name) # Replace spaces for HTTP Request
        try:
            http = urllib.request.urlopen(config.SUMMONER_URL + tempName + auth)
            httpData = http.read().decode("utf-8")
            jsonData = json.loads(httpData)
        except urllib.error.HTTPError:
            print("Error: " + name + " is not a valid summoner!")
            sys.exit(1)
        except Exception as e:
            print("Error: " + str(e))
            sys.exit(1)
        self.summonerId = jsonData['id']
        self.accountId = jsonData['accountId']
        self.id = jsonData['id']
        self.summonerLevel = jsonData['summonerLevel']
    #end def __init__

    # Current Match Functions
    #---------------------------------------------------------------------------------------------------------------
    def getCurrentMatchData(self):
        try:
            http = urllib.request.urlopen(config.CURRENT_MATCH_URL + str(self.summonerId) + auth)
            httpData = http.read().decode("utf-8")
            jsonData = json.loads(httpData)
        except urllib.error.HTTPError:
            print("Error: " + self.name + " is not currently in a match!")
            sys.exit(1)
        return jsonData
    #end def getCurrentMatchData

    def getTeamsFromCurrentMatch(self, currentMatchData):
        team1List = []
        team2List = []
        allTeamsList = {}
        i = 1
        for summoner in currentMatchData["participants"]:
            tempName = summoner["summonerName"]
            tempName = urllib.parse.quote(tempName) # Deals with special characters

            try:
                print("Fetching summoner " + str(i))
                http = urllib.request.urlopen(config.SUMMONER_URL + tempName + auth)
                httpData = http.read().decode("utf-8")
                jsonData = json.loads(httpData)
            except Exception as e:
                print("Error occured for summoner "  + str(i) + ": " + str(e))
            summonerLevel = jsonData['summonerLevel']

            if summoner["teamId"] == 100:
                team1List.append({'summonerName': summoner["summonerName"], 'champion': summoner["championId"], 'summonerLevel': summonerLevel})
            elif summoner["teamId"] == 200:
                team2List.append({'summonerName': summoner["summonerName"], 'champion': summoner["championId"], 'summonerLevel': summonerLevel})
            i += 1

        allTeamsList["Team1"] = team1List
        allTeamsList["Team2"] = team2List
        return allTeamsList
    # Previous Match Functions

    def printTeamsData(self, teamsData):
        for team in teamsData:
            print("")
            print(team + ": ")
            print("")
            for player in teamsData[team]:
                champion = self.convertIdToChampion(player['champion'])
                print("Summoner Name: " + player['summonerName'] + ", Level: " + str(player['summonerLevel']) + ", Champion: " + champion["name"])
    #end def printTeamsData

    #---------------------------------------------------------------------------------------------------------------
    def getPreviousMatchesData(self):
        try:
            http = urllib.request.urlopen(config.PREVIOUS_MATCH_URL + str(self.accountId) + auth +'&beginIndex=0&endIndex=20') # Get total games (find better way of getting this data?)
            httpData = http.read().decode("utf-8")
            jsonData = json.loads(httpData)
        except Exception as e:
            print("Error: " + str(e))
            sys.exit(1)
        return jsonData["matches"]
    #end def getPreviousMatchIds

    # Champion Functions
    #---------------------------------------------------------------------------------------------------------------
    def convertIdToChampion(self, championId):
        championDict = championFile.championData
        return championDict[str(championId)]['name']
    #end def convertIdToChampion
    #---------------------------------------------------------------------------------------------------------------

    # Game Mode Functions
    #---------------------------------------------------------------------------------------------------------------
    def convertIdToGameMode(self, gameModeId):
        gameModeDict = gameModeFile.gameModeData
        return gameModeDict[gameModeId]
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
                try:
                    http = urllib.request.urlopen(config.MATCH_URL + str(match) + auth)
                    httpData = http.read().decode("utf-8")
                    jsonData = json.loads(httpData)
                except Exception as e:
                    print("Error: " + str(e))
                    sys.exit(1)
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