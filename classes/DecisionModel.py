from classes.Player import Player
from classes.Game import Game
import random

class DecisionModel: 
    def decide_bet_amount(self, player: Player, game: Game = None) -> int: 
        return 0
    
    def decide_hit_or_stand(self, player: Player, game: Game = None) -> bool: 
        return False
    
#TODO: test this 
class BaselineDecisionModel(DecisionModel): 
    def decide_bet_amount(self, player: Player, game: Game) -> int: 
        return game.current_round.options.minimum_bet if (game.current_round.options.minimum_bet <= player.balance) else player.balance
    
    def decide_hit_or_stand(self, player: Player, game: Game = None) -> bool: 
        total = player.hand_total
        if (total < 21): 
            if (total <= 16): 
                return True 
        return False

#TODO: test this 
class DealerDecisionModel(DecisionModel): 
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
    def decide_bet_amount(self, player: Player, game: Game) -> int: 
        return game.current_round.options.minimum_bet if (game.current_round.options.minimum_bet <= player.balance) else player.balance
    
    def decide_hit_or_stand(self, player: Player, game: Game = None) -> bool: 
        total = player.hand_total
        if (total < 21): 
            if (total <= 16): 
                return False 
        return True

class RandomDecisionModel(DecisionModel): 
    def decide_bet_amount(self, player: Player, game: Game) -> int: 
        return game.current_round.options.minimum_bet if (game.current_round.options.minimum_bet <= player.balance) else player.balance
    
    def decide_hit_or_stand(self, player: Player, game: Game = None) -> bool: 
        return random.randint(0, 1) == 0
    