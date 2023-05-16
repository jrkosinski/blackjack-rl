from classes.Player import Player
from classes.Game import Game
import random

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
        return game.current_round.options.minimum_bet if (game.current_round.options.minimum_bet <= player.balance) else player.balance
    
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
        return game.current_round.options.minimum_bet if (game.current_round.options.minimum_bet <= player.balance) else player.balance
    
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
        return game.current_round.options.minimum_bet if (game.current_round.options.minimum_bet <= player.balance) else player.balance
    
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
        return game.current_round.options.minimum_bet if (game.current_round.options.minimum_bet <= player.balance) else player.balance
    
    def decide_hit_or_stand(self, player: Player, game: Game = None) -> bool: 
        return random.randint(0, 1) == 0
    