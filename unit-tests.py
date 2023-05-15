from classes.Card import *
from classes.Shoe import * 
from classes.Player import *
from classes.Dealer import *
from classes.Round import * 
from classes.Game import * 
from classes.DecisionModel import *

import unittest

class TestCardValues(unittest.TestCase):
    
    def test_card_numeric_values_correct(self):
        suits = all_card_suits()
        for i, suit in enumerate(suits): 
            card2 = Card(CardSuit.Hearts, CardValue.Two)
            self.assertEqual (card2.number_value, 2)
            card3 = Card(CardSuit.Hearts, CardValue.Three)
            self.assertEqual (card3.number_value, 3)
            card4 = Card(CardSuit.Hearts, CardValue.Four)
            self.assertEqual  (card4.number_value, 4)
            card5 = Card(CardSuit.Hearts, CardValue.Five)
            self.assertEqual  (card5.number_value, 5)
            card6 = Card(CardSuit.Hearts, CardValue.Six)
            self.assertEqual  (card6.number_value, 6)
            card7 = Card(CardSuit.Hearts, CardValue.Seven)
            self.assertEqual  (card7.number_value, 7)
            card8 = Card(CardSuit.Hearts, CardValue.Eight)
            self.assertEqual  (card8.number_value, 8)
            card9 = Card(CardSuit.Hearts, CardValue.Nine)
            self.assertEqual  (card9.number_value, 9)
            card10 = Card(CardSuit.Hearts, CardValue.Ten)
            self.assertEqual  (card10.number_value,  10)
            cardAce = Card(CardSuit.Hearts, CardValue.Ace)
            self.assertEqual  (cardAce.number_value,  1)
            cardKing = Card(CardSuit.Hearts, CardValue.King)
            self.assertEqual  (cardKing.number_value, 10)
            cardQueen = Card(CardSuit.Hearts, CardValue.Queen)
            self.assertEqual  (cardQueen.number_value,  10)
            cardJack = Card(CardSuit.Hearts, CardValue.Jack)
            self.assertEqual  (cardJack.number_value,  10)
            
    def test_is_face_cards_and_is_ace_consistent(self): 
        face_cards = [
            Card(CardSuit.Clubs, CardValue.King), 
            Card(CardSuit.Clubs, CardValue.Jack), 
            Card(CardSuit.Clubs, CardValue.Queen), 
        ]
        non_face_cards = [
            Card(CardSuit.Clubs, CardValue.Two), 
            Card(CardSuit.Clubs, CardValue.Three), 
            Card(CardSuit.Clubs, CardValue.Four), 
            Card(CardSuit.Clubs, CardValue.Five), 
            Card(CardSuit.Clubs, CardValue.Six), 
            Card(CardSuit.Clubs, CardValue.Seven), 
            Card(CardSuit.Clubs, CardValue.Eight), 
            Card(CardSuit.Clubs, CardValue.Nine), 
            Card(CardSuit.Clubs, CardValue.Ten), 
            Card(CardSuit.Clubs, CardValue.Ten), 
            Card(CardSuit.Clubs, CardValue.Ace), 
        ]
        for i in range (len(face_cards)): 
            self.assertTrue(face_cards[i].is_face_card)
            self.assertFalse(face_cards[i].is_ace)
        for i in range (len(non_face_cards)): 
            self.assertFalse(non_face_cards[i].is_face_card)
            if (non_face_cards[i].value == CardValue.Ace): 
                self.assertTrue(non_face_cards[i].is_ace)
            else: 
                self.assertFalse(non_face_cards[i].is_ace)
            
