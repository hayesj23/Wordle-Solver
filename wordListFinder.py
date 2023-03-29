import csv
from fileinput import close
from ntpath import join
from os.path import exists
import sys
from turtle import pos
import requests
import pandas as pd
import io


from numpy import true_divide
import wordleWordFilterer

url = "https://raw.githubusercontent.com/hayesj23/Wordle-Solver/main/allWords.csv"

if not exists('wooordleWords.csv'):
    if not exists('allWords.csv'):
        print ("download start!")
        download = requests.get(url).content
        print ("download complete!")
        csvIn=io.StringIO(download.decode('utf-8'))
        csvOut=open('allWords.csv', 'w')
        wordWriter = csv.writer(csvOut, delimiter=' ', dialect=csv.excel)
        wordReader = csv.reader(csvIn, dialect=csv.unix_dialect)
        for row in wordReader:
            word = str(''.join(row))
            wordWriter.writerow([word])
        csvOut.close()
    wordleWordFilterer.filterForWordleWords()
#argv[1]==0 means filter for finding sets of words with no repeating letters. 
# 1 means filter for most common letter starting words with repeat letters having their value lowered.
# 2 gives a list of the 5 best next words based upon the rules of 1 and a provided, comma delineated, 
# csv file 'usedLetters.csv' with row 1 giving letters known to be in the final word and row 2 giving
# letters known not to be in the final word
print(sys.argv[1])
if int(sys.argv[1]) == 0:
    if not exists('repeatLetterRemovedWordleWords.csv'):
        wordleWordFilterer.filterOutRepeatLetters()
    csvIn=open('repeatLetterRemovedWordleWords.csv', 'r')
    words = ["", "", "", "", ""]
    for j in range(5):
        csvIn=open('repeatLetterRemovedWordleWords.csv', 'r')
        wordReader = csv.reader(csvIn)
        currentScore = 0
        currentBestWord = ""
        for row in wordReader:
            word = str(''.join(row))
            if not word in words:
                tempWord = ""
                tempScore = 0
                for i in word:
                    letterScore = wordleWordFilterer.wordScore(i)
                    tempScore = tempScore+letterScore
                    tempWord+=str(i)
                if tempScore>currentScore:
                    currentScore = tempScore
                    words[j] = tempWord
        csvIn.close()
    print("The 5 best first word options are:")
    print(words[0]+", "+words[1]+", "+words[2]+", "+words[3]+", and "+words[4])
if int(sys.argv[1]) == 1:
    csvIn=open('wordleWords.csv', 'r')
    wordReader = csv.reader(csvIn)
    currentScore = 0
    currentBestWord = ""
    for row in wordReader:
        word = str(''.join(row))
        tempWord = ""
        tempScore = 0
        for i in word:
            letterScore = wordleWordFilterer.wordScore(i)
            if i in tempWord:
                tempScore = tempScore+(letterScore/2)
            else:
                tempScore = tempScore+letterScore
                tempWord+=str(i)
        if tempScore>currentScore:
            currentScore = tempScore
            currentBestWord = tempWord
    csvIn.close()
    print(currentBestWord+ " is the best starting wordle word!")
if int(sys.argv[1]) == 2:
    if not exists('usedLetters.csv'):
        temp = open('usedLetters.csv', 'w')
        wordWriter = csv.writer(temp, delimiter=' ', dialect=csv.excel)
        wordWriter.writerow([])
        wordWriter.writerow([])
        wordWriter.writerow(["_,_,_,_,_"])
        temp.close()
        print("Please fill out 'usedLetters.csv' with row 1 being letters known to be present in the final word\n")
        print("and row 2 being letters known not to be in the final word. Also fill out the third row for any letter locations that are known. Fill this out in the following format:\n")
        print("e,p,r,s\n")
        print("z,x,o\n")
        print("p,r,e,_,s")
        quit()
    csvWordsIn = open('wordleWords.csv', 'r')
    csvLettersIn = open('usedLetters.csv', 'r')
    wordReader = csv.reader(csvWordsIn)
    letterReader = csv.reader(csvLettersIn, delimiter=',')
    includedLetters = letterReader.__next__()
    excludedLetters = letterReader.__next__()
    row = letterReader.__next__()
    knownLetterPositions = str(''.join(row))
    posits = ["", "", "", "", ""]
    check = [False, False, False, False, False]
    
    if not knownLetterPositions[0] == '_':
        check[0] = True
        posits[0] = knownLetterPositions[0]
    if not knownLetterPositions[1] == '_':
        check[1] = True
        posits[1] = knownLetterPositions[1]
    if not knownLetterPositions[2] == '_':
        check[2] = True
        posits[2] = knownLetterPositions[2]
    if not knownLetterPositions[3] == '_':
        check[3] = True
        posits[3] = knownLetterPositions[3]
    if not knownLetterPositions[4] == '_':
        check[4] = True
        posits[4] = knownLetterPositions[4]
    csvLettersIn.close()
    scores = [0, 0, 0, 0, 0]
    words = ["", "", "", "", ""]
    for row in wordReader:
        word = str(''.join(row))
        stop = False
        for x in includedLetters:
            if stop:
                break
            if not x in word:
                stop = True
        for y in excludedLetters:
            if stop:
                break
            if y in word:
                stop = True
        if not stop:
            if check[0]:
                if not word[0] == posits[0]:
                    stop = True
            if check[1]:
                if not word[1] == posits[1]:
                    stop = True
            if check[2]:
                if not word[2] == posits[2]:
                    stop = True
            if check[3]:
                if not word[3] == posits[3]:
                    stop = True
            if check[4]:
                if not word[4] == posits[4]:
                    stop = True
        if stop:
            continue
        tempWord = ""
        tempScore = 0
        for i in word:
            letterScore = wordleWordFilterer.wordScore(i)
            if i in tempWord:
                tempScore += letterScore/2
            else:
                tempScore += letterScore
                tempWord+=str(i)
        if tempScore>scores[4]:
            if tempScore>scores[0]:
                scores[4] = scores[3]
                scores[3] = scores[2]
                scores[2] = scores[1]
                scores[1] = scores[0]
                scores[0] = tempScore
                words[4] = words[3]
                words[3] = words[2]
                words[2] = words[1]
                words[1] = words[0]
                words[0] = word
            elif tempScore>scores[1]:
                scores[4] = scores[3]
                scores[3] = scores[2]
                scores[2] = scores[1]
                scores[1] = tempScore
                words[4] = words[3]
                words[3] = words[2]
                words[2] = words[1]
                words[1] = word
            elif tempScore>scores[2]:
                scores[4] = scores[3]
                scores[3] = scores[2]
                scores[2] = tempScore
                words[4] = words[3]
                words[3] = words[2]
                words[2] = word
            elif tempScore>scores[3]:
                scores[4] = scores[3]
                scores[3] = tempScore
                words[4] = words[3]
                words[3] = word
            else:
                scores[4] = tempScore
                words[4] = word
    print("The 5 best next word options based upon the letters you've already guessed are:")
    print(words[0]+", "+words[1]+", "+words[2]+", "+words[3]+", and "+words[4])
    csvWordsIn.close()