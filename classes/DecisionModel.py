from classes.Player import Player
from classes.Game import Game
import random

def _decide_default_minimum_bet(player: Player, game: Game) -> int: 
    return game.current_round.options.minimum_bet if (game.current_round.options.minimum_bet <= player.balance) else player.balance

class DecisionModel: 
    '''
    @title DecisionModel
    @desc Encapsulates logic for making gameplay decisions for a player, during gameplay.
    '''
    def decide_bet_amount(self, player: Player, game: Game = None) -> int: 
        '''
        @title decide_bet_amount
        @desc Decides how much the player should bet on the current round.
        @param player The player for whom to make a decision.
        @param game Game context. 
        @returns A bet amount (int)
        '''
        return 0
    
    def decide_hit_or_stand(self, player: Player, game: Game = None) -> bool: 
        '''
        @title decide_hit_or_stand
        @desc Decides whether the player should hit or stand, based on game context and 
        (presumably) player's current cards. 
        @param player The player for whom to make a decision.
        @param game Game context. 
        @returns A decision: True=hit, False=stand (stick)
        '''
        return False
    
#TODO: test this 
class BaselineDecisionModel(DecisionModel): 
    '''
    @title BaselineDecisionModel
    @desc To be used as a baseline for performance testing, this model makes the same 
    decisions as a Vegas dealer would (e.g. hit on 16, stick on 17, hit on soft 17)
    '''
    
    def __init__(self, hit_soft_17:bool = True): 
        self.hit_soft_17 = hit_soft_17
        
    def decide_bet_amount(self, player: Player, game: Game) -> int: 
        return _decide_default_minimum_bet(player, game)
        
    def decide_hit_or_stand(self, player: Player, game: Game = None) -> bool: 
        total = player.hand_total
        if (total < 21): 
            if (self.hit_soft_17): 
                if (total == 17 and player.has_ace): 
                    return False
            if (total <= 16): 
                return True 
        return False

#TODO: test this 
class DealerDecisionModel(DecisionModel): 
    '''
    @title DealerDecisionModel
    @desc Follows Vegas dealer rules for deciding when to hit/stick. 
    '''
    
    def decide_hit_or_stand(self, player: Player, game: Game = None) -> bool: 
        total = player.hand_total
        if (total < 21): 
            #dealer must hit on soft 17
            if (total == 17 and player.has_ace): 
                return True
            elif (total <= 16): 
                return True 
        return False

#TODO: test this 
class RainManDecisionModel(DecisionModel): 
    '''
    @title RainManDecisionModel
    @desc Calculates probabilities of certain cards being dealt, based on perfect 
    card counts (can be taken from Game context object)
    '''
    
    def decide_bet_amount(self, player: Player, game: Game) -> int: 
        return _decide_default_minimum_bet(player, game)
        
    def decide_hit_or_stand(self, player: Player, game: Game) -> bool: 
        total = player.hand_total
        if (total < 21): 
            diff_21 = 21 - total
            prob_over_21 = game.card_count.probability_of_n_or_over(diff_21 + 1)
            prob_improvement = game.card_count.probability_of_n_or_under(diff_21)
            
            #print(prob_improvement)
            return (prob_improvement > 0.5 and prob_over_21 < 0.3)
            
        return False

class BadDecisionModel(DecisionModel): 
    '''
    @title BadDecisionModel
    @desc A decision model that is purposely very bad, will result in mostly losses.
    To be used as a benchmark in testing. 
    '''
    
    def decide_bet_amount(self, player: Player, game: Game) -> int: 
        return _decide_default_minimum_bet(player, game)
    
    def decide_hit_or_stand(self, player: Player, game: Game = None) -> bool: 
        total = player.hand_total
        if (total < 21): 
            if (total <= 16): 
                return False 
        return True

class RandomDecisionModel(DecisionModel): 
    '''
    @title RandomDecisionModel
    @desc A decision model that makes random decisions regarding hit/stick. 
    '''
    
    def decide_bet_amount(self, player: Player, game: Game) -> int: 
        return _decide_default_minimum_bet(player, game)
    
    def decide_hit_or_stand(self, player: Player, game: Game = None) -> bool: 
        return random.randint(0, 1) == 0
    
class MonteCarloDecisionInput: 
    '''
    @title MonteCarloDecisionInput
    @desc All available inputs needed to make a hit/stand decision. 
    
    @prop hand_total The total value of all non-ace cards in hand 
    @prop num_aces The number of aces held 
    @prop dealer_showing The numeric value of the dealer's showing card. A '1' is used 
    to denote an Ace (for the dealer)
    '''
    def __init__(self, hand_total: int = 0, num_aces: int = 0, dealer_showing: int = 0): 
        self.hand_total = hand_total
        self.num_aces = num_aces
        self.dealer_showing = dealer_showing
        
    def to_string(self): 
        return f'{self_hand_total}:{self.num_aces}:{self.dealer_showing}'
        
    def read_from_hands(game: Game, player: Player): 
        hand_total = 0
        num_aces = 0
        
        for i, c in enumerate(player.hand): 
            if (c.is_ace): 
                num_aces += 1
            else:
                hand_total += c.numeric_value
        
        self.dealer_showing = game.dealer.hand[0].numeric_value
        self.hand_total = hand_total
        self.num_aces = num_aces
    
class MonteCarloResult: 
    def __init__(self, hit_expected_return: float = 0, stand_expected_return: float = 0): 
        self.hit_expected_return = hit_expected_return
        self.stand_expected_return = stand_expected_return
        
class MonteCarloLookup: 
    def __init__(self): 
        self.lookup_table = {}
    
    def get_or_add_result(self, game: Game, player: Player) -> int: 
        result = self.get_result(game, player)
        if (result < 0):
            result = self.add_result(game, player)
        
        return result
    
    def get_result(self, game: Game, player: Player) -> int: 
        input = MonteCarloDecisionInput(game, player)
        result = self.lookup_table[input.to_string()]
        
        if (result is None): 
            return -1
        
        return 1 if result.hit_expected_return > result.stand_expected_return else 0
        
    def add_result(self, game: Game, player: Player) -> int: 
        input = MonteCarloDecisionInput(game, player)
        
        # calculate expected return after hit 
        
    def calculate_expected_return(self, game: Game, player: Player): 
        hands = calculate_player_possible_hands(self, MonteCarloDecisionInput(game, player))
        for i, h in enumerate(hands): 
            if (h == 21): # the best case 
                return 1
    
    def calculate_player_possible_hands(self, input: MonteCarloDecisionInput): 
        base_total = input.hand_total 
        if (input.num_aces == 0): 
            output = [base_total]
        else:   
            #at most, only one ace can be 11 (because 2 11s is over 21)
            
            output.append(base_total + input.num_aces) #all aces are 1 
            
            if (base_total + (input.num_aces -1) + 11 <= 21):   
                output.append(base_total + (input.num_aces -1) + 11) #one ace is 11
            
            return output
        
        
class MonteCarloDecisionModel(DecisionModel): 
    '''
    @title MonteCarloDecisionModel
    @desc A decision model that makes hit/stand decisions after running Monte Carlo 
    simulations to determine the best course of action based on expected outcomes. 
    '''
    
    def __init__(self): 
        self.lookup = MonteCarloLookup()
    
    def decide_bet_amount(self, player: Player, game: Game) -> int: 
        return _decide_default_minimum_bet(player, game)
        
    def decide_hit_or_stand(self, player: Player, game: Game = None) -> bool: 
        return self.lookup.get_or_add_result(game, player)
    