class TestShoe(unittest.TestCase): 
    def test_shoe_count(self): 
        shoe = Shoe()
        self.assertEqual(shoe.num_cards, 52)
        
        shoe = Shoe(2)
        self.assertEqual(shoe.num_cards, (52 * 2))
        
        shoe = Shoe(3)
        self.assertEqual(shoe.num_cards, (52 * 3))
        self.assertEqual(shoe.num_cards, shoe.max_num_cards)
        
    def test_shoe_shuffle(self):
        shoe = Shoe()
        
        # test that card count stays the same after shuffle
        self.assertEqual(shoe.num_cards, 52)
        
        shoe.shuffle()
        self.assertEqual(shoe.num_cards, 52)
        
        shoe.get_next(10)
        self.assertEqual(shoe.num_cards, 42)
        
        shoe.shuffle()
        self.assertEqual(shoe.num_cards, 42)
        
    def test_shoe_reset(self): 
        shoe = Shoe()
        
        # test that card count returns to original after reset
        shoe.get_next(2)
        self.assertEqual(shoe.num_cards, 50)
        
        shoe.reset()
        self.assertEqual(shoe.num_cards, 52)
        
    def test_shoe_get_next(self): 
        shoe = Shoe()
        shoe.get_next()
        shoe.get_next()
        
        self.assertEqual(shoe.num_cards, 50)
        
        shoe.get_next(2)
        self.assertEqual(shoe.num_cards, 48)
        
        shoe.get_next(10)
        self.assertEqual(shoe.num_cards, shoe.max_num_cards - 14)

    def test_shoe_top_up(self): 
        shoe = Shoe(3)
        self.assertEqual(shoe.num_cards, shoe.max_num_cards)
        self.assertEqual(shoe.num_cards, 52 * 3)
        
        shoe.get_next(60)
        self.assertEqual(shoe.num_cards, shoe.max_num_cards - 60)
        
        shoe.top_up()
        self.assertEqual(shoe.max_num_cards, 52 * 3)
        self.assertEqual(shoe.num_cards, shoe.max_num_cards - 60 + 52)
        
        shoe.top_up()
        self.assertEqual(shoe.max_num_cards, 52 * 3)
        self.assertEqual(shoe.num_cards, shoe.max_num_cards - 60 + 52)
        
    def test_remove_card(self): 
        shoe = Shoe(2)
        self.assertEqual(shoe.num_cards, shoe.max_num_cards)
        
        #ensure that there are two 2 of hears
        self.assertEqual(shoe.get_count_of(get_card("H2")), 2)
        
        #remove first 2 of hearts
        shoe.remove_card(get_card("H2"))
        self.assertEqual(shoe.num_cards, shoe.max_num_cards-1)
        
        #ensure that 1 remains
        self.assertEqual(shoe.get_count_of(get_card("H2")), 1)
        
        #remove second 2 of hearts
        shoe.remove_card(get_card("H2"))
        self.assertEqual(shoe.num_cards, shoe.max_num_cards-2)
        
        #remove has no effect, since all are gone
        shoe.remove_card(get_card("H2"))
        self.assertEqual(shoe.num_cards, shoe.max_num_cards-2)
        
        #ensure that all are gone
        self.assertEqual(shoe.get_count_of(get_card("H2")), 0)
        
    def test_place_on_top(self): 
        shoe = Shoe(2)
        self.assertEqual(shoe.num_cards, shoe.max_num_cards)
        self.assertEqual(shoe.num_cards, 52 * 2)
        
        #ensure that there are two 5 of spades
        self.assertEqual(shoe.get_count_of(get_card("S5")), 2)
        
        # place one on top 
        shoe.place_on_top(get_card("S5"))
        
        #count should be unchanged
        self.assertEqual(shoe.num_cards, 52 * 2)
        
        #next card dealt should be 5 of spades
        self.assertTrue(shoe.get_next().equals(get_card("S5")))
        
class TestPlayer(unittest.TestCase): 
    def test_player_has_blackjack(self): 
        player = Player(100, BaselineDecisionModel())
        player.hand.append(get_card("DA"))
        self.assertFalse(player.has_blackjack)
        
        player.hand.append(get_card("H10"))
        self.assertTrue(player.has_blackjack)
            
        player = Player(100, BaselineDecisionModel())
        player.hand.append(get_card("DK"))
        self.assertFalse(player.has_blackjack)
        
        player.hand.append(get_card("CA"))
        self.assertTrue(player.has_blackjack)
        
    def test_player_has_21(self): 
        player = Player(100, BaselineDecisionModel())
        
        player.hand.append(get_card("D2"))
        self.assertFalse(player.has_21 or player.has_blackjack)
            
        player.hand.append(get_card("H10"))
        self.assertFalse(player.has_21 or player.has_blackjack)
        
        player.hand.append(get_card("H9"))
        self.assertFalse(player.has_blackjack)
        self.assertTrue(player.has_21)
        
    def test_player_is_bust(self): 
        player = Player(100, BaselineDecisionModel())
        player.hand.append(Card(CardSuit.Diamonds, CardValue.Two))
        self.assertFalse(player.is_bust)
        
        player.hand.append(Card(CardSuit.Hearts, CardValue.Ten))
        self.assertFalse(player.is_bust)
        
        player.hand.append(Card(CardSuit.Hearts, CardValue.Nine))
        self.assertFalse(player.is_bust)
        
        player.hand.append(Card(CardSuit.Diamonds, CardValue.Two))
        self.assertTrue(player.is_bust)

