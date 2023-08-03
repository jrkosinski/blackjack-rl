from lib.Shoe import Shoe
from lib.Hand import Hand 
from math import floor

class DealerHand(Hand): 
    def __init__(self): 
        super().__init__()
        
    @property
    def showing(self): 
        if (self.count > 1): 
            return self.cards[1:]
        return []
        
class Player: 
    def __init__(self, decision_model): 
        self.hand: Hand = Hand()
        self.decision_model = decision_model
        self.balance = 0
        self.bet = 0

    def add_card(self, card: int): 
        self.hand.add_card(card)
        
    def request_bet(self, minimum_bet: int): 
        #TODO: should be determined by decision model
        self.bet = minimum_bet
        
class Dealer(Player): 
    def __init__(self): 
        super().__init__(DealerDecisionModel())
        self.hand = DealerHand()
        
    def deal_hands(self, shoe: Shoe, players): 
        #deal a card to players 
        for player in players: 
            player.add_card(shoe.deal_card())
            
        #deal one to self 
        self.add_card(shoe.deal_card())
        
        #deal a card to players 
        for player in players: 
            player.add_card(shoe.deal_card())
            
        #deal one to self 
        self.add_card(shoe.deal_card())
    
    def take_bets(self, players, minimum_bet: int): 
        for player in players: 
            player.request_bet(minimum_bet)
            if (player.bet < minimum_bet): 
                player.bet = minimum_bet
    
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
        self.dealer = dealer
        self.players = []
        self.minimum_bet = minimum_bet
    
    def deal_hands(self): 
        self.dealer.take_bets(self.players, self.minimum_bet)
        self.dealer.deal_hands(self.shoe, self.players)

class DecisionModel: 
    def decide_hit(self, table: Table, player_index: int): 
        return False
        
    def _get_hand(self, table: Table, player_index: int): 
        if (player_index < 0): 
            return table.dealer.hand
        return table.players[player_index].hand
        
class DealerDecisionModel(DecisionModel): 
    def decide_hit(self, table: Table, player_index: int): 
        hand = self._get_hand(table, player_index)
        
        #always hit on less than 17
        if (hand.total < 17): 
            return True
            
        #hit on soft 17 
        if (hand.total == 17 and hand.card_count(11) > 0): 
            return True
            
        return False