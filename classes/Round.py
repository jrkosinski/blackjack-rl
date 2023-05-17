import random 

from classes.Card import CardSuit
from classes.Card import CardValue
from classes.Card import Card
from classes.Shoe import Shoe 

from classes.CardCount import CardCount

from classes.Player import Player
from classes.Dealer import Dealer

class RoundOptions: 
    def __init__(self): 
        self.blackjack_payout = 1.5
        self.dealer_hits_soft_17 = False
        self.minimum_bet = 2
        
    @staticmethod
    def default(): 
        return RoundOptions()
    
class Round: 
    '''
    @title Round 
    @desc One round of play has the following steps: 
     - Dealer requests bets 
     - All players except the dealer place bets 
     - Dealer deals all cards to players & self 
     - All players take their turns, deciding to hit or stick based on their decision models 
     - The dealer takes his turn (based on his decision model) 
     - Winnings are paid out and losing bets taken by dealer 
    '''
    def __init__(self, game, players, options: RoundOptions.default()): 
        '''
        @title constructor 
        @param game The game context (the game in which the round takes place)
        @param players Array of Player instances (players taking part in this round)
        @param options Struct of blackjack-specific options 
        '''
        self.winner = None
        self.options = options
        self.players = players
        self.bets = list()
        self.game = game
        for i in range(len(players)): 
            self.bets.append(0)
            
        self.card_count = CardCount(self.game.dealer.shoe.num_decks)
            
    def execute_round(self): 
        '''
        @title execute_round
        @desc Executes the steps to make a complete round, in the right order 
        '''
        # request bets
        self.request_bets()
            
        # dealing 
        self.deal_hands()
        
        # player & dealer turns
        self.do_turns()
        
        # finish round 
        self.finish_round()
        
    def request_bets(self): 
        '''
        @title request_bets
        @desc Requests each player to choose a bet amount, then takes that amount from 
        each player's balance (to be used in the round, and possibly returned at the 
        end of the round)
        '''
        for i, player in enumerate(self.players):
            bet = player.decide_bet_amount(self.game)
            if (bet > 0): 
                self.bets[i] = bet
                player.balance -= bet
            else: 
                raise Exception(f"Player {i} does not have enough for the minimum bet")
        
    def deal_hands(self): 
        '''
        @title deal_hands
        @desc Causes the dealer to deal his own hand, then deal to each of the players.
        '''
        # deal to self 
        self.card_count.append(self.game.dealer.deal_self())
        self.card_count.append(self.game.dealer.deal_self())
        
        # check for blackjack 
        if (not self.game.dealer.has_blackjack): 
            # deal to players
            for n in range (2): 
                for i, player in enumerate(self.players):
                    self.card_count.append(self.game.dealer.deal_player(player))
                    
    def do_turns(self):
        '''
        @title do_turns
        @desc Causes each player to take his turn, then the dealer to take his turns. 
        '''
        if (not self.game.dealer.has_blackjack): 

            # each player's turn 
            self.do_player_turns()

            # dealer's turn
            self.do_dealer_turn()
                
    def do_player_turns(self): 
        '''
        @title do_player_turns
        @desc Causes each player to take his turn to play. 
        '''
        for i, player in enumerate(self.players):
            #each player must take action 
            while not player.is_bust and not player.has_21: 
                hit = player.decide_hit_or_stand(self.game)
                if (hit): 
                    self.card_count.append(self.game.dealer.deal_player(player))
                else: 
                    break
    
    def do_dealer_turn(self): 
        '''
        @title do_dealer_turn
        @desc Causes the dealer to execute his own turn. 
        '''
        #TODO: (HIGH) use dealer's decision model here 
        while (self.game.dealer.hand_total < 16 and not self.game.dealer.is_bust): 
            self.card_count.append(self.game.dealer.deal_self())
          
    def finish_round(self): 
        '''
        @title finish_round
        @desc Decides who won and who lost, and causes winners to be paid and losers 
        to lose their bets (lost bets go to the dealer's balance)
        '''
        self.results = list()
        for i, player in enumerate(self.players):
            if (player.is_bust):
                self.results.append(-1)
            else: 
                if (self.game.dealer.is_bust): 
                    self.results.append(1)
                else: 
                    if (player.hand_total > self.game.dealer.hand_total):
                        self.results.append(1)
                    elif (player.hand_total == self.game.dealer.hand_total):  
                        self.results.append(0)
                    else: 
                        self.results.append(-1)
        
        self.pay_winners()
                
    def pay_winners(self): 
        '''
        @title pay_winners
        @desc Based on results of the round, losers' bets go to the dealer's balance, 
        and winners get their original bets back plus winnings from the dealer's balance. 
        (Or if it's a push, a player gets his original bet back only)
        '''
        for i, player in enumerate(self.players):
            if (self.results[i] > 0): 
                payout = self.bets[i]
                
                #payout is more, for blackjack
                if (player.has_blackjack):
                    payout *= self.options.blackjack_payout
                    
                #give payout
                player.balance += payout
                self.game.dealer.balance -= payout
                
                #give back original bet 
                player.balance += self.bets[i]
                
            elif (self.results[i] < 0): 
                #dealer collects player's bet
                self.game.dealer.balance += self.bets[i]
            
            #push: return bet to player
            else: 
                player.balance += self.bets[i]
                
            #reset bet
            self.bets[i] = 0
                
          