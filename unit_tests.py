from classes.Card import *
from classes.Deck import * 
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
            
    def test_face_cards_consistent(self): 
        face_cards = [
            Card(CardSuit.Clubs, CardValue.King), 
            Card(CardSuit.Clubs, CardValue.Jack), 
            Card(CardSuit.Clubs, CardValue.Queen), 
        ]
        non_face_cards = [
            Card(CardSuit.Clubs, CardValue.Two), 
            Card(CardSuit.Clubs, CardValue.Five), 
            Card(CardSuit.Clubs, CardValue.Ten), 
            Card(CardSuit.Clubs, CardValue.Ace), 
        ]
        for i in range (len(face_cards)): 
            self.assertTrue(face_cards[i].is_face_card)
            self.assertFalse(face_cards[i].is_ace)
        for i in range (len(non_face_cards)): 
            self.assertFalse(non_face_cards[i].is_face_card)
            
class TestDeck(unittest.TestCase): 
    def test_deck_count(self): 
        deck = Deck()
        self.assertEqual(deck.num_cards, 52)
        
        deck = Deck(2)
        self.assertEqual(deck.num_cards, (52 * 2))
        
        deck = Deck(3)
        self.assertEqual(deck.num_cards, (52 * 3))
        self.assertEqual(deck.num_cards, deck.max_num_cards)
        
    def test_deck_shuffle(self):
        deck = Deck()
        
        # test that card count stays the same after shuffle
        self.assertEqual(deck.num_cards, 52)
        
        deck.shuffle()
        self.assertEqual(deck.num_cards, 52)
        
        deck.get_next(10)
        self.assertEqual(deck.num_cards, 42)
        
        deck.shuffle()
        self.assertEqual(deck.num_cards, 42)
        
    def test_deck_reset(self): 
        deck = Deck()
        
        # test that card count returns to original after reset
        deck.get_next(2)
        self.assertEqual(deck.num_cards, 50)
        
        deck.reset()
        self.assertEqual(deck.num_cards, 52)
        
    def test_deck_get_next(self): 
        deck = Deck()
        deck.get_next()
        deck.get_next()
        
        self.assertEqual(deck.num_cards, 50)
        
        deck.get_next(2)
        self.assertEqual(deck.num_cards, 48)
        
        deck.get_next(10)
        self.assertEqual(deck.num_cards, deck.max_num_cards - 14)

    def test_deck_top_up(self): 
        deck = Deck(3)
        self.assertEqual(deck.num_cards, deck.max_num_cards)
        
        deck.get_next(60)
        self.assertEqual(deck.num_cards, deck.max_num_cards - 60)
        
        deck.top_up_deck()
        self.assertEqual(deck.max_num_cards, 52 * 3)
        self.assertEqual(deck.num_cards, deck.max_num_cards - 60 + 52)
        
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
        dealer = Dealer(10000)
        self.assertEqual(len(dealer.hand), 0)
        self.assertEqual(dealer.deck.num_cards, dealer.deck.max_num_cards)
        
        dealer.deal_self()
        self.assertEqual(len(dealer.hand), 1)
        self.assertEqual(dealer.deck.num_cards, dealer.deck.max_num_cards - len(dealer.hand))
        
        dealer.deal_self(5)
        self.assertEqual(len(dealer.hand), 6)
        self.assertEqual(dealer.deck.num_cards, dealer.deck.max_num_cards - len(dealer.hand))
    
    def test_deal_player(self): 
        dealer = Dealer(10000)
        player = Player(10000)
        
        self.assertEqual(len(dealer.hand), 0)
        self.assertEqual(len(player.hand), 0)
        
        dealer.deal_player(player)
        self.assertEqual(len(dealer.hand), 0)
        self.assertEqual(len(player.hand), 1)
        self.assertEqual(dealer.deck.num_cards, dealer.deck.max_num_cards - len(player.hand))
        
        dealer.deal_player(player, 10)
        self.assertEqual(len(dealer.hand), 0)
        self.assertEqual(len(player.hand), 11)
        self.assertEqual(dealer.deck.num_cards, dealer.deck.max_num_cards - len(player.hand))
        
    #TODO: test shuffle 
    #TODO: test reset deck 
    
#class TestRound(unittest.TestCase): 
    #TODO: test card counts per round
    #TODO: test that player+dealer balances are zero-sum
    
if __name__ == '__main__':
    unittest.main()