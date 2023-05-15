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
    def __init__(self, game, players, options: RoundOptions.default()): 
        self.winner = None
        self.options = options
        self.players = players
        self.bets = list()
        self.game = game
        for i in range(len(players)): 
            self.bets.append(0)
            
        self.card_count = CardCount(self.game.dealer.shoe.num_decks)
            
    def execute_round(self): 
        # request bets
        self.request_bets()
            
        # dealing 
        self.deal_hands()
        
        # player & dealer turns
        self.do_turns()
        
        # finish game 
        self.finish_game()
        
    def request_bets(self): 
        for i, player in enumerate(self.players):
            bet = player.decide_bet_amount(self.game)
            if (bet > 0): 
                self.bets[i] = bet
                player.balance -= bet
            else: 
                raise Exception(f"Player {i} does not have enough for the minimum bet")
        
    def deal_hands(self): 
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
        if (not self.game.dealer.has_blackjack): 

            # each player's turn 
            self.do_player_turns()

            # dealer's turn
            self.do_dealer_turn()
                
    def do_player_turns(self): 
        for i, player in enumerate(self.players):
            #each player must take action 
            self.do_player_turn(player)
            
    def do_player_turn(self, player: Player): 
        while not player.is_bust and not player.has_21: 
            action = player.decide_hit_or_stand(self.game)
            if (action): 
                self.card_count.append(self.game.dealer.deal_player(player))
            else: 
                break
    
    def do_dealer_turn(self): 
        while (self.game.dealer.hand_total < 16 and not self.game.dealer.is_bust): 
            self.card_count.append(self.game.dealer.deal_self())
          
    def finish_game(self): 
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
        for i, player in enumerate(self.players):
            if (self.results[i] > 0): 
                payout = self.bets[i]
                
                #payout is more for blackjack
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
                
          