import random 

from classes.Card import CardSuit
from classes.Card import CardValue
from classes.Card import Card
from classes.Shoe import Shoe 

class Player: 
    '''
    @title Player 
    @desc A blackjack player; owns a hand and is responsible for its own decisions 
    regarding that hand.
    '''
    def __init__(self, balance: int, decision_model = None):  #TODO: should not allow None 
        '''
        @title constructor
        @param balance Initial finite money balance (int)
        @param decision_model Required; controls how the player decides whether to hit or 
        stick per turn, and how much to bet (any decisions to make during gameplay)
        '''
        self.hand = list()
        self.balance = balance 
        self.bet = 0
        self.decision_model = decision_model
    
    # True if the player's hand contains at least one ace 
    @property
    def has_ace(self) -> bool: 
        for i in range(len(self.hand)): 
            if (self.hand[i].is_ace): 
                return True
        return False
        
    # True if the player has a natural (blackjack with two cards only, must include one ace)
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
    
    # True if the player's hand equals a total of exactly 21 (not under or over)
    @property
    def has_21(self) -> bool: 
        return self.hand_total == 21
        
    # True if the player's hand equals a value greater than 21 
    @property
    def is_bust(self) -> bool:
        return self.hand_total > 21
    
    # Gets the sum numeric total value of the player's current hand 
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
        '''
        @title decide_bet_amount
        @desc Calls the player's decision model to determine how much to bet at the 
        beginning of the turn. 
        @param game The game context 
        @returns An amount to bet
        '''
        return self.decision_model.decide_bet_amount(self, game)
    
    def decide_hit_or_stand(self, game) -> bool: 
        '''
        @title decide_hit_or_stand
        @desc Calls the player's decision model to determine whether to hit or stick (stand)
        on the current turn. 
        @param game The game context 
        @returns True for hit, False for stand (stick)
        '''
        return self.decision_model.decide_hit_or_stand(self, game)
    
    def reset_hand(self): 
        '''
        @title reset_hand
        @desc Removes all cards from the player's hand. 
        '''
        self.hand = list()
    
