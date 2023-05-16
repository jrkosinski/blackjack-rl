import random 

from classes.Card import CardSuit
from classes.Card import CardValue
from classes.Card import Card
from classes.Card import get_card
from classes.Shoe import Shoe 

from classes.Player import Player

class Dealer(Player): 
    '''
    @title Dealer
    @desc Special type of player who deals the hands (but also has a hand and in some ways, 
    behaves as a player.
    
    @prop shoe Shoe 
    '''
    def __init__(self, balance: int, decision_model, num_decks: int = 1): 
        '''
        @title constructor
        @param balance Initial finite money balance (int)
        @param decision_model Required; controls how the dealer decides whether to hit or 
        stick per turn 
        '''
        super().__init__(balance: int, decision_model)
        self.shoe = Shoe(num_decks)
        
    def deal_self(self, num: int = 1): 
        '''
        @title constructor
        @param balance Initial finite money balance (int)
        @param decision_model Required; controls how the dealer decides whether to hit or 
        stick per turn 
        '''
        return self.deal_player(self, num)
            
    def deal_player(self, player: Player, num_cards: int = 1): 
        '''
        @title deal_player 
        @desc Deals a given number of cards to a given player 
        @param player The player to whom to deal
        @param num_cards The number of cards to deal (default 1)
        @returns The card dealt, if num_cards is 1; otherwise, an array of cards dealt
        in the order in which they were dealt. 
        '''
        cards = list()
        
        for i in range (num_cards): 
            card = self.shoe.get_next()
            player.hand.append(card)
            cards.append(card)
            
        return cards if len(cards) > 1 else cards[0]
    
    #TODO: test this 
    def reset_shoe(self): 
        '''
        @title reset_shoe 
        @desc Sets the shoe back to its original state (including initial card count), 
        and reshuffles.
        '''
        self.shoe.reset()
    
    #TODO: test this 
    def shuffle(self):
        '''
        @title shuffle 
        @desc Shuffles (randomizes) the remaining cards currently in the shoe
        '''
        self.shoe.shuffle()
    
    #TODO: test this 
    def top_up(self) -> int: 
        '''
        @title top_up 
        @desc Tops up the Shoe (see Shoe.top_up)
        @returns The number of decks added to top up the shoe
        '''
        return self.shoe.top_up()
        
    def load_deck(self, card_names:list()): 
        '''
        @title load_deck 
        @param card_names List of strings in the form '<suit><card>', e.g. 'HK' (King
        of Hearts), indicating what cards to place on top (and in what order)
        @desc Moves specific cards to the front of the deck; can be used for testing 
        (e.g. forcing specific hands to be dealt, in order to test the outcome)
        '''
        for c in reversed(card_names): 
            self.shoe.place_on_top(get_card(c))
        
