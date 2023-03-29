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
    csvOut=open('result.csv', 'w')
    wordWriter = csv.writer(csvOut, delimiter=',')
    wordReader = csv.reader(csvIn)
    word1 = ""
    word2 = ""
    word3 = ""
    word4 = ""
    word5 = ""
    csvIn.close()
    csvOut.close()
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
    pos0 = ""
    pos1 = ""
    pos2 = ""
    pos3 = ""
    pos4 = ""
    check0 = False
    check1 = False
    check2 = False
    check3 = False
    check4 = False
    if not knownLetterPositions[0] == '_':
        check0 = True
        pos0 = knownLetterPositions[0]
    if not knownLetterPositions[1] == '_':
        check1 = True
        pos1 = knownLetterPositions[1]
    if not knownLetterPositions[2] == '_':
        check2 = True
        pos2 = knownLetterPositions[2]
    if not knownLetterPositions[3] == '_':
        check3 = True
        pos3 = knownLetterPositions[3]
    if not knownLetterPositions[4] == '_':
        check4 = True
        pos4 = knownLetterPositions[4]
    csvLettersIn.close()
    score1 = 0
    score2 = 0
    score3 = 0
    score4 = 0
    score5 = 0
    word1 = ""
    word2 = ""
    word3 = ""
    word4 = ""
    word5 = ""
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
            if check0:
                if not word[0] == pos0:
                    stop = True
            if check1:
                if not word[1] == pos1:
                    stop = True
            if check2:
                if not word[2] == pos2:
                    stop = True
            if check3:
                if not word[3] == pos3:
                    stop = True
            if check4:
                if not word[4] == pos4:
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
        if tempScore>score5:
            if tempScore>score1:
                score5 = score4
                score4 = score3
                score3 = score2
                score2 = score1
                score1 = tempScore
                word5 = word4
                word4 = word3
                word3 = word2
                word2 = word1
                word1 = word
            elif tempScore>score2:
                score5 = score4
                score4 = score3
                score3 = score2
                score2 = tempScore
                word5 = word4
                word4 = word3
                word3 = word2
                word2 = word
            elif tempScore>score3:
                score5 = score4
                score4 = score3
                score3 = tempScore
                word5 = word4
                word4 = word3
                word3 = word
            elif tempScore>score4:
                score5 = score4
                score4 = tempScore
                word5 = word4
                word4 = word
            else:
                score5 = tempScore
                word5 = word
    print("The 5 best next word options based upon the letters you've already guessed are:\n")
    print(word1+", "+word2+", "+word3+", "+word4+", and "+word5+"\n")
    csvWordsIn.close()