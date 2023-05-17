import random 

from classes.Card import CardSuit
from classes.Card import CardValue
from classes.Card import Card
from classes.Shoe import Shoe 

from classes.Player import Player
from classes.Dealer import Dealer

from classes.CardCount import CardCount

from classes.Round import RoundOptions
from classes.Round import Round

class Game: 
    '''
    @title Game 
    @desc Context of a game; has a dealer, and rounds. Players are not properties of 
    a game, but to specific Rounds; because through the course of a game, players may 
    come and go. 
    '''
    def __init__(self, dealer: Dealer, verbosity:int = 1): 
        '''
        @title constructor 
        @param dealer The dealer for this game. 
        @param verbosity Verbosity of diagnostic messages (0 for none)
        '''
        self.dealer = dealer
        self.current_round = None
        self.card_count = CardCount(dealer.shoe.num_decks)
        self.verbosity = verbosity
    
    def execute_next_round(self, players, options: RoundOptions = RoundOptions.default()) -> Round: 
        '''
        @title execute_next_round 
        @desc Initiates and executes a new round of play.
        @param players Array of Player instances (players taking part in the round)
        @param options List of blackjack-specific play options for the round
        @returns Round instance representing executed current round 
        '''
        
        #reset hands
        self._reset_hands(players)
        
        self.current_round = Round(self, players, options) 
        
        self._print('')
        self._print('round initiated')
        self._print(f'cards remaining: {self.dealer.shoe.num_cards}')
        
        #check first if shoe needs to be topped up
        if (self.dealer.shoe.num_cards <= (self.dealer.shoe.max_num_cards / 2)): 
            self._print('topping up the shoe')
            added_decks = self.dealer.top_up()  
            self.card_count.add_decks(added_decks)
            self._print(f'cards after top-up: {self.dealer.shoe.num_cards}')
            
        self.current_round.execute_round()
        
        if (self.verbosity > 0):
            if (self.dealer.is_bust): 
                self._print("dealer is bust")
            elif (self.dealer.has_blackjack): 
                self._print("dealer has blackjack")
            elif (self.dealer.has_21): 
                self._print("dealer has 21")
            
            for i in range(len(players)): 
                if (players[i].is_bust): 
                    self._print(f'player {i} is bust')
                elif (players[i].has_blackjack): 
                    self._print("player has blackjack")
                elif (players[i].has_21): 
                    self._print("player has 21")
                    
        self._print(f'dealer balance: {self.dealer.balance}')
        for i in range(len(players)): 
            self._print(f'player {i} balance: {players[i].balance}')
            
        #TODO: card counts not accruing 
        self.card_count.add_counts(self.current_round.card_count)
        
        # print report of card count 
        if (self.verbosity > 1): 
            for i in range (1, 11):
                self._print(f'card value {i}: {self.current_round.card_count.cards_dealt[i]}')
            
        self._print(f'round results: {self.current_round.results}')
        return self.current_round
         
    def reset_cards(self): 
        '''
        @title reset_cards 
        @desc 
        '''
        print('not implemented')
    
    def copy(self): 
        gcopy = Game(self.dealer, 0)
        gcopy.dealer = self.dealer.copy()
        return gcopy
        
    def _reset_hands(self, players): 
        '''
        @title _reset_hands 
        @desc Resets all players' hands (e.g. after a round is completed)
        @param players All players whose hands to reset 
        '''
        self.dealer.reset_hand()
        for i, player in enumerate(players): 
            player.reset_hand()
            
    def _print(self, msg, threshold=1): 
        '''
        @title _print 
        @desc Prints a diagnostic message if verbosity > threshold
        @param msg The message to print (maybe)
        @param threshold If self.verbosity exceeds this value, msg will print
        '''
        if (self.verbosity >= threshold): 
            print(msg)