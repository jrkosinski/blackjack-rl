from lib.Hand import Hand

import unittest

class TestHandValues(unittest.TestCase):
    
    def test_hand_totals(self): 
        hand = Hand()
        
        self.assertEqual(hand.count, 0)
        self.assertEqual(hand.total, 0)
        
        hand.add_card(3)
        
        self.assertEqual(hand.count, 1)
        self.assertEqual(hand.total, 3)
        
        hand.add_card(10)
        
        self.assertEqual(hand.count, 2)
        self.assertEqual(hand.total, 13)
        
        hand.add_card(10)
        
        self.assertEqual(hand.count, 3)
        self.assertEqual(hand.total, 23)
        
    def test_hand_is_21_or_blackjack(self): 
        hand = Hand()
        
        self.assertTrue(hand.is_under)
        self.assertFalse(hand.is_21)
        self.assertFalse(hand.is_blackjack)
        self.assertFalse(hand.is_natural)
        self.assertFalse(hand.is_over)
        
        hand.add_card(10)
        
        self.assertTrue(hand.is_under)
        self.assertFalse(hand.is_21)
        self.assertFalse(hand.is_blackjack)
        self.assertFalse(hand.is_natural)
        self.assertFalse(hand.is_over)
        
        hand.add_card(10)
        
        self.assertTrue(hand.is_under)
        self.assertFalse(hand.is_21)
        self.assertFalse(hand.is_blackjack)
        self.assertFalse(hand.is_natural)
        self.assertFalse(hand.is_over)
        
        hand.add_card(2)
        
        self.assertFalse(hand.is_under)
        self.assertFalse(hand.is_21)
        self.assertFalse(hand.is_blackjack)
        self.assertFalse(hand.is_natural)
        self.assertTrue(hand.is_over)
        
        hand.clear()
        hand.add_card(10)
        hand.add_card(11)
        
        self.assertFalse(hand.is_under)
        self.assertTrue(hand.is_21)
        self.assertTrue(hand.is_blackjack)
        self.assertTrue(hand.is_natural)
        self.assertFalse(hand.is_over)
        
        hand.clear()
        hand.add_card(10)
        hand.add_card(5)
        hand.add_card(6)
        
        self.assertFalse(hand.is_under)
        self.assertTrue(hand.is_21)
        self.assertFalse(hand.is_blackjack)
        self.assertFalse(hand.is_natural)
        self.assertFalse(hand.is_over)

    def test_subscriptable(self): 
        hand = Hand()
        hand.add_card(3)

        self.assertEqual(hand[0], 3)
        with self.assertRaises(IndexError):
            h = hand[1]


if __name__ == '__main__':
    unittest.main()
    