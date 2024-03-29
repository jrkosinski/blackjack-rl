from math import floor
from random import randint
from .Deck import Deck

class Shoe: 
    '''
    @title Shoe
    
    @desc A shoe can hold a number of decks from which cards can be dealt, shuffled, 
    and topped up. Also provides statistical data on the card counts and probabilities.
    '''
    def __init__(self, num_decks: int, top_up_rate: float = 0.3): 
        self.cards = []
        self.max_deck_count = num_decks
        self.add_deck(num_decks)
        self.probabilities = {}
        self.top_up_rate = top_up_rate
        self._hi_lo_count = None
        
        self.statistical_analysis()
        
    @property
    def count(self): 
        return len(self.cards)
    
    @property
    def max_count(self):
        return self.max_deck_count * 52
        
    @property
    def hi_lo_count(self) -> int: 
        if (self._hi_lo_count is None): 
            self._calculate_hi_lo()
            
        return self._hi_lo_count

    def shuffle(self): 
        cards = []
        while(self.count > 0): 
            r = randint(0, self.count-1)
            cards.append(self.cards[r])
            self.cards.pop(r)
        self.cards = cards
    
    def auto_top_up(self): 
        if (self.count < (self.max_count * self.top_up_rate)): 
            self.top_up()
            
    def top_up(self): 
        max_count = 52 * self.max_deck_count
        diff = max_count - self.count
        deck_count = int(diff//52)
        
        if (deck_count > 0):
            self.add_deck(count=deck_count, shuffle=True)
            
            #reset hi_lo count 
            self._hi_lo_count = None
        
    def deal_card(self) -> int: 
        if (self.count > 0): 
            card = self.cards[0]
            self.cards.pop(0)
            
            if (self._hi_lo_count is None):
                self._calculate_hi_lo()
            
            #adjust the count 
            if (card <= 6): 
                self._hi_lo_count += 1
            elif (card >= 10): 
                self._hi_lo_count -= 1
            return card
        
        return None
            
    def add_deck(self, count: int = 1, shuffle: bool = True): 
        for i in range(count): 
            deck = Deck()
            self.cards.extend(deck.cards)
        
        if (shuffle): 
            self.shuffle()
    
    def reset(self): 
        self.cards = []
        self.add_deck(self.max_deck_count)
        self.probabilities = {}
        
    def probability_of_lte(self, value) -> float: 
        prob = 0
        for i in range(1, value+1): 
            prob += self.probabilities[i]
        return prob
        
    def probability_of_gt(self, value) -> float: 
        prob = 0
        for i in range(value+1, 12): 
            prob += self.probabilities[i]
        return prob
    
    def statistical_analysis(self): 
        counts = {}
        self.probabilities = {}
        
        for i in range(2, 12): 
            counts[i] = 0
            self.probabilities[i] = 0
        
        #count all card values 
        for card in self.cards: 
            counts[card] += 1
        
        #calculate probabilities
        for value in counts.keys(): 
            self.probabilities[value] = counts[value] / self.count
        
        #add one more, probability of 1s (aces)
        '''
        This makes the probabilities add up to a sum of > 1
        This is ok, because it only makes a difference if you query a set of values 
        that includes both 1 and 11. You would never do that, because the answer would 
        obviously be 100% (it's pointless). The cure would be to subtract ~~ 0.0746 from 
        any queries that include both 1 and 11 (but again, not really worthwhile)
        '''
        self.probabilities[1] = self.probabilities[11]
        
        summ = 0
        for key in self.probabilities: 
            summ += self.probabilities[key]
            
    def _calculate_hi_lo(self):
        count = 0

        for c in self.cards: 
            if (c <= 6): 
                count -= 1
            elif (c >= 10): 
                count += 1
        self._hi_lo_count = count