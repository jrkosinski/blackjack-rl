from ..Shoe import Shoe
from ..Blackjack import DecisionModel, Dealer

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
            17: 9999,
            18: 2.7,
            19: -9999,
            20: -9999
        }, 
        'hard': {
            11: 9999,
            12: 9999,
            13: 38.7,
            14: 26.9,
            15: 18.8,
            16: 16.8,
            17: -12.0,
            18: -9999, 
            19: -9999, 
            20: -9999
        }
    },
    2: {
        'soft': {
            17: 9999,
            18: -29.4,
            19: -9999,
            20: -9999
        }, 
        'hard': {
            11: 9999,
            12: 5.8,
            13: -2.0,
            14: -7.9,
            15: -11.9,
            16: -18.3,
            17: -9999,
            18: -9999, 
            19: -9999, 
            20: -9999
        }
    },
    3: {
        'soft': {
            17: 9999,
            18: -29.5,
            19: -9999,
            20: -9999
        }, 
        'hard': {
            11: 9999,
            12: 2.5,
            13: -4.8,
            14: -10.3,
            15: -14.0,
            16: -20.4,
            17: -9999,
            18: -9999, 
            19: -9999, 
            20: -9999
        }
    },
    4: {
        'soft': {
            17: 9999,
            18: -30.1,
            19: -9999,
            20: -9999
        }, 
        'hard': {
            11: 9999,
            12: -0.4,
            13: -7.4,
            14: -12.6,
            15: -16.1,
            16: -22.5,
            17: -9999,
            18: -9999, 
            19: -9999, 
            20: -9999
        }
    },
    5: {
        'soft': {
            17: 9999,
            18: -30.5,
            19: -9999,
            20: -9999
        }, 
        'hard': {
            11: 9999,
            12: -3.3,
            13: -10.1,
            14: -15.1,
            15: -18.3,
            16: -24.9,
            17: -9999,
            18: -9999, 
            19: -9999, 
            20: -9999
        }
    },
    6: {
        'soft': {
            17: 9999,
            18: -35.9,
            19: -9999,
            20: -9999
        }, 
        'hard': {
            11: 9999,
            12: -2.5,
            13: -10.5,
            14: -16.2,
            15: -19.8,
            16: -27.3,
            17: -9999,
            18: -9999, 
            19: -9999, 
            20: -9999
        }
    },
    7: {
        'soft': {
            17: 9999,
            18: -9999,
            19: -9999,
            20: -9999
        }, 
        'hard': {
            11: 9999,
            12: 9999,
            13: 9999,
            14: 34.0,
            15: 18.3,
            16: 14.7,
            17: -9999,
            18: -9999, 
            19: -9999, 
            20: -9999
        }
    },
    8: {
        'soft': {
            17: 9999,
            18: -29.7,
            19: -9999,
            20: -9999
        }, 
        'hard': {
            11: 9999,
            12: 9999,
            13: 9999,
            14: 38.8,
            15: 17.9,
            16: 12.0,
            17: -44.2,
            18: -9999, 
            19: -9999, 
            20: -9999
        }
    },
    9: {
        'soft': {
            17: 9999,
            18: 9999,
            19: -9999,
            20: -9999
        }, 
        'hard': {
            11: 9999,
            12: 9999,
            13: 9999,
            14: 9999,
            15: 15.3,
            16: 8.6,
            17: -40.2,
            18: -9999, 
            19: -9999, 
            20: -9999
        }
    },
    10: {
        'soft': {
            17: 9999,
            18: 9999,
            19: -9999,
            20: -9999
        }, 
        'hard': {
            11: 9999,
            12: 9999,
            13: 9999,
            14: 9999,
            15: 8.2,
            16: 0.1,
            17: -43.3,
            18: -9999, 
            19: -9999, 
            20: -9999
        }
    },
    11: {
        'soft': {
            17: 9999,
            18: 2.7,
            19: -9999,
            20: -9999
        }, 
        'hard': {
            11: 9999,
            12: 9999,
            13: 38.7,
            14: 26.9,
            15: 18.8,
            16: 16.8,
            17: -12.0,
            18: -9999, 
            19: -9999, 
            20: -9999
        }
    },
}

class FixedWithCardCounting(DecisionModel): 
    def __init__(self): 
        super().__init__()

    def decide_bet(self, dealer: Dealer, shoe: Shoe, players, player_index: int, minimum_bet: int = 1):
        count = 100 * shoe.hi_lo_count/shoe.count
        if (count > 3.6): 
            if (count > 10): 
                return minimum_bet * 3
            return minimum_bet * 2
        
        return 0

    def decide_hit(self, dealer: Dealer, shoe: Shoe, players, player_index: int):
        #list of actions based on dealer's showing card 
        table = _fixed_strategy_table[dealer.showing]
        count = 100 * shoe.hi_lo_count/shoe.count

        #list of actions based on soft or hard player hand
        hand = self._get_hand(dealer, players, player_index)
        if (hand.is_soft): 
            table = table['soft']
            
            if hand.total <= 17:
                return table[17] > count
            else: 
                return table[hand.total] > count
        else:
            table = table['hard']
            
            if hand.total <= 11:
                return table[11] > count
            return table[hand.total] > count
    
        return False