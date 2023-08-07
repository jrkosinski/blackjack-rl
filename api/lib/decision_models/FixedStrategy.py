from ..Shoe import Shoe
from ..Blackjack import Dealer, DecisionModel

'''
First dimension is the dealer's showing card, second is whether the player's hand
is hard or soft; third is the player's total hand value (with ace as 11). 
Example: 
    dealer is showing 3, player's hand is 13: 
        _fixed_strategy_table[3]['hard'][13]
'''
_fixed_strategy_table = {
    1: {
        'soft': {
            17: True,
            18: True,
            19: False,
            20: False
        }, 
        'hard': {
            11: True,
            12: True,
            13: True,
            14: True,
            15: True,
            16: True,
            17: False,
            18: False, 
            19: False, 
            20: False
        }
    },
    2: {
        'soft': {
            17: True,
            18: False,
            19: False,
            20: False
        }, 
        'hard': {
            11: True,
            12: True,
            13: False,
            14: False,
            15: False,
            16: False,
            17: False,
            18: False, 
            19: False, 
            20: False
        }
    },
    3: {
        'soft': {
            17: True,
            18: False,
            19: False,
            20: False
        }, 
        'hard': {
            11: True,
            12: True,
            13: False,
            14: False,
            15: False,
            16: False,
            17: False,
            18: False, 
            19: False, 
            20: False
        }
    },
    4: {
        'soft': {
            17: True,
            18: False,
            19: False,
            20: False
        }, 
        'hard': {
            11: True,
            12: False,
            13: False,
            14: False,
            15: False,
            16: False,
            17: False,
            18: False, 
            19: False, 
            20: False
        }
    },
    5: {
        'soft': {
            17: True,
            18: False,
            19: False,
            20: False
        }, 
        'hard': {
            11: True,
            12: False,
            13: False,
            14: False,
            15: False,
            16: False,
            17: False,
            18: False, 
            19: False, 
            20: False
        }
    },
    6: {
        'soft': {
            17: True,
            18: False,
            19: False,
            20: False
        }, 
        'hard': {
            11: True,
            12: False,
            13: False,
            14: False,
            15: False,
            16: False,
            17: False,
            18: False, 
            19: False, 
            20: False
        }
    },
    7: {
        'soft': {
            17: True,
            18: False,
            19: False,
            20: False
        }, 
        'hard': {
            11: True,
            12: True,
            13: True,
            14: True,
            15: True,
            16: True,
            17: False,
            18: False, 
            19: False, 
            20: False
        }
    },
    8: {
        'soft': {
            17: True,
            18: False,
            19: False,
            20: False
        }, 
        'hard': {
            11: True,
            12: True,
            13: True,
            14: True,
            15: True,
            16: True,
            17: False,
            18: False, 
            19: False, 
            20: False
        }
    },
    9: {
        'soft': {
            17: True,
            18: True,
            19: False,
            20: False
        }, 
        'hard': {
            11: True,
            12: True,
            13: True,
            14: True,
            15: True,
            16: True,
            17: False,
            18: False, 
            19: False, 
            20: False
        }
    },
    10: {
        'soft': {
            17: True,
            18: True,
            19: False,
            20: False
        }, 
        'hard': {
            11: True,
            12: True,
            13: True,
            14: True,
            15: True,
            16: True,
            17: False,
            18: False, 
            19: False, 
            20: False
        }
    },
    11: {
        'soft': {
            17: True,
            18: True,
            19: False,
            20: False
        }, 
        'hard': {
            11: True,
            12: True,
            13: True,
            14: True,
            15: True,
            16: True,
            17: False,
            18: False, 
            19: False, 
            20: False
        }
    },
}

class FixedStrategy(DecisionModel): 
    def __init__(self): 
        super().__init__()

    def decide_hit(self, dealer: Dealer, shoe: Shoe, players, player_index: int):
        #list of actions based on dealer's showing card 
        table = _fixed_strategy_table[dealer.showing]

        #list of actions based on soft or hard player hand
        hand = self._get_hand(dealer, players, player_index)
        if (hand.is_soft): 
            table = table['soft']
            
            if hand.total <= 17:
                return table[17]
            else: 
                return table[hand.total]
        else:
            table = table['hard']
            
            if hand.total <= 11:
                return table[11]
            return table[hand.total]
    
        return False

        