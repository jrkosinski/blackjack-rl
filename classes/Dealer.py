import random 

from classes.Card import CardSuit
from classes.Card import CardValue
from classes.Card import Card
from classes.Deck import Deck 

from classes.Player import Player

class Dealer(Player): 
    def __init__(self, balance: int, num_decks: int = 1): 
        super().__init__(balance)
        self.deck = Deck(num_decks)
        
    def deal_self(self, num: int = 1): 
        return self.deal_player(self, num)
            
    def deal_player(self, player: Player, num: int = 1): 
        cards = list()
        
        for i in range (num): 
            card = self.deck.get_next()
            player.hand.append(card)
            cards.append(card)
            
        return cards if len(cards) > 1 else cards[0]
    
    def reset_deck(self): 
        self.deck.reset()
    
    def shuffle(self):
        self.deck.shuffle()
    
    #TODO: can this be removed (it's inherited)
    def decide_hit_or_stand(self, round) -> bool: 
        return self.decision_model.decide_hit_or_stand(self, round)
    
    def top_up_deck(self): 
        self.deck.top_up_deck() 
        
