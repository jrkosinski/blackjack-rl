import random 

from classes.Card import CardSuit
from classes.Card import CardValue
from classes.Card import Card
from classes.Deck import Deck 

class Player: 
    def __init__(self, balance: int, decision_model = None):  #TODO: should not allow None 
        self.hand = list()
        self.balance = balance 
        self.bet = 0
        self.decision_model = decision_model
    
    @property
    def has_ace(self) -> bool: 
        for i in range(len(self.hand)): 
            if (self.hand[i].is_ace): 
                return True
        return False
        
    @property
    def has_blackjack(self) -> bool: 
        has_ace = False
        has_ten = False
        for i in range(len(self.hand)): 
            if self.hand[i].is_ace: 
                has_ace = True 
            if (self.hand[i].number_value == 10): 
                has_ten = True
        return has_ten and has_ace
        
    @property
    def has_21(self) -> bool: 
        return self.hand_total == 21
        
    @property
    def is_bust(self) -> bool:
        return self.hand_total > 21
    
    @property
    def hand_total(self) -> int: 
        total = 0
        aces = list()
        for i in range(len(self.hand)): 
            card = self.hand[i]
            if (card.is_ace): 
                aces.append(card)
            else: 
                total += card.number_value
                
        for i in range(len(aces)):
            if (total + 11 > 21): 
                total += 1
            else: 
                total += 11
            
        return total
    
    def decide_bet_amount(self, game) -> int: 
        return self.decision_model.decide_bet_amount(self, game)
    
    def decide_hit_or_stand(self, game) -> bool: 
        return self.decision_model.decide_hit_or_stand(self, game)
    
    def reset_hand(self): 
        self.hand = list()
    
