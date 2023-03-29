# Wordle Solver
 Fun project to help solve the daily Wordle puzzle

This project contains two different python script files as well as 4 input/output files.



allWords.csv has been sourced from https://github.com/dwyl/english-words

It contains 370,105 English language words of every length. This is an important dataset when you are filtering for a word that is the potential solution to a puzzle. There is no guarantee that every wordle word is in this list, however, it should have the vast majority of them.



wordleWordFilterer.py contains 2 different methods that can be useful for different types of preprocessing for this kind of project. It is not intended to be directly used for this project but rather to be used as a library file for wordListFinder.py

filterForWordleWords() reads allWords.csv and looks for only words of length 5 (valid Wordle words) and outputs these into wordleWords.csv.

filterOutRepeatLetters() reads wordleWords.csv (to cut down on processing time) and filters out the words that have repeated letters. Words with repeated letters can be used as the final Wordle word but they are not necessarily the best words to use for an initial guess as these words tell you less about what letters are in the final solution. 



wordListFinder.py is the file that does the actual processing to help find the solution word. This is run based upon the arguments that are passed to it.

python3 wordListFinder.py 0: Intended to utilize wordleWordFilterer.py/filterOutRepeatLetters() and provide a list of 5 words that have no repeated letters, intended to be utilized for finding a starting word that is useful.

python3 wordListFinder.py 1: Filter for the words that fit the rules and use as many common letters from the english language as possible (the table used to prioritize letters is in wordleWordFilterer.py and is sourced from https://leancrew.com/all-this/2022/01/wordle-letters/) and while it does not eliminate repeated letter words it does deprioritize the popularity of the letter if it is repeated in the word. It is intended to give the best possible starting word. The biggest reason this is included in the project as an existing method is in the event of discovering a wordle appropriate word that is not included in allWords.csv that gets added to the file or a word is tried and wordle says it is not a valid word. (I have had this happen a few times in testing)

python3 wordListFinder.py 2: Follow the exact same rules as 1, however, this time it provides 5 words to choose from rather than the best one only. It also takes in a user generated file 'usedLetters.csv' that has users input letters (separated by commas) that they know to be in the final word on the first line, letters(separated by commas) they know are not in the final word on the second line, and any letters that they know where they belong should go should get filled into the blank space that corresponds to the spot it belongs in.