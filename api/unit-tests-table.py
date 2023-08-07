from lib.blackjack import Dealer, DealerDecisionModel, Table, Player

import unittest

class TestTable(unittest.TestCase):
    
    def test_initialize_table_deal_hands(self): 
        
        #table with 5 deck shoe and dealer
        dealer = Dealer()
        table = Table(dealer, 5)
        
        #2 players
        table.players.append(Player(DealerDecisionModel()))
        table.players.append(Player(DealerDecisionModel()))
        
        table.deal_hands()

        #deal the dealer one exxtra card to account for missing 'down' card
        table.dealer.add_card(table.shoe.deal_card())
        
        self.assertEqual(table.dealer.hand.count, 2)
        
        for player in table.players: 
            self.assertEqual(player.hand.count, 2)
        
    def test_deal_cards_all_blackjack(self): 
        dealer = Dealer()
        table = Table(dealer, 5)
        
        #2 players
        table.players.append(Player(DealerDecisionModel()))
        table.players.append(Player(DealerDecisionModel()))
        
        #load the shoe 
        table.shoe.cards = [
            10, 10, 10, 11, 11, 11
        ]
        
        table.deal_hands()

        #deal the dealer one exxtra card to account for missing 'down' card
        table.dealer.add_card(table.shoe.deal_card())
        
        #everyone has blackjack? 
        self.assertTrue(table.dealer.hand.is_blackjack)
        self.assertTrue(table.players[0].hand.is_blackjack)
        self.assertTrue(table.players[1].hand.is_blackjack)
        
    def test_results_all_blackjack(self): 
        dealer = Dealer()
        table = Table(dealer, 5)
        
        #2 players
        table.players.append(Player(DealerDecisionModel()))
        table.players.append(Player(DealerDecisionModel()))
        
        #load the shoe 
        table.shoe.cards = [
            10, 10, 10, 11, 11, 11
        ]
        
        table.deal_hands()

        #deal the dealer one exxtra card to account for missing 'down' card
        table.dealer.add_card(table.shoe.deal_card())
        
        #everyone has blackjack? 
        self.assertTrue(table.dealer.hand.is_blackjack)
        self.assertTrue(table.players[0].hand.is_blackjack)
        self.assertTrue(table.players[1].hand.is_blackjack)
        
        table.dealer.assess_winners(table.players)
        
        self.assertEqual(table.dealer.balance, -6)
        self.assertEqual(table.players[0].balance, 3)
        self.assertEqual(table.players[1].balance, 3)
         
    def test_results_push(self): 
        dealer = Dealer()
        table = Table(dealer, 5)
        
        #2 players
        table.players.append(Player(DealerDecisionModel()))
        table.players.append(Player(DealerDecisionModel()))
        
        #load the shoe 
        table.shoe.cards = [
            10, 10, 10, 6, 6, 6
        ]
        
        table.deal_hands()

        #deal the dealer one exxtra card to account for missing 'down' card
        table.dealer.add_card(table.shoe.deal_card())
        
        table.dealer.assess_winners(table.players)
        
        self.assertEqual(table.dealer.balance, 0)
        self.assertEqual(table.players[0].balance, 0)
        self.assertEqual(table.players[1].balance, 0)
        
    def test_dealer_wins_on_points(self): 
        dealer = Dealer()
        table = Table(dealer, 5)
        
        #2 players
        table.players.append(Player(DealerDecisionModel()))
        table.players.append(Player(DealerDecisionModel()))
        
        #load the shoe 
        table.shoe.cards = [
            10, 10, 10, 6, 6, 8
        ]
        
        table.deal_hands()

        #deal the dealer one exxtra card to account for missing 'down' card
        table.dealer.add_card(table.shoe.deal_card())
        
        table.dealer.assess_winners(table.players)
        
        self.assertEqual(table.dealer.balance, 4)
        self.assertEqual(table.players[0].balance, -2)
        self.assertEqual(table.players[1].balance, -2)
        
    def test_dealer_breaks_even(self): 
        dealer = Dealer()
        table = Table(dealer, 5)
        
        #2 players
        table.players.append(Player(DealerDecisionModel()))
        table.players.append(Player(DealerDecisionModel()))
        
        #load the shoe 
        table.shoe.cards = [
            10, 10, 10, 9, 6, 8
        ]
        
        table.deal_hands()

        #deal the dealer one exxtra card to account for missing 'down' card
        table.dealer.add_card(table.shoe.deal_card())
        
        table.dealer.assess_winners(table.players)
        
        self.assertEqual(table.dealer.balance, 0)
        self.assertEqual(table.players[0].balance, 2)
        self.assertEqual(table.players[1].balance, -2)
    
    def test_play_round_no_hits(self): 
        dealer = Dealer()
        table = Table(dealer, 1)
        
        #2 players
        table.players.append(Player(DealerDecisionModel()))
        table.players.append(Player(DealerDecisionModel()))
        
        #load the shoe 
        table.shoe.cards = [
            10, 10, 10, 9, 7, 8
        ]
        
        table.play_round()
        
        self.assertEqual(table.dealer.balance, 0)
        self.assertEqual(table.players[0].balance, 2)
        self.assertEqual(table.players[1].balance, -2)
        
    def test_play_round_dealer_hits(self): 
        dealer = Dealer()
        table = Table(dealer, 1)
        
        #2 players
        table.players.append(Player(DealerDecisionModel()))
        table.players.append(Player(DealerDecisionModel()))
        
        #load the shoe 
        table.shoe.cards = [
            10, 10, 10, 9, 7, 5, 3
        ]
        
        table.play_round()
        
        self.assertEqual(table.dealer.balance, 0)
        self.assertEqual(table.players[0].balance, 2)
        self.assertEqual(table.players[1].balance, -2)
        
if __name__ == '__main__':
    unittest.main()
    