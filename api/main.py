from lib.blackjack import Table, Dealer, Player, DealerDecisionModel
from lib.decision_models.FixedStrategy import FixedStrategy
from lib.decision_models.FixedWithCardCounting import FixedWithCardCounting
from lib.decision_models.QDecisionModel import QDecisionModel
import tensorflow as tf

dealer = Dealer()
table = Table(dealer, 12)

table.add_player(Player(DealerDecisionModel()))
table.add_player(Player(FixedStrategy()))
table.add_player(Player(FixedWithCardCounting()))
table.add_player(Player(QDecisionModel(tf.keras.models.load_model("model/model_saved"))))

for i in range(10000): 
    table.play_round()
    
for i in range(len(table.players)): 
    print(f"player {i}: {table.players[i].balance}")