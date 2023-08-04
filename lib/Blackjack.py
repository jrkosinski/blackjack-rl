from lib.Shoe import Shoe
from lib.Hand import Hand 
from math import floor, ceil

class Player: 
    def __init__(self, decision_model): 
        self.hand: Hand = Hand()
        self.decision_model: DecisionModel = decision_model
        self.balance: int = 0
        self.bet: int = 0

    def add_card(self, card: int): 
        self.hand.add_card(card)
        
    def request_bet(self, minimum_bet: int): 
        #TODO: should be determined by decision model
        self.bet = minimum_bet
        
    def request_action(self, dealer, shoe: Shoe, players, player_index: int) -> bool: 
        return self.decision_model.decide_hit(dealer=dealer, shoe=shoe, players=players, player_index=player_index)
        
class Dealer(Player): 
    def __init__(self): 
        super().__init__(DealerDecisionModel())
        
    def take_bets(self, players, minimum_bet: int): 
        for player in players: 
            player.request_bet(minimum_bet)
            if (player.bet < minimum_bet): 
                player.bet = minimum_bet
    
    def deal_hands(self, shoe: Shoe, players): 
        #clear hand 
        self.hand.clear()
        
        #deal a card to players 
        for player in players: 
            player.hand.clear()
            player.add_card(shoe.deal_card())
            
        #deal one to self 
        self.add_card(shoe.deal_card())
        
        #deal a card to players 
        for player in players: 
            player.add_card(shoe.deal_card())
    
    def play_round(self, shoe: Shoe, players): 
        for i in range(len(players)):
            player = players[i]
            
            #let player hit or stand 
            while (player.hand.is_playable): 
                hit = player.request_action(self, shoe, players, i)
                if (hit):
                    player.add_card(shoe.deal_card())
                else: 
                    break

        '''
        At this point, the dealer might only have one card. This is because, to 
        avoid messing up the probabilities in the deck, we don't deal the dealer a 
        'down' card initially. That 'down' card is just considered part of the deck
        as far as proabilities are concerned, and so we just actually keep it in the 
        deck, to simplify calculations. 
        Instead, at the time that the dealer would normally 'flip' the down card, a
        there is no down card to flip, and the dealer just deals himself that card
        from the deck. 
        '''
        if (self.hand.count == 1): 
            #this takes the place of the dealer's 'down card', now showing
            self.add_card(shoe.deal_card())
        
        #now dealer takes a turn 
        while (self.hand.is_playable): 
            hit = self.request_action(self, shoe, players, -1)
            if (hit):
                self.add_card(shoe.deal_card())
            else: 
                break
    
    def assess_winners(self, players): 
        for player in players: 
            if (player.hand.is_over): 
                #player is bust 
                self._player_settle(player, -1)
            elif (player.hand.is_blackjack): 
                #player has natural blackjack
                self._player_settle(player, 1.5)
            else: 
                if (self.hand.is_over): 
                    #dealer bust, and player not 
                    self._player_settle(player, 1)
                else: 
                    diff = player.hand.total - self.hand.total
                    if (diff < 0): 
                        #dealer won on points
                        self._player_settle(player, -1)
                    elif (diff > 0): 
                        #player won on points
                        self._player_settle(player, 1)
                    else: 
                        #push
                        player.bet = 0
    
    def _player_settle(self, player, multiplier): 
        value = int(floor(player.bet * multiplier))
        self.balance -= value
        player.balance += value
        player.bet = 0

class Table: 
    def __init__(self, dealer: Dealer, num_decks: int, minimum_bet: int = 2): 
        self.shoe = Shoe(num_decks)
        self.dealer: Dealer = dealer
        self.players = [] #Player
        self.minimum_bet: int = minimum_bet
        self.min_decks: int = int(ceil(self.shoe.max_deck_count / 2))
    
    def deal_hands(self): 
        self.dealer.take_bets(self.players, self.minimum_bet)
        self.dealer.deal_hands(self.shoe, self.players)
        
    def play_round(self): 
        
        #check if need to top up shoe 
        if (self.shoe.count < self.min_decks * 52): 
            self.shoe.top_up()
        
        #take bets & deal hands 
        self.deal_hands()
        self.dealer.play_round(self.shoe, self.players)
        self.dealer.assess_winners(self.players)

class DecisionModel: 
    def __init__(self): 
        pass

    def decide_hit(self, dealer: Dealer, shoe: Shoe, players, player_index: int): 
        return False
        '''
        What can go into a decision: 
        - dealer's 'up' card 
        - players' showing cards (all cards on table)
        - cards that have already been dealt since last shoe top-up
        - cards in my hand 
        
        Simplified: 
        - complete statistical count of shoe, minus cards dealt and cards showing 
        - card values in my hand 
        - dealer's 'up' card 
        '''
        
    def _get_hand(self, dealer: Dealer, players, player_index: int): 
        if (player_index < 0): 
            return dealer.hand
        return players[player_index].hand
        
class DealerDecisionModel(DecisionModel): 
    def __init__(self): 
        super().__init__()

    def decide_hit(self, dealer: Dealer, shoe: Shoe, players, player_index: int): 
        hand = self._get_hand(dealer, players, player_index)
        
        #always hit on less than 17
        if (hand.total < 17): 
            return True
            
        #hit on soft 17 
        if (hand.total == 17 and hand.card_count(11) > 0): 
            return True
            
        return False