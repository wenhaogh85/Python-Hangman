import random
from datetime import datetime

# ----------------------------------------------------------------------------
# initialses a list of stages in hangman
stages = [
    "\n    ________" +
    "\n    |     \|" +
    "\n           |" +
    "\n           |" +
    "\n           |" +
    "\n           |" +
    "\n        =======",
    "\n    ________" +
    "\n    |     \|" +
    "\n    O      |" +
    "\n           |" +
    "\n           |" +
    "\n           |" +
    "\n        =======",
    "\n    ________" +
    "\n    |     \|" +
    "\n    O      |" +
    "\n    |      |" +
    "\n           |" +
    "\n           |" +
    "\n        =======",
    "\n    ________" +
    "\n    |     \|" +
    "\n    O      |" +
    "\n   /|      |" +
    "\n           |" +
    "\n           |" +
    "\n        =======",
    "\n    ________" +
    "\n    |     \|" +
    "\n    O      |" +
    "\n   /|\     |" +
    "\n           |" +
    "\n           |" +
    "\n        =======",
    "\n    ________" +
    "\n    |     \|" +
    "\n    O      |" +
    "\n   /|\     |" +
    "\n   /       |" +
    "\n           |" +
    "\n        =======",
    "\n    ________" +
    "\n    |     \|" +
    "\n    O      |" +
    "\n   /|\     |" +
    "\n   / \     |" +
    "\n           |" +
    "\n        =======",
]

# ----------------------------------------------------------------------------
# updates log file to keep track of game history
def updateLogFile(category, word, isWin):

    currentDate = datetime.today().strftime("%d-%m-%Y")
    currentTime = datetime.today().strftime("%H:%M:%S")

    status = "win" if isWin else "lose"

    fileMode = "a"

    file = open("log.txt", fileMode)

    logMessage = "category: {}\nword: {}\nstatus: {}\ntimestamp: {} - {}\n\n".format(
                                                                    category,
                                                                    word,
                                                                    status,
                                                                    currentDate,
                                                                    currentTime
                                                                    )

    file.write(logMessage)
    file.close()

# ----------------------------------------------------------------------------
# checks if the input is a digit
def isDigit(token):

    DIGITS = "1234567890"

    for digit in DIGITS:

        if digit == token:
            return True
    return False

# checks if the input is an alphabet
def isAlphabet(token):

    ALPHABETS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    for alphabet in ALPHABETS:

        if token.upper() == alphabet:
            return True
    return False

# get a list of words from the specified filename
def getWords(filename):

    #read only from file
    mode = "r"

    file = open(filename, mode)

    rawContents = file.readlines()

    words = []
    for rawContent in rawContents:

        # removes newline characters
        words.append(rawContent.strip("\n"))

    file.close()

    return words

# get a random word based on a random index value from a list of words
def getRandomWord(words):

    length = len(words)

    index = 0
    if length > 0 and length > 1:
        index = random.randrange(0, len(words))
    return words[index]

# converts a word to a list of letters
def toLetters(word):

    letters = []

    for letter in word:
        letters.append(letter)

    return letters

# converts a list of letters to form a word
def toWord(letters):

    word = ""

    for letter in letters:
        word += letter

    return word

# checks if the letter user has entered is in the random word
# returns the indexes of the letter in the random word if it matches
def isLetterInWord(userLetter, word):

    indexes = []
    for index in range(len(word)):

        if userLetter.upper() == word[index].upper():
            indexes.append(index)

    # returns the index of the letter from the word
    return indexes

# returns a word where all the letters are changed to "_"
# to mask the letters of the random word
def getHiddenWord(word):

    userLetters = []

    for letter in word:
        userLetters.append("_" if isAlphabet(letter) else letter)

    # returns the userLetter in the form of ["_", "_"]
    return userLetters

# updates the hidden word based on the indexes of the letter
# from the random word
def updateHiddenWord(word, hiddenWord, indexes):

    for index in indexes:
        hiddenWord[index] = word[index]

# formats the word with whitespaces for the user to see
def formatLetters(letters):

    text = ""
    for letter in letters:
        text += letter + " "

    return text

# checks if the entire letter in the user guessed word is equal to the word
def isGuessEqualWord(guessWord, word):

    for index in range(len(word)):

        # checks if every guess letter matches the actual word letter
        if guessWord[index].upper() != word[index].upper():
            return False
    return True

# checks if the user has entered the same letter before
def isLetterDuplicate(userLetter, word):

    for letter in word:

        # checks for duplicate
        if userLetter == letter:
            return True
    return False

# gets a valid user input (letter)
def getUserLetter():

    while True:

        letter = input("\nEnter guess (a-z): ")

        if len(letter) > 1:
            print('You can only guess one letter. Try again...')

        elif letter == "0":
            return letter

        elif isAlphabet(letter):
            return letter

        else:
            print("That was not a letter. Try again...")

