# Readme

## Phase 0
Test against various baseline decision models as benchmarks 
- dealer's own decision model 
- random decision model 
- a standard 'fixed' decision model based on dealer's showing card, player's total, and soft ace count 
- a standard 'fixed' decision model like the aforementioned that also takes into account the hi-lo card count 

In all of the above, the bet amount is fixed (never varies, player always bets the minimum)

## Phase 1 
Test against a Q-learning trained model that does not count cards, and the bet amount is fixed. Its output is only hit/stand. 

## Phase 2 
Test against a Q-learning trained model that takes the hi-lo card count into account, and the bet amount is fixed. Its output is only hit/stand. 

-- we are here --

## Phase 3
Test against a Q-learning trained model that takes the hi-lo card count into account, and varies its bet amount accordingly. The model for choosing hit/stand is the same model from 
Phase 2, and choosing an optimal bet amount will use a new model which will be trained 
with usage of an already-trained instance of the Phase 2 model. 