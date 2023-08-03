from lib.Shoe import Shoe
from lib.Hand import Hand 
from lib.Blackjack import Dealer, DecisionModel
from random import randint

class RandomStrategy(DecisionModel): 
    def __init__(self): 
        super().__init__()

    def decide_hit(self, dealer: Dealer, shoe: Shoe, players, player_index: int):
        n = randint(0, 1)
        return True if n > 0 else False