from classes.Player import Player
from classes.Game import Round

class DecisionModel: 
    def decide_bet_amount(self, player: Player, round: Round) -> int: 
        return 0
    
    def decide_hit_or_stand(self, player: Player, round: Round) -> bool: 
        return False
    
class BaselineDecisionModel(DecisionModel): 
    def decide_bet_amount(self, player: Player, round: Round) -> int: 
        return round.options.minimum_bet if (round.options.minimum_bet <= player.balance) else player.balance
    
    def decide_hit_or_stand(self, player: Player, round: Round) -> bool: 
        total = player.hand_total
        if (total < 21): 
            if (total <= 16): 
                return True 
        return False

class DealerDecisionModel(DecisionModel): 
    def decide_bet_amount(self, player: Player, round: Round) -> int: 
        return 0
    
    def decide_hit_or_stand(self, player: Player, round: Round) -> bool: 
        total = player.hand_total
        if (total < 21): 
            #dealer must hit on soft 17
            if (total == 17 and player.has_ace): 
                return True
            elif (total <= 16): 
                return True 
        return False

class RainManDecisionModel(DecisionModel): 
    def decide_bet_amount(self, player: Player, round: Round) -> int: 
        return round.options.minimum_bet if (round.options.minimum_bet <= player.balance) else player.balance
    
    def decide_hit_or_stand(self, player: Player, round: Round) -> bool: 
        return False