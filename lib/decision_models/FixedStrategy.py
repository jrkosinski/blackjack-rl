from lib.Shoe import Shoe
from lib.Hand import Hand 
from lib.Blackjack import Dealer, DecisionModel

class FixedStrategy(DecisionModel): 
    def __init__(self): 
        super().__init__()

    def decide_hit(self, dealer: Dealer, shoe: Shoe, players, player_index: int):
        pass