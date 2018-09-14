# -*- coding: utf-8 -*-
import urllib.request
import json
from collections import Counter
import config.config as config
import data.gameModeData as gameModeData
auth = '?api_key=' + config.API_KEY

def getSummonerData():
    summoner = input("Enter the summoner name: ")
    http = urllib.request.urlopen(config.SUMMONER_URL + summoner + auth)
    httpData = http.read().decode("utf-8")
    jsonData = json.loads(httpData)
    return jsonData
#end def getSummonerData

def getPreviousMatchesData(accountId):
    http = urllib.request.urlopen(config.PREVIOUS_MATCH_URL + str(accountId) + auth +'&beginIndex=0&endIndex=20') # Get total games (find better way of getting this data?)
    httpData = http.read().decode("utf-8")
    jsonData = json.loads(httpData)
    return jsonData["matches"]
#end def getPreviousMatchIds

def appendPreviousPlayers(playersHolderDict, matchId):
    http = urllib.request.urlopen(config.MATCH_URL + str(matchId) + auth)
    httpData = http.read().decode("utf-8")
    jsonData = json.loads(httpData)
    matchPlayersInfo = jsonData["participantIdentities"]
    for summoner in matchPlayersInfo:
    	if summoner['player']['summonerName'] not in playersHolderDict:
    		playersHolderDict[summoner['player']['summonerName']] = 1
    	else:
    		playersHolderDict[summoner['player']['summonerName']] += 1
#end def getMatchHistory

def formatList(unsortedList):
    unsortedList = [[x, unsortedList.count(x)] for x in set(unsortedList)] # Set list to contain count of each item\
    unsortedList.sort(key = lambda x: x[1], reverse = True) # Orders list by number of occurences descending
    return unsortedList
#end def reverseList

def printPreviousPlayers(previousPlayersList):
	for player in previousPlayersList:
		print(player[0], ":", player[1])
#end def printPreviousPlayers
def getPreviousPlayers(matchesIdList, summonerName):
    tempDict = {}
    i = 1
    for game in matchesIdList:
        appendPreviousPlayers(tempDict, game)
        print("Fetching game number: " + str(i))
        i += 1
    previousPlayersList = sorted(tempDict.items(), key=lambda x: x[1], reverse=True)
    previousPlayersList = [x for x in previousPlayersList if x[1] > 1 and x[0] != summonerName]
    return previousPlayersList
#end def getPreviousPlayers

def appendToList(previousMatchesData, templateList, identifier):
    for match in previousMatchesData:
        templateList.append(str(match[identifier]))
    templateList = formatList(templateList)

def main():
    summonerData = getSummonerData()
    print(summonerData)
    userInput = input("Enter 1 to get previous matches: ")
    if(userInput == "1"):
        previousMatchesData = getPreviousMatchesData(summonerData["accountId"])
        championsList = []
        gameModeList = []
        matchesIdList = []
        laneList = []
        previousPlayersDict = {}
        # Insert data from previous match to respective lists
        appendToList(previousMatchesData, championsList, "champion")
        appendToList(previousMatchesData, gameModeList, "queue")
        appendToList(previousMatchesData, laneList, "lane")
        appendToList(previousMatchesData, matchesIdList, "gameId")

        userInput = input("Enter 1 to see players recently played with for the past 20 games: ")
        if(userInput == "1"):
        	previousPlayers = getPreviousPlayers(matchesIdList, summonerData["name"])
        	printPreviousPlayers(previousPlayers)
if __name__ == "__main__":
    main()