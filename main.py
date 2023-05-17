from classes.Card import *
from classes.Shoe import * 
from classes.Player import *
from classes.Dealer import *
from classes.Round import * 
from classes.Game import * 
from classes.DecisionModel import *
from classes.MonteCarlo import * 



balance = 1000000
num_decks = 3
dealer = Dealer(balance, DealerDecisionModel(), num_decks=num_decks)
player = Player(balance, MonteCarloDecisionModel())
game = Game(dealer)

game.execute_next_round([player])