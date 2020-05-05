"""
Author:ChrstphrHll
A quiz game that scrapes wikipedia for questions/facts
#m = w.page(s.argv[1], auto_suggest = True)
tst_pg = w.page(s.argv[1], auto_suggest = True)
print(printLinks(tst_pg.links))
"""
import threading as th
import wikipedia as w
import keyboard as k
import random as r
import time as t
import sys as s

scores = {}

def getChars():
    f = open("characters.txt", "r")
    f.readline()
    chars = []
    while(True):
        current_line = f.readline()
        if current_line == "":
            break
        split_string = current_line.partition(",")
        chars.append(split_string[0])
    return chars

def getLink(linkList):
    return linkList[r.randint(0, len(linkList)-1)]

def listener(lst):
    lst.append(k.read_key())

def printLinks(subList):
    buzzed = []
    input = th.Thread(target = listener, args=(buzzed, ), daemon=True)
    input.start()
    while len(buzzed) == 0:
        print(getLink(subList))
        t.sleep(2)
    return buzzed[0]

def match(guess, answer):
    if guess.lower() == answer.lower():
        return True
    return False

def playGame():
    chars = getChars()
    scores = {}
    winner = ""
    points = 1
    pts_to_win = 10
    while winner == "":
        print("Selecting wikipedia page. Get ready to begin")
        targ = w.page(chars[r.randint(0, len(chars)-1)], auto_suggest = True)
        while True:
            guesser = printLinks(targ.links)
            ###Todo: Find a way to set a time limit for giving answer
            print("What is your guess?")
            guess = input("> ")
            if guess.lower() == "give up":
                print("The answer was " + str(targ.title))
                break
            elif match(guess, targ.title):
                if not guesser in scores.keys():
                    scores[guesser] = points
                else:
                    scores[guesser] += points
                print("Correct!")
                print(str(guesser) + " gets " + str(points) + " points!")
                if scores[guesser] >= pts_to_win:
                    print(str(guesser) + " wins the game!")
                    winner = guesser
                    break
                input("Press enter to continue")
                break
            else:
                ###Todo: implement system to keep players from guessing multiple times
                print("Sorry that was incorrect")
                t.sleep(1)

playGame()
