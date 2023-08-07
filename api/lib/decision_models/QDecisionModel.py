import tensorflow as tf
import numpy as np

from ..blackjack.Shoe import Shoe
from ..blackjack import Dealer, DecisionModel

class QDecisionModel(DecisionModel): 
    def __init__(
        self, 
        model, 
        use_hi_lo_count: bool = False
    ): 
        super().__init__()
        self.model = model
        self.use_hi_lo_count = use_hi_lo_count

    def decide_hit(self, dealer: Dealer, shoe: Shoe, players, player_index: int):
        
        #TODO: this code is duplicated 
        soft_ace_count = players[player_index].hand.soft_ace_count
        if (soft_ace_count > 2): 
            soft_ace_count = 2
            
        state = [
            dealer.showing, 
            players[player_index].hand.total,
            soft_ace_count
        ]
        
        if (self.use_hi_lo_count): 
            state.append(100 * shoe.hi_lo_count/shoe.count)
             
        state_tensor = tf.convert_to_tensor(state)
        state_tensor = tf.expand_dims(state_tensor, 0)
        q_values = self.model.predict(state_tensor, verbose=0)
        return np.argmax(q_values[0])