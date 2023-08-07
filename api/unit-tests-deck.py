from lib.blackjack.Deck import Deck

import unittest

class TestDeck(unittest.TestCase):
    
    def test_deck_counts(self): 
        deck = Deck()
        
        self.assertEqual(len(deck.cards), 52)
        self.assertEqual(self.get_card_count(deck.cards, 2), 4)
        self.assertEqual(self.get_card_count(deck.cards, 3), 4)
        self.assertEqual(self.get_card_count(deck.cards, 4), 4)
        self.assertEqual(self.get_card_count(deck.cards, 5), 4)
        self.assertEqual(self.get_card_count(deck.cards, 6), 4)
        self.assertEqual(self.get_card_count(deck.cards, 7), 4)
        self.assertEqual(self.get_card_count(deck.cards, 8), 4)
        self.assertEqual(self.get_card_count(deck.cards, 9), 4)
        self.assertEqual(self.get_card_count(deck.cards, 10), 16)
        self.assertEqual(self.get_card_count(deck.cards, 11), 4)
        
    def get_card_count(self, cards, value) -> int: 
        count = 0
        for card in cards: 
            if (card == value): 
                count+= 1
        return count
            
        
if __name__ == '__main__':
    unittest.main()