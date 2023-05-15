from classes.Card import *
from classes.Shoe import * 
from classes.Player import *
from classes.Dealer import *
from classes.Round import * 
from classes.Game import * 

from classes.DecisionModel import BaselineDecisionModel
from classes.DecisionModel import RainManDecisionModel

player = Player(10000, DealerDecisionModel())
dealer = Dealer(1000000, DealerDecisionModel, num_decks=6)

game = Game(dealer, verbose=1)

for i in range (1000):
    game.execute_next_round([player])