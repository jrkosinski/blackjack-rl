import random 

from classes.Card import CardSuit
from classes.Card import CardValue
from classes.Card import Card
from classes.Deck import Deck 

from classes.Player import Player
from classes.Dealer import Dealer

from classes.CardCount import CardCount

from classes.Round import RoundOptions
from classes.Round import Round

class Game: 
    def __init__(self, dealer: Dealer, verbose:int = 1): 
        self.dealer = dealer
        self.current_round = None
        self.card_count = CardCount(dealer.deck.num_decks)
        self.verbose = verbose
    
    def execute_next_round(self, players, options: RoundOptions = RoundOptions.default()) -> Round: 
        self.current_round = Round(self, players, options) 
        
        self._print('')
        self._print('round initiated')
        self._print(f'cards remaining: {self.dealer.deck.num_cards}')
        
        #check first if deck needs to be topped up
        if (self.dealer.deck.num_cards <= (self.dealer.deck.max_num_cards / 2)): 
            self._print('topping up the deck')
            self.dealer.top_up_deck()  #TODO: this affects card count
            self._print(f'cards after top-up: {self.dealer.deck.num_cards}')
            
        self.current_round.execute_round()
        
        self._print(f'dealer balance: {self.dealer.balance}')
        for i in range(len(players)): 
            self._print(f'player {i} balance: {players[i].balance}')
            
        #TODO: card counts not accruing 
        self.card_count.add_counts(self.current_round.card_count)
        
        # print report of card count 
        for i in range (1, 11):
            self._print(f'card value {i}: {self.current_round.card_count.cards_dealt[i]}')
            
        self._print(f'round results: {self.current_round.results}')
        return self.current_round
         
    def reset_cards(self): 
        print('d')
        
    def _print(self, msg, threshold=1): 
        if (self.verbose >= threshold): 
            print(msg)