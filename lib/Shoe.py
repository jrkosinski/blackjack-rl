from math import floor
from random import randint
from lib.Deck import Deck

class Shoe: 
    def __init__(self, num_decks: int): 
        self.cards = []
        self.add_deck(num_decks)
        self.max_deck_count = num_decks
        
    @property
    def count(self): 
        return len(self.cards)
        
    def shuffle(self): 
        cards = []
        while(self.count > 0): 
            r = randint(0, self.count-1)
            cards.append(self.cards[r])
            self.cards.pop(r)
        self.cards = cards
            
    def top_up(self): 
        max_count = 52 * self.max_deck_count
        diff = max_count - self.count
        deck_count = int(floor(diff/52))
        self.add_deck(count=deck_count, shuffle=True)
        
    def deal_card(self) -> int: 
        if (self.count > 0): 
            card = self.cards[0]
            self.cards.pop(0)
            return card
        
        return None
            
    def add_deck(self, count: int = 1, shuffle: bool = True): 
        for i in range(count): 
            deck = Deck()
            self.cards.extend(deck.cards)
        
        if (shuffle): 
            self.shuffle()
            