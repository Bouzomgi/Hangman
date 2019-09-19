from turtle import *
import functools
from time import *

#Initializes my two Turtles: One for drawing the hangman, and other for writing all the text
bg = Screen()
bg.title("Hangman")
drawPointer = Turtle()
textPointer = Turtle()
drawPointer.speed(4)
textPointer.speed(4)
drawPointer.hideturtle()
textPointer.hideturtle()

#Because the code for drawing the hands and legs are similar, we can remove the commonality and create this interior function that we can call in rhand,lhand,rleg,lleg
def reposition(direction,part):
    currenty = 90 if part == "arm" else -10
    drawPointer.sety(currenty)
    drawPointer.seth(240)if direction == "L" else drawPointer.seth(300)
    drawPointer.pendown()
    drawPointer.forward(50) if part == "arm" else drawPointer.forward(70)
    drawPointer.setpos(-100,currenty)
    drawPointer.penup()

#Draws our stand
def stand():
    drawPointer.pendown()
    drawPointer.speed(10)
    drawPointer.width(10);drawPointer.penup();drawPointer.setpos(-280,-120);drawPointer.pendown();drawPointer.setx(-150);drawPointer.setx(-215);drawPointer.sety(220);drawPointer.setx(-100)
    drawPointer.width(5);drawPointer.color("brown");drawPointer.sety(170)
    drawPointer.speed(4)
    drawPointer.penup()

#Draws our head
def head():
    drawPointer.pendown()
    drawPointer.setpos(-100,170)
    drawPointer.color("black");drawPointer.right(180);drawPointer.circle(30,360)
    drawPointer.penup()

#Draws our head
def body():
    drawPointer.setpos(-100,110)
    drawPointer.pendown()
    drawPointer.seth(360);drawPointer.right(90);drawPointer.color("brown");drawPointer.forward(10);drawPointer.color("black");drawPointer.forward(110)
    drawPointer.penup()
    
#Returns boolean depending if a character is a letter or space
def isValid(letter):
    return letter.isalpha() or letter == " "

#Prompts the user for a word. If the word is invalid, continuously prompt until a valid word is given. Return that word in all uppercase
def wordToGuess():
    inputWord = bg.textinput("Hangman", "Please input a word for your opponent to guess")
    while (inputWord == None or (len(inputWord) > 10) or (len(inputWord) == 0) or not all(map(lambda x: isValid(x),list(inputWord))) or inputWord.isspace()):
        if inputWord == None:
            bg.bye()
        else:
            inputWord = bg.textinput("Hangman", "Invalid word, please try again")
    return inputWord.upper()

#Take in the word to be guessed and a list of all the letters already guessed. Fill all unguessed letters in that word with underscores and print it to the screen
def refreshWord(inputWord, lettersUsed):
    bg.delay(20)
    textPointer.clear()
    displayWord = (" ".join([letter if (letter in lettersUsed) else "_" if letter.isalpha() else " " for letter in list(inputWord)]))
    textPointer.penup()
    textPointer.setpos(0,-230)
    textPointer.pendown()
    textPointer.write(displayWord, False, align="center",font=("Comic Sans", 50, "normal"))
    textPointer.penup()

#Prompt the user for a valid letter. Continously prompts if the letter is invalid or the letter has already been guessed. Return a boolean depending on if the letter
#guessed is in the word
def letterPrompt(inputWord, lettersUsed):
    letterGuess = bg.textinput("Hangman", "Guess a letter")

    while (letterGuess == None or not letterGuess.isalpha() or (letterGuess.upper() in lettersUsed) or len(letterGuess) != 1):
        if letterGuess == None:
            bg.bye()
        elif not letterGuess.isalpha() or len(letterGuess) != 1:
           letterGuess = bg.textinput("Hangman", "Please input a letter")
        else:
            letterGuess = bg.textinput("Hangman", "You've already guessed that letter")
    letterGuess = letterGuess.upper()
    lettersUsed.append(letterGuess)
    if letterGuess in inputWord:
        return True
    return False

#The definition of a "win" is when all letters in the word have been guessed. Return True if such an event occurs
def win(inputWord, lettersGuessed):
    return(all(map(lambda x: x in lettersGuessed, list(inputWord))))

#Prints out YOU WIN! to the GUI
def endOfGameWin():
    bg.delay(20)
    textPointer.penup()
    textPointer.setpos(150, 150)
    textPointer.color("green")
    textPointer.pendown()
    textPointer.write("You Win", False, align = "center", font=("Comic Sans", 50, "bold"))
    sleep(10000)

#Shows the full word at the bottom of the GUI and prints YOU LOSE to the GUI
def endOfGameLose(inputWord):
    refreshWord(inputWord, list(inputWord))
    bg.delay(20)
    textPointer.penup()
    textPointer.setpos(150, 150)
    textPointer.color("red")
    textPointer.pendown()
    textPointer.write("You Lose", False, align = "center", font=("Comic Sans", 50, "bold"))
    sleep(10000)

#Calling that interior function written above with different parameters to perform a similar, but not the same, drawing.
def rArm():
    reposition("R", "arm")
def lArm():
    reposition("L", "arm")
def rLeg():
    reposition("R", "leg")
def lLeg():
    reposition("L", "leg")

#Perform Hangman. Interesting part: I use a list to act as a stage progression system. Each string is evaluated into its respective function to be executed
#on the GUI
def main():
    
    lettersUsed = [" "]
    inputWord = ''
    letterGuess = ''
    stage = 0
    progression = ["head()", "body()", "lArm()", "rArm()", "rLeg()", "lLeg()"]

    stand()
    inputWord = wordToGuess()
    refreshWord(inputWord, lettersUsed)
    while not win(inputWord, lettersUsed):
        if letterPrompt(inputWord, lettersUsed):
            refreshWord(inputWord, lettersUsed)
        else:
            eval(progression[stage])
            stage += 1
            if stage == len(progression):
                endOfGameLose(inputWord)
                return()
    endOfGameWin()
        
main()


