import random
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def shuffle_decks():
#The shuffle_decks function creates cards with different values for each sort
#and for each of the 6 decks we use. It then creates a deck by randomly assigning them an index.
  decks=[]
  for i in range (0,6):
    for j in range(0,4):
      decks.append('Ace') #The ace's value changes depending on the situation
      decks.append(2)
      decks.append(3)
      decks.append(4)
      decks.append(5)
      decks.append(6)
      decks.append(7)
      decks.append(8)
      decks.append(9)
      decks.append(10)
      decks.append(10) #The jacks,queens and kings also have values of 10 in the game of Blackjack
      decks.append(10)
      decks.append(10)
  random.shuffle(decks) #This will create the element of randomness to the card picked.
  return decks

def receive_card(decks):
#The receive_card function picks the first card from the shuffled deck and removes it from the deck.
  received_card=decks[0]
  decks.remove(received_card)
  return received_card

def assign_initial_points(received_cards_list,points):
#The assign_initial_points function gives an initial amount of points to the player
#after he receives his two initial cards
  for i in range(0,len(received_cards_list)):
    if received_cards_list[i]!='Ace':
      points+=received_cards_list[i]
    else:
      #If one of the cards picked is an ace, its value will be assumed to be 11 if
      #the total points is between 19 and 21 inclusively, and it will be 1 otherwise.
      x=11+points
      if x>21 or x<19:
        points+=1
      else:
        points+=11
  return points

def assign_further_points(card,points): 
#The assign_further_points adds the points of each additional card picked by
#either the player or the dealer to their respective total amount of points.
  if card!='Ace':
    points+=card
  else:
    x=points+11
    if x>21 or x<19:
      points+=1
    else:
      points+=11
  return points

def check_bust(points):
#The check_bust function verifies if the player or the dealer's points are
#higher than 21, which would automatically end the game.
  if points>21:
    return True
  else:
    return False

def hit(strategy,points):
#The hit function determines whether the player should hit or stand
#depending on the strategy he is currently using.
  if points>strategy:
    return False
  else:
    return True

def hit_dealer(dealer_points):
#The hit function determines whether the dealer hits or stands
#depending on whether his points are greater than or equal to 17.
  if dealer_points>=17:
    return False
  else:
    return True

def play_blackjack(strategy,deck):
#The play_blackjack function uses the previously mentioned functions to simulate
#a game of blackjack.
  received_cards_list=[]
  points=0
  dealer_points=0

#This block of code serves to pick the player's first two cards and assign
#their values to his total amount of points. The len(deck)==0 condition is present
#before each picking of a card so that it reshuffles the deck if the deck is empty.
  if len(deck)==0:
    deck=shuffle_decks()
  picked_card=receive_card(deck)
  received_cards_list.append(picked_card)
  if len(deck)==0:
    deck=shuffle_decks()
  picked_card_2=receive_card(deck)
  received_cards_list.append(picked_card_2)
  points=assign_initial_points(received_cards_list,points)
 
 
#As long as the player has not busted yet, he can choose to hit or stand
#depending on the strategy he is using.
  while check_bust(points)==False:
    if hit(strategy,points)==False:
      break
    else:
      if len(deck)==0:
        deck=shuffle_decks()
      picked_card=receive_card(deck)
      points=assign_further_points(picked_card,points)

#Once the player has ended by either busting or standing, we can proceed with
#the dealer's cards. 
  if len(deck)==0:
    deck=shuffle_decks()
  dealer_picked_card=receive_card(deck)
  dealer_points=assign_further_points(dealer_picked_card,dealer_points)

#The dealer will keep on hitting until he either lands between 17 and 21
#or busts (goes directly above 21) 
  while check_bust(dealer_points)==False:
    if hit_dealer(dealer_points)==False:
      break
    else:
      if len(deck)==0:
        deck=shuffle_decks()
      dealer_picked_card=receive_card(deck)
      dealer_points=assign_further_points(dealer_picked_card,dealer_points)

#If the player has more points than the dealer and did not go over 21, or 
#if the player has less than 21 points and the dealer busted, we will say
#that the player won. In all other cases, we will assume that the player has 
#lost (if the player ties, we consider it a loss).
  if (points>dealer_points and points<=21) or (points<=21 and dealer_points>21):
    return True
  else:
    return False
#The function play_blackjack will return True if the player wins, and False if he loses.


list_of_games=[]
list_of_results=[]
pandas_list=[]
list_of_strategies=[]
total=0
deck=shuffle_decks()
random.seed(10) #This function is useful in order to make each simulation give the same random results, because it will make each simualation start at the same place.
#For each strategy, the game is played 1000 times. The amount of wins
#are recorded in the list_of_results and then added to the pandas_list.
#This experiment is then repeated 100 times, so that we can get an average 
#of wins for each strategy used. The first game starts with a shuffled deck,
#and the deck will slowly go down in each game until it is emptied, where it is
#shuffled again in the play_blackjack function to keep playing the game.


#This code takes approximatively 4 min seconds to run
for j in range(0,100):
  for strategy in range(9,20):
    list_of_strategies.append(strategy)
    for i in range(0,1000):
      if play_blackjack(strategy,deck)==True:
        list_of_results.append(1)
        list_of_games.append(1)
      else:
        list_of_results.append(0)
        list_of_games.append(1)
      total+=list_of_results[i]
    pandas_list.append(total)
    total=0
    list_of_results=[]
print(pandas_list)



#We create a dataframe containing the average number of wins out of 1000 games
#according to the strategy used.
data={'Strategies':list_of_strategies,
        'Games won':pandas_list}
df=pd.DataFrame(data=data);
results=df.groupby("Strategies")

#This shows the Standard error for each strategy
error=results.sem()
print (error)


#This code lets us plot the graph of the dataframe previously mentioned.
fig, ax = plt.subplots(figsize=(18,10))
ax=sns.barplot(
    data=df,
    x='Strategies',
    y='Games won',
    ci=95, #This shows a confidence interval of 95% on each bar of the barplot
    capsize=0.3

)
ax.set_xlabel("Last point total up to which the player hits",fontsize=24);
ax.set_ylabel("Number of Games Won out of 1000",fontsize=24);
ax.set_title('Probability of Winning a Blackjack Game Based on the Strategy Used',fontsize=30);
ax.annotate(('Maximum number of games won: 428'), xy= (3,428),
            xytext= (3.50,440), arrowprops= dict(facecolor= 'red', shrink=2),fontsize=15);
