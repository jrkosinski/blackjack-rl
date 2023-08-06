import tensorflow as tf
import numpy as np

from lib.Shoe import Shoe
from lib.Hand import Hand 
from lib.Blackjack import Dealer, DecisionModel

class QDecisionModel(DecisionModel): 
    def __init__(self, model): 
        super().__init__()
        self.model = model

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
             
        state_tensor = tf.convert_to_tensor(state)
        state_tensor = tf.expand_dims(state_tensor, 0)
        q_values = self.model.predict(state_tensor, verbose=0)
        return np.argmax(q_values[0])