import random

from classes.Card import Card
from classes.Card import CardSuit
from classes.Card import CardValue
from classes.Card import all_card_values

from classes.CardCount import CardCount

class Deck: 
    def __init__(self, num_decks = 1): 
        self.cards = list()
        self.num_decks = num_decks
        self.reset()
            
    # Gets the number of cards remaining in the deck 
    @property
    def num_cards(self) -> int: 
        return len(self.cards)
        
    @property 
    def max_num_cards(self) -> int: 
        return self.num_decks * 52
        
    def reset(self): 
        """Returns all dealt cards to the deck, and reshuffles the deck.

        The number of cards in the deck will return to what it was originally.
        """
        self.cards = list()
        self.top_up_deck()
            
    def shuffle(self): 
        """Randomizes the positions of all remaining cards in the deck.
        """
        cards = [None] * self.num_cards
        indices = random.sample(range(self.num_cards), self.num_cards)
        
        for i in range(len(indices)): 
            cards[indices[i]] = self.cards[i]
        self.cards = cards
    
    def top_up_deck(self, num_decks=1): 
        while(self.num_cards + 52 <= self.max_num_cards): 
            self._add_deck()
            
        self.shuffle()
    
    def _add_deck(self): 
        suits = [CardSuit.Spades, CardSuit.Hearts, CardSuit.Clubs, CardSuit.Diamonds]
        
        for i in range(len(suits)): 
            cards = self._get_all_of_suit(suits[i])
            for n in range(len(cards)): 
                self.cards.append(cards[n])
        
    def get_next(self, count=1): 
        """Gets the next n cards from the deck, returns them, and removes them from the deck.
        
        If the count is 1 (the default), then the single card will not be returned as a list, but 
        as a single Card instance. Otherwise, the function returns a list of Cards. 
        
        Parameters
        count: int, optional 
        
        Returns
        A single Card instance or a list of Card instances 
        """
        if (count > self.num_cards): 
            raise Exception("Number of cards to get is greater than number of cards available")
        output = list()
        for i in range(count): 
            output.append(self.cards[0])
            self.cards.pop(0)
        
        if (count == 1): 
            return output[0]
        return output
        
    #TODO: should be global in Card
    def _get_all_of_suit(self, suit: CardSuit) -> list: 
        output = list()
        card_values = all_card_values()
        for i in range(len(card_values)): 
            output.append(Card(suit, card_values[i]))
        return output