# ----------------------------------------------------------------------------
# gets a valid user input (option)
def getOption():

    while True:

        print(
            "\n============================" +
            "\nWelcome to Hangman" +
            "\n============================\n" +
            "\nChoose a category:\n" +
            "\n+--------+---------------+" +
            "\n| Option | Category      |" +
            "\n+--------+---------------+" +
            "\n|   1    | Countries     |" +
            "\n+--------+---------------+" +
            "\n|   2    | Movies        |" +
            "\n+--------+---------------+" +
            "\n|   3    | Choosen Word  |" +
            "\n+--------+---------------+" +
            "\n============================\n"
        )

        option = input("Enter option (1-3): ")

        validOptions = ["1", "2", "3"]

        if option in validOptions:
            return option

        else:
            print("That was an invalid option. Try again...")

# controls the flow of the hangman game based on the option 
# that the user has choose 
def playHangman():

    option = getOption()
    category = ""

    if option == "1":
        category = "countries"
    elif option == "2":
        category = "movies"
    elif option == "3":
        category = "custom"

    # forms filename bssed on the category the user chooses
    filename = category + ".txt"

    # gets the random word from the list of words in the text file
    randomWord = toLetters((getRandomWord(getWords(filename))))

    # create a copy of letters that masks letters in the random word with "_"
    userLetters = getHiddenWord(randomWord)

    # initialses the initial game state
    wrongLetters = []
    correctLetters = []

    stage = 0

    isWin = False

    # displays to the user the initial status of the hangman game
    print(
        "\n============================" +
        "\nEnter 0 to quit hangman" +
        "\n" + stages[stage] +
        "\n\n" + formatLetters(userLetters) +
        "\n\nHits  : " + formatLetters((correctLetters)) +
        "\nMisses: " + formatLetters((wrongLetters))
    )

    # starts the hangman game
    stopPlaying = ""
    while isWin != True and stage < len(stages) - 1 and stopPlaying != "0":

        # gets the user input (letter)
        letter = getUserLetter()

        # checks if the user wants to quit current hangman game
        if letter == "0":
            print("Quiting hangman...")
            stopPlaying = "0"
            continue

        # checks if the user input (letter) has been entered before
        if isLetterDuplicate(letter, wrongLetters + correctLetters):
            print("This letter has been entered before. Try again...")
            continue

        else:
            # checks if the letter that the user has entered is in the random word
            indexesOfLetter = isLetterInWord(letter, randomWord)

            # if the list (indexes of letter) is not empty,
            # this indicates that the letter that the user entered
            # is in the random word
            if len(indexesOfLetter) != 0:

                # updates the masked letters that is in the random word
                updateHiddenWord(randomWord, userLetters, indexesOfLetter)

                # checks if the user has guessed all the letters in the random word
                isWin = isGuessEqualWord(randomWord, userLetters)

                # updates the correct letters that the user has input before
                correctLetters.append(letter)

            else:

                # updates the wrong letters that the user has input before
                wrongLetters.append(letter)

                # updates the hangman diagram image
                stage += 1

        # displays to the user the current status of the hangman game
        print(
            "\n============================" +
            "\nEnter 0 to quit hangman" +
            "\n" + stages[stage] +
            "\n\n" + formatLetters(userLetters) +
            "\n\nHits  : " + formatLetters(correctLetters) +
            "\nMisses: " + formatLetters(wrongLetters)
        )

    # final outcome of the game
    print("\n======== Game Over =========")

    # prints the message accordingly if the user win or loses
    if isWin:
        print("\nCongrats! You managed to guess the word \"{}\" correctly :)".format(toWord(randomWord)))
    else:
        print(
            "\nYou lose, sorry :'(" +
            "\nThe word was: " + toWord(randomWord)
        )

    updateLogFile(category, toWord(randomWord), isWin)

# ----------------------------------------------------------------------------
# main program
if __name__ == "__main__":

    continuePlaying = True
    while continuePlaying != False:

        # start the hangman game
        playHangman()

        # displays a list of options to the user once they have finish
        # playing hangman
        while True:

            print(
                "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" +
                "\nEnter one of the following options:\n" +
                "\n+--------+-----------------------+" +
                "\n| Option |       Function        |" +
                "\n+--------+-----------------------+" +
                "\n|   p    | To play hangman again |" +
                "\n+--------+-----------------------+" +
                "\n|   q    | To quit hangman       |" +
                "\n+--------+-----------------------+" +
                "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
            )

            # prompts the user if they want to continue playing 
            # or quit the hangman game
            userInput = input("Enter option (p or q): ").lower()

            # checks if the user input is to continue playing the game
            # or quit the hangman game
            if userInput == "p":
                print("\n======== New Game ==========")
                break

            elif userInput == "q":
                continuePlaying = False
                break

            else:
                print("That was an invalid option. Try again...")

    # displays goodbye message once user have quit the game
    print("Thank you for playing hangman :)")
    wait = input()
