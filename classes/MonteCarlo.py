from classes.Player import Player
from classes.Game import Game
from classes.Card import Card
from classes.DecisionModel import DecisionModel
import random

def _decide_default_minimum_bet(player: Player, game: Game) -> int: 
    return game.current_round.options.minimum_bet if (game.current_round.options.minimum_bet <= player.balance) else player.balance


class HandDefinition: 
    def __init__(self): 
        self.num_cards = 0
        self.dealer_showing = 0 #TODO: (MED) dealer_showing is not needed I think 
        self.num_aces = 0
        self.has_eleven = False
        self.base_total = 0
        
    @property 
    def hand_value(self): 
        total = self.base_total + self.num_aces
        if (self.has_eleven): 
            total += 10
        return total
        
    @property 
    def is_blackjack(self): 
        return self.num_cards == 2 and self.hand_value == 21
        
    @property 
    def is_21(self): 
        return self.num_cards == 2 and self.hand_value == 21
        
    @property 
    def is_over(self): 
        return self.hand_value > 21
        
    def read_hand(self, player: Player, game: Game): 
        self.num_cards = player.num_cards
        self.dealer_showing = game.dealer.showing.numeric_value
        self.num_aces = 0
        self.has_eleven = False
        self.base_total = 0
        
        for i, c in enumerate(player.hand): 
            if (c.is_ace): 
                self.num_aces+= 1
            else: 
                self.base_total += c.numeric_value
    
    #TODO: this isn't used I don't believe
    def add_card(self, card: Card): 
        copy = HandDefinition()
        copy.num_cards = self.num_cards + 1
        copy.dealer_showing = self.dealer_showing
        copy.num_aces = self.num_aces
        copy.has_eleven = self.has_eleven
        
        if (card.is_ace): 
            copy.num_aces += 1
        
        return copy
        
class DecisionDefinition: 
    def __init__(self, hit: bool, use_eleven: bool): 
        self.hit = hit
        self.use_eleven = use_eleven
        self.expected_return = 0
        
class DecisionRoot: 
    def __init__(self, player: Player, game: Game): 
        self.hand_def = HandDefinition()
        self.hand_def.read_hand(player, game)
        self.game = game
        self.player = player
        
        #0: stand, no eleven (or no aces)
        #1: hit, no eleven (or no aces) 
        #2: stand, ace is eleven 
        #3: hit, ace is eleven
        self.decisions = [0,0,0,0]
        
    def calculate_best_path(self) -> DecisionDefinition: 
        self.hand_def.has_eleven = False
        self.decisions[0] = self._do_calculate(False)
        self.decisions[1] = self._do_calculate(True)
        
        if (self.hand_def.num_aces > 0):
            self.hand_def.has_eleven = True
            self.decisions[2] = self._do_calculate(False)
            self.decisions[3] = self._do_calculate(True)
            
        #find which is the best decision (highest expected return), and return it 
        max_index = 0
        for i in range(1, len(self.decisions)): 
            if (self.decisions[i] > self.decisions[i-1]): 
                max_index = i
                
        print(f'best decision is {max_index} with expected return of {self.decisions[max_index]}')
        return self.decision_from_index(max_index)
        
    def decision_from_index(self, index: int) -> DecisionDefinition: 
        hit = False
        use_eleven = False
        if (index > 1): 
            use_eleven = True
        if (index % 2 != 0): 
            hit = True 
        return DecisionDefinition(hit, use_eleven)
            
    def _do_calculate(self, hit: bool) -> float: 
        count = 100
        sum = 0
        for i in range(count): 
            #print('iteration ', i)
            sum += self._simulate_turns(hit)
            #print()
        
        #calculate the expected returns from all attempts
        #print(f'{sum}/{count} = {sum/count}')
        return sum/count
        
    def _simulate_turns(self, hit: bool) -> int: 
        #make a copy of game
        #TODO: (HIGH) do this without making deep copies 
        game = self.game.copy()
        player = self.player.copy()
        game.dealer.shuffle()
        
        # do player's turn
        if (hit): 
            game.dealer.deal_player(player)
            if (player.is_bust): 
                #bust
                return -2 #TODO: use actual bet size 
            else: 
                #TODO: (HIGH) go into another simulation dealer_showing
                while not player.is_bust and not player.has_21: 
                    _hit = player.decide_hit_or_stand(game)
                    if (_hit): 
                        game.dealer.deal_player(player)
                    else: 
                        break
        
        # do dealer's turn
        #TODO: (HIGH) use dealer's decision model here 
        while (game.dealer.hand_total < 16 and not game.dealer.is_bust): 
            game.dealer.deal_self()
            
        if (game.dealer.is_bust): 
            return 2
        
        if (player.hand_total > game.dealer.hand_total): 
            return 2
            
        return 0
              
class OutcomeTree: 
    def __init__(self, player: Player, game: Game): 
        self.root = DecisionRoot(player, game)
        
    def decide(self): 
        decision = self.root.calculate_best_path()
        return decision
            
    
class MonteCarloDecisionModel(DecisionModel): 
    '''
    @title MonteCarloDecisionModel
    @desc A decision model that makes hit/stand decisions after running Monte Carlo 
    simulations to determine the best course of action based on expected outcomes. 
    '''
    
    def decide_bet_amount(self, player: Player, game: Game) -> int: 
        return _decide_default_minimum_bet(player, game)
        
    def decide_hit_or_stand(self, player: Player, game: Game = None) -> bool: 
        tree = OutcomeTree(player, game)
        decision = tree.decide()
        return decision.hit
    