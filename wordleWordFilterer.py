import csv
from fileinput import close

def filterForWordleWords():
    csvIn=open('allWords.csv', 'r')##Sourced from 'https://github.com/dwyl/english-words' using alpha words
    csvOut=open('wordleWords.csv', 'w')
    wordWriter = csv.writer(csvOut, delimiter=' ', dialect=csv.excel)
    wordReader = csv.reader(csvIn, dialect=csv.excel)
    for row in wordReader:
        word = str(''.join(row))
        if len(word) == 5:
            wordWriter.writerow([word])
    csvIn.close()
    csvOut.close()

def filterOutRepeatLetters():
    csvIn=open('wordleWords.csv', 'r')
    csvOut=open('repeatLetterRemovedWordleWords.csv', 'w')
    wordWriter = csv.writer(csvOut, delimiter=' ', dialect=csv.excel)
    wordReader = csv.reader(csvIn, dialect=csv.excel)
    for row in wordReader:
        word = str(''.join(row))
        hasRepeatLetters = False
        tempWord = ""
        for i in word:
            if i in tempWord:
                hasRepeatLetters = True
                break
            else:
                tempWord+=str(i)
        if not hasRepeatLetters:
            wordWriter.writerow([word])
    csvIn.close()
    csvOut.close()

def wordScore(letter):
    if letter == 'a':
        return 10.5
    if letter == 'b':
        return 2.7
    if letter == 'c':
        return 3.6
    if letter == 'd':
        return 3.3
    if letter == 'e':
        return 10.0
    if letter == 'f':
        return 1.6
    if letter == 'g':
        return 2.6
    if letter == 'h':
        return 3.1
    if letter == 'i':
        return 6.1
    if letter == 'j':
        return 0.4
    if letter == 'k':
        return 2.1
    if letter == 'l':
        return 5.6
    if letter == 'm':
        return 3.1
    if letter == 'n':
        return 5.2
    if letter == 'o':
        return 6.6
    if letter == 'p':
        return 3.0
    if letter == 'q':
        return 0.2
    if letter == 'r':
        return 7.2
    if letter == 's':
        return 5.6
    if letter == 't':
        return 5.6
    if letter == 'u':
        return 4.4
    if letter == 'v':
        return 1.1
    if letter == 'w':
        return 1.6
    if letter == 'x':
        return 0.4
    if letter == 'y':
        return 3.8
    if letter == 'z':
        return 0.6
    #letter frequencies sourced from 'https://leancrew.com/all-this/2022/01/wordle-letters/'
    
