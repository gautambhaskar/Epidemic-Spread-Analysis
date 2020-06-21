import math
import random
wordbank = ["skyfall 2", "cars 3", "winnie the pooh", "descendants 2", "avengers endgame", "toy story 4", "aladdin", "hobbs and shaw", "godzilla", "john wick", "terminator dark fate", "captain marvel"]
word_id = random.randrange(0,12)
word = wordbank[word_id]
terms = word.split(" ")
display_terms = []
idi = -1
for term in terms:
    char_num = 0
    idi += 1
    new_term = []
    for char in term:
        char_num += 1
        new_term += "_"
    display_terms += [new_term]
def display():
    for term in display_terms:
        statement = ""
        for char in term:
            statement += char + " "
        print(statement)
def check_done():
    done = True
    for term in display_terms:
        for char in term:
            if char == "_":
                done = False
    return done
display()
correct = False
strikes = 0
while correct == False:
    character = input("Enter a Character: ")
    if len(character) > 1:
        "Enter a SINGLE CHARACTER!"
    else:
        term_id = -1
        found = False
        found_id = []
        for term in terms:
            term_id += 1
            idii = -1
            for char in term:
                idii += 1
                if char == character:
                    found = True
                    found_id += [term_id, idii],
        if found:
            print("This character is in the name!")
            for ids in found_id:
                display_terms[ids[0]][ids[1]] = character
            display()
            if check_done():
                print(" ")
                print(" ")
                print(" ")
                print("Congratulations! You've Won! The word was:")
                print("'"+word+"'")
                print(" ")
                print(" ")
                print(" ")
    
                break
        else:
            print("Sorry! That character isn't in the name!")
            strikes += 1
            print ("Strike # " + str(strikes) +"/7" )
            if strikes >= 7:
                print(" ")
                print(" ")
                print("GAME OVER!!! The correct answer was '" + word + "'!")
                print(" ")
                print(" ")
                print(" ")
                print("Try Again by typing 'python3 hangman.py'")
                print(" ")
                print(" ")
                print(" ")
                break
exit()    