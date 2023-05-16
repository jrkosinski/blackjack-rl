from enum import Enum
import random

class CardSuit(Enum):
    '''
    @title CardSuit
    @desc Enumerates 4 playing card suits 
    '''
    Spades = 0, 
    Diamonds = 1,
    Clubs = 2,
    Hearts = 3
    
class CardValue(Enum): 
    '''
    @title CardValue
    @desc Enumerates 13 distinct cards (per suit)
    '''
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
    '''
    @title Card
    @desc A playing card with suit, value, and numeric (blackjack) value 
    
    @prop suit CardSuit
    @prop value CardValue
    '''
    def __init__(self, suit: CardSuit, value: CardValue):            
        '''
        @title constructor 
        @param suit One of 4 card suits: hearts, diamonds, clubs, spades
        @param value Numeric blackjack value of the card (e.g. 10 for King)
        '''
        self.suit = suit
        self.value = value
        
    # True if card is an ace
    @property 
    def is_ace(self) -> bool: 
        return self.value == CardValue.Ace
        
    @property 
    # True if card is jack, queen, or king
    def is_face_card(self) -> bool: 
        return self.value in [CardValue.Jack, CardValue.Queen, CardValue.King]
    
    @property 
    # Gets the numerical value in blackjack for the card
    def number_value(self) -> int: 
        return _card_numeric_values[self.value]
    
    #TODO: test this
    def equals(self, card) -> bool: 
        '''
        @title equals
        @desc Returns value indicating value equality; cards are equal only if both their 
        suit and numeric value match. 
        @returns True if given card equals this card 
        '''
        return self.suit == card.suit and self.value == card.value 
        
    def __str__(self) -> str:
        return f"{self.suit} {self.value}"

#TODO: (LOW) test this 
def get_card(s: str) -> Card: 
    '''
    @title get_card
    @desc Lets you construct a Card instance with a string, in the form: 
        '<suit><card>' 
    examples: 
        H2 -> 2 of Hearts
        DK -> King of Diamonds 
        SQ -> Queen of Spades 
        CA -> Ace of Clubs 
        HJ -> Jack of Hearts 
        D9 -> Nine of Diamonds 
    @returns Card
    '''
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
    '''
    @title all_card_values 
    @desc Gets all 13 possible card values: 2,3,...9,10,J,Q,K,A
    @returns List of CardValue enum values 
    '''
    return _all_card_values
    
def all_card_suits(): 
    '''
    @title all_card_suits
    @desc Gets all 4 suits as CardSuit enum values
    @returns List of CardSuit enum values
    '''
    return _all_card_suits
    
def card_numeric_values(): 
    '''
    @title card_numeric_values
    @desc Gets all possible numeric values for cards, as a Dictionary of 
        key: CardValue enum value
        value: int 
    @returns Dictionary of CardValue: int
    '''
    return _card_numeric_values