import random 

from classes.Card import CardSuit
from classes.Card import CardValue
from classes.Card import Card
from classes.Card import get_card
from classes.Shoe import Shoe 

from classes.Player import Player

class Dealer(Player): 
    def __init__(self, balance: int, decision_model, num_decks: int = 1): 
        super().__init__(balance, decision_model)
        self.shoe = Shoe(num_decks)
        
    def deal_self(self, num: int = 1): 
        return self.deal_player(self, num)
            
    def deal_player(self, player: Player, num: int = 1): 
        cards = list()
        
        for i in range (num): 
            card = self.shoe.get_next()
            player.hand.append(card)
            cards.append(card)
            
        return cards if len(cards) > 1 else cards[0]
    
    #TODO: test this 
    def reset_shoe(self): 
        self.shoe.reset()
    
    #TODO: test this 
    def shuffle(self):
        self.shoe.shuffle()
    
    #TODO: can this be removed (it's inherited)
    def decide_hit_or_stand(self, game) -> bool: 
        return self.decision_model.decide_hit_or_stand(self, game)
    
    #TODO: test this 
    def top_up(self) -> int: 
        return self.shoe.top_up()
        
    def load_deck(self, card_names:list()): 
        for c in reversed(card_names): 
            self.shoe.place_on_top(get_card(c))
        
