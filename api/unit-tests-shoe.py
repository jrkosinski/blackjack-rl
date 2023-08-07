from lib.Shoe import Shoe

import unittest

class TestShoe(unittest.TestCase):
    
    def test_initialize_shoe(self): 
        shoe = Shoe(5)
        
        self.assertEqual(shoe.max_deck_count, 5)
        self.assertEqual(shoe.count, 5 * 52)
        
    def test_shuffle_shoe(self): 
        shoe = Shoe(5)
        
        #capture first 10 cards 
        first_10 = []
        for i in range(10): 
            first_10.append(shoe.cards[i])
        
        count_before = shoe.count
        
        for i in range(len(first_10)): 
            self.assertEqual(first_10[i], shoe.cards[i])
        
        #shuffle shoe 
        shoe.shuffle()
        
        self.assertEqual(shoe.count, count_before)
        
        #statistically very unlikely for more than 6 to be equal
        equal_count: int = 0
        for i in range(len(first_10)): 
            if (first_10[i] == shoe.cards[i]): 
                equal_count += 1
                
        self.assertFalse(equal_count > 6)
        
    def test_deal(self): 
        shoe = Shoe(5)
        
        count = shoe.count
        
        #deal one card out 
        card = shoe.deal_card()
        self.assertEqual(shoe.count, count-1)
        self.assertTrue(card > 1)
        
        #deal all cards out 
        while(shoe.count > 0): 
            count = shoe.count
            card = shoe.deal_card()
            self.assertEqual(shoe.count, count-1)
            self.assertTrue(card > 1)
            
        #can't deal with no cards left 
        self.assertEqual(shoe.count, 0)
        card = shoe.deal_card()
        self.assertIsNone(card)
    
    def test_top_up(self): 
        shoe = Shoe(5)
        
        #topping up after dealing one card has no effect
        shoe.deal_card()
        shoe.top_up()
        self.assertEqual(shoe.count, 52 * 5 -1)
        
        #deal 52 more 
        for i in range(52): 
            shoe.deal_card()
        
        #then top up 
        self.assertEqual(shoe.count, 52 * 4 -1)
        shoe.top_up()
        self.assertEqual(shoe.count, 52 * 5 -1)
    
    def test_statistics(self): 
        shoe = Shoe(5) 
        
        shoe.statistical_analysis()
        
        for i in range(1, 10): 
            self.assertEqual(round(shoe.probabilities[i], 4), 0.0769)
        self.assertEqual(round(shoe.probabilities[10], 2), 0.31)
        self.assertEqual(round(shoe.probabilities[11], 4), 0.0769)
        
        self.assertEqual(round(shoe.probability_of_lte(5), 4), 0.3846)
        self.assertEqual(round(shoe.probability_of_lte(1), 4), 0.0769)
        self.assertEqual(round(shoe.probability_of_lte(0), 4), 0.0)
        self.assertEqual(round(shoe.probability_of_gt(4), 4), 0.7692)
        self.assertEqual(round(shoe.probability_of_gt(11), 4), 0.0)
    
    def test_hi_lo_count(self): 
        shoe = Shoe(5)

        self.assertEqual(shoe.hi_lo_count, 0)
        
        #remove a 2 
        shoe.cards.remove(2)
        shoe._calculate_hi_lo()
        
        self.assertTrue(shoe.hi_lo_count > 0)
        
        #remove 2 10s 
        shoe.cards.remove(10)
        shoe.cards.remove(10)
        shoe._calculate_hi_lo()
        
        self.assertTrue(shoe.hi_lo_count < 0)

        #assure that removing an 8 has no effect 
        precount = shoe.hi_lo_count
        
        shoe.cards.remove(7)
        shoe.cards.remove(8)
        shoe.cards.remove(9)
        shoe._calculate_hi_lo()

        postcount = shoe.hi_lo_count
        self.assertEqual(postcount, precount)

if __name__ == '__main__':
    unittest.main()
    