class TestDealer(unittest.TestCase):
    def test_dealer_deal_self(self):
        dealer = Dealer(10000, DealerDecisionModel())
        self.assertEqual(len(dealer.hand), 0)
        self.assertEqual(dealer.shoe.num_cards, dealer.shoe.max_num_cards)
        
        dealer.deal_self()
        self.assertEqual(len(dealer.hand), 1)
        self.assertEqual(dealer.shoe.num_cards, dealer.shoe.max_num_cards - len(dealer.hand))
        
        dealer.deal_self(5)
        self.assertEqual(len(dealer.hand), 6)
        self.assertEqual(dealer.shoe.num_cards, dealer.shoe.max_num_cards - len(dealer.hand))
    
    def test_deal_player(self): 
        dealer = Dealer(10000, DealerDecisionModel())
        player = Player(10000)
        
        self.assertEqual(len(dealer.hand), 0)
        self.assertEqual(len(player.hand), 0)
        
        dealer.deal_player(player)
        self.assertEqual(len(dealer.hand), 0)
        self.assertEqual(len(player.hand), 1)
        self.assertEqual(dealer.shoe.num_cards, dealer.shoe.max_num_cards - len(player.hand))
        
        dealer.deal_player(player, 10)
        self.assertEqual(len(dealer.hand), 0)
        self.assertEqual(len(player.hand), 11)
        self.assertEqual(dealer.shoe.num_cards, dealer.shoe.max_num_cards - len(player.hand))
        
    #TODO: test shuffle 
    #TODO: test reset shoe 
    
class TestCardCount(unittest.TestCase): 
    def test_initial_values(self): 
        cc = CardCount()
        self.assertEqual(cc.num_decks, 1)
        for i in range(1, 11): 
            self.assertEqual(cc.cards_dealt[i], 0)
        
        cc = CardCount(8)
        self.assertEqual(cc.num_decks, 8)
        
    def test_append(self): 
        cc = CardCount()
        self.assertEqual(cc.cards_dealt[1], 0)
        self.assertEqual(cc.cards_dealt[2], 0)
        self.assertEqual(cc.cards_dealt[10], 0)
        
        cc.append(get_card("H2"))
        self.assertEqual(cc.cards_dealt[1], 0)
        self.assertEqual(cc.cards_dealt[2], 1)
        self.assertEqual(cc.cards_dealt[10], 0)
        
        cc.append(get_card("D2"))
        self.assertEqual(cc.cards_dealt[1], 0)
        self.assertEqual(cc.cards_dealt[2], 2)
        self.assertEqual(cc.cards_dealt[10], 0)
        
        cc.append(get_card("C2"))
        self.assertEqual(cc.cards_dealt[1], 0)
        self.assertEqual(cc.cards_dealt[2], 3)
        self.assertEqual(cc.cards_dealt[10], 0)
        
        cc.append(get_card("CK"))
        self.assertEqual(cc.cards_dealt[1], 0)
        self.assertEqual(cc.cards_dealt[2], 3)
        self.assertEqual(cc.cards_dealt[10], 1)
        
        cc.append(get_card("C10"))
        self.assertEqual(cc.cards_dealt[1], 0)
        self.assertEqual(cc.cards_dealt[2], 3)
        self.assertEqual(cc.cards_dealt[10], 2)
        
        cc.append(get_card("CJ"))
        self.assertEqual(cc.cards_dealt[1], 0)
        self.assertEqual(cc.cards_dealt[2], 3)
        self.assertEqual(cc.cards_dealt[10], 3)
        
        cc.append(get_card("SA"))
        self.assertEqual(cc.cards_dealt[1], 1)
        self.assertEqual(cc.cards_dealt[2], 3)
        self.assertEqual(cc.cards_dealt[10], 3)
    
    def test_probability_of_card(self): 
        cc_single = CardCount()
        cc_multi = CardCount(3)
        
        prev_p_single =  0
        prev_p_multi =  0
        prob_sum_single = 0
        prob_sum_multi = 0
        for i in range(1, 11): 
            p_single = cc_single.probability_of_getting(i)
            p_multi = cc_multi.probability_of_getting(i)
            
            prob_sum_single += p_single
            prob_sum_multi += p_multi
            
            self.assertEqual(p_single, p_multi)
            
            if (i > 1 and i != 10): 
                #all probabilities should be equal (except 10)
                self.assertEqual(p_single, prev_p_single) 
                self.assertEqual(p_multi, prev_p_multi) 
            elif (i == 10): 
                #because there are 4 cards worth 10
                self.assertEqual(p_single, (prev_p_single * 4)) 
                self.assertEqual(p_multi, (prev_p_multi * 4)) 
            prev_p_single = p_single
            prev_p_multi = p_multi
            
        self.assertEqual(prob_sum_single, 1)
        self.assertEqual(prob_sum_multi, 1)
    
    def test_probability_of_over(self): 
        cc_single = CardCount()
        cc_multi = CardCount()
        
        prev_p_single = cc_single.probability_of_n_or_over(1)
        self.assertEqual(prev_p_single, 1)
        prev_p_multi = cc_multi.probability_of_n_or_over(1)
        self.assertEqual(prev_p_multi, 1)
        
        for i in range(2, 11): 
            p_single = cc_single.probability_of_n_or_over(i)
            p_multi = cc_multi.probability_of_n_or_over(i)
            
            self.assertTrue(p_single < prev_p_single)
            self.assertTrue(p_multi < prev_p_multi)
            self.assertEqual(p_single, p_multi)
            
            prev_p_single = p_single
            prev_p_multi = p_multi
    
    def test_probability_of_under(self): 
        cc_single = CardCount()
        for i in range(0, 20): 
            print(i, cc_single.probability_of_n_or_under(i))
    
    def test_add_decks_probability_unchanged(self): 
        cc = CardCount()
        
        #adding decks doesn't change probability if card not dealt
        p1 = cc.probability_of_getting(10)
        cc.add_decks(1)
        
        p2 = cc.probability_of_getting(10)
        cc.add_decks(1)
        
        p3 = cc.probability_of_getting(10)
        
        self.assertEqual(p1, p2)
        self.assertEqual(p2, p3)
            
    def test_add_decks_probability_changed(self): 
        cc = CardCount()
        cc.append(get_card("D10"))
        
        #adding decks doesn't change probability if card not dealt
        p1 = cc.probability_of_getting(10)
        cc.add_decks(1)
        
        p2 = cc.probability_of_getting(10)
        cc.add_decks(1)
        
        p3 = cc.probability_of_getting(10)
        
        self.assertTrue(p1 < p2)
        self.assertTrue(p2 < p3)
        
    def test_add_counts(self): 
        cc1 = CardCount()
        cc2 = CardCount()
        
        cc1.append(get_card("D2"))
        
        cc2.append(get_card("D2"))
        cc2.append(get_card("S2"))
        
        self.assertEqual(cc1.cards_dealt[2], 1)
        self.assertEqual(cc1.cards_dealt[3], 0)
        
        self.assertEqual(cc2.cards_dealt[2], 2)
        self.assertEqual(cc2.cards_dealt[3], 0)
        
        cc1.add_counts(cc2)
        self.assertEqual(cc1.cards_dealt[2], 3)
        self.assertEqual(cc1.cards_dealt[3], 0)
        
