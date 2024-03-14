import random
import time

#Starts game.

players=[]
colours=["Yellow", "Red", "Green", "Blue"]

numberOfPlayers=int(input("How many players? "))
while numberOfPlayers<2 or numberOfPlayers>4:
    numberOfPlayers=int(input("Not a valid number. Please enter numbers between 2-4. How many players? "))

numberofDrawnCards=int(input("How many cards do you want to start game with? "))
while numberofDrawnCards<1 or numberofDrawnCards>7:
    numberofDrawnCards=int(input("Not a valid number. Please enter numbers between 1-7. How many cards do you want to start game with? "))

#Builds an UNO Deck and shuffles it.

def BuildDeck():
    deck=[]
    colours=["Yellow", "Red", "Green", "Blue"]
    values=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "Draw Two", "Skip", "Reverse"]
    wilds=["Wild", "Wild Draw Four"]
    for colour in colours:
        for value in values:
            card="{} {}".format(colour, value)
            deck.append(card)
            if value!=0:
                deck.append(card)
    for i in range(0, 4):
        deck.append(wilds[0])
        deck.append(wilds[1])
    random.shuffle(deck)
    return deck

UNODeck=BuildDeck()
discard=[]
discard.append(UNODeck.pop(0))

#Draws wanted amount of cards.

def DrawCards(numberOfCards):
    drawnCards=[]
    for i in range(0, numberOfCards):
        drawnCards.append(UNODeck.pop(0))
    return drawnCards

#Deals cards to wanted amount of players.

def DealCards():
    for i in range(0, numberOfPlayers):
        players.append(DrawCards(numberofDrawnCards))

#Shows player's hand.

def ShowHand(player, playerHand):
    print("")
    print("Player {}'s turn".format(player+1))
    print("Your hand:")
    print("----------")
    n=1
    for i in playerHand:
        print("| {}) {}".format(n, i))
        n=n+1
    print("----------")
    print("")

#Checks if player can play or not.

def CanPlay(colour, value, playerHand):
    for card in playerHand:
        if "Wild" in card:
            return True
        elif colour in card or value in card:
            return True
    return False

#Gets colour and value of the card that is on top of the discard pile.

def GetDiscardCard():
    discardCard=discard[-1].split(" ", 1)
    colour=discardCard[0]
    if colour!="Wild":
        value=discardCard[1]
    else:
        value="Any"
    return colour, value

#Setups game.

playerTurn=0
playDirection=1
playing=True

DealCards()
colour, value=GetDiscardCard()

#Runs game.

while playing:
    ShowHand(playerTurn, players[playerTurn])
    print("Card on top of the discard pile is {}.".format(discard[-1]))

    if CanPlay(colour, value, players[playerTurn])==True:
        chosenCard=int(input("Which card do you want to play? "))

        while CanPlay(colour, value, [players[playerTurn][chosenCard-1]])==False:
            chosenCard=int(input("Not a valid card. Which card do you want to play? "))

        print("You played {}.".format(players[playerTurn][chosenCard-1]))
        discard.append(players[playerTurn].pop(chosenCard-1))
        colour, value=GetDiscardCard()

        #Checks if player won the game.

        if len(players[playerTurn])==0:
            playing=False
            print("")
            print("Player {} won the game. Congratulations!".format(playerTurn+1))

        else:

            #Applies cards' abilities.

            playedCard=discard[-1].split(" ", 1)

            if colour=="Wild":
                print("")
                for i in range(0, len(colours)):
                    print("{}) {}".format(i+1, colours[i]))
                print("")
                newColour=int(input("Which colour would you like to choose? "))
                while newColour<1 or newColour>4:
                    newColour=int(input("Not a valid colour. Which colour would you like to choose? "))
                print("You chose {}.".format(colours[newColour-1]))
                colour=colours[newColour-1]

            if len(playedCard)==1:
                playedValue="Any"
            else:
                playedValue=playedCard[1]

            if playedValue=="Reverse":
                playDirection=playDirection*-1

            if playedValue=="Skip":
                playerTurn=playerTurn+playDirection
                if playerTurn>=numberOfPlayers:
                    playerTurn=0
                elif playerTurn<0:
                    playerTurn=numberOfPlayers-1

            if playedValue=="Draw Two":
                playerDraw=playerTurn+playDirection
                if playerDraw>=numberOfPlayers:
                    playerDraw=0
                elif playerDraw<0:
                    playerDraw=numberOfPlayers-1
                players[playerDraw].extend(DrawCards(2))

            if playedValue=="Draw Four":
                playerDraw=playerTurn+playDirection
                if playerDraw>=numberOfPlayers:
                    playerDraw=0
                elif playerDraw<0:
                    playerDraw=numberOfPlayers-1
                players[playerDraw].extend(DrawCards(4))   

    else:
        print("You can not play. Drawing a card.")
        drawnCard=DrawCards(1)
        print("You drawed {}.".format(drawnCard[0]))
        players[playerTurn].extend(drawnCard)

    playerTurn=playerTurn+playDirection
    if playerTurn>=numberOfPlayers:
        playerTurn=0
    elif playerTurn<0:
        playerTurn=numberOfPlayers-1

    time.sleep(2)

print("")
print("Take care!")
time.sleep(2)