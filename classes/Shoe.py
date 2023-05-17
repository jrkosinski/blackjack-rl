import random

from classes.Card import Card
from classes.Card import CardSuit
from classes.Card import CardValue
from classes.Card import all_card_values

from classes.CardCount import CardCount

#TODO: might it be easier to let the Shoe keep track of probabilities, and remove CardCount?
class Shoe: 
    '''
    @title Shoe
    @desc Contains a number of decks, from which the Dealer deals the game. As the shoe is 
    dealt from, the number of cards in the shoe decreases. The shoe can be topped up by 
    the dealer at any time. 
    '''
    def __init__(self, num_decks = 1): 
        '''
        @title constructor
        @param num_decks The initial number of decks in the shoe; also the max number of 
        decks that the shoe should be able to hold. 
        '''
        self.cards = list()
        self.num_decks = num_decks
        self.reset()
            
    # Gets the number of cards remaining in the deck 
    @property
    def num_cards(self) -> int: 
        return len(self.cards)
        
    # Gets the total number of cards that the shoe can have (based on max number of decks)
    @property 
    def max_num_cards(self) -> int: 
        return self.num_decks * 52
        
    def reset(self): 
        '''
        @title reset 
        @desc Resets the deck to its initial count, and reshuffles. 
        '''
        self.cards = list()
        self.top_up()
            
    def shuffle(self): 
        '''
        @title shuffle
        @desc Randomizes the positions of all remaining cards in the deck.
        '''
        cards = [None] * self.num_cards
        indices = random.sample(range(self.num_cards), self.num_cards)
        
        for i in range(len(indices)): 
            cards[indices[i]] = self.cards[i]
        self.cards = cards
    
    def top_up(self) -> int: 
        '''
        @title top_up
        @desc Meant to refill the shoe to as near as possible to its original count, 
        but only adding whole entire decks at a time. 
        example: 
            shoe's original count is 52 * 3 (three decks)
            shoe's count gets down to 53 cards 
            topping up can only add one deck (or else it will overfill the shoe), so the 
            count after topping up will be 53 + 52 (105)
        @returns The number of decks added during the top-up (can be zero)
        '''
        count = 0
        while(self.num_cards + 52 <= self.max_num_cards): 
            self._add_deck()
            count += 1
            
        self.shuffle()
        return count 
    
    def _add_deck(self): 
        '''
        @title _add_deck
        @desc Fills the shoe with one deck of cards (does not reshuffle automatically)
        '''
        suits = [CardSuit.Spades, CardSuit.Hearts, CardSuit.Clubs, CardSuit.Diamonds]
        
        for i in range(len(suits)): 
            cards = self._get_all_of_suit(suits[i])
            for n in range(len(cards)): 
                self.cards.append(cards[n])
        
    def peek_next(self, index=0): 
        '''
        @title peek_next
        @param count The index of the card to peek (default 0)
        @desc Looks at the next nth card to be drawn, without removing it from the shoe.
        @returns Card instance (if count is 1), or an array of Card instances
        '''
        if (index > self.num_cards): 
            raise Exception("Number of cards to get is greater than number of cards available")
        output = list()
        return self.cards[index]
        
    def get_next(self, count=1): 
        '''
        @title get_next
        @param count The number of cards to get (default 1)
        @desc Gets the specified number of cards from the top of the shoe, removing those 
        cards from the shoe. 
        @returns Card instance (if count is 1), or an array of Card instances
        '''
        if (count > self.num_cards): 
            raise Exception("Number of cards to get is greater than number of cards available")
        output = list()
        for i in range(count): 
            output.append(self.cards[0])
            self.cards.pop(0)
        
        if (count == 1): 
            return output[0]
        return output
        
    # test this 
    def get_count_of(self, card: Card) -> int: 
        '''
        @title get_count_of
        @param card The card to get a count of 
        @desc Counts the number of occurrences in the shoe of the given card value.
        @returns The number of occurrences in the shoe of the given card's value. 
        '''
        count = 0
        for i in range(len(self.cards)): 
            if (self.cards[i].equals(card)): 
                count += 1
                
        return count
        
    def remove_card(self, card: Card) -> bool: 
        '''
        @title remove_card
        @param card The card to remove 
        @desc Removes the first instance of the given card value found in the shoe.
        @returns True if a card was found & removed; False if not found, not removed.
        '''
        for i in range(len(self.cards)): 
            if (self.cards[i].equals(card)): 
                del self.cards[i] 
                return True
        
        return False
                
    def place_on_top(self, card: Card): 
        '''
        @title place_on_top
        @param card 
        @desc Finds the first occurrence of the given card in the shoe, removes it from 
        its found location, and places it on the top of the deck, so that it will be the 
        next card dealt. 
        '''
        self.remove_card(card)
        self.cards.insert(0, card)
        
    def copy(self): 
        '''
        @title copy
        @desc Returns a shallow copy of the entire shoe 
        @returns A Shoe instance
        '''
        scopy = Shoe(0)
        scopy.num_decks = self.num_decks
        for i in range(len(self.cards)): 
            scopy.cards.append(self.cards[i])
            
        return scopy
        
    #TODO: should be global in Card
    def _get_all_of_suit(self, suit: CardSuit) -> list: 
        output = list()
        card_values = all_card_values()
        for i in range(len(card_values)): 
            output.append(Card(suit, card_values[i]))
        return output