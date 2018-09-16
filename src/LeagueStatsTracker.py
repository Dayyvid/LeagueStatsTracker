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
    userInput = input("Enter 1 to get match data: ")
    if(userInput == "1"):
        previousMatchesData = player.getPreviousMatchesData()
        #appendToList(previousMatchesData, player.laneList, "lane")
        userInput = input("Enter 1 to see players recently played with for the past 20 games:\nEnter 2 to see champions played for past 20 games:\nEnter 3 to see game modes played for past 20 games: ")
        if userInput == "1":
            previousMatchesDataList = player.createList(previousMatchesData, "gameId")
            previousPlayersList = player.createList(previousMatchesDataList, "previousPlayers")
            previousPlayersList = player.formatList(previousPlayersList)
            previousPlayersList = [[x[0], x[1]] for x in previousPlayersList if x[0] != player.name and x[1] > 1]
            player.printSortedList(previousPlayersList)

        elif userInput == "2":
            previousChampionsList = player.createList(previousMatchesData, "champion")
            previousChampionsList = player.convertIdToChampion(previousChampionsList)
            previousChampionsList = player.formatList(previousChampionsList)
            player.printSortedList(previousChampionsList)

        elif userInput == "3":
            previousGameModesList = player.createList(previousMatchesData, "queue")
            previousGameModesList = player.convertIdToGameMode(previousGameModesList)
            previousGameModesList = player.formatList(previousGameModesList)
            player.printSortedList(previousGameModesList)

if __name__ == "__main__":
    main()