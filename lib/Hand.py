
from typing import Any


class Hand: 
    '''
    @title Hand
    
    @desc Encapsulates any blackjack hand of cards, including the dealer's hand.
    '''
    def __init__(self):
        self.cards = []

    def __getitem__(self, index: int) -> int:
        return self.cards[index]
        
    @property 
    def total(self) -> int: 
        return sum(self.cards)
        
    @property 
    def count(self) -> int: 
        return len(self.cards)
        
    @property 
    def is_over(self) -> bool: 
        return self.total > 21
        
    @property 
    def is_under(self) -> bool: 
        return self.total < 21
        
    @property 
    def is_natural(self) -> bool:
        return self.total == 21 and self.count == 2
        
    @property 
    def is_blackjack(self) -> bool:
        return self.is_natural
        
    @property 
    def is_21(self) -> bool:
        return self.total == 21
        
    @property 
    def is_playable(self) -> bool:
        return self.total < 21
        
    @property 
    def ace_count(self) -> int: 
        count = 0
        for c in self.cards: 
            if c == 11 or c == 1: 
                count += 1
        return count 
        
    @property 
    def soft_ace_count(self) -> int: 
        return self.card_count(11) 
    
    @property 
    def is_soft(self) -> bool: 
        return self.card_count(11) > 0

    def add_card(self, card: int): 
        self.cards.append(card)
        
        #if over, can some aces be converted to 1? 
        if (self.is_over and self.ace_count > 0): 
            for i in range(len(self.cards)): 
                if (self.cards[i] == 11): 
                    self.cards[i] = 1
                    if (not self.is_over): 
                        break
    
    def card_count(self, card: int): 
        count =0
        for c in self.cards:
            if (card == c): 
                count += 1
        return count 
            
    def clear(self): 
        self.cards = []
        