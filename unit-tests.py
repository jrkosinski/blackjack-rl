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
        
        shoe.get_next(60)
        self.assertEqual(shoe.num_cards, shoe.max_num_cards - 60)
        
        shoe.top_up()
        self.assertEqual(shoe.max_num_cards, 52 * 3)
        self.assertEqual(shoe.num_cards, shoe.max_num_cards - 60 + 52)
        
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
        
#class TestRound(unittest.TestCase): 
    #TODO: test card counts per round
    #TODO: test that player+dealer balances are zero-sum
    
if __name__ == '__main__':
    unittest.main()