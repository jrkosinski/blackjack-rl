from enum import Enum
import random

class CardSuit(Enum):
    Spades = 0, 
    Diamonds = 1,
    Clubs = 2,
    Hearts = 3
    
class CardValue(Enum): 
    Two = 2,
    Three = 3,
    Four = 4,
    Five = 5,
    Six = 6,
    Seven = 7,
    Eight = 8,
    Nine = 9,
    Ten = 10, 
    Jack = 11, 
    Queen = 12,
    King = 13,
    Ace = 14
    
_card_numeric_values = {
    CardValue.Two: 2,
    CardValue.Three: 3,
    CardValue.Four: 4, 
    CardValue.Five: 5,
    CardValue.Six: 6, 
    CardValue.Seven: 7, 
    CardValue.Eight: 8, 
    CardValue.Nine: 9, 
    CardValue.Ten: 10, 
    CardValue.Jack: 10, 
    CardValue.Queen: 10, 
    CardValue.King: 10, 
    CardValue.Ace: 1, 
}

_all_card_suits = [
    CardSuit.Hearts, CardSuit.Diamonds, CardSuit.Clubs, CardSuit.Spades
]

_all_card_values = [
    CardValue.Two,
    CardValue.Three,
    CardValue.Four,
    CardValue.Five,
    CardValue.Six,
    CardValue.Seven,
    CardValue.Eight,
    CardValue.Nine,
    CardValue.Ten, 
    CardValue.Jack, 
    CardValue.Queen,
    CardValue.King,
    CardValue.Ace
]

class Card: 
    '''A playing card'''
    def __init__(self, suit: CardSuit, value: CardValue):
        self.suit = suit
        self.value = value
        
    # True if card is an ace
    @property 
    def is_ace(self): 
        return self.value == CardValue.Ace
        
    @property 
    # True if card is jack, queen, or king
    def is_face_card(self): 
        return self.value in [CardValue.Jack, CardValue.Queen, CardValue.King]
    
    @property 
    # Gets the numerical value in blackjack for the card
    def number_value(self): 
        return _card_numeric_values[self.value]
    
    def __str__(self) -> str:
        return f"{self.suit} {self.value}"

#TODO: (LOW) test this 
def get_card(s: str) -> Card: 
    ssuit = s[0:1]
    sval = s[1:]
    suit = None
    val = None
    if ssuit == "H": 
        suit = CardSuit.Hearts
    elif ssuit == "C": 
        suit = CardSuit.Clubs
    elif ssuit == "S": 
        suit = CardSuit.Spades
    elif ssuit == "D": 
        suit = CardSuit.Diamonds
        
    if sval == "2": 
        val = CardValue.Two
    elif sval == "3": 
        val = CardValue.Three
    if sval == "4": 
        val = CardValue.Four
    if sval == "5": 
        val = CardValue.Five
    if sval == "6": 
        val = CardValue.Six
    if sval == "7": 
        val = CardValue.Seven
    if sval == "8": 
        val = CardValue.Eight
    if sval == "9": 
        val = CardValue.Nine
    if sval == "10": 
        val = CardValue.Ten
    if sval == "J": 
        val = CardValue.Jack
    if sval == "Q": 
        val = CardValue.Queen
    if sval == "K": 
        val = CardValue.King
    if sval == "A": 
        val = CardValue.Ace
        
    return Card(suit, val)
    
def all_card_values(): 
    return _all_card_values
    
def all_card_suits(): 
    return _all_card_suits
    
def card_numeric_values(): 
    return _card_numeric_values