class TestCardProbabilities(unittest.TestCase): 
    def test_baseline_non10_probability(self): 
        cc_single = CardCount()
        cc_multi = CardCount(3)
        
        self.assertEqual(cc_single.probability_of_getting(4), 4/52)
        self.assertEqual(cc_multi.probability_of_getting(4), 4/52)
        
    def test_baseline_10_probability(self): 
        cc_single = CardCount()
        cc_multi = CardCount(3)
        
        self.assertEqual(cc_single.probability_of_getting(10), 16/52)
        self.assertEqual(cc_multi.probability_of_getting(10), 16/52)
        
    def test_baseline_1_and_11_probability(self): 
        cc_single = CardCount()
        cc_multi = CardCount(3)
        
        self.assertEqual(cc_single.probability_of_getting(1), 4/52)
        #self.assertEqual(cc_multi.probability_of_getting(11), 4/52)
        
    def test_dealt_non10_probability(self): 
        cc_single = CardCount()
        cc_multi = CardCount(3)
        
        cc_single.append(get_card("D4"))
        
        cc_multi.append(get_card("D4"))
        cc_multi.append(get_card("S4"))
        
        self.assertEqual(cc_single.probability_of_getting(4), 3/51)
        self.assertEqual(cc_multi.probability_of_getting(4), 10/(52*3 -2))
        
    def test_dealt_10_probability(self): 
        cc_single = CardCount()
        cc_multi = CardCount(3)
        
        cc_single.append(get_card("D10"))
        
        cc_multi.append(get_card("D10"))
        cc_multi.append(get_card("S10"))
        
        self.assertEqual(cc_single.probability_of_getting(10), 15/51)
        self.assertEqual(cc_multi.probability_of_getting(10), 46/(52*3 -2))

class TestDealerDecisionModel(unittest.TestCase):
    def test_dealer_hits_on_12(self):
        player = Player(10000, DealerDecisionModel())
        player.hand.append(get_card("H10"))
        player.hand.append(get_card("H2"))
        
        self.assertTrue(player.decision_model.decide_hit_or_stand(player, None))
        
    def test_dealer_hits_on_15(self):
        player = Player(10000, DealerDecisionModel())
        player.hand.append(get_card("H10"))
        player.hand.append(get_card("H5"))
        
        self.assertTrue(player.decision_model.decide_hit_or_stand(player, None))
        
    def test_dealer_hits_on_16(self):
        player = Player(10000, DealerDecisionModel())
        player.hand.append(get_card("H10"))
        player.hand.append(get_card("H6"))
        
        self.assertTrue(player.decision_model.decide_hit_or_stand(player, None))
        
    def test_dealer_sticks_on_hard_17(self):
        player = Player(10000, DealerDecisionModel())
        player.hand.append(get_card("H10"))
        player.hand.append(get_card("H7"))
        
        self.assertFalse(player.decision_model.decide_hit_or_stand(player, None))
        
    def test_dealer_hits_on_soft_17(self):
        player = Player(10000, DealerDecisionModel())
        player.hand.append(get_card("HA"))
        player.hand.append(get_card("H6"))
        
        self.assertTrue(player.decision_model.decide_hit_or_stand(player, None))
        
    def test_dealer_sticks_on_18(self):
        player = Player(10000, DealerDecisionModel())
        player.hand.append(get_card("HJ"))
        player.hand.append(get_card("H8"))
        
        self.assertFalse(player.decision_model.decide_hit_or_stand(player, None))
        
#class TestRound(unittest.TestCase): 
    #TODO: test card counts per round
    #TODO: test that player+dealer balances are zero-sum
    
class TestGame(unittest.TestCase): 
    def test_dealer_bust(self): 
        balance = 10000
        dealer = Dealer(balance, DealerDecisionModel(), num_decks=3)
        player = Player(balance, BaselineDecisionModel())
        game = Game(dealer)
        dealer.load_deck([
            "H9",
            "H5",
            "D10",
            "D7",
            "H8"
        ])
        
        game.execute_next_round([player])
        
        self.assertEqual(dealer.balance, balance-2)
        self.assertEqual(player.balance, balance+2)
        
    def test_player_bust(self):     
        dealer = Dealer(10000, DealerDecisionModel(), num_decks=3)
        player = Player(10000, BaselineDecisionModel())
        game = Game(dealer)
        dealer.load_deck([
            "H9",
            "H8",
            "D10",
            "D6",
            "D7",
        ])
        
        game.execute_next_round([player])
    
    def test_dealer_blackjack(self): 
        dealer = Dealer(10000, DealerDecisionModel(), num_decks=3)
        player = Player(10000, BaselineDecisionModel())
        game = Game(dealer)
        dealer.load_deck([
            "H10",
            "HA",
            "D10",
            "D6"
        ])
        
        game.execute_next_round([player])
    
    def test_player_blackjack(self): 
        dealer = Dealer(10000, DealerDecisionModel(), num_decks=3)
        player = Player(10000, BaselineDecisionModel())
        game = Game(dealer)
        dealer.load_deck([
            "H10",
            "HK",
            "DQ",
            "DA"
        ])
        
        game.execute_next_round([player])
    
if __name__ == '__main__':
    unittest.main()
    
    
# top-up
# # does top-up result in the right amount of cards when the shoe is 52? 
# # does top-up result in the right amount of cards when the shoe is < 52? 
# # does top-up result in the right amount of cards when the shoe is > 52? 

# card counts 
# # do card counts add correctly? 

# card probabilities 
# # is the probability of non-10 card x correct baseline? 
# # is the probability of non-10 card x correct after removing from shoe? 
# # is the probability of 10 card x correct baseline? 
# # is the probability of 10 card x correct after removing from shoe? 
# - does the probability of non-10 card x reset when shoe is reset? 
# - does the probability of 10 card x reset when shoe is reset? 
# - does the probability of non-10 card x change when shoe is topped up? 
# - does the probability of 10 card x change when shoe is topped up? 

# gameplay: 
# - does game top up automatically when it's supposed to? 
# - is game's card count correct after dealing some cards? 
# - is game's card count correct after a top-up? 
# - is game's card count correct after multiple top-ups? 

# decision models: dealer 
# # does dealer hit on 16? 
# # does dealer stick on hard 17? 
# # does dealer hit on soft 17? 
# # does dealer stick on 18? 
# # does dealer hit on 12? 

# decision models: baseline 

# decision models: 