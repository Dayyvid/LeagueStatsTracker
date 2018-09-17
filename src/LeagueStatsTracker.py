# -*- coding: utf-8 -*-
import urllib.request
import json
from collections import Counter
import config.config as config
import data.gameModeData as gameModeFile
import data.championData as championFile
from Player import Player

def main():
    player = Player(input("Enter the summoner name: "))
    print("\n")
    userInput = input("Enter 1 to get previous match data:\nEnter 2 to get current match data: \n")
    print("\n")
    if userInput == "1":
        previousMatchesData = player.getPreviousMatchesData()
        #appendToList(previousMatchesData, player.laneList, "lane")
        userInput = input("Enter 1 to see players recently played with for the past 20 games:\nEnter 2 to see champions played for past 20 games:\nEnter 3 to see game modes played for past 20 games:\n")
        print("\n")
        if userInput == "1":
            previousMatchesDataList = player.createList(previousMatchesData, "gameId")
            previousPlayersList = player.createList(previousMatchesDataList, "previousPlayers")
            previousPlayersList = player.formatList(previousPlayersList)
            previousPlayersList = [[x[0], x[1]] for x in previousPlayersList if x[0] != player.name and x[1] > 1]
            print("\n----- Recently Played With -----")
            player.printSortedList(previousPlayersList)

        elif userInput == "2":
            previousChampionsList = player.createList(previousMatchesData, "champion")
            for i in range(0, len(previousChampionsList)):
                previousChampionsList[i] = player.convertIdToChampion(previousChampionsList[i])
            previousChampionsList = player.formatList(previousChampionsList)
            print("\n----- Champions in the past 20 games -----")
            player.printSortedList(previousChampionsList)

        elif userInput == "3":
            previousGameModesList = player.createList(previousMatchesData, "queue")
            for i in range(0, len(previousGameModesList)):
                previousGameModesList[i] = player.convertIdToGameMode(previousGameModesList[i])
            previousGameModesList = player.formatList(previousGameModesList)
            print("\n----- Gamemodes for the past 20 games -----")
            player.printSortedList(previousGameModesList)
    elif userInput == "2":
        currentMatchData = player.getCurrentMatchData()
        teamsList = player.getTeamsFromCurrentMatch(currentMatchData)
        player.printTeamsData(teamsList)
        # figure out who is premade
if __name__ == "__main__":